
from lesson_1.asper7.api import API
from lesson_1.asper7.jinja import render


app = API()

@app.route("/")
def main(request, response):
    user_agent = request.environ.get("HTTP_USER_AGENT", "No User Agent Found")
    response.text = f"Здравствуй, мой друг с браузером: {user_agent}"



@app.route("/home/")
def home(request, response):
    response.text = "Привет! Это ГЛАВНАЯ страница"


@app.route("/about/")
def about(request, response):
    response.text = "Привет! Это страница О НАС!"


@app.route("/hi/{name}/")
def greeting(request, response, name):
    response.text = f"Hi, {name}"


@app.route("/hello/{your_name}/")
def hello(request, response, your_name):
    name = your_name
    # Используем шаблонизатор
    # response.text = f"Hello, {name}"
    response.text = render('index.html', name=name)


if __name__ == '__main__':
    app.run()
    app.handle_request(request='')
    print(app.routes)