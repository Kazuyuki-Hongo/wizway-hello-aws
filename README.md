# wizway-hello-aws

?????????????? **Hello World** ?????  
**React + Python Lambda + API Gateway (HTTP API)** ???DynamoDB ????

???????????????????????:  
https://github.com/Kazuyuki-Hongo/wizway-memo-aws

## ???????????????

- ????: https://d25bl1xmuu0yux.cloudfront.net
- API: https://3k3bug5qo8.execute-api.ap-northeast-1.amazonaws.com/prod/hello

## ??

```
backend/          Python Lambda (GET /hello)
frontend/         React (Vite) ? Hello World ??
template.yaml     SAM (HTTP API + S3 + CloudFront)
samconfig.toml    stack: wizway-hello-aws
.cursor/mcp.json  AWS Serverless MCP (profile=deploy)
```

### ???

![AWS architecture](docs/images/hello-architecture.png)

1. ????? CloudFront ? S3 ?????????????  
2. ?????? React ?????  
3. React ? API Gateway ? `/hello` ???  
4. Lambda ? JSON ???  

## ??

```powershell
aws sso login --profile deploy
aws sts get-caller-identity --profile deploy
```

Docker Desktop?`sam local` ??:

```powershell
winget install -e --id Docker.DockerDesktop
```

## ????

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

## ????

```powershell
sam build
sam local start-api
```

??????:

```powershell
curl http://127.0.0.1:3000/hello
```

????:

```powershell
cd frontend
npm ci
# .env.local ? VITE_API_URL=http://127.0.0.1:3000
npm run dev
```

## ??

- ????DynamoDB?: https://github.com/Kazuyuki-Hongo/wizway-memo-aws
- ?????: https://github.com/Kazuyuki-Hongo/ai-utilization-pack ?`3.???????/04`?
