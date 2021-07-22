'''front controllers'''

def secret_front(request):
    request['secret'] = 'secretKey'

def other_front(request):
    request['key'] = 'key'

def name_front(request):
    request['name'] = 'Мир'

fronts = [secret_front, other_front, name_front]
