#!/usr/bin/env python3
"""
Record a multi-item receipt (finance-automation skill).

Workflow (verified 2026-08-12, No 47 Pawon Pendopo Manahan):
  1. Compute next "No" = max(numeric A in Transaksi Harian) + 1  (BEFORE append)
  2. Create "Detail Item" tab via batchUpdate addSheet if missing + header row
  3. Upload receipt photo to Drive COA folder (mapped via ~/.hermes/finance_drive_folders.json)
  4. Append header row to Transaksi Harian (Drive link -> column J Catatan, no-ref -> column I)
  5. Append per-item rows to Detail Item
  6. Verify by reading back

Usage:
  python record_multi_item_receipt.py \
    --date 2026-08-12 \
    --no-ref MNH01026-120826 \
    --desc "Makan di Pawon Pendopo Manahan (Soto)" \
    --coa-name "Beban Makanan" \
    --coa-code 6000 \
    --total 45000 \
    --method QRIS \
    --penjual "SMM Pawon Pendopo Manahan" \
    --photo /path/to/nota.jpg \
    --items '[["Soto Daging Besar",1,10000,"Makanan"],["Teh Manis Panas",2,3500,"Minuman"]]'
    # items = list of [nama_item, qty, harga_satuan, kategori_item]

Requires: ~/.hermes/google_token.json (refresh token) — same pattern as
references/google-sheets-rest-api.md. Uses requests (no gspread).
"""

import argparse, json, os, sys, requests

HOME = os.path.expanduser("~")
SPREADSHEET_ID = "13W8pmkqdXwv_Nv4x-reIrw7m0JXOGVWENmXEtgrjG7U"
FOLDER_MAP = json.load(open(os.path.join(HOME, ".hermes/finance_drive_folders.json")))
DETAIL_HEADERS = ["No Ref", "Tanggal", "Nama Item", "Qty", "Harga Satuan",
                  "Total Item", "Kategori Item", "Penjual / Lokasi"]


def get_headers():
    tk = json.load(open(os.path.join(HOME, ".hermes/google_token.json")))
    refresh = requests.post(tk["token_uri"], data={
        "grant_type": "refresh_token",
        "refresh_token": tk["refresh_token"],
        "client_id": tk["client_id"],
        "client_secret": tk["client_secret"],
    }).json()
    return {"Authorization": f"Bearer {refresh['access_token']}"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", required=True)
    ap.add_argument("--no-ref", required=True)
    ap.add_argument("--desc", required=True)
    ap.add_argument("--coa-name", required=True)  # must exist in FOLDER_MAP["folders"]
    ap.add_argument("--coa-code", required=True)
    ap.add_argument("--total", type=int, required=True)
    ap.add_argument("--method", required=True)
    ap.add_argument("--penjual", required=True)
    ap.add_argument("--photo", required=True)
    ap.add_argument("--items", required=True)  # JSON: [[name, qty, unit, kategori], ...]
    args = ap.parse_args()

    headers = get_headers()
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}"
    items = json.loads(args.items)

    # 1. Next No = max numeric A + 1
    r = requests.get(f"{url}/values/Transaksi%20Harian!A4:A", headers=headers).json()
    nums = [int(row[0]) for row in r.get("values", []) if row and row[0].isdigit()]
    no = (max(nums) + 1) if nums else 1
    print(f"No: {no}")

    # 2. Ensure Detail Item tab + header row
    meta = requests.get(url, headers=headers).json()
    titles = [s["properties"]["title"] for s in meta["sheets"]]
    if "Detail Item" not in titles:
        body = {"requests": [{"addSheet": {"properties": {"title": "Detail Item"}}}]}
        assert requests.post(f"{url}:batchUpdate", headers=headers, json=body).status_code == 200
        aw = requests.post(f"{url}/values/Detail%20Item!A1:H1:append?valueInputOption=USER_ENTERED",
                           headers={**headers, "Content-Type": "application/json"},
                           json={"values": [DETAIL_HEADERS]})
        assert aw.status_code == 200, aw.text
        print("Detail Item tab created")

    # 3. Upload photo to Drive COA folder
    folder = FOLDER_MAP["folders"][args.coa_name]
    with open(args.photo, "rb") as f:
        up = requests.post(
            "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
            headers=headers,
            files={
                "metadata": (None, json.dumps({"name": f"{args.no_ref}.jpg",
                                               "parents": [folder]}), "application/json"),
                "file": (f"{args.no_ref}.jpg", f, "image/jpeg"),
            })
    assert up.status_code == 200, up.text
    drive_link = f"https://drive.google.com/file/d/{up.json()['id']}/view"
    print("Drive:", drive_link)

    # 4. Append header row to Transaksi Harian (A=No filled in; link only in J)
    th_row = [str(no), args.date, args.desc, "Pengeluaran", args.coa_code,
              args.coa_name, args.total, args.method, args.no_ref, drive_link]
    aw = requests.post(f"{url}/values/Transaksi%20Harian!A:J:append?valueInputOption=USER_ENTERED",
                       headers={**headers, "Content-Type": "application/json"},
                       json={"values": [th_row]})
    assert aw.status_code == 200, aw.text

    # 5. Append item rows
    detail_rows = [[args.no_ref, args.date, name, qty, unit, qty * unit, kat, args.penjual]
                   for name, qty, unit, kat in items]
    aw = requests.post(f"{url}/values/Detail%20Item!A:H:append?valueInputOption=USER_ENTERED",
                       headers={**headers, "Content-Type": "application/json"},
                       json={"values": detail_rows})
    assert aw.status_code == 200, aw.text

    # 6. Verify
    th = requests.get(f"{url}/values/Transaksi%20Harian!A4:J", headers=headers).json().get("values", [])
    last = th[-1] if th else []
    assert last and last[0] == str(no) and last[8] == args.no_ref, f"VERIFY FAILED: {last}"
    print("VERIFIED TH:", last)
    di = requests.get(f"{url}/values/Detail%20Item!A1:H", headers=headers).json().get("values", [])
    print(f"Detail Item rows: {len(di) - 1}")
    for row in di[-len(items):]:
        print(row)


if __name__ == "__main__":
    sys.exit(main())
