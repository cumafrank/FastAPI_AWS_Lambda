import boto3
import os

def lambda_handler(event: any, context: any):
    user = event['user']
    visit_count: int = 0
    
    # Create a DynamoDB client
    dynamodb = boto3.resource("dynamodb")
    
    table_name = os.environ["TABLE_NAME"]
    table = dynamodb.Table(table_name)
    
    # Get the current visit count
    response = table.get_item(Key={"user": user})
    if "Item" in response:
        visit_count = response["Item"]["count"]
    
    # Increment visit count by 1
    visit_count += 1
    
    # Write back to DynamoDB
    table.put_item(Item={"user": user, "count": visit_count})
    
    message = f"Hello {user} ! You've visited this page for {visit_count} time"
    return {"Message": message}

if __name__ == "__main__":
    os.environ["TABLE_NAME"] = "visit-count-table"
    event = {'user': 'Cumafrank'}
    print(lambda_handler(event, None))
    