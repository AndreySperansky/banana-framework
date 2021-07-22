from lesson_3.banana6.views import *
from lesson_3.banana6.api import API
from lesson_3.banana6.middleware import fronts


routes = {
    '/': index_view,
    '/other/': Other(),
    '/about/': about_view,
    '/secret/': secret_view,
    '/authors/': authors_view,
    '/contact/': contact_view,
}



app = API(routes, fronts)
app.run()