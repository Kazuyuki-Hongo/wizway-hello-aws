# wizway-hello-aws

ウィズウェイ実績づくり向けのサンプル。  
最小構成の **Hello World**（永続化なし）。

**React + Python Lambda + API Gateway (HTTP API)**。DynamoDB は含まない。

データが残る版（雑メモボード）はこちら:  
https://github.com/Kazuyuki-Hongo/wizway-memo-aws

## 動いている画面（デプロイ済み）

- フロント: https://d25bl1xmuu0yux.cloudfront.net
- API: https://3k3bug5qo8.execute-api.ap-northeast-1.amazonaws.com/prod/hello

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

1. ブラウザが CloudFront → S3 のフロントを取得する  
2. 画面に載った React が表示される  
3. React が API Gateway の `/hello` を呼ぶ  
4. Lambda が JSON を返す  

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

## ローカル確認

```powershell
sam build
sam local start-api
```

API だけ:

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
