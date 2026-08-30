#!/usr/bin/env python3
"""
Auto-classify transaction -> Sheets + Drive upload
Part of finance-automation skill.

Usage:
  python auto_finance.py --date "2026-05-30" --desc "Beli bensin" --amount 50000 --method "Cash"
  python auto_finance.py --date "2026-05-30" --desc "Bensin motor" --amount 45000 --method "Cash" --file "/path/to/nota.jpg"
"""

import os, sys, json, re, argparse
from datetime import datetime

MAP_PATH = os.path.expanduser("~/.hermes/finance_drive_folders.json")
SPREADSHEET_ID = "13W8pmkqdXwv_Nv4x-reIrw7m0JXOGVWENmXEtgrjG7U"
GAPI = f"python {os.environ.get('HERMES_HOME', os.path.expanduser('~/.hermes'))}/skills/productivity/google-workspace/scripts/google_api.py"

COA_RULES = [
    (r"gaji|salary|payroll|upah", "Gaji/Pendapatan Utama", "5000", "Pemasukan"),
    (r"sampingan|freelance|jualan|side.income", "Pendapatan Sampingan", "5100", "Pemasukan"),
    (r"investasi|deposito|bunga|dividen", "Pendapatan Investasi", "5200", "Pemasukan"),
    (r"modal|setoran.awal|investasi.pribadi", "Modal", "4000", "Pemasukan"),
    (r"prive|tarik.tunai.pribadi|penarikan", "Prive/Penarikan", "4100", "Pengeluaran"),
    (r"makan|makanan|kopi|snack|catering|warteg", "Beban Makanan", "6000", "Pengeluaran"),
    (r"bensin|parkir|toll|gojek|grab|transport|taksi|commuting", "Beban Transportasi", "6100", "Pengeluaran"),
    (r"listrik|pln|air|pam", "Beban Listrik & Air", "6200", "Pengeluaran"),
    (r"internet|wifi|pulsa|kuota|paket.data", "Beban Internet & Pulsa", "6300", "Pengeluaran"),
    (r"kursus|bimbel|seminar|pelatihan|buku|pendidikan", "Beban Pendidikan", "6400", "Pengeluaran"),
    (r"dokter|obat|rumah.sakit|klinik|bpjs", "Beban Kesehatan", "6500", "Pengeluaran"),
    (r"baju|sepatu|tas|pakaian|laundry", "Beban Pakaian", "6600", "Pengeluaran"),
    (r"nonton|game|hiburan|spotify|netflix|bioskop|jalan.jalan", "Beban Hiburan", "6700", "Pengeluaran"),
    (r"sedekah|infaq|zakat|amal|donasi", "Beban Amal/Sedekah", "6800", "Pengeluaran"),
    (r"printer|laptop|peralatan|elektronik|projector|komputer", "Peralatan", "2000", "Pengeluaran"),
    (r"motor|mobil|kendaraan|service.kendaraan", "Kendaraan", "2100", "Pengeluaran"),
    (r"utang.supplier|utang.dagang|hutang.usaha", "Utang Usaha", "3000", "Pengeluaran"),
    (r"utang.bank|pinjaman.bank|kpr|kredit", "Utang Bank", "3100", "Pengeluaran"),
    (r"transfer.bca|bca|setor.bca", "Bank BCA", "1100", "Aset"),
    (r"transfer.mandiri|mandiri|setor.mandiri", "Bank Mandiri", "1200", "Aset"),
    (r"kas|tarik.tunai|setor.tunai", "Kas", "1000", "Aset"),
    (r"piutang|utang.pelanggan|pinjaman.dibayar", "Piutang", "1300", "Aset"),
]

def classify_coa(description):
    desc_lower = re.sub(r'[^\w\s]', '.', description.lower())
    for pattern, name, code, tipe in COA_RULES:
        if re.search(pattern, desc_lower):
            return name, code, tipe
    return "Beban Lain-lain", "6900", "Pengeluaran"

def get_next_row_no():
    import subprocess
    result = subprocess.run(
        [GAPI.replace("python ", ""), "sheets", "get", SPREADSHEET_ID, "'Transaksi Harian'!A:A"],
        capture_output=True, text=True, shell=True
    )
    try:
        data = json.loads(result.stdout)
        return len(data)
    except:
        return 5

def append_to_sheets(date_str, desc, tipe, coa_code, coa_name, amount, method, ref="-"):
    import subprocess
    row_no = get_next_row_no()
    values = json.dumps([[str(row_no - 2), date_str, desc, tipe, coa_code, coa_name, str(amount), method, ref]])
    cmd = f"{GAPI} sheets append {SPREADSHEET_ID} \"'Transaksi Harian'!A:I\" --values '{values}'"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.returncode == 0, result.stdout

def upload_to_drive(file_path, coa_name, date_str, desc):
    import subprocess
    if not os.path.exists(MAP_PATH):
        return False, f"Folder map not found at {MAP_PATH}"
    with open(MAP_PATH) as f:
        folder_map = json.load(f)
    folder_id = folder_map.get("folders", {}).get(coa_name)
    if not folder_id:
        return False, f"Folder for {coa_name} not found"
    ext = os.path.splitext(file_path)[1] or ".jpg"
    new_name = f"{date_str.replace('-','')}_{desc.replace(' ','_')}{ext}"
    cmd = f"{GAPI} drive upload {file_path} --name \"{new_name}\" --parent {folder_id}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.returncode == 0, result.stdout

def create_folder_structure():
    import subprocess
    # Create root finance folder
    result = subprocess.run(f"{GAPI} drive create-folder \"finance\"", shell=True, capture_output=True, text=True)
    root = json.loads(result.stdout) if result.returncode == 0 else {}
    root_id = root.get("id", "")
    if not root_id:
        print("Failed to create root folder")
        return
    
    # Create 2026 folder
    result = subprocess.run(f"{GAPI} drive create-folder \"2026\" --parent {root_id}", shell=True, capture_output=True, text=True)
    year = json.loads(result.stdout) if result.returncode == 0 else {}
    year_id = year.get("id", "")
    
    coa_list = [
        "Kas", "Bank BCA", "Bank Mandiri", "Piutang", "Peralatan", "Kendaraan",
        "Utang Usaha", "Utang Bank", "Modal", "Prive",
        "Gaji", "Pendapatan Sampingan", "Pendapatan Investasi",
        "Beban Makanan", "Beban Transportasi", "Beban Listrik & Air",
        "Beban Internet & Pulsa", "Beban Pendidikan", "Beban Kesehatan",
        "Beban Pakaian", "Beban Hiburan", "Beban Amal", "Beban Lain-lain"
    ]
    
    folder_map = {"root": root_id, "2026": year_id, "folders": {}}
    for coa in coa_list:
        result = subprocess.run(f"{GAPI} drive create-folder \"{coa}\" --parent {year_id}", shell=True, capture_output=True, text=True)
        data = json.loads(result.stdout) if result.returncode == 0 else {}
        folder_map["folders"][coa] = data.get("id", "")
    
    with open(MAP_PATH, 'w') as f:
        json.dump(folder_map, f, indent=2)
    print(f"Folder structure created. Map saved to {MAP_PATH}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=datetime.now().strftime("%Y-%m-%d"))
    parser.add_argument("--desc", required=True)
    parser.add_argument("--amount", type=int, required=True)
    parser.add_argument("--method", default="Cash")
    parser.add_argument("--ref", default="-")
    parser.add_argument("--file", default=None)
    parser.add_argument("--setup-only", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    
    if args.setup_only:
        create_folder_structure()
        sys.exit(0)
    
    coa_name, coa_code, tipe = classify_coa(args.desc)
    
    if args.dry_run:
        print(json.dumps({
            "dry_run": True, "date": args.date, "desc": args.desc,
            "coa": coa_name, "code": coa_code, "tipe": tipe, "amount": args.amount
        }, indent=2))
        sys.exit(0)
    
    ok_sheet, msg_sheet = append_to_sheets(args.date, args.desc, tipe, coa_code, coa_name, args.amount, args.method, args.ref)
    
    drive_msg = "Tidak ada nota"
    if args.file and os.path.exists(args.file):
        ok_drive, msg_drive = upload_to_drive(args.file, coa_name, args.date, args.desc)
        drive_msg = "Nota tersimpan di Drive" if ok_drive else f"Gagal upload: {msg_drive}"
    
    print(json.dumps({
        "success": ok_sheet, "date": args.date, "description": args.desc,
        "coa": coa_name, "coa_code": coa_code, "tipe": tipe,
        "amount": args.amount, "method": args.method, "drive_status": drive_msg
    }, indent=2))
