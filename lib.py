import requests
import json
import urllib
import urllib.request
from gtts import gTTS
import vk_api
from vk_api import VkUpload


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
    decodedData = json.loads(responseData)
    if decodedData.get("error_code") is None:
        speech_text = decodedData.get('result')
        return speech_text
    else:
        return 'Не понимаю, что ты сказал'


def gtts_write(text, vk_session, peer_id):
    f = open(r'speech.mp3', 'wb')
    tts = gTTS(text, lang='ru')
    tts.write_to_fp(f)
    f.close()

    upload = vk_api.VkUpload(vk_session)
    audio_message = upload.audio_message(f, peer_id=peer_id)

    print(audio_message)
    print('test')
