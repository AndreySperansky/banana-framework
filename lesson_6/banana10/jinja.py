from jinja2 import FileSystemLoader
from jinja2.environment import Environment


def render(template_name, folder='templates', **kwargs):
    # file_path = os.path.join(folder, template_name)
    # # Открываем шаблон по имени
    # with open(file_path, encoding='utf-8') as f:
    #     # Читаем
    #     template = Template(f.read())
    # # рендерим шаблон с параметрами
    # return template.render(**kwargs)
    env = Environment()
    # указываем папку для поиска шаблонов
    env.loader = FileSystemLoader(folder)
    #file_path = os.path.join(folder, template_name)
    # находим шаблон в окружении
    template = env.get_template(template_name)
    return template.render(**kwargs)


if __name__ == '__main__':
    # Пример использования
    output_test = render('authors.html', object_list=[{'name': 'Leo'}, {'name': 'Kate'}])
    print(output_test)
