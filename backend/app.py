import json


def lambda_handler(event, context):
    event = event or {}
    path = event.get("rawPath") or event.get("path") or "/hello"
    if path.rstrip("/") not in ("", "/hello"):
        return {
            "statusCode": 404,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "GET,OPTIONS",
            },
            "body": json.dumps({"error": "not found"}, ensure_ascii=False),
        }

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "GET,OPTIONS",
        },
        "body": json.dumps(
            {
                "message": "Hello World",
                "service": "wizway-hello-aws",
            },
            ensure_ascii=False,
        ),
    }
