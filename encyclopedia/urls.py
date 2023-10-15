from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/newpage",views.newpage, name="newpage"),
    path("wiki/random_page",views.random_page, name="random_page"),
    path("wiki/link_redirect/<str:page_name>" , views.link_redirect,name="link_redirect"),
    path("wiki/edit_page/<str:title>" , views.edit_page,name="edit_page"),
    path("wiki/search_result" , views.search_result ,name="search_result"),
    path("wiki/<str:name>",views.entry,name="entry")
]
