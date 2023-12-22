import json
import os
import urllib3


def get_widgets(widgets):
    result = []
    inst_id = widgets
    result.append({
            "decoratedText": {
                "text": inst_id
            }
    })

    return result


def get_sections(data):
    result = []

    for value in data:
         result.append({
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
                        "title": "Unscheduled Instances",
                    },
                    "sections": get_sections(data)
                }
            }
        ]
    }


def sent_gchat_message(items):
    message = get_message(items)
    print( message)
#    url = os.environ['gchat_url']
#    http = urllib3.PoolManager()
#    http.request('POST', url, headers={'Content-Type': 'application/json'}, body=json.dumps(message))
