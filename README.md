# py_telebot
Небольшой бот на бибилиотеке pyTelegramBotApi.

## Бот позволяет организовать диалог с ChatGPT.

## Для запуска бота выполните следующие инструкции:

* Клонируйте репозиторий себе на компьютер

```bash
git clone https://github.com/makskhaliosa/py_telebot.git
```

* В корневой директории создайте виртуальное окружение

```bash
python -m venv venv
source venv/Scripts/activate
python -m pip install --upgrade pip
```

* Установите зависимости проекта

```bash
pip install requirements.txt
```

* Создайте файл .env в корневой директории по примеру .env-sample,
туда добавьте ключ для телеграм бота и ключ Openai Api Key

* Запустите бота командой

```bash
python run.py
```

### Телеграм бот готов к работе.
