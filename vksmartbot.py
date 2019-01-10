import vk_api
import random
import requests
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

API_KEY = '386f42c8e90decc0b69903e39ff2b3df71fb2afb42e5463df3830e77097532ad707228314279a726a90c1'

vk_session = vk_api.VkApi(token=API_KEY)
vk = vk_session.get_api()

longpoll = VkBotLongPoll(vk_session, '176461659')

for event in longpoll.listen():

        if event.type == VkBotEventType.MESSAGE_NEW:
            if event.from_user:  # Если написали в ЛС
                vk.messages.send(  # Отправляем сообщение
                    user_id=event.user_id,
                    random_id=random.randint(0,1000),
                    message='Ваш текст'
                )
            elif event.from_chat:  # Если написали в Беседе
                vk.messages.send(  # Отправляем собщение
                    chat_id=event.chat_id,
                    random_id=random.randint(0,1000),
                    message='Ваш текст'
                )

