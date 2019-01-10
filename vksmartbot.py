import vk_api
import lib
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

OAUTH = 'AQAAAAAhCBSBAATuwXFbrFfLpECUtyfTrytLZFs'
API_KEY = '386f42c8e90decc0b69903e39ff2b3df71fb2afb42e5463df3830e77097532ad707228314279a726a90c1'
FOLDER_ID = 'b1g5ijjultbev6ue6u3l'

GROUP_ID = '176461659'
iam_token = lib.get_iam_token(OAUTH)

vk_session = vk_api.VkApi(token=API_KEY)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, GROUP_ID)

for event in longpoll.listen():

        if event.type == VkBotEventType.MESSAGE_NEW:
            if event.from_user:
                file = lib.parse_voice_message(event)
                if file:
                    stt = lib.yandex_stt(file, FOLDER_ID, iam_token)
                    vk.messages.send(
                        user_id=event.obj.from_id,
                        random_id=event.obj.random_id,
                        message=stt
                    )
                    lib.gtts_write(stt, vk_session, event.obj.peer_id, GROUP_ID)
            if event.from_chat:
                file = lib.parse_voice_message(event)
                if file:
                    stt = lib.yandex_stt(file, FOLDER_ID, iam_token)
                    vk.messages.send(
                        chat_id=event.chat_id,
                        random_id=event.obj.random_id,
                        message=stt
                    )


