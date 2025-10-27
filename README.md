1. Установи виртуальное окружение и зависимости:
python -m venv venv
source venv/bin/activate # на Windows: venv\Scripts\activate
pip install -r requirements.txt


2. Запуск:
python app.py
# или FLASK_APP=app.py flask run


3. Открой http://127.0.0.1:5000


4. Чтобы запустить тесты:
pytest -q


5. Структура проекта:
voenkom/
app.py
requirements.txt
templates/
base.html
index.html
news_detail.html
documents.html
document_detail.html
announcements.html
static/
css/custom.css
docs/ (помести PDF здесь)
tests/
test_app.py


6. Настроить: поменяй SITE_TITLE, добавь/удали новости в app.py или сделай загрузку из JSON.