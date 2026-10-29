import re


def unit_for_topic(topic_id: str) -> int | None:
    match = re.search(r"/u([1-5])(?:/|$)", topic_id)
    return int(match.group(1)) if match else None


def validate_tree(tree: dict) -> list[str]:
    errors: list[str] = []
    if not isinstance(tree, dict):
        return ["Tree must be a JSON object"]
    course = tree.get("course")
    if not isinstance(course, dict) or not isinstance(course.get("code"), str) or not course.get("code", "").strip() or not isinstance(course.get("title"), str) or not course.get("title", "").strip():
        errors.append("Tree needs a course code and title")
    nodes = tree.get("nodes")
    if not isinstance(nodes, list) or any(not isinstance(node, dict) for node in nodes):
        return errors + ["Tree nodes must be an array of objects"]
    ids = [node.get("id") for node in nodes]
    if any(not isinstance(node_id, str) or not node_id.strip() for node_id in ids):
        errors.append("Every node needs a non-empty string ID")
    valid_ids = [node_id for node_id in ids if isinstance(node_id, str)]
    if len(valid_ids) != len(set(valid_ids)):
        errors.append("Node IDs must be unique")
    known = set(valid_ids)
    by_id = {node.get("id"): node for node in nodes if isinstance(node.get("id"), str)}
    allowed_kinds = {"course", "unit", "heading", "topic"}
    for node in nodes:
        node_id = node.get("id")
        kind = node.get("kind")
        if not isinstance(kind, str) or kind not in allowed_kinds:
            errors.append(f"Invalid node kind: {node_id}")
        if not isinstance(node.get("label"), str) or not node.get("label", "").strip():
            errors.append(f"Node needs a label: {node_id}")
        parent = node.get("parent")
        if parent is not None and (not isinstance(parent, str) or parent not in known):
            errors.append(f"Unknown parent for {node_id}")
        if kind in ("heading", "topic"):
            description = node.get("description", "")
            if not isinstance(description, str):
                errors.append(f"Description must be text: {node_id}")
            elif len(description.split()) > 45:
                errors.append(f"Description exceeds 45 words: {node_id}")
        seen, parent_id = set(), parent
        while isinstance(parent_id, str) and parent_id in by_id:
            if parent_id in seen or parent_id == node_id:
                errors.append(f"Parent cycle: {node_id}")
                break
            seen.add(parent_id)
            parent_id = by_id[parent_id].get("parent")
        links = node.get("distinguish_from", [])
        if not isinstance(links, list):
            errors.append(f"distinguish_from must be an array: {node_id}")
            continue
        seen_targets = set()
        for link in links:
            if not isinstance(link, dict) or not isinstance(link.get("node"), str):
                errors.append(f"Invalid distinction link: {node_id}")
                continue
            target = link["node"]
            if target in seen_targets:
                errors.append(f"Duplicate distinction link: {node_id} -> {target}")
            seen_targets.add(target)
            if target == node_id:
                errors.append(f"Self distinction is invalid: {node_id}")
            if target not in known:
                errors.append(f"Unknown distinction target: {target}")
            elif node.get("kind") != "topic" or by_id[target].get("kind") != "topic":
                errors.append(f"Distinction links must connect topic nodes: {node_id} -> {target}")
            elif unit_for_topic(target) != unit_for_topic(node_id if isinstance(node_id, str) else ""):
                errors.append(f"Cross-unit distinction: {node_id} -> {target}")
            else:
                if not isinstance(link.get("note"), str) or not link.get("note", "").strip() or len(link.get("note", "")) > 500:
                    errors.append(f"Distinction links need a note of at most 500 characters: {node_id} -> {target}")
                reverse = by_id[target].get("distinguish_from", [])
                if not isinstance(reverse, list) or not any(isinstance(back, dict) and back.get("node") == node_id for back in reverse):
                    errors.append(f"Nonreciprocal distinction: {node_id} -> {target}")
    courses = [node for node in nodes if node.get("kind") == "course"]
    units = [node for node in nodes if node.get("kind") == "unit"]
    if len(courses) != 1:
        errors.append("A tree must have exactly one course node")
    elif isinstance(course, dict) and courses[0].get("id") != course.get("code"):
        errors.append("Course node ID must match course code")
    if len(units) != 5:
        errors.append("A subject must have five units")
    if len({unit_for_topic(node["id"]) for node in units if isinstance(node.get("id"), str)}) != 5:
        errors.append("Unit node IDs must identify five distinct units")
    return errors


def topic_context(tree: dict, topic_ids: list[str]) -> list[dict]:
    by_id = {node["id"]: node for node in tree["nodes"]}
    return [by_id[x] for x in topic_ids if x in by_id]
