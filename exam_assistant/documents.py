import re
from collections import Counter
from io import BytesIO
from zipfile import BadZipFile, ZipFile
from xml.etree import ElementTree as ET

import pymupdf


MAX_BYTES = 25 * 1024 * 1024
MAX_EXPANDED_BYTES = 100 * 1024 * 1024
MAX_ARCHIVE_ENTRIES = 2_000


def _validate_file_type(filename: str, data: bytes) -> str:
    ext = filename.lower().rsplit(".", 1)[-1] if "." in filename else ""
    signatures = {
        "pdf": data.startswith(b"%PDF-"),
        "png": data.startswith(b"\x89PNG\r\n\x1a\n"),
        "jpg": data.startswith(b"\xff\xd8\xff"),
        "jpeg": data.startswith(b"\xff\xd8\xff"),
        "webp": len(data) >= 12 and data[:4] == b"RIFF" and data[8:12] == b"WEBP",
        "tif": data.startswith((b"II*\x00", b"MM\x00*")),
        "tiff": data.startswith((b"II*\x00", b"MM\x00*")),
    }
    if ext in ("txt", "md"):
        try:
            data.decode("utf-8-sig")
        except UnicodeDecodeError as exc:
            raise ValueError("Text uploads must be valid UTF-8") from exc
        return ext
    if ext in signatures:
        if not signatures[ext]:
            raise ValueError(f"File contents do not match the .{ext} extension")
        return ext
    if ext in ("docx", "pptx"):
        if not data.startswith(b"PK"):
            raise ValueError(f"File contents do not match the .{ext} extension")
        try:
            with ZipFile(BytesIO(data)) as archive:
                entries = archive.infolist()
                if len(entries) > MAX_ARCHIVE_ENTRIES:
                    raise ValueError("Office document contains too many archive entries")
                if sum(entry.file_size for entry in entries) > MAX_EXPANDED_BYTES:
                    raise ValueError("Expanded document exceeds the 100 MB safety limit")
                names = set(archive.namelist())
                required = "word/document.xml" if ext == "docx" else "ppt/presentation.xml"
                if required not in names:
                    raise ValueError(f"File contents are not a valid .{ext} document")
        except BadZipFile as exc:
            raise ValueError("Office document is not a valid ZIP package") from exc
        return ext
    raise ValueError("Supported files: PDF, DOCX, PPTX, TXT, MD and common image formats")


async def ocr_image(data: bytes) -> str:
    from .model_runtime import ModelUnavailable, ocr_image_text
    try:
        return await ocr_image_text(data)
    except ModelUnavailable as exc:
        raise ValueError(str(exc)) from exc


async def extract_text(filename: str, data: bytes) -> tuple[str, list[str]]:
    if len(data) > MAX_BYTES:
        raise ValueError("File exceeds the 25 MB upload limit")
    ext = _validate_file_type(filename, data)
    warnings = []
    if ext in ("txt", "md"):
        text = data.decode("utf-8-sig")
    elif ext == "pdf":
        from .model_runtime import ModelUnavailable
        try:
            with pymupdf.open(stream=data, filetype="pdf") as document:
                if document.is_encrypted:
                    raise ValueError("Password-protected PDFs cannot be extracted")
                if len(document) > 200:
                    raise ValueError("PDF exceeds the 200 page limit")
                pages = [page.get_text(sort=True) for page in document]
                unreadable = [index for index, page_text in enumerate(pages) if len(page_text.strip()) < 30 or any(
                    rect.width * rect.height > document[index].rect.width * document[index].rect.height * .8
                    for image in document[index].get_images(full=True)
                    for rect in document[index].get_image_rects(image[0])
                )]
                if unreadable:
                    from .model_runtime import ocr_session
                    async with ocr_session() as read_page:
                        for index in unreadable:
                            image = document[index].get_pixmap(matrix=pymupdf.Matrix(1.5, 1.5)).tobytes("png")
                            ocr_text = await read_page(image)
                            repeats = Counter(line.strip() for line in ocr_text.splitlines() if len(line.strip()) > 40)
                            if len(ocr_text) > 12000 or any(count > 3 for count in repeats.values()):
                                if len(pages[index].strip()) < 30:
                                    raise ValueError(f"Page {index + 1} OCR repeated text and the PDF has no usable text layer")
                                warnings.append(f"Page {index + 1} OCR repeated text; used the PDF text layer instead. Check this page carefully")
                            else:
                                pages[index] = ocr_text
                                warnings.append(f"Page {index + 1} used PaddleOCR-VL; check names, negation and symbols")
                text = "\n\f\n".join(pages)
        except ModelUnavailable as exc:
            raise ValueError(str(exc)) from exc
        except (pymupdf.FileDataError, RuntimeError) as exc:
            raise ValueError("PDF is damaged or could not be read") from exc
        if any(len(p.strip()) < 30 for p in pages):
            warnings.append("Some pages remain unreadable after OCR")
    elif ext in ("docx", "pptx"):
        try:
            with ZipFile(BytesIO(data)) as archive:
                paths = [p for p in archive.namelist() if p == "word/document.xml"] if ext == "docx" else sorted(p for p in archive.namelist() if re.fullmatch(r"ppt/slides/slide\d+\.xml", p))
                if len(paths) > 200:
                    raise ValueError("Document exceeds the 200 section limit")
                chunks = []
                for path in paths:
                    root = ET.fromstring(archive.read(path))
                    chunks.append(" ".join(e.text or "" for e in root.iter() if e.tag.endswith("}t")))
                text = "\n\f\n".join(chunks)
        except ET.ParseError as exc:
            raise ValueError("Office document contains invalid XML") from exc
    elif ext in ("png", "jpg", "jpeg", "webp", "tif", "tiff"):
        text = await ocr_image(data)
        warnings.append("Image OCR requires manual review, especially for handwriting and technical symbols")
    else:
        raise ValueError("Supported files: PDF, DOCX, PPTX, TXT, MD and common image formats")
    if not text.strip():
        raise ValueError("No readable text was extracted; this file needs OCR or manual entry")
    return text, warnings


# Only split on a top-level question number.  Subparts such as ``Q1(a)`` and
# choice lines such as ``OR`` belong to the current question: keeping them in
# one source record lets the requirement extractor reason about the complete
# compound ask instead of silently treating each subpart as an independent
# paper question.
QUESTION_START = re.compile(r"^\s*(?:Q(?:uestion)?\.?\s*)?(\d{1,2})\s*[.):\-]\s*(.+)", re.I)
QUESTION_HEADING = re.compile(r"^\s*(?:Question\s*No\.?|Q\.?\s*No\.?)\s*(\d{1,2})\s*$", re.I)
NUMBERED_SUBPART = re.compile(r"^\s*(?:\d{1,2}\s*|[Il']\s*)?([a-d])\s*\)\s*(.*)", re.I)
SUBPART_START = re.compile(r"^\s*(?:\(?[a-z]\)|[ivx]+[.)])\s+", re.I)
CHOICE_LINE = re.compile(r"^\s*(?:Group\s+)?(?:OR|EITHER|OR\s+ANSWER)\s*$", re.I)
MARKS_AT_END = re.compile(r"(?:\[(\d+)\s*(?:marks?|m)\]|\((\d+)\s*marks?\)|\((\d+)\)\s*(?:CO[1-9Il]+)?|\b(\d+)\s+marks?)\s*[.]?\s*$", re.I)


def draft_questions(text: str) -> list[dict]:
    questions = []
    current = None
    has_headings = any(QUESTION_HEADING.match(line) for line in text.splitlines())
    in_questions = not has_headings

    def structure_for(question_text: str) -> dict:
        parts, alternatives = [], [[]]
        active = None

        def finish_part():
            nonlocal active
            if active:
                part_text = " ".join(active["lines"]).strip()
                match = MARKS_AT_END.search(part_text)
                part_marks = next((int(value) for value in match.groups() if value), None) if match else None
                if match:
                    part_text = part_text[:match.start()].rstrip()
                part = {"id": active["id"], "label": active["label"], "text": part_text, "marks": part_marks}
                parts.append(part)
                if part["label"] != "prompt":
                    alternatives[-1].append(part["id"])
                active = None

        for line in question_text.splitlines():
            if CHOICE_LINE.match(line):
                finish_part()
                if alternatives[-1]:
                    alternatives.append([])
                continue
            match = SUBPART_START.match(line)
            if match:
                finish_part()
                label = match.group(0).strip().strip("().").lower()
                active = {"id": f"p{len(parts) + 1}", "label": label, "lines": [line[match.end():].strip()]}
            elif active:
                active["lines"].append(line.strip())
            elif line.strip():
                active = {"id": f"p{len(parts) + 1}", "label": "prompt", "lines": [line.strip()]}
        finish_part()
        alternatives = [group for group in alternatives if group]
        choices = []
        if len(alternatives) > 1:
            choices.append({"id": "choice-1", "rule": "choose_any", "choose_count": 1, "alternatives": alternatives})
        warnings = ["Check that the detected OR alternatives match the paper's full choice grouping."] if choices else []
        return {"parts": parts, "choice_groups": choices, "warnings": warnings}

    def finish():
        if current and current["text"].strip():
            question = dict(current)
            if question["marks"] is None:
                compound = any(SUBPART_START.match(line) or CHOICE_LINE.match(line) for line in question["text"].splitlines())
                marks = MARKS_AT_END.search(question["text"])
                question["marks"] = next((int(value) for value in marks.groups() if value), None) if marks and not compound else None
            question["structure"] = structure_for(question["text"])
            questions.append(question)

    for line in text.splitlines():
        heading = QUESTION_HEADING.match(line)
        if heading:
            finish()
            current = {"number": heading.group(1), "text": "", "marks": None}
            in_questions = True
            continue
        if not in_questions or re.search(r"end of (?:the )?question paper", line, re.I):
            continue
        part = NUMBERED_SUBPART.match(line)
        if part and current:
            line = f"{part.group(1)}) {part.group(2)}"
        if CHOICE_LINE.match(line):
            line = "OR"
        line = re.sub(r"\s*\((\d{1,3})\)\s*CO[1-9Il]+\s*$", r" [\1 marks]", line, flags=re.I)
        match = QUESTION_START.match(line)
        if match:
            finish()
            root_marks = MARKS_AT_END.search(match.group(2))
            current = {"number": match.group(1).strip(), "text": match.group(2).strip(), "marks": next((int(value) for value in root_marks.groups() if value), None) if root_marks else None}
        elif current and line.strip():
            # Preserve line boundaries around subparts and alternatives.  The
            # classifier needs the labels and OR structure to evaluate full
            # two-way coverage; flattening them to prose loses that signal.
            separator = "\n" if SUBPART_START.match(line) or CHOICE_LINE.match(line) else " "
            current["text"] += separator + line.strip()
    finish()
    return questions


def expand_subquestions(questions: list[dict]) -> list[dict]:
    """Store labeled exam subquestions independently while retaining OR context."""
    expanded = []
    for question in questions:
        parts = (question.get("structure") or {}).get("parts", [])
        if not any(str(part.get("label", "")).casefold() in {"a", "b", "c", "d"} for part in parts):
            expanded.append(question)
            continue
        groups = []
        active = None
        part_to_number = {}
        for part in parts:
            label = str(part.get("label", "")).casefold()
            if label in {"a", "b", "c", "d"}:
                if active:
                    groups.append(active)
                number = f"{question['number']}{label}"
                active = {"number": number, "label": label, "part_ids": [part["id"]], "parts": [part]}
            elif active:
                active["part_ids"].append(part["id"])
                active["parts"].append(part)
            if active:
                part_to_number[part.get("id")] = active["number"]
        if active:
            groups.append(active)
        if not groups:
            expanded.append(question)
            continue
        choice_sets = []
        for choice in (question.get("structure") or {}).get("choice_groups", []):
            alternatives = []
            for alternative in choice.get("alternatives", []):
                numbers = list(dict.fromkeys(part_to_number[part_id] for part_id in alternative if part_id in part_to_number))
                if numbers:
                    alternatives.append(numbers)
            if len(alternatives) > 1:
                choice_sets.append(alternatives)
        for group in groups:
            lines = []
            for part in group["parts"]:
                prefix = f"({part['label']}) " if part["label"] not in {group["label"]} else ""
                lines.append(prefix + str(part.get("text", "")).strip())
            group_choices = [{"group": index + 1, "alternatives": alternatives,
                              "alternative_index": next((i for i, alternative in enumerate(alternatives, 1) if group["number"] in alternative), None)}
                             for index, alternatives in enumerate(choice_sets)
                             if any(group["number"] in alternative for alternative in alternatives)]
            primary = group["parts"][0]
            expanded.append({
                "number": group["number"],
                "text": "\n".join(lines).strip(),
                "marks": primary.get("marks"),
                "structure": {
                    "parts": [{"id": "p1", "label": group["label"], "text": "\n".join(lines).strip(), "marks": primary.get("marks")}],
                    "choice_groups": [],
                    "warnings": [],
                    "paper_context": {"root_number": str(question["number"]), "choice_groups": group_choices},
                },
            })
    return expanded


def suggest_paper_pattern(text: str, filename: str, file_hash: str) -> dict:
    """Build an editable slot outline; never infer syllabus units or choice rules."""
    questions = draft_questions(text)
    groups: dict[int | None, list[dict]] = {}
    for question in questions:
        groups.setdefault(question.get("marks"), []).append(question)
    slots = [
        {
            "name": f"{marks}-mark questions" if marks else "Questions with unspecified marks",
            "count": len(items),
            "marks": marks,
            "unit": None,
            "topic_ids": [],
            "source_question_numbers": [item.get("number") for item in items],
        }
        for marks, items in groups.items()
    ]
    return {
        "sections": [{"name": "Imported paper structure", "slots": slots}],
        "source": {"filename": filename, "sha256": file_hash, "detected_question_count": len(questions)},
        "mapping_notes": [
            "Question counts and explicit marks are suggested from extracted numbering.",
            "Syllabus units, topic IDs, section boundaries and OR/choose-any rules need direct configuration.",
        ],
    }
