# Blog Generation API (AWS Lambda + Bedrock + API Gateway + S3)

## Overview
A serverless HTTP endpoint that accepts a JSON body with a blog topic, asks **Amazon Bedrock** (Meta Llama 3 Instruct) to generate ~200 words, saves the result to **S3**, and returns a simple JSON success message. Designed to be called from Postman, cURL, or any HTTPS client via **API Gateway**. :contentReference[oaicite:0]{index=0}

---

## Architecture

![High-level flow](screenshots/architecture.png)

<details>
<summary>Mermaid (renders on GitHub)</summary>

flowchart LR
    A[Client (Postman/cURL)] -- HTTPS POST /blog-generation --> B[Amazon API Gateway (proxy)]
    B --> C[AWS Lambda (app.py)]
    C -->|invoke_model| D[Bedrock Runtime\nmeta.llama3-70b-instruct-v1:0]
    C -->|put_object| E[S3 bucket\nawsbedrockproject3/blog-output/]
    C -->|logs| F[CloudWatch Logs]
    C -->|200 JSON| B
    B --> A

