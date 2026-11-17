# wizway-hello-aws

実績づくり向けのサンプル。  
最小構成の **Hello World**（永続化なし）。

**React + TypeScript + Python Lambda + API Gateway (HTTP API)**。DynamoDB は含まない。

データが残る版（雑メモボード）はこちら:  
https://github.com/Kazuyuki-Hongo/wizway-memo-aws

## 動いている画面（デプロイ済み）

- フロント: https://d25bl1xmuu0yux.cloudfront.net
- API: https://3k3bug5qo8.execute-api.ap-northeast-1.amazonaws.com/prod/hello

上の URL は見るだけで、このスタックは変更しません。

## 構成

```
backend/          Python Lambda (GET /hello)
frontend/         React + TypeScript (Vite) — Hello World 表示
template.yaml     SAM (HTTP API + S3 + CloudFront)
samconfig.toml    stack: wizway-hello-aws
.cursor/mcp.json  AWS Serverless MCP (AWS_PROFILE は自分のプロファイル名に書き換える)
```

### `.cursor/mcp.json` の設定

AWS Serverless MCP（AWS のデプロイ操作を Agent から使えるようにする仕組み）の設定ファイルです。

- 最後の引数 `awslabs.aws-serverless-mcp-server.exe` の `.exe` は Windows 専用です。Linux / macOS では `awslabs.aws-serverless-mcp-server` に書き換えます。
- `AWS_PROFILE` の `<自分のプロファイル名>` は、自分の AWS CLI のプロファイル名に書き換えます。ファイルをコピーしてから書き換えます。

### 構成図

![AWS architecture](docs/images/hello-architecture.png)

1. ブラウザが CloudFront → S3 のフロントを取得する  
2. 画面に載った React（TypeScript）が表示される  
3. その画面が API Gateway の `/hello` を呼ぶ  
4. Lambda が JSON を返す  

## 前提

```powershell
aws sso login --profile <自分のプロファイル名>
aws sts get-caller-identity --profile <自分のプロファイル名>
```

Docker Desktop（`sam local` 用）:

```powershell
winget install -e --id Docker.DockerDesktop
```

## デプロイ

```powershell
sam build
sam deploy --profile <自分のプロファイル名>
```

`frontend/.env.production`:

```env
VITE_API_URL=https://xxxx.execute-api.ap-northeast-1.amazonaws.com/prod
```

```powershell
cd frontend
npm ci
npm run build
aws s3 sync dist/ s3://<FrontendBucketName>/ --delete --profile <自分のプロファイル名>
aws cloudfront create-invalidation --distribution-id <CloudFrontDistributionId> --paths "/*" --profile <自分のプロファイル名>
```

## ローカル確認

Windows と Linux / macOS で同じ流れです。違うのはコマンドの書き方だけで、違う箇所には両方の例を書いています。

### バックエンド（Docker がある場合）

リポジトリ直下で実行します。Docker Desktop（Linux では Docker Engine）が動いている必要があります。

```powershell
sam build
sam local start-api
```

起動すると `Running on http://127.0.0.1:3000` のように API の URL が表示されます。この URL をメモします。

Windows（PowerShell）:

```powershell
curl.exe http://127.0.0.1:3000/hello
```

Linux / macOS:

```bash
curl http://127.0.0.1:3000/hello
```

`message` と `service` を含む JSON が返れば完了です。Windows PowerShell 5.1 では `curl` が別のコマンドになるので、`curl.exe` と書きます。

### バックエンド（Docker が無い場合）

Python で `lambda_handler` を直接呼びます。リポジトリ直下で実行します。

Windows（PowerShell）:

```powershell
@'
import json, sys
sys.path.insert(0, "backend")
from app import lambda_handler
res = lambda_handler({}, None)
print(res["statusCode"], json.loads(res["body"]))
'@ | python -
```

Linux / macOS:

```bash
python3 - <<'EOF'
import json, sys
sys.path.insert(0, "backend")
from app import lambda_handler
res = lambda_handler({}, None)
print(res["statusCode"], json.loads(res["body"]))
EOF
```

`200 {'message': 'Hello World', 'service': 'wizway-hello-aws'}` のように、`message` と `service` が見えれば完了です。Docker が無い人のローカルの確認は、ここまでと、次の「フロント」で `npm run dev` を実行して、API が未設定のときの表示が出ることの2つです。この方法では API の URL は出ないので、画面から API を呼ぶところは、Docker を使う方法か、クラウドに載せてから確かめます。
1本目が動いたあとなら、学習パックのコースC 05（Playwright）の「Docker が無いとき」の方法でも、画面の動きを確かめられます。

### フロント

`sam local start-api` が表示した API の URL を `VITE_API_URL` に書きます。

Windows（PowerShell）:

```powershell
cd frontend
npm ci
Set-Content -Path .env.local -Value "VITE_API_URL=<表示された API の URL>"
npm run dev
```

Linux / macOS:

```bash
cd frontend
npm ci
echo "VITE_API_URL=<表示された API の URL>" > .env.local
npm run dev
```

`npm run dev` が表示する URL（例: `http://localhost:5173`）をブラウザで開きます。

Docker が無い場合は、`.env.local` を作らずに `cd frontend`、`npm ci`、`npm run dev` だけを実行します。画面に「(VITE_API_URL 未設定 — ローカル確認用)」と出れば、フロントのローカル確認は完了です。

## 関連

- 雑メモ（DynamoDB）: https://github.com/Kazuyuki-Hongo/wizway-memo-aws
- 学習パック（ページの位置は同じ。案内された入口を開く）
  - ウィズウェイ: https://github.com/Kazuyuki-Hongo/ai-utilization-pack （`3.実績づくり向け/04`）
  - それ以外のグループ会社: https://github.com/Kazuyuki-Hongo/ai-utilization-pack-common （`3.実績づくり向け/04`）
