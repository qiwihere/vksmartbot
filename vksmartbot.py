import vk_api
import requests
from vk_api.longpoll import VkLongPoll, VkEventType

API_KEY = '386f42c8e90decc0b69903e39ff2b3df71fb2afb42e5463df3830e77097532ad707228314279a726a90c1'

vk_session = vk_api.VkApi(token=API_KEY)

longpoll = VkLongPoll(vk_session)
print('test')
vk = vk_session.get_api()
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:

        if event.text == '1':
            if event.from_user:
                vk.messages.send(user_id=event.user_id, message='Ваш текст')
            elif event.from_chat:
                vk.messages.send(chat_id=event.chat_id, message='Ваш текст')