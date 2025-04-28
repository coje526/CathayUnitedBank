# **CathayUnitedBank** (Backend + API Test)

## 項目介紹

- 使用 **FastAPI** 寫一個簡單後端服務
- 有 2 個 API
    - `GET /products` : 列出商品列表
    - `GET /products/{product_id}` : 查看單一商品詳細
    - `POST /messages` : 接收使用者留言，並驗證資料格式
- 使用 **pytest + httpx** 寫自動化 API Testing
- 用 **Docker** 封裝後端與測試
- 通過 **docker-compose** 簡化啟動

## 啟動流程

### 1. 安裝相關軟體

- 安裝 Docker, Docker-Compose

### 2. 啟動服務

```bash
# 一鍵啟動 backend + api-test
$ docker-compose up --build

```

- backend 服務會上線在 [http://localhost:8000](http://localhost:8000/)
- 服務上線前，會先等 **health check** 成功。
- 自動測試 api-test 會自動啟動

### 3. 看自動測試報告

測試完成後，會在 `/reports/report.html`

可以用瀏覽器打開看。

## 文件組織

```bash
.
├── Dockerfile         # backend build
├── Dockerfile.test    # api-test build
├── docker-compose.yml # 總管理
├── main.py            # FastAPI app
├── test_api.py        # pytest 測試檔
├── reports/           # pytest-html 報告資料夾
├── requirements.txt   # backend dependencies
├── requirements-test.txt # api-test dependencies

```

## 支援的測試案例

- 正常查詢 products
- 查詢商品詳細 (products/{id})
- 搜尋 price range 與 sort
- POST /messages 正確送出
- POST /messages 錯誤資料格式檢驗
- 錯誤路徑 (e.g., `/products/&`) 設計失敗測試
