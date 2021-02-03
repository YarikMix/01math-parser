### Системные требования:

* Windows 7 и выше
* Python 3 и выше
* ChromeDriver / geckodriver для вашей версии Chrome / Firefox

### Как использовать:

Скачиваем зависимости:
```bash
pip3 install -r requirements.txt
```
В файл auth_data.py вписываем свой логин и пароль от сайта 01math:
```bash
login = ""  # Ваш логин
password = ""  # Ваш пароль
```
Запускаем скрипт:
```bash
python main.py
```
Вводим тему, ответы на которую нужно получить, например ЕГЭ.03.02
```bash
> ЕГЭ.03.02
```
После этого в папке answers появится папка с названием темы, в ней будут фотографии ответов и решений.