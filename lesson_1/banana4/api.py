from wsgiref.simple_server import make_server
from webob import Request, Response
from parse import parse

class API:

    def __init__(self):
        '''
        В методе __init__ мы определили словарь  под названием self.routes,
        в котором мы будем хранить пути в качестве ключей,
        а обработчики - в качестве значений.
        '''
        self.routes = {}

        # print(self.routes)
        # {   "/home": ,  "/about": }

    def route(self, path):
        '''
        Функция - декоратор, принимает путь и оборачивает методы -
        обработчики страниц - Page controllers
        В методе route, мы возьмем путь в качестве аргумента и в методе wrapper
        просто внесем этот путь в словарь self.routes в качестве ключа,
        а обработчик - в качестве значения.
        '''
        def wrapper(handler):
            self.routes[path] = handler
            return handler

        print(self.routes)
        return wrapper

    def __call__(self, environ, start_response):
        request = Request(environ)
        response = self.handle_request(request)
        return response(environ, start_response)

    def default_response(self, response):
        response.status_code = 404
        response.text = "404 Not found!"

    def find_handler(self, request_path):
        '''функция - обработчик для его собственного метода
         исключительно ради читаемости (не обязательно)
         он просто итерирует над self.route , сравнивает пути с путем
         запроса и возвращает обработчик, если пути совпадают.
         или None, если обработчик не был найден
        '''
        for path, handler in self.routes.items():
            parse_result = parse(path, request_path)
            if parse_result is not None:
                return handler, parse_result.named
        return None, None


    def handle_request(self, request):
        '''
        Функция - обработчик запросов
        :param request: словарь {путь: обработчик, }
        :return:
        '''
        response = Response()
        handler, kwargs = self.find_handler(request_path=request.path)
        if handler is not None:
            handler(request, response, **kwargs)
        else:
            self.default_response(response)
        return response



    def run(self, debug=False):
        port = 8000
        host = "127.0.0.1"
        server = make_server(host, port, self)
        print('Запустите браузер, кликнув по ссылке ниже')
        print(f'http://{host}:{port}')
        print('Первый отклик сервера может занять некоторое время (до 30 сек.)')
        server.serve_forever()



if __name__ == '__main__':
    app = API()
    app.run()