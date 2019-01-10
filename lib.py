import requests
import json
import urllib


def parse_voice_message(event):
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


def yandex_stt(file, folder_id, IAM_TOKEN):
    f = open(r'voice.ogg', 'wb')
    wf = requests.get(file)
    f.write(wf.content)
    f.close()

    data = open('voice.ogg','rb').read()
    params = "&".join([
        "topic=general",
        "folderId=%s" % folder_id,
        "lang=ru-RU"
    ])

    url = urllib.request.Request("https://stt.api.cloud.yandex.net/speech/v1/stt:recognize/?%s" % params, data=data)
    url.add_header("Authorization", "Bearer %s" % IAM_TOKEN)
    url.add_header("Transfer-Encoding", "chunked")

    responseData = urllib.request.urlopen(url).read().decode('UTF-8')
    #decodedData = json.loads(responseData)
    return responseData
