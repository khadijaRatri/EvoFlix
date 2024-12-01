from django.urls import path
from recommendation import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('similarity/', views.similarity_view, name='similarity_view'),
    path('user/', views.user_dashboard, name='user_dashboard'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

