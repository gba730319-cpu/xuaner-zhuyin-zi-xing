# 題庫資料管理規格

## 單一資料來源
- 正式題目集中放在 `data/questions/catalog.json`。
- 網站練習、錯題本及模擬考都讀取同一份題庫資料。
- `schema/question.schema.json` 定義每題必填欄位與驗證狀態。

## 分類欄位
- `competition`: `keelung`、`national`、`other_city`、`school` 或 `demo`。
- `year`: 民國年度；示範題使用 null。
- `type`: `phonetic`（字音）或 `form`（字形）。
- `group`: 目前目標組別為 `elementary`。
- `source_id`、`source_page`: 對應 `data/sources.json` 的來源及頁碼。
- `verification_status`: `demo`、`transcribed_unverified`、`verified`。

## 匯入與審核原則
1. 先確認競賽類型、年度、組別及原始頁面。
2. 逐題轉錄題目，不以 OCR 結果直接當作定稿。
3. 對照官方答案卷及教育部標準；字音依《國語一字多音審訂表》，字形依常用字標準字體。
4. 題目與答案均核對後，才可標記 `verified`。
5. 只有 `verified` 題目可以進入正式練習與正式模擬考；示範題只能用於測試介面。
6. 不確定的字、答案或出處保持未驗證，不猜答案。

## 版本狀態
目前 catalog 內只有 6 題示範題，尚無已驗證的歷屆正式題目。
