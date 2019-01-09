import vk_api
import random
import requests
from vk_api.longpoll import VkLongPoll, VkEventType

API_KEY = '386f42c8e90decc0b69903e39ff2b3df71fb2afb42e5463df3830e77097532ad707228314279a726a90c1'

vk_session = vk_api.VkApi(token=API_KEY)

longpoll = VkLongPoll(vk_session)

vk = vk_session.get_api()
for event in longpoll.listen():

        if event.type == VkEventType.MESSAGE_NEW:
            print('Новое сообщение:')

            if event.from_me:
                print('От меня для: ', end='')
            elif event.to_me:
                print('Для меня от: ', end='')

            if event.from_user:
                print(event.user_id)
            elif event.from_chat:
                print(event.user_id, 'в беседе', event.chat_id)
            elif event.from_group:
                print('группы', event.group_id)

            print('Текст: ', event.text)
            print()

        elif event.type == VkEventType.USER_TYPING:
            print('Печатает ', end='')

            if event.from_user:
                print(event.user_id)
            elif event.from_group:
                print('администратор группы', event.group_id)

        elif event.type == VkEventType.USER_TYPING_IN_CHAT:
            print('Печатает ', event.user_id, 'в беседе', event.chat_id)

        elif event.type == VkEventType.USER_ONLINE:
            print('Пользователь', event.user_id, 'онлайн', event.platform)

        elif event.type == VkEventType.USER_OFFLINE:
            print('Пользователь', event.user_id, 'оффлайн', event.offline_type)

        else:
            print(event.type, event.raw[1:])