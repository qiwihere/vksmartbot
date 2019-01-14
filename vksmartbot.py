import vk_api
import lib
import json
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

OAUTH = 'AQAAAAAhCBSBAATuwXFbrFfLpECUtyfTrytLZFs'
API_KEY = '418496b115781695441809b525dc0d3053e416179d0ef7a8243b71dd95fcc7d57b0c916a8b3d72dfcac79'
FOLDER_ID = 'b1g5ijjultbev6ue6u3l'
APIAI_TOKEN = '496b61334b5a4450b84957f6e18a70e9'
GT_KEY = 'trnsl.1.1.20190107T005840Z.04ecacdc7bfd25ac.9026ad4fc123511c3b40305fe406323a9a6c9e0e'
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
                # dialogflow
                if event.obj.text:
                    answer = lib.df_answer(APIAI_TOKEN, event.obj.text)
                    # if json
                    try:
                        answer_func = json.loads('{%s}' % answer)
                        func = answer_func['action']
                        arg = answer_func['value']

                        if func == 'translate_n_speech':
                            vk.messages.send(
                                user_id=event.obj.from_id,
                                random_id=event.obj.random_id,
                                attachment=lib.translate_n_speech(arg, GT_KEY, vk_session, event.obj.from_id)
                            )


                    except ValueError:
                        gif = lib.giphy_upload(answer, vk_session, event.obj.from_id)
                        if gif:
                            vk.messages.send(
                                user_id=event.obj.from_id,
                                random_id=event.obj.random_id,
                                attachment=gif
                            )
                        else:
                            vk.messages.send(
                                user_id=event.obj.from_id,
                                random_id=event.obj.random_id,
                                message=answer
                            )

            if event.from_chat:
                file = lib.parse_voice_message(event)
                if file:
                    stt = lib.yandex_stt(file, FOLDER_ID, iam_token)
                    vk.messages.send(
                        chat_id=event.chat_id,
                        random_id=event.obj.random_id,
                        message=stt
                    )
                # dialogflow
                if event.obj.text and event.obj.text[0:3].lower() == 'бот':
                    answer = lib.df_answer(APIAI_TOKEN, event.obj.text[4:])
                    gif = lib.giphy_upload(answer, vk_session, 2000000000+event.chat_id)
                    if gif:
                        vk.messages.send(
                            chat_id=event.chat_id,
                            random_id=event.obj.random_id,
                            attachment=gif
                        )
                    else:
                        vk.messages.send(
                            chat_id=event.chat_id,
                            random_id=event.obj.random_id,
                            message=answer
                        )
