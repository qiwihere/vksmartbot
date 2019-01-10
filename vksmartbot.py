import vk_api
import random
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

API_KEY = '386f42c8e90decc0b69903e39ff2b3df71fb2afb42e5463df3830e77097532ad707228314279a726a90c1'

vk_session = vk_api.VkApi(token=API_KEY)
vk = vk_session.get_api()

longpoll = VkBotLongPoll(vk_session, '176461659')

for event in longpoll.listen():

        if event.type == VkBotEventType.MESSAGE_NEW:
            if event.from_user:
                if event.obj.text:
                    vk.messages.send(
                        user_id=event.obj.from_id,
                        random_id=event.obj.random_id,
                        message=event.obj.text
                    )
                print(event.obj.attachments)
            if event.from_chat:
                vk.messages.send(
                    chat_id=event.chat_id,
                    random_id=random.randint(0, 10 ^ 24),
                    message=event.obj.text
                )

