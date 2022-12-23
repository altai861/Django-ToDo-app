from django.urls import path
from . import views






urlpatterns = [
    path('', views.tasks, name="tasks"),
    path('login', views.login_view, name="login"),
    path('logout', views.logout_view, name="logout"),
    path('register', views.register, name="register"),

    path('add-task', views.add_task, name="add_task"),
    path('tasks/<int:task_id>', views.view_task, name="view_task"),
    path('tasks/<int:task_id>/delete', views.delete_task, name="delete_task"),
    path('tasks/<int:task_id>/update', views.update_task, name="update_task"),

]