import requests
import json

def parse_voice(event):
    if event.obj.attachments:
        attachments = event.obj.attachments.pop()
        if attachments['type'] == 'audio_message':
            return attachments['audio_message']['link_ogg']


def get_iam_token(oauth):
    headers = {
        'Content-Type': 'application/json',
    }
    data = '{"yandexPassportOauthToken": "' + oauth + '"}'
    response = requests.post('https://iam.api.cloud.yandex.net/iam/v1/tokens', headers=headers, data=data)
    iam_token = json.loads(response.text)['iamToken']
    return iam_token
