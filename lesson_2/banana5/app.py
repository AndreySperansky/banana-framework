from lesson_2.banana5.views import *
from lesson_2.banana5.api import API
from lesson_2.banana5.middleware import fronts


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