import boto3

# from arnparse import arnparse

def get_widgets(widgets):
    result = []
    for item in widgets[:50]:
        result.append({
            "decoratedText": {
                "text": item[0] + ": " + item[1],
                "bottomLabel": "Tags: " + ', '.join(item[2])
            }
        })

    return result


def get_sections(data):
    result = []

    for key, value in data.items():
        result.append({
            "header": key,
            "collapsible": True,
            "uncollapsibleWidgetsCount": 1,
            "widgets": get_widgets(value)
        })

    return result


def get_message(data):
    return {
        "cardsV2": [
            {
                "cardId": "unique-card-id",
                "card": {
                    "header": {
                        "title": "Untagged Resources",
                    },
                    "sections": get_sections(data)
                }
            }
        ]
    }


def sent_gchat_message(items):
     message = get_message(items)
     print(message)


def get_tag(tags, tag_key):
    if tags is None:
        return ''

    for tag in tags:
        if tag["Key"] == tag_key:
            return tag["Value"]
    return ''

def get_untagged_resouces(aws_account_id):
    ec2 = boto3.client('ec2')
    regions = ec2.describe_regions().get('Regions', [])

    result = {}
    for region in regions:
        data = get_untagged_resouces_by_region(aws_account_id, region['RegionName'])
        print(data)
        if len(data) > 0:
            key = aws_account_id + ":" + region['RegionName']
            result[key] = data

    return result


def get_untagged_resouces_by_region(aws_account_id, region):
    result = []

    data = get_resouces_by_region(aws_account_id, region)

    for i in data:
        missing_tags = []
        for tag in ["Owner", "customerName", "productFamily"]:
            if get_tag(i[2], tag) == '':
                missing_tags.append(tag)

        if len(missing_tags) > 0:
            result.append([i[0], i[1], missing_tags])


    return result


def get_resouces_by_region(aws_account_id, region):
    ec2_resource = boto3.resource('ec2', region_name=region)

    result = []

    for i in ec2_resource.images.filter(Owners=[aws_account_id]).all():
        result.append(["Image", i.id, i.tags])

    for i in ec2_resource.snapshots.filter(OwnerIds=[aws_account_id]).all():
        result.append(["Snapshot", i.id, i.tags])

    for i in ec2_resource.instances.all():
        result.append(["Instance", i.id, i.tags])

    for i in ec2_resource.volumes.all():
        result.append(["Volume", i.id, i.tags])

    return result
dev = boto3.Session(profile_name="skyvera")
iam = dev.resource("iam")
account_id = iam.CurrentUser().arn.split(':')[4]
resources = get_untagged_resouces(account_id)
if len(resources) > 0:
    sent_gchat_message(resources)

