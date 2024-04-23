# Игра Глаголов - Умный Бот

Телеграм и vk бот для получения ответов на частые вопросы.
Шаблонные ответы генерируются через сервис 
[dialogflow](https://cloud.google.com/dialogflow).


## Установка

```commandline
git clone https://github.com/zatomis/dev-verb-games-bot
```

## Установка зависимостей
В директории с исполняемым файлом

```commandline
cd dev-verb-games-bot
```

Установка
```commandline
pip install -r requirements.txt
```

## Предварительная подготовка

### Подготовка vk

Создайте группу в [vk](vk.com), получите [API для сообщений сообществ](https://dev.vk.com/ru/api/community-messages/getting-started?ref=old_portal), установите права доступа для сообщений 
сообщества. Включите сообщения сообщества в настройках группы.

### Запуск telegram Бота

Создайте 2 ботов в [botfather](https://t.me/BotFather).
1-ый - отвечает на вопросы
2-ой - мониторинг состояния бота в vk и 1-ого бота.

### Подготовка Dialogflow

Создайте DialogFlow [проект](https://cloud.google.com/dialogflow/es/docs/quick/setup). 
[Получите токен и credentials](https://cloud.google.com/docs/authentication/api-keys)


## Создание и настройка .env

Создайте в корне папки `Game_of_verbs` файл `.env`. Откройте его для редактирования любым текстовым редактором
и запишите туда данные в таком формате: `ПЕРЕМЕННАЯ=значение`.
Доступны следующие переменные:

 - VERBBOT_TOKEN = ваш телеграм бот API ключ(бот, который отвечает на вопросы).
 - PROJECT_ID = id проекта DIALOGFLOW 
 - LANGUAGE_CODE='RU'
 - VK_KEY = Ваш vk API ключ(для бота, который отвечает на вопросы)
 - TELEGRAM_LOGS_TOKEN - ваш телеграм бот API ключ(бот, который отправляет уведомления в личку/канал/чат, при наличии, каких-либо ошибок, а также уведомление о старте бота).
 - TELEGRAM_CHAT_ID - telegram id для уведомлений о состоянии

### Обучение DialogFlow

Для добвления новых фраз и связок слов создайте `json` файл, на примере вложенного файла `questions.json`.  
Запустите скрипт:

```commandline
python3 create_intent.py file
```
Аргумент:
file - путь к вашему файлу

Например:

```commandline
python3 create_intent.py questions.json
```

Данный пример запустит обучение на основании файла `questions.json`.

## Запуск телеграм бота

```commandline
python3 verb_bot.py
```

Пример работы телеграм бота:  
![telegram example](https://dvmn.org/filer/canonical/1569214094/323/)

Образец бота:
https://t.me/zatomis_bot

## Запуск бота в vk

```commandline
python3 vk.py
```

Пример работы vk бота:

![vk example](https://dvmn.org/filer/canonical/1569214089/322/)

Образец бота:
https://vk.com/club225511420