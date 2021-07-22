from lesson_6.banana10.jinja import render
from lesson_6.banana10.api import API, MockApplication, DebugApplication
from lesson_6.banana10.models import TrainingSite, BaseSerializer, EmailNotifier, SmsNotifier
from lesson_6.banana10.logging_mod import Logger, debug
from lesson_6.banana10.middleware import fronts
from lesson_6.banana10.cbv import ListView, CreateView


site = TrainingSite()
logger = Logger('main')
email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()


def main_view(request):
    logger.log('Список курсов')
    return '200 OK', render('course_list.html', objects_list=site.courses)

def not_found_404_view(request):
    return '404 WHAT', '<h1 style="color: red">404 PAGE Not Found</h1>'


def about_view(request):
    logger.log('О нас')
    return '200 OK', render('about_us.html')


def hello_view(request):
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


@debug
def create_course(request):
    if request['method'] == 'POST':
        # метод пост
        data = request['data']
        name = data['name']
        category_id = data.get('category_id')
        print(category_id)
        if category_id:
            category = site.find_category_by_id(int(category_id))

            course = site.create_course('record', name, category)
            # Добавляем наблюдателей на курс
            course.observers.append(email_notifier)
            course.observers.append(sms_notifier)
            site.courses.append(course)
        # редирект?
        # return '302 Moved Temporarily', render('create_course.html')
        # Для начала можно без него
        categories = site.categories
        return '200 OK', render('create_course.html', categories=categories)
    else:
        categories = site.categories
        return '200 OK', render('create_course.html', categories=categories)


class CategoryCreateView(CreateView):
    template_name = 'create_category.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['categories'] = site.categories
        return context

    def create_obj(self, data: dict):
        name = data['name']
        category_id = data.get('category_id')

        category = None
        if category_id:
            category = site.find_category_by_id(int(category_id))

        new_category = site.create_category(name, category)
        site.categories.append(new_category)


# def create_category(request):
#     if request['method'] == 'POST':
#         # метод пост
#         data = request['data']
#         # print(data)
#         name = data['name']
#         category_id = data.get('category_id')
#
#         category = None
#         if category_id:
#             category = site.find_category_by_id(int(category_id))
#
#         new_category = site.create_category(name, category)
#         site.categories.append(new_category)
#         # редирект?
#         # return '302 Moved Temporarily', render('create_course.html')
#         # Для начала можно без него
#         return '200 OK', render('create_category.html')
#     else:
#         categories = site.categories
#         return '200 OK', render('create_category.html', categories=categories)


class CategoryListView(ListView):
    queryset = site.categories
    template_name = 'category_list.html'


class StudentListView(ListView):
    queryset = site.students
    template_name = 'student_list.html'


class StudentCreateView(CreateView):
    template_name = 'create_student.html'

    def create_obj(self, data: dict):
        name = data['name']
        new_obj = site.create_user('student', name)
        site.students.append(new_obj)


class AddStudentByCourseCreateView(CreateView):
    template_name = 'add_student.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['courses'] = site.courses
        context['students'] = site.students
        return context

    def create_obj(self, data: dict):
        course_name = data['course_name']
        course = site.get_course(course_name)
        student_name = data['student_name']
        student = site.get_student(student_name)
        course.add_student(student)


urlpatterns = {
    '/': main_view,
    '/hello/': hello_view,
    '/about/': about_view,
    # '/secret/': secret_view,
    # '/authors/': authors_view,
    '/contact/': contact_view,
    '/create-course/': create_course,
    '/create-category/': CategoryCreateView(),
    '/category-list/': CategoryListView(),
    '/student-list/': StudentListView(),
    '/create-student/': StudentCreateView(),
    '/add-student/': AddStudentByCourseCreateView(),
}


def secret_controller(request):
    request['secret'] = 'secret'



application = API(urlpatterns, fronts)


# proxy
# application = DebugApplication(urlpatterns, front_controllers)
# application = MockApplication(urlpatterns, front_controllers)


@application.add_route('/copy-course/')
def copy_course(request):
    request_params = request['request_params']
    # print(request_params)
    name = request_params['name']
    old_course = site.get_course(name)
    if old_course:
        new_name = f'copy_{name}'
        new_course = old_course.clone()
        new_course.name = new_name
        site.courses.append(new_course)

    return '200 OK', render('course_list.html', objects_list=site.courses)


# @application.add_route('/category-list/')
# def category_list(request):
#     logger.log('Список категорий')
#     return '200 OK', render('category_list.html', objects_list=site.categories)


@application.add_route('/api/')
def course_api(request):
    return '200 OK', BaseSerializer(site.courses).save()

if __name__ == '__main__':

    app = API(urlpatterns, fronts)
    app.run()