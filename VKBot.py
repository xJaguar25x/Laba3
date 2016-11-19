# -*- coding: utf-8 -*-
import vk
import time
import datetime
# импортируем файл с первой лабы
import OWM


print ('VkBot_v1.0 считывает сообщения...')

# Авторизируем сессию с помощью access token
session = vk.Session('f96af61ea309631edd77daccea43268fe475480eef67bc9173c866f0e5f61eda5f5bd3d803715032fc151')

# Или с помощью id приложения и данных авторизации пользователя
# session = vk.AuthSession('app id','login','pass')

# Создаем объект Api
api = vk.API(session)

while (True):
    # Получим 20 последних смс
    messages = api.messages.get()

    # Создадим список используемых команд
    commands = ['help', 'Help', 'weather', 'Weather', 'Погода', 'погода', 'stop']

    # Найдем среди них непрочитанные смс с поддерживаемыми командами
    # таким образом получим список в формате [(id_пользователя , id_ смс , команда), ...]
    messages = [(m['uid'], m['mid'], m['body'])
                for m in messages[1:] if m['body'] in commands and m['read_state'] == 0]

    # Отвечаем на полученные команды
    for m in messages:
        user_id = m[0]
        message_id = m[1]
        command = m[2]

        # Сформируем строку с датой и временем сервера
        date_time_string = datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]')

        if command == 'help' or command == 'Help':
            api.messages.send(user_id=user_id,
                              message=date_time_string +'\n>VKBOT v1.0\n>Разработал: Jaguar25')
        # Русские команды не робят, с большой буквы норм
        if command == 'weather' or command == 'Weather' or command == 'погода' or command == 'Погода':
            api.messages.send(user_id=user_id,
                              message='\n' + OWM.full_weather)

        if command == 'stop':
            break
    # Формируем id всех смс с командами через запятую
    ids = ', '.join([str(m[1]) for m in messages])

    # Помечаем полученные смс как прочитанные
    if ids:
        api.messages.markAsRead(message_ids=ids)

    # Проверяем смс каждые 2 сек
    time.sleep(2)

    #print OWM.full_weather