from wsgiref.simple_server import make_server
from lesson_2.banana5.views import *
from lesson_2.banana5.middleware import fronts


class API:

    def parse_input_data(self, data: str):
        '''
        фанкция парсит часть строки запроса которая начинается
        после знака вопроса ?name=max&age=18
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


    def get_wsgi_input_data(self, env) -> bytes:
        '''
        Функция получает данные из POST запроса которые приходят
        в теле запроса в виде байт
        :param env: объект словаря (dict) содержащий CGI переменные
        :return:
        '''
        # получаем содержимое заголовка Content-Length
        # полаем длинучу тела
        # из переменной словаря environ в HTTP запросе
        content_length_data = env.get('CONTENT_LENGTH')
        # приводим к int
        content_length = int(content_length_data) if content_length_data else 0
        # считываем данные из переменной wsgi.input словаря environ если они есть
        data = env['wsgi.input'].read(content_length) if content_length > 0 else b''
        return data


    def parse_wsgi_input_data(self, data: bytes) -> dict:
        '''
        Функция парсит полученные данные из POST запроса
        и собирает их в словарь
        :param data: значения переменной wsgi.input словаря environ
        :return: словарь типв {name: 'max', age: 18}
        '''
        result = {}
        if data:
            # декодирование данных
            data_str = data.decode(encoding='utf-8')
            # собираем данные в словарь
            result = self.parse_input_data(data_str)
        return result


    def __init__(self, routes, fronts):
        self.routes = routes
        self.fronts = fronts


    def __call__(self, environ, start_response):
        headers = [('Content-Type', 'text/html')]
        path = environ['PATH_INFO']

        # добавление закрывающего слеша
        if not path.endswith('/'):
            path = f'{path}/'

        # Получаем тип запроса (POST, GET ...)
        method = environ['REQUEST_METHOD']
        # получаем данные POST запроса
        data = self.get_wsgi_input_data(environ)
        data = self.parse_wsgi_input_data(data)
        # Получаем данные GET запроса
        query_string = environ['QUERY_STRING']
        request_params = self.parse_input_data(query_string)

        # получаем view по url
        if path in self.routes:
            view = self.routes[path]
        else:
            view = not_found_404_view

        request = {}

        # добавляем параметры запросов
        request['method'] = method
        request['data'] = data
        request['request_params'] = request_params

        # добавляем в запрос данные из front controllers
        for front in self.fronts:
            front(request)
        # вызываем view, получаем результат
        code, body = view(request)
        # возвращаем заголовки
        start_response(code, headers)
        # return body
        return [body.encode('utf-8')]


    def run(self, debug=False):
            port = 8000
            host = "127.0.0.1"
            server = make_server(host, port, self)
            print('Запустите сервер, кликнув по ссылке ниже')
            print(f'http://{host}:{port}')
            print('Подъем сервера может занять некоторое время')
            server.serve_forever()



if __name__ == '__main__':

    routes = {
        '/': index_view,
        '/abc/': abc_view,
        '/other/': Other(),
        '/about/': about_view,
        '/secret/': secret_view,
        '/contact/': contact_view
    }
    app = API(routes, fronts)
    app.run()