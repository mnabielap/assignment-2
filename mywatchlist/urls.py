from django.urls import path
from mywatchlist.views import show_html, show_xml, show_json

urlpatterns = [
    path('', show_html, name='watchlist'),
    path('html/', show_html, name='show_html'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
]