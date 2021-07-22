from lesson_2.banana5.jinja import render

'''
Page controllers
добавляем request и принтим его
'''


def abc_view(request):
    print(request)
    # return '200 OK', [b'ABC']
    return '200 OK', '<h1 style="color: blue">ABC</h1>'


def not_found_404_view(request):
    print(request)
    return '404 WHAT', '<h1 style="color: red">404 PAGE Not Found</h1>'

def secret_view(request):
    secret = request.get('secret', None)
    # Используем шаблонизатор
    return '200 OK', render('index.html', secret=secret)


def about_view(request):
    print(request)
    # Просто возвращаем текст
    # return '200 OK', [b'<h1 style="color: green">Hello! This page about us!</h1>']
    return '200 OK', '<h1 style="color: green">Hello! This page about us!</h1>'

def index_view(request):
    name = request.get('name', None)
        # Используем шаблонизатор
    return  '200 OK', render('hello.html', name=name)


def contact_view(request):
    # Проверка метода запроса
    if request['method'] == 'POST':
        data = request['data']
        title = data['title']
        text = data['text']
        email = data['email']
        print(f'Нам пришло сообщение от {email} с темой {title} и текстом {text}')
        return '200 OK', render('contact.html')
    else:
        return '200 OK', render('contact.html')



class Other:

    def __call__(self, request):
        print(request)
        # return '200 OK', [b'<h1 style="color: blue">other</h1>']
        return '200 OK', '<h1 style="color: blue">other</h1>'






