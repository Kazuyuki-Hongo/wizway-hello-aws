# wizway-hello-aws

ウィズウェイ実績づくり向けの **Hello World** サンプル。  
**React + Python Lambda + API Gateway (HTTP API)** のみ（DynamoDB なし）。

データが残る見本（雑メモボード）は別リポジトリ:  
https://github.com/Kazuyuki-Hongo/wizway-memo-aws

## 構成

```
backend/          Python Lambda (GET /hello)
frontend/         React (Vite) — Hello World 表示
template.yaml     SAM (HTTP API + S3 + CloudFront)
samconfig.toml    stack: wizway-hello-aws
.cursor/mcp.json  AWS Serverless MCP (profile=deploy)
```

### 構成図

![AWS architecture](docs/images/hello-architecture.png)

1. ブラウザが CloudFront → S3 から画面ファイルを取得  
2. ブラウザ内で React が起動  
3. React が API Gateway の `/hello` を呼ぶ  
4. Lambda が JSON を返す  

## 動いている画面（デプロイ後に追記）

デプロイ後、Outputs の `FrontendUrl` / `HelloEndpoint` をここに書く。

## 前提

```powershell
aws sso login --profile deploy
aws sts get-caller-identity --profile deploy
```

Docker Desktop（`sam local` 用）:

```powershell
winget install -e --id Docker.DockerDesktop
```

## デプロイ

```powershell
sam build
sam deploy --profile deploy
```

`frontend/.env.production`:

```env
VITE_API_URL=https://xxxx.execute-api.ap-northeast-1.amazonaws.com/prod
```

```powershell
cd frontend
npm ci
npm run build
aws s3 sync dist/ s3://<FrontendBucketName>/ --delete --profile deploy
aws cloudfront create-invalidation --distribution-id <CloudFrontDistributionId> --paths "/*" --profile deploy
```

## ローカル

```powershell
sam build
sam local start-api
```

別ターミナル:

```powershell
curl http://127.0.0.1:3000/hello
```

フロント:

```powershell
cd frontend
npm ci
# .env.local に VITE_API_URL=http://127.0.0.1:3000
npm run dev
```

## 関連

- 雑メモ（DynamoDB）: https://github.com/Kazuyuki-Hongo/wizway-memo-aws
- 学習パック: https://github.com/Kazuyuki-Hongo/ai-utilization-pack （`3.実績づくり向け/04`）
