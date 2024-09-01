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
    path('download/<int:product_id>/', views.download_image, name='download_image'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('profile/', views.profile, name='profile'),
    path('userprofile/', views.userprofile, name='userprofile'),
    path('category/<int:maincategory_id>/', views.category, name='category_view'),
    path('add-product/<int:category_id>/', views.add_product, name='add_product_view'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('userprofile/<int:user_id>/', views.userprofile, name='userprofile'),
    path('userprofile/<str:username>/', views.userprofile, name='userprofile'),
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', views.unfollow_user, name='unfollow_user'),
    path('reset_password',auth_views.PasswordResetView.as_view(template_name='password/password_reset_form.html'),name="reset_password"),
    path('reset_password_sent',auth_views.PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'),name="password_reset_done"),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='password/password_reset_confirm.html'),name="password_reset_confirm"),
    path('reset_password_complete',auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'),name="password_reset_complete"),
]
