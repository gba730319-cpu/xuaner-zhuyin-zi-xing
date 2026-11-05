#!/usr/bin/env python3
"""Extract page-level text from historical competition PDFs for human review.

This deliberately does NOT turn OCR text into verified questions or answers.
Requires: python -m pip install pymupdf
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

try:
    import fitz
except ImportError as exc:
    raise SystemExit("缺少 PyMuPDF，請先執行：python -m pip install pymupdf") from exc


def main() -> None:
    parser = argparse.ArgumentParser(description="逐頁抽取字音字形 PDF 文字")
    parser.add_argument("--pdf", required=True, type=Path, help="來源 PDF 路徑")
    parser.add_argument("--year", required=True, type=int, help="民國年度，例如 113")
    parser.add_argument("--competition", choices=["national", "keelung", "other_city", "school"], default="national")
    parser.add_argument("--group", default="elementary")
    parser.add_argument("--kind", choices=["question", "answer", "question_and_answer"], required=True)
    parser.add_argument("--source-url", required=True)
    parser.add_argument("--out", type=Path, default=Path("artifacts/extracted"))
    args = parser.parse_args()

    pdf_path = args.pdf.expanduser().resolve()
    if not pdf_path.is_file():
        raise SystemExit(f"找不到 PDF：{pdf_path}")

    digest = hashlib.sha256(pdf_path.read_bytes()).hexdigest()
    doc = fitz.open(pdf_path)
    pages = []
    for index, page in enumerate(doc, start=1):
        raw_text = page.get_text("text").strip()
        pages.append({
            "page": index,
            "text": raw_text,
            "text_char_count": len(raw_text),
            "needs_ocr": len(raw_text) < 20,
            "review_status": "unreviewed"
        })

    args.out.mkdir(parents=True, exist_ok=True)
    stem = f"{args.year}-{args.competition}-{args.group}-{args.kind}"
    payload = {
        "year": args.year,
        "competition": args.competition,
        "group": args.group,
        "document_kind": args.kind,
        "source_file": pdf_path.name,
        "source_url": args.source_url,
        "sha256": digest,
        "page_count": len(doc),
        "extraction_engine": f"PyMuPDF {fitz.VersionBind}",
        "warning": "逐頁文字僅供人工校對；尚未拆題、驗證答案或核對教育部標準。",
        "pages": pages
    }
    json_path = args.out / f"{stem}.json"
    text_path = args.out / f"{stem}.txt"
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    text_path.write_text(
        "\n\n".join(f"===== PDF 第 {p['page']} 頁 =====\n{p['text']}" for p in pages),
        encoding="utf-8"
    )
    empty_pages = sum(1 for page in pages if page["needs_ocr"])
    print(f"完成逐頁抽取：{json_path}")
    print(f"純文字校對稿：{text_path}")
    print(f"頁數：{len(pages)}；需要 OCR/人工檢查：{empty_pages} 頁")
    print("注意：這不是已匯入題庫，必須逐題校對後才能建立正式題目資料。")


if __name__ == "__main__":
    main()
