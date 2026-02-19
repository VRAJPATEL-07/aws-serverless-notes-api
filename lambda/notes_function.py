import json
import boto3
import uuid

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('NotesTable')

def lambda_handler(event, context):

    print("EVENT:", event)  # For debugging

    method = event.get("httpMethod", "")

    if method == "POST":
        try:
            body = event.get("body")

            if isinstance(body, str):
                body = json.loads(body)

            if not body or "content" not in body:
                return {
                    "statusCode": 400,
                    "body": json.dumps({"message": "Content is required"})
                }

            note_id = str(uuid.uuid4())

            table.put_item(
                Item={
                    "noteId": note_id,
                    "content": body["content"]
                }
            )

            return {
                "statusCode": 200,
                "body": json.dumps({
                    "message": "Note created successfully",
                    "noteId": note_id
                })
            }

        except Exception as e:
            print("ERROR:", str(e))
            return {
                "statusCode": 500,
                "body": json.dumps({"message": str(e)})
            }

    elif method == "GET":
        try:
            response = table.scan()
            return {
                "statusCode": 200,
                "body": json.dumps(response.get("Items", []))
            }
        except Exception as e:
            return {
                "statusCode": 500,
                "body": json.dumps({"message": str(e)})
            }

    return {
        "statusCode": 400,
        "body": json.dumps({"message": "Unsupported method"})
    }
