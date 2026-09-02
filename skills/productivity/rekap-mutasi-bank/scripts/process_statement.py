import sys
import re
import pymupdf

sys.path.append('/home/satyaaditech/.hermes/skills/productivity/google-workspace/scripts')
import google_api

SPREADSHEET_ID = '1qYLKwSpFH9iDTEEBpfxhDuGW6JrMHCHn2cNbf7v0iD4'
FOLDER_ID = '1maRGm6UcCWxQYygk8WWxH3QcJO-jHMQK'

def parse_num(s):
    if not s: return 0.0
    return float(s.replace(',', ''))

def format_date_simple(d_str):
    m = re.match(r'(\d{2})/(\d{2})/(\d{4})', d_str)
    if m:
        day, month, year = m.groups()
        return f'{day}/{month}/{year[2:]}'
    return d_str

def process_bank_pdf(pdf_path, tab_name):
    doc = pymupdf.open(pdf_path)
    
    # 1. Anchors
    anchors = []
    for p_idx, page in enumerate(doc):
        spans = []
        for b in page.get_text('dict')['blocks']:
            if 'lines' in b:
                for l in b['lines']:
                    for s in l['spans']:
                        t = s['text'].strip()
                        if t:
                            spans.append({'text': t, 'x0': s['bbox'][0], 'y0': s['bbox'][1]})
        p_anchors = [s for s in spans if s['text'] in ('D', 'K') and 570 <= s['x0'] <= 610 and 320 < s['y0'] < (450 if p_idx == len(doc)-1 else 850)]
        p_anchors.sort(key=lambda s: s['y0'])
        
        for anc in p_anchors:
            y_anc = anc['y0']
            base_spans = [s for s in spans if abs(s['y0'] - y_anc) < 3.0]
            p_dates = [s['text'] for s in base_spans if 20 <= s['x0'] < 125]
            amt_spans = [s['text'] for s in base_spans if 500 <= s['x0'] < 580 and re.search(r'[\d,]+\.\d{2}', s['text'])]
            amts = [parse_num(a) for a in amt_spans]
            non_zero = [a for a in amts if a > 0]
            chosen_amt = non_zero[0] if non_zero else (amts[0] if amts else 0.0)
            bal_spans = [s['text'] for s in base_spans if 615 <= s['x0'] < 720 and re.search(r'[\d,]+\.\d{2}', s['text'])]
            bal = parse_num(bal_spans[-1]) if bal_spans else 0.0
            anchors.append({'page': p_idx, 'y': y_anc, 'p_date': p_dates[0] if p_dates else '', 'amount': chosen_amt, 'db_cr': anc['text'], 'balance': bal})

    # 2. Descriptions
    desc_lines = []
    for p_idx, page in enumerate(doc):
        for b in page.get_text('dict')['blocks']:
            if 'lines' in b:
                for l in b['lines']:
                    for s in l['spans']:
                        if 335 <= s['bbox'][0] <= 500 and 315 < s['bbox'][1] < (450 if p_idx == len(doc)-1 else 850):
                            t = s['text'].strip()
                            if t: desc_lines.append((p_idx, s['bbox'][1], t))
    desc_lines.sort(key=lambda item: (item[0], item[1]))

    start_patterns = ['TRANSFER DARI', 'TRANSFER KE', 'TRF/PAY/TOP-UP', 'BY TRX', 'BV TRK', 'JASA GIRO', 'PPH', 'BIAYA ADM', 'RTGS']
    start_indices = [idx for idx, (p, y, t) in enumerate(desc_lines) if any(t.startswith(sp) for sp in start_patterns)]

    descriptions = []
    for i in range(len(start_indices)):
        idx_start = start_indices[i]
        idx_end = start_indices[i+1] if i + 1 < len(start_indices) else len(desc_lines)
        descriptions.append(re.sub(r'\s+', ' ', ' '.join(desc_lines[k][2] for k in range(idx_start, idx_end))).strip())

    # Build values
    values = [['TANGGAL', 'KETERANGAN', 'DEBET', 'KREDIT', 'SALDO']]
    for i in range(len(anchors)):
        a = anchors[i]
        tgl = format_date_simple(a['p_date'])
        ket = descriptions[i]
        debet = int(round(a['amount'])) if a['db_cr'] == 'D' else 0
        kredit = 0 if a['db_cr'] == 'D' else int(round(a['amount']))
        saldo = int(round(a['balance']))
        values.append([tgl, ket, debet, kredit, saldo])

    last_row = len(values)
    values.append(['TOTAL', '', f'=SUM(C2:C{last_row})', f'=SUM(D2:D{last_row})', int(round(anchors[-1]['balance']))])

    # Google Sheets upload
    sheets_service = google_api.build_service('sheets', 'v4')
    
    # Add new sheet
    add_resp = sheets_service.spreadsheets().batchUpdate(
        spreadsheetId=SPREADSHEET_ID,
        body={"requests": [{"addSheet": {"properties": {"title": tab_name}}}]}
    ).execute()
    new_sheet_id = add_resp['replies'][0]['addSheet']['properties']['sheetId']

    # Update values
    sheets_service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=f"'{tab_name}'!A1:E{len(values)}",
        valueInputOption='USER_ENTERED',
        body={'values': values}
    ).execute()

    # Format
    format_reqs = [
        {"repeatCell": {"range": {"sheetId": new_sheet_id, "startRowIndex": 0, "endRowIndex": 1, "startColumnIndex": 0, "endColumnIndex": 5}, "cell": {"userEnteredFormat": {"backgroundColor": {"red": 0.95, "green": 0.95, "blue": 0.95}, "textFormat": {"fontSize": 10, "bold": True}, "horizontalAlignment": "CENTER", "verticalAlignment": "MIDDLE"}}, "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment,verticalAlignment)"}},
        {"repeatCell": {"range": {"sheetId": new_sheet_id, "startRowIndex": 1, "endRowIndex": len(values)-1, "startColumnIndex": 0, "endColumnIndex": 1}, "cell": {"userEnteredFormat": {"horizontalAlignment": "LEFT", "verticalAlignment": "MIDDLE", "textFormat": {"fontSize": 10}}}, "fields": "userEnteredFormat(horizontalAlignment,verticalAlignment,textFormat)"}},
        {"repeatCell": {"range": {"sheetId": new_sheet_id, "startRowIndex": 1, "endRowIndex": len(values)-1, "startColumnIndex": 1, "endColumnIndex": 2}, "cell": {"userEnteredFormat": {"horizontalAlignment": "LEFT", "verticalAlignment": "MIDDLE", "wrapStrategy": "WRAP", "textFormat": {"fontSize": 10}}}, "fields": "userEnteredFormat(horizontalAlignment,verticalAlignment,wrapStrategy,textFormat)"}},
        {"repeatCell": {"range": {"sheetId": new_sheet_id, "startRowIndex": 1, "endRowIndex": len(values), "startColumnIndex": 2, "endColumnIndex": 5}, "cell": {"userEnteredFormat": {"horizontalAlignment": "RIGHT", "verticalAlignment": "MIDDLE", "numberFormat": {"type": "NUMBER", "pattern": "#,##0"}, "textFormat": {"fontSize": 10}}}, "fields": "userEnteredFormat(horizontalAlignment,verticalAlignment,numberFormat,textFormat)"}},
        {"repeatCell": {"range": {"sheetId": new_sheet_id, "startRowIndex": len(values)-1, "endRowIndex": len(values), "startColumnIndex": 0, "endColumnIndex": 5}, "cell": {"userEnteredFormat": {"backgroundColor": {"red": 0.93, "green": 0.95, "blue": 0.98}, "textFormat": {"bold": True, "fontSize": 10}, "horizontalAlignment": "RIGHT", "verticalAlignment": "MIDDLE"}}, "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment,verticalAlignment)"}},
        {"repeatCell": {"range": {"sheetId": new_sheet_id, "startRowIndex": len(values)-1, "endRowIndex": len(values), "startColumnIndex": 0, "endColumnIndex": 1}, "cell": {"userEnteredFormat": {"horizontalAlignment": "CENTER", "textFormat": {"bold": True}}}, "fields": "userEnteredFormat(horizontalAlignment,textFormat)"}},
        {"updateSheetProperties": {"properties": {"sheetId": new_sheet_id, "gridProperties": {"frozenRowCount": 1}}, "fields": "gridProperties.frozenRowCount"}},
        {"updateDimensionProperties": {"range": {"sheetId": new_sheet_id, "dimension": "COLUMNS", "startIndex": 0, "endIndex": 1}, "properties": {"pixelSize": 95}, "fields": "pixelSize"}},
        {"updateDimensionProperties": {"range": {"sheetId": new_sheet_id, "dimension": "COLUMNS", "startIndex": 1, "endIndex": 2}, "properties": {"pixelSize": 520}, "fields": "pixelSize"}},
        {"updateDimensionProperties": {"range": {"sheetId": new_sheet_id, "dimension": "COLUMNS", "startIndex": 2, "endIndex": 3}, "properties": {"pixelSize": 140}, "fields": "pixelSize"}},
        {"updateDimensionProperties": {"range": {"sheetId": new_sheet_id, "dimension": "COLUMNS", "startIndex": 3, "endIndex": 4}, "properties": {"pixelSize": 140}, "fields": "pixelSize"}},
        {"updateDimensionProperties": {"range": {"sheetId": new_sheet_id, "dimension": "COLUMNS", "startIndex": 4, "endIndex": 5}, "properties": {"pixelSize": 150}, "fields": "pixelSize"}},
        {"updateBorders": {"range": {"sheetId": new_sheet_id, "startRowIndex": 0, "endRowIndex": len(values), "startColumnIndex": 0, "endColumnIndex": 5}, "top": {"style": "SOLID", "width": 1, "color": {"red": 0.6, "green": 0.6, "blue": 0.6}}, "bottom": {"style": "SOLID", "width": 2, "color": {"red": 0.4, "green": 0.4, "blue": 0.4}}, "innerHorizontal": {"style": "SOLID", "width": 1, "color": {"red": 0.85, "green": 0.85, "blue": 0.85}}, "innerVertical": {"style": "SOLID", "width": 1, "color": {"red": 0.85, "green": 0.85, "blue": 0.85}}}}
    ]
    sheets_service.spreadsheets().batchUpdate(spreadsheetId=SPREADSHEET_ID, body={"requests": format_reqs}).execute()
    print(f"Tab '{tab_name}' successfully added and formatted!")
