import boto3


iam = boto3.resource("iam")
account_id = iam.CurrentUser().arn.split(':')[4]
print(account_id)

'''dy_resource=session.resource(service_name="dynamodb")
tables = list(dy_resource.tables.all())
print(tables)'''




'''   boto3.Session()

        dynamodb_table = DynamoDBUtils.get_dynamodb_table_resource_ref(profile self._tablename)
        print( dynamodb_table)
        resp = dynamodb_table.get_item(
            Key={"name": "scheduler", "type": "config"}, ConsistentRead=True
        )
        config = resp.get("Item", {})
        resp = dynamodb_table.query(KeyConditionExpression=Key("type").eq("period"))
        config[configuration.PERIODS] = resp.get("Items")
        resp = dynamodb_table.query(KeyConditionExpression=Key("type").eq("schedule"))
        config[configuration.SCHEDULES] = resp.get("Items")

        return config'''
