#!/usr/bin/env python3
"""Extract text from references/pdfs/*.pdf into references/texts/*.txt.

Fallback for environments without poppler's ``pdftotext``. Uses pymupdf
(``fitz``) with reading-order sorting. Skips files already extracted.

Usage:
    python scripts/pdf_to_text.py
"""

from __future__ import annotations

import os
import sys

PDF_DIR = "references/pdfs"
TXT_DIR = "references/texts"


def main():
    try:
        import fitz
    except ImportError:
        sys.exit("pymupdf not installed; run: pip install pymupdf")

    os.makedirs(TXT_DIR, exist_ok=True)
    n_done = n_skip = n_err = 0
    for f in sorted(os.listdir(PDF_DIR)):
        if not f.lower().endswith(".pdf"):
            continue
        out = os.path.join(TXT_DIR, f[:-4] + ".txt")
        if os.path.exists(out):
            n_skip += 1
            continue
        try:
            doc = fitz.open(os.path.join(PDF_DIR, f))
            with open(out, "w", encoding="utf-8") as fh:
                for i in range(doc.page_count):
                    fh.write(f"\n===== PAGE {i+1} =====\n")
                    fh.write(doc[i].get_text("text", sort=True))
            doc.close()
            n_done += 1
        except Exception as e:
            n_err += 1
            print(f"  ERROR {f}: {type(e).__name__}")
    print(f"extracted {n_done}, skipped {n_skip}, errors {n_err} -> {TXT_DIR}/")


if __name__ == "__main__":
    main()
