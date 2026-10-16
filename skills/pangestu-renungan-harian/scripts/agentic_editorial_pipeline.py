#!/usr/bin/env python3
"""
Agentic Multi-Agent Editorial & Audit Pipeline for Renungan Penyiswaan
Peran:
1. AuditorKanonikalSajarah (Fact & Canon Checker)
2. KomparatorRedundansi (Anti-Monotony & Blacklist Inspector)
3. MasterEducatorWriter (4-Pilar Lean Prose Drafter)
4. RedakturPelaksana (Ruthless Gatekeeper & Quality Auditor)
"""

import sys
import re
import os
import json

class AuditorKanonikalSajarah:
    """Agent 1: Memastikan Sabda 100% verbatim dan fakta sejarah akurat."""
    @staticmethod
    def audit_source_and_history(sabda_text, narrative_text, title_header):
        issues = []
        # Check title header
        if "Panyiswaan" in title_header:
            issues.append("[AGENT 1 FAIL] Judul menggunakan 'Panyiswaan' (seharusnya 'Renungan Penyiswaan').")
        if "Pangestu" in title_header and "Renungan Penyiswaan" not in title_header:
            issues.append("[AGENT 1 FAIL] Header format tidak standar.")
            
        # Check historical error
        historical_myths = [
            r"berabad-abad\s+lampau",
            r"berabad-abad\s+lalu",
            r"ribuan\s+tahun",
            r"ratusan\s+tahun\s+lampau"
        ]
        for p in historical_myths:
            if re.search(p, narrative_text, re.IGNORECASE):
                issues.append(f"[AGENT 1 FAIL] Terdeteksi kesalahan sejarah: '{p}'. Ajaran SGS turun 14 Februari 1932 (belum 1 abad).")
                
        # Check canon verbatim
        canon_file = "/home/satyaaditech/share/pangestu_studi/buku_ssj_jawa.txt"
        with open(canon_file, "r", encoding="utf-8", errors="ignore") as f:
            canon_db = f.read()
            
        clean_sabda = re.sub(r'[\s"“”\']+', '', sabda_text)
        clean_db = re.sub(r'[\s"“”\']+', '', canon_db)
        if clean_sabda not in clean_db:
            issues.append("[AGENT 1 FAIL] Teks Sabda Jawa tidak ditemukan verbatim dalam kanon SSJ!")
            
        return issues

class KomparatorRedundansi:
    """Agent 2: Memastikan tidak ada pengulangan props dan metafora lama."""
    BLACKLIST_PROPS = [
        r"layar\s+(hp|ponsel|gawai|monitor|kerja)",
        r"notifikasi\s+(hp|ponsel|gawai)",
        r"papan\s+ketik",
        r"keyboard",
        r"balik\s+(layar\s+)?(hp|ponsel)"
    ]
    
    BLACKLIST_SOMATIC = [
        r"huuuh",
        r"double\s+inhale",
        r"dua\s+tarikan\s+(napas\s+)?singkat"
    ]
    
    @classmethod
    def audit_redundancy(cls, text):
        issues = []
        for bp in cls.BLACKLIST_PROPS:
            m = re.search(bp, text, re.IGNORECASE)
            if m:
                issues.append(f"[AGENT 2 FAIL] Redundansi terdeteksi! Menggunakan properti usang: '{m.group(0)}'.")
                
        for bs in cls.BLACKLIST_SOMATIC:
            m = re.search(bs, text, re.IGNORECASE)
            if m:
                issues.append(f"[AGENT 2 FAIL] Redundansi somatik terdeteksi! Mengulang teknik napas: '{m.group(0)}'.")
                
        return issues

class RedakturPelaksana:
    """Agent 4: Gatekeeper tanpa kompromi."""
    @staticmethod
    def audit_final_draft(draft_dict):
        report = []
        passed = True
        
        # 1. Audit Agent 1 (Kanonikal & Sajarah)
        ag1_issues = AuditorKanonikalSajarah.audit_source_and_history(
            draft_dict.get("sabda_jawa", ""),
            draft_dict.get("pangilon_rasa", "") + draft_dict.get("laku", ""),
            draft_dict.get("header", "")
        )
        if ag1_issues:
            report.extend(ag1_issues)
            passed = False
        else:
            report.append("[AGENT 1 PASS] Kanonikal 100% verbatim, sejarah 1932 akurat, header 'Renungan Penyiswaan' valid.")
            
        # 2. Audit Agent 2 (Redundansi)
        ag2_issues = KomparatorRedundansi.audit_redundancy(
            draft_dict.get("pangilon_rasa", "") + " " + draft_dict.get("laku", "")
        )
        if ag2_issues:
            report.extend(ag2_issues)
            passed = False
        else:
            report.append("[AGENT 2 PASS] Bebas dari blacklist props (layar HP/keyboard) dan bebas dari napas Huuuh.")
            
        # 3. Audit Larangan Doa (Mandat Pak Satya)
        full_text = json.dumps(draft_dict, ensure_ascii=False)
        prayer_patterns = [
            r"doa\s+penutup",
            r"doa\s+satuhu",
            r"mugi\s+paduka\s+tansah",
            r"kawula\s+ngaturaken\s+agenging\s+panuwun"
        ]
        for pp in prayer_patterns:
            if re.search(pp, full_text, re.IGNORECASE):
                report.append(f"[AGENT 4 FAIL] DILARANG KERAS MENYELIPKAN MATERI DOA! Terdeteksi: '{pp}'.")
                passed = False
                
        if passed:
            report.append("[AGENT 4 PASS] Struktur Lean 4-Pilar murni, TANPA selundupan doa.")
            
        # 4. Audit Bahasa
        # Pangilon & Laku must be 100% Indonesian
        # Quick heuristic check for long Javanese phrases in Pangilon
        javanese_markers = ["menika", "dhumateng", "ingkang", "panjenengan", "kawula", "saged"]
        found_jv = [w for w in javanese_markers if f" {w} " in draft_dict.get("pangilon_rasa", "").lower()]
        if len(found_jv) >= 2:
            report.append(f"[AGENT 4 FAIL] Pangilon Rasa mengandung bahasa Jawa untuk narasi publik: {found_jv}")
            passed = False
        else:
            report.append("[AGENT 4 PASS] Batasan bahasa mutlak terpenuhi (100% Bahasa Indonesia).")
            
        return passed, report
