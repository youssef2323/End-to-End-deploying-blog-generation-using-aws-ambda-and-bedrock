# Blog Generation API (AWS Lambda + Bedrock + API Gateway + S3)

## Overview
A serverless HTTP endpoint that accepts a JSON body with a blog topic, asks **Amazon Bedrock** (Meta **Llama-3 Instruct**) to generate ~200 words, saves the text to **S3**, and returns a simple JSON success message. Designed to be called from Postman, cURL, or any HTTPS client via **API Gateway**.

---

## ✨ What it does
- **Public HTTPS** via **API Gateway** → Lambda **proxy** request.
- **Lambda** parses `{"blogtopic": "..."}` from `event.body` and validates input.
- Calls **Bedrock Runtime** `invoke_model` with model **`meta.llama3-70b-instruct-v1:0`** (native chat template).
- Saves output text to **S3** at `blog-output/<UTC>.txt` (bucket e.g., `awsbedrockproject3`).
- Returns **HTTP 200** with body **"Blog Generation is completed"**.

---

## Architecture

![High-level flow](screenshots/architecture.png)

<details>
<summary>Mermaid (renders on GitHub)</summary>

flowchart LR
  A[Client (Postman/cURL)] -->|HTTPS POST /blog-generation| B[Amazon API Gateway (proxy)]
  B --> C[AWS Lambda (app.py)]
  C -->|invoke_model| D[Bedrock Runtime<br/>meta.llama3-70b-instruct-v1:0]
  C -->|put_object| E[S3 bucket<br/>awsbedrockproject3/blog-output/]
  C -->|logs| F[CloudWatch Logs]
  C -->|HTTP 200 JSON| B
  B --> A

