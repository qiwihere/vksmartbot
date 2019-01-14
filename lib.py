import requests
import json
import urllib
import urllib.request
import apiai
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


def df_answer(token, text):
    request = apiai.ApiAI(token).text_request()
    request.lang = 'ru'
    request.session_id = 'vksmartbot'
    request.query = text
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    response = responseJson['result']['fulfillment']['speech']
    if response:
        return response
    else:
        return 'Я только проснулся, попробуй еще разок!'


def giphy_upload(link, vk_session, peer_id):
    if link.find('giphy.gif')+1:

        f = open(r'giphy.gif', 'wb')
        wf = requests.get(link)
        f.write(wf.content)
        f.close()

        upload = vk_api.VkUpload(vk_session)
        doc = upload.document('giphy.gif', message_peer_id=peer_id)
        att_str = 'doc'+str(doc['doc']['owner_id'])+'_'+str(doc['doc']['id'])
        return att_str


def say(text, vk_session, peer_id):
    tts = gTTS(text, lang='en')
    f = open(r'tts.mp3', 'wb')
    tts.write_to_fp(f)
    f.close()

    upload = vk_api.VkUpload(vk_session)
    doc = upload.document('tts.mp3', message_peer_id=peer_id, doc_type='audio_message')
    att_str = 'doc' + str(doc['audio_message']['owner_id']) + '_' + str(doc['audio_message']['id'])
    return att_str


def translate_n_speech(text, key, vk_session, peer_id):
    params = "&".join([
        "key=%s" % key,
        "text=%s" % text,
        "lang=ru-en"
    ])

    url = urllib.request.Request("https://translate.yandex.net/api/v1.5/tr.json/translate?%s" % params)
    responseData = urllib.request.urlopen(url).read().decode('UTF-8')
    decodedData = json.loads(responseData)
    translated = decodedData.get('data')

    return say(translated,vk_session,peer_id)
