# Blog Generation API (AWS Lambda + Bedrock + API Gateway + S3)

## Overview
A serverless HTTP endpoint that accepts a JSON body with a blog topic, asks **Amazon Bedrock** (Llama-3 Instruct) to generate ~200 words, saves the text to **S3**, and returns a simple success message. Designed for Postman/cURL/any HTTPS client via **API Gateway**.

---

## ✨ What it does
- **Public HTTPS** via **API Gateway** → Lambda proxy request.
- **Lambda** parses `{"blogtopic": "..."}` from `event.body`, validates input.
- Calls **Bedrock Runtime** `invoke_model` with `meta.llama3-70b-instruct-v1:0` (native chat template).
- Saves output text to **S3** at `blog-output/<UTC>.txt`.
- Returns HTTP **200** with body `"Blog Generation is completed"`.

---

## Architecture
![High-level flow](screenshots/architecture.png)

---

## Request & Response

### Endpoint
