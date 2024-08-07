from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('detail/', views.detail, name='detail'),
    path('blog/', views.blog, name='blog'),
    path('blog_detail/', views.blog_detail, name='blog_detail'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register, name='register'),
    path('product/', views.product, name='product'),
    path('product/<int:pk>/', views.detail, name='detail'),
    path('reset_password',auth_views.PasswordResetView.as_view(template_name='password/password_reset_form.html'),name="reset_password"),
    path('reset_password_sent',auth_views.PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'),name="password_reset_done"),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='password/password_reset_confirm.html'),name="password_reset_confirm"),
    path('reset_password_complete',auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'),name="password_reset_complete"),
]
