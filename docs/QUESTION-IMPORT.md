# 歷屆題庫匯入流程

## 1. 準備 JSON
以 `data/questions/import-template.json` 為外層格式，題目欄位依 `data/questions/schema/question.schema.json`。

每題至少包含：
- `id`：唯一 ID，例如 `national-114-elementary-phonetic-001`
- `competition`：`keelung`、`national`、`other_city`、`school` 或 `demo`
- `year`：民國年度；示範題填 null
- `group`：目前使用 `elementary`
- `type`：`phonetic` 或 `form`
- `prompt`、`answer`、`display`
- `source_id`：對應 `data/sources.json`；無來源的示範題填 null
- `verification_status`：`transcribed_unverified` 或 `verified`

## 2. 使用網站檢查
1. 開啟「題庫匯入」。
2. 選擇 JSON 檔並按「檢查匯入檔」。
3. 修正缺漏欄位、重複 ID 或與現有題庫衝突的 ID。
4. 檢查通過後，下載合併後的 `catalog.json`。

## 3. 更新 GitHub
將下載的 `catalog.json` 內容更新至 `data/questions/catalog.json`。網站讀取的是 GitHub 上的中央題庫；只在瀏覽器匯入預覽不會自動更新 GitHub。

## 4. 查證原則
- `transcribed_unverified` 題目只存檔，不會出現在練習或模擬考。
- `verified` 必須已核對題目、答案、年度、組別及來源。
- 不可把其他縣市、校內題目或全國賽題目誤標為基隆市正式題目。
- OCR 結果必須回看原始檔逐題核對。
