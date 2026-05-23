#!/usr/bin/env python3
"""Screen references/pdfs/ for tight-binding + perovskite papers.

Purpose
-------
Papers accumulate automatically in ``references/pdfs/``.  Run this script
periodically to (1) detect newly added papers, (2) rank them by relevance to
tight-binding band-structure modelling of perovskites, (3) flag high-relevance
papers that are *not yet incorporated* into ``data/parameters/``, and (4) report
broken/truncated PDF downloads to retry later.

Usage
-----
    python scripts/screen_papers.py            # full ranked table
    python scripts/screen_papers.py --top 15   # only the top candidates

Requires ``pymupdf`` (``pip install pymupdf``).
"""

from __future__ import annotations

import argparse
import os
import sys

PDF_DIR = "references/pdfs"

# arXiv IDs already turned into parameter sets in data/parameters/.
INCORPORATED = {
    "2101.08562",  # Kashikar, Gupta, Nanda -- 13/4-orbital SK-TB, CsBX3
    "2012.14705",  # Nestoklon -- sp3d5s* ETB, cubic CsPbI3
}

KW_TB = ["tight-binding", "tight binding", "tightbinding", "slater-koster",
         "slater koster", "slater–koster"]
KW_PEROV = ["perovskite", "halide", "cspbi", "cspbbr", "cspbcl", "mapbi",
            "fapbi", "cssni", "csgei", "ch3nh3", "lead halide"]
KW_PARAM = ["hopping", "on-site", "onsite", "transfer integral", "spds",
            "sp3d5s", "tight-binding parameter", "wannier"]


def screen():
    try:
        import fitz  # noqa: F401
    except ImportError:
        sys.exit("pymupdf not installed; run: pip install pymupdf")
    import fitz

    rows, broken = [], []
    for f in sorted(os.listdir(PDF_DIR)):
        if not f.lower().endswith(".pdf"):
            continue
        arxiv_id = f.replace("arxiv_", "").replace(".pdf", "")
        path = os.path.join(PDF_DIR, f)
        try:
            doc = fitz.open(path)
            txt = "".join(doc[i].get_text() for i in range(min(doc.page_count, 6))).lower()
            title = " ".join(l.strip() for l in doc[0].get_text().split("\n")[:4]
                             if l.strip())[:90]
            doc.close()
        except Exception as e:  # truncated / corrupt download
            broken.append((f, type(e).__name__))
            continue
        tb = sum(txt.count(k) for k in KW_TB)
        pv = sum(txt.count(k) for k in KW_PEROV)
        pr = sum(txt.count(k) for k in KW_PARAM)
        score = tb * 3 + pv + pr  # weight TB presence
        rows.append((score, tb, pv, pr, arxiv_id, arxiv_id in INCORPORATED, title))

    rows.sort(reverse=True)
    return rows, broken


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--top", type=int, default=0, help="show only the top N rows")
    args = ap.parse_args(argv)

    rows, broken = screen()
    shown = rows[: args.top] if args.top else rows

    print(f"{'score':>5} {'TB':>3} {'PV':>3} {'PAR':>3} {'arXiv':>11} {'in?':>4}  title")
    print("-" * 110)
    for score, tb, pv, pr, aid, inc, title in shown:
        flag = "yes" if inc else ""
        print(f"{score:5d} {tb:3d} {pv:3d} {pr:3d} {aid:>11} {flag:>4}  {title}")

    # Candidates: high TB+perovskite relevance, not yet incorporated.
    candidates = [r for r in rows if r[1] > 0 and r[2] > 0 and not r[5]][:10]
    print("\n=== High-relevance papers NOT yet incorporated (review candidates) ===")
    for score, tb, pv, pr, aid, _inc, title in candidates:
        print(f"  {aid}  (TB={tb}, PV={pv})  {title}")

    if broken:
        print("\n=== Broken/truncated PDFs (retry after re-download) ===")
        for f, err in broken:
            print(f"  {f}  [{err}]")

    print(f"\nTotal PDFs scanned OK: {len(rows)}; broken: {len(broken)}; "
          f"already incorporated: {sum(1 for r in rows if r[5])}")


if __name__ == "__main__":
    main()
