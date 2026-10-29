"""Two-sheet paper report for comparisons saved in a conversation."""
import io
import re
from collections import OrderedDict

from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference
from openpyxl.chart.label import DataLabelList
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter


COLORS = {
    "ink": "263445",
    "blue": "1F4E78",
    "pale_blue": "D9EAF7",
    "line": "A6B5C3",
    "A": "C6EAD0",
    "B": "FFE69A",
    "C": "F5C6C6",
    "review": "E7E6E6",
}


def _safe(value):
    value = str(value or '')
    return "'" + value if value.startswith(('=', '+', '-', '@')) else value


def _key(number):
    return re.sub(r'[^a-z0-9]', '', str(number).casefold()).removeprefix('q')


def _comparison_name(index):
    return f"Base vs Comparison {index}"


def _set_page(sheet, orientation='landscape'):
    sheet.sheet_view.showGridLines = False
    sheet.sheet_properties.pageSetUpPr.fitToPage = True
    sheet.page_setup.fitToWidth = 1
    sheet.page_setup.fitToHeight = 0
    sheet.page_setup.orientation = orientation
    sheet.sheet_properties.outlinePr.summaryBelow = True


def _title(sheet, title, subtitle, last_col):
    sheet.merge_cells(start_row=1, start_column=1, end_row=1, end_column=last_col)
    cell = sheet.cell(1, 1, _safe(title))
    cell.font = Font(name='Times New Roman', size=15, bold=True, color=COLORS['ink'])
    cell.alignment = Alignment(vertical='center')
    sheet.row_dimensions[1].height = 27
    sheet.merge_cells(start_row=2, start_column=1, end_row=2, end_column=last_col)
    cell = sheet.cell(2, 1, _safe(subtitle))
    cell.font = Font(name='Times New Roman', size=10, italic=True, color='555555')
    cell.alignment = Alignment(vertical='center', wrap_text=True)
    sheet.row_dimensions[2].height = 31


def _header(sheet, row, first_col, last_col):
    for cells in sheet.iter_rows(min_row=row, max_row=row, min_col=first_col, max_col=last_col):
        for cell in cells:
            cell.fill = PatternFill('solid', fgColor=COLORS['blue'])
            cell.font = Font(name='Times New Roman', size=10, bold=True, color='FFFFFF')
            cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
            cell.border = Border(bottom=Side(style='thin', color='FFFFFF'))
    sheet.row_dimensions[row].height = 30


def _paper_sections(book, pair_groups):
    sheet = book.create_sheet('Papers')
    _title(sheet, 'Paper comparison report', 'Base paper questions shown beside each comparison paper in question-number order.', 4)
    for col, width in enumerate((17, 70, 17, 70), 1):
        sheet.column_dimensions[get_column_letter(col)].width = width
    thin = Side(style='thin', color=COLORS['line'])
    row = 4
    for group in pair_groups:
        sheet.merge_cells(start_row=row, start_column=1, end_row=row, end_column=4)
        heading = sheet.cell(row, 1, _safe(f"{group['name']}: {group['base_title']} vs {group['reference_title']}"))
        heading.fill = PatternFill('solid', fgColor=COLORS['pale_blue'])
        heading.font = Font(name='Times New Roman', size=12, bold=True, color=COLORS['ink'])
        heading.alignment = Alignment(vertical='center')
        sheet.row_dimensions[row].height = 24
        row += 1
        for col, value in enumerate(('Base question no.', 'Base question', 'Comparison question no.', 'Comparison question'), 1):
            sheet.cell(row, col, value)
        _header(sheet, row, 1, 4)
        row += 1

        base_questions = group['base_questions']
        comparison_questions = group['comparison_questions']
        by_base = OrderedDict((_key(q['number']), q) for q in base_questions)
        by_comparison = OrderedDict((_key(q['number']), q) for q in comparison_questions)
        numbers = list(by_base)
        numbers.extend(number for number in by_comparison if number not in by_base)
        if not numbers:
            numbers = ['']
        for number in numbers:
            base_q, comparison_q = by_base.get(number), by_comparison.get(number)
            values = [base_q.get('number', '') if base_q else '', base_q.get('text', '') if base_q else '', comparison_q.get('number', '') if comparison_q else '', comparison_q.get('text', '') if comparison_q else '']
            for col, value in enumerate(values, 1):
                cell = sheet.cell(row, col, _safe(value))
                cell.font = Font(name='Times New Roman', size=10, color=COLORS['ink'])
                cell.alignment = Alignment(vertical='top', wrap_text=True, horizontal='center' if col in (1, 3) else 'left')
                cell.border = Border(bottom=thin)
            lines = max(1, max((len(str(v or '')) // width + str(v or '').count('\n') + 1 for v, width in ((values[1], 68), (values[3], 68))), default=1))
            sheet.row_dimensions[row].height = min(240, max(24, 15 * lines))
            row += 1
        row += 2
    sheet.print_title_rows = '1:2'
    sheet.freeze_panes = 'A5'
    _set_page(sheet)
    return sheet


def _classification_sheet(book, pair_groups, detail_rows):
    sheet = book.create_sheet('A-B-C Classification')
    last_col = 12
    _title(
        sheet,
        'Classification and predictability',
        'A = exactly the same question. B = a similar problem with changed values or minor wording. C = a completely different question. Predictability = (A + B) / all classified questions. Low <30%, Moderate 30–60%, High >60%.',
        last_col,
    )
    summary_header = 4
    headers = ('Paper comparison', 'Base paper', 'Comparison paper', 'Type A', 'Type B', 'Type C', 'Needs review', 'Total questions', 'Predictability score', 'Predictability band')
    for col, value in enumerate(headers, 1):
        sheet.cell(summary_header, col, value)
    _header(sheet, summary_header, 1, len(headers))

    detail_header = max(12, summary_header + len(pair_groups) + 3)
    detail_headers = ('Paper comparison', 'Base paper', 'Base Q. No.', 'Base question', 'Comparison paper', 'Unit', 'Classification', 'Reason', 'Evidence / comparison block', 'Status', 'Stale')
    for col, value in enumerate(detail_headers, 1):
        sheet.cell(detail_header, col, value)
    _header(sheet, detail_header, 1, len(detail_headers))
    first_detail_row = detail_header + 1
    for offset, item in enumerate(detail_rows):
        row = first_detail_row + offset
        values = (item['name'], item['base_title'], item['base_number'], item['base_text'], item['reference_title'], item['unit'], item['label'], item['reason'], item['reference_text'], item['status'], item['stale'])
        for col, value in enumerate(values, 1):
            cell = sheet.cell(row, col, _safe(value))
            cell.font = Font(name='Times New Roman', size=10, color=COLORS['ink'])
            cell.alignment = Alignment(vertical='top', wrap_text=True)
            cell.border = Border(bottom=Side(style='thin', color=COLORS['line']))
            if col == 7 and value in COLORS:
                cell.fill = PatternFill('solid', fgColor=COLORS[value])
        row_lines = max(1, len(str(item['reason'] or '')) // 70 + str(item['reason'] or '').count('\n') + 1)
        sheet.row_dimensions[row].height = min(180, max(28, 15 * row_lines))

    final_detail_row = max(first_detail_row, first_detail_row + len(detail_rows) - 1)
    for offset, group in enumerate(pair_groups):
        row = summary_header + 1 + offset
        sheet.cell(row, 1, group['name'])
        sheet.cell(row, 2, group['base_title'])
        sheet.cell(row, 3, group['reference_title'])
        for col, label in ((4, 'A'), (5, 'B'), (6, 'C'), (7, 'review')):
            sheet.cell(row, col, f'=COUNTIFS($A${first_detail_row}:$A${final_detail_row},$A{row},$G${first_detail_row}:$G${final_detail_row},"{label}")')
        sheet.cell(row, 8, f'=SUM(D{row}:G{row})')
        sheet.cell(row, 9, f'=IF(H{row}=0,"",(D{row}+E{row})/H{row})')
        sheet.cell(row, 10, f'=IF(I{row}="","",IF(I{row}<30%,"Low",IF(I{row}<=60%,"Moderate","High")))')
        for col in range(1, 11):
            cell = sheet.cell(row, col)
            cell.font = Font(name='Times New Roman', size=10, bold=col >= 4, color=COLORS['ink'])
            cell.alignment = Alignment(vertical='center', wrap_text=True, horizontal='center' if col >= 4 else 'left')
            cell.border = Border(bottom=Side(style='thin', color=COLORS['line']))
            if col in (4, 5, 6):
                cell.fill = PatternFill('solid', fgColor=COLORS[('A', 'B', 'C')[col - 4]])
        sheet.cell(row, 9).number_format = '0.00%'
        sheet.row_dimensions[row].height = 31

    summary_end = summary_header + len(pair_groups)
    if pair_groups:
        chart = BarChart()
        chart.type = 'col'
        chart.style = 10
        chart.grouping = 'clustered'
        chart.title = 'A/B/C question counts by comparison'
        chart.y_axis.title = 'Questions'
        chart.x_axis.title = 'Paper comparison'
        chart.y_axis.scaling.min = 0
        chart.height = 8
        chart.width = 17
        chart.legend.position = 'b'
        chart.varyColors = False
        chart_data = Reference(sheet, min_col=4, max_col=6, min_row=summary_header, max_row=summary_end)
        categories = Reference(sheet, min_col=1, min_row=summary_header + 1, max_row=summary_end)
        chart.add_data(chart_data, titles_from_data=True)
        chart.set_categories(categories)
        chart.dataLabels = DataLabelList()
        chart.dataLabels.showVal = True
        for series, label in zip(chart.series, ('A', 'B', 'C')):
            series.graphicalProperties.solidFill = COLORS[label]
            series.graphicalProperties.line.solidFill = COLORS[label]
        sheet.add_chart(chart, 'L4')

    widths = (30, 24, 25, 13, 13, 13, 16, 17, 21, 19, 12, 3)
    for col, width in enumerate(widths, 1):
        sheet.column_dimensions[get_column_letter(col)].width = width
    for row in range(summary_header + 1, summary_end + 1):
        sheet.cell(row, 9).number_format = '0.00%'
    sheet.auto_filter.ref = f'A{detail_header}:K{max(detail_header, final_detail_row)}'
    sheet.freeze_panes = 'A5'
    sheet.print_title_rows = f'{detail_header}:{detail_header}'
    _set_page(sheet)
    return sheet


def build_chat_report(comparisons, db, question_model, result_model, report_row_values):
    from sqlalchemy import select

    book = Workbook()
    book.remove(book.active)
    pair_groups = OrderedDict()
    detail_rows = []
    for comparison in comparisons:
        results = db.scalars(select(result_model).where(result_model.comparison_id == comparison.id).order_by(result_model.id)).all()
        for result in results:
            target, reference = db.get(question_model, result.target_id), db.get(question_model, result.reference_id)
            if not target or not reference:
                continue
            values = report_row_values(comparison, result, db)
            pair_key = (comparison.id, target.paper_id, reference.paper_id)
            if pair_key not in pair_groups:
                base_questions = db.scalars(select(question_model).where(question_model.paper_id == target.paper_id).order_by(question_model.id)).all()
                comparison_questions = db.scalars(select(question_model).where(question_model.paper_id == reference.paper_id).order_by(question_model.id)).all()
                pair_groups[pair_key] = {
                    'comparison_id': comparison.id,
                    'base_title': target.paper.title,
                    'reference_title': reference.paper.title,
                    'base_questions': [{'number': q.number, 'text': q.text} for q in base_questions],
                    'comparison_questions': [{'number': q.number, 'text': q.text} for q in comparison_questions],
                    'entries': [],
                }
            pair_groups[pair_key]['entries'].append((comparison, result, target, reference, values))

    indexed_pairs = []
    pair_index = 0
    for group in pair_groups.values():
        pair_index += 1
        group['name'] = _comparison_name(pair_index)
        indexed_pairs.append(group)
        for comparison, result, target, reference, values in group['entries']:
            detail_rows.append({
                'name': group['name'],
                'base_title': group['base_title'],
                'base_number': values['base_question_number'],
                'base_text': values['base_question'],
                'reference_title': group['reference_title'],
                'unit': target.unit or '',
                'label': result.label,
                'reason': result.reason or '',
                'reference_text': values['reference_question'],
                'status': comparison.status,
                'stale': values['stale'],
            })

    _paper_sections(book, indexed_pairs)
    _classification_sheet(book, indexed_pairs, detail_rows)
    book.calculation.fullCalcOnLoad = True
    book.calculation.forceFullCalc = True
    book.calculation.calcMode = 'auto'
    output = io.BytesIO()
    book.save(output)
    return output.getvalue()
