import json
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
from datetime import datetime, timezone

# 1) Create the Bedrock Runtime client
client = boto3.client(
    "bedrock-runtime",
    region_name="us-east-1",
    config=Config(
        read_timeout=300,
        retries={"max_attempts": 3},
    ),
)

# 2) Choose a model ID (fixed)
MODEL_ID = "meta.llama3-70b-instruct-v1:0"


def generate_with_invoke(topic: str) -> str:
    # 3) Build a prompt in the model's native format (Meta Llama 3 chat template)
    formatted_prompt = f"""
<|begin_of_text|><|start_header_id|>user<|end_header_id|>
Write a 200-word blog post about: {topic}
<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>
""".strip()

    # 4) Request body as a dict (no json.dumps here)
    native_request = {
        "prompt": formatted_prompt,
        "max_gen_len": 512,
        "temperature": 0.5,
        "top_p": 0.9,
    }

    try:
        # 5) Call invoke_model (dump ONCE here)
        resp = client.invoke_model(
            modelId=MODEL_ID,
            body=json.dumps(native_request).encode("utf-8"),
            accept="application/json",
            contentType="application/json",
        )
        # 6) Read the stream, then load JSON
        payload = json.loads(resp["body"].read())

        # 7) Extract text (Meta Llama native returns "generation")
        return payload.get("generation", "")
    except (ClientError, Exception) as e:
        print(f"Invoke error: {e}")
        return ""


def save_blog_details_s3(s3_key, s3_bucket, generate_blog: str):
    s3 = boto3.client("s3")
    try:
        s3.put_object(Bucket=s3_bucket, Key=s3_key, Body=generate_blog.encode("utf-8"))
    except Exception as e:
        print(f"Error when saving to S3: {e}")


def lambda_handler(event, context):
    # Safely parse the incoming JSON body
    try:
        body = json.loads(event.get("body") or "{}")
    except Exception as e:
        return {"statusCode": 400, "body": json.dumps({"error": f"Invalid JSON: {e}"})}

    blogtopic = (body.get("blogtopic") or "").strip()
    if not blogtopic:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "blogtopic is required"}),
        }

    generate_blog = generate_with_invoke(topic=blogtopic)

    if generate_blog:
        # Use a colon-free UTC timestamp for S3 keys
        current_time = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        s3_key = f"blog-output/{current_time}.txt"
        s3_bucket = "awsbedrockproject3"
        save_blog_details_s3(s3_key, s3_bucket, generate_blog)
    else:
        print("No blog was generated")

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps("Blog Generation is completed"),
    }


# def blog_generate_using_bedrock(blogtopic: str) -> str:
#     prompt = f"""<s>[INST]Human: Write a 200 words blog on the topic {blogtopic}
#     Assistant:[/INST]


#     """

#     body = {
#         "prompt": prompt,
#         "maxTokens": 512,
#         "temperature": 0.5,
#         "topP": 0.9,
#     }

#     try:
#         bedrock = boto3.client(
#             "bedrock-runtime",
#             region_name="us-east-1",
#             config=botocore.config.Config(
#                 read_timeout=300,
#                 retries={"max_attempts": 3},
#             ),
#         )
#         bedrock.invoke_model(
#             body=json.dumps(body),
#             modelId="meta.llama3-3-70b-instruct-v1:0",
#         )

#         response_content = response.get("body").read()
#         response_data = json.loads(response_content)
#         print(response_data)
#         blog_details = response_data["generation"]
#         return blog_details

#     except Exception as e:
#         print(f"Error generating the blog: {e}")
#         return ""
