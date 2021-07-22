'''
"Чистый сервер" для тестирования и отладки
'''

from wsgiref.simple_server import make_server

host = '127.0.0.1'
port = 8000

def run(environ, start_response):
    response_body = b"Hello, World!"
    status = "200 OK"
    start_response(status, headers=[])
    return iter([response_body])

server = make_server(host, port, run)
print(f'http://{host}:{port}')
server.serve_forever()

