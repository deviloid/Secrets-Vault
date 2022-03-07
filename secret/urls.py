from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import Index, SecretDetail, SecretCreate, SecretUpdate, SecretDelete, CustomLoginView, RegisterPage, getPasswd
urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('', Index.as_view(), name='index'),
    path('secret/<int:pk>/', SecretDetail.as_view(), name='secret_detail'),
    path('secret-create/', SecretCreate.as_view(), name='secret_create'),
    path('secret-update/<int:pk>/', SecretUpdate.as_view(), name='secret_update'),
    path('secret-delete/<int:pk>/', SecretDelete.as_view(), name='secret_delete'),
    path('ajax/getPasswd/', getPasswd.as_view(), name='get_password'),
]