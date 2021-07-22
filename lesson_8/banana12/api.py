from wsgiref.simple_server import make_server


class API:

    def add_route(self, url):
        # паттерн декоратор
        def inner(view):
            self.urlpatterns[url] = view

        return inner

    def parse_input_data(self, data: str):
        '''
        фанкция парсит часть строки запроса которая начинается
        после знака вопроса типа ?name=max&age=18
        :param data: строка запроса после знака  ?
        :return: словарь с данными {name: 'max', age: 18}
        '''
        result = {}
        if data:
            # делим параметры через &
            params = data.split('&')
            # делим ключ и значение через =
            for item in params:
                k, v = item.split('=')
                result[k] = v
        return result

    def parse_wsgi_input_data(self, data: bytes):
        '''
        Функция парсит полученные данные из POST запроса
        и собирает их в словарь
        :param data: значения переменной wsgi.input словаря environ
        :return: словарь типа {name: 'max', age: 18}
        '''
        result = {}
        if data:
            # декодирование данных
            data_str = data.decode(encoding='utf-8')
            # собираем данные в словарь
            result = self.parse_input_data(data_str)
        return result

    def get_wsgi_input_data(self, env):
        '''
        Функция получает данные из POST запроса которые приходят
        в теле запроса в виде байт
        :param env: объект словаря (dict) содержащий CGI переменные
        :return:
        '''
        # получаем содержимое заголовка Content-Length
        # т.е. длину тела из переменной словаря environ в HTTP запросе
        content_length_data = env.get('CONTENT_LENGTH')
        # приводим к int
        content_length = int(content_length_data) if content_length_data else 0
        # считываем данные из переменной wsgi.input словаря environ если они есть
        data = env['wsgi.input'].read(content_length) if content_length > 0 else b''
        return data

    def __init__(self, urlpatterns, front_controllers):
        self.urlpatterns = urlpatterns
        self.front_controllers = front_controllers

    def __call__(self, env, start_response):

        path = env['PATH_INFO']

        # добавление закрывающего слеша
        if not path.endswith('/'):
            path = f'{path}/'

        # Получаем тип запроса (POST, GET ...)
        method = env['REQUEST_METHOD']
        data = self.get_wsgi_input_data(env)
        data = self.parse_wsgi_input_data(data)
        # Получаем данные GET запроса
        query_string = env['QUERY_STRING']
        request_params = self.parse_input_data(query_string)

        # получаем view по url
        if path in self.urlpatterns:
            # паттерн page controller
            view = self.urlpatterns[path]

            # Добавляем пустой словарь в request
            request = {}
            # добавляем параметры запросов
            request['method'] = method
            request['data'] = data
            request['request_params'] = request_params
            # добавляем в запрос данные из front controllers
            for controller in self.front_controllers:
                # паттерн front controller
                controller(request)
            # вызываем view, получаем результат
            code, text = view(request)
            # возвращаем заголовки
            start_response(code, [('Content-Type', 'text/html')])
            # return body
            return [text.encode('utf-8')]
        else:
            start_response('404 NOT FOUND', [('Content-Type', 'text/html')])
            return [b"Not Found"]


    def run(self, debug=False):

        port = 8000
        host = "127.0.0.1"
        server = make_server(host, port, self)
        print('Запустите сервер, кликнув по ссылке ниже')
        print(f'http://{host}:{port}')
        print('Подъем сервера может занять некоторое время')
        server.serve_forever()


class DebugApplication(API):

    def __init__(self, urlpatterns, front_controllers):
        self.application = API(urlpatterns, front_controllers)
        super().__init__(urlpatterns, front_controllers)

    def __call__(self, env, start_response):
        print('DEBUG MODE')
        print(env)
        return self.application(env, start_response)
        # super().__call__(env, start_response)


class MockApplication(API):

    def __init__(self, urlpatterns, front_controllers):
        self.application = API(urlpatterns, front_controllers)
        super().__init__(urlpatterns, front_controllers)

    def __call__(self, env, start_response):
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [b'Hello from Mock']
