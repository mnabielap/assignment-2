from django.urls import path
from .views import register, login_user, show_todolist, create_task, update_status ,delete_task, logout_user, create_task_ajax, show_todolist_json
app_name = 'todolist'

urlpatterns = [
    path('', show_todolist, name='show_todolist'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('create-task/', create_task, name='create_task'),
    path('delete-task/<int:id>/', delete_task, name='delete-task'),
    path('update-task/<int:id>', update_status, name='update-task'),
    path('json/', show_todolist_json, name='show_todolist_json'),
    path('add/', create_task_ajax, name='create_task_ajax'),
]