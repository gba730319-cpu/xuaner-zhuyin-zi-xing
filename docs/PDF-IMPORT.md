# 歷屆 PDF 匯入流程

## 目前原則
題本與答案 PDF 先分開保存。抽出的文字只算「待校對原始文字」，不可直接當成正式題目，也不可把題本上的空格或 OCR 推測當成答案。

## 本機資料夾
將取得的原始 PDF 放在專案根目錄的 `source-pdfs/`（此資料夾已加入 gitignore，不會把整批原始 PDF 推上公開 GitHub）。抽取結果放在 `artifacts/extracted/`，同樣不納入版本控制。

## 安裝
```bash
python -m pip install pymupdf
```

## 執行範例
```bash
python scripts/extract_pdf_pages.py \
  --pdf "source-pdfs/113國語字音字形-國小組(題目).pdf" \
  --year 113 \
  --competition national \
  --group elementary \
  --kind question \
  --source-url "https://www.mhps.cyc.edu.tw/modules/tadnews/index.php?nsn=6030"
```

答案 PDF 的 `--kind` 改為 `answer`，並使用對應答案檔。

## 產出內容
- JSON：年度、競賽類型、組別、檔名、來源網址、SHA-256、頁數、逐頁文字及 OCR 警示。
- TXT：方便人工逐頁檢查的文字稿。
- `needs_ocr=true`：該頁抽不到足夠文字，應進行 OCR 或人工抄錄。

## 正式入庫前的人工驗收
1. 封面年度與檔名一致。
2. 確認「全國賽國小組」，不可混入其他組別或校內題。
3. 核對題目頁數、題號、字音/字形區段與題數。
4. 對照答案卷逐題核對；不確定者標記 `needs_review`。
5. 字音依教育部《國語一字多音審訂表》覆核；字形依教育部常用字標準字體覆核。
6. 完成後才把題目轉成 `data/questions/` 內符合 schema 的 JSON。

## 狀態定義
- 找到索引：來源頁列出附件。
- 附件網址已確認：已取得可直接下載的附件連結。
- 已下載：PDF 檔案本體已取得並檢查可開啟。
- 已抽取：已產生逐頁文字稿。
- 已校對：題目、答案、年度與組別均已人工覆核。
- 已匯入：符合題目 schema，網站實際載入成功。

上述狀態不可互相替代。
