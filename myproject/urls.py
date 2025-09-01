"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from myapp import views

if settings.DEBUG:
    urlpatterns = [
        path('admin/', admin.site.urls),
        path('', views.index, name='index'),
        path('about', views.about, name='about'),
        path('contact', views.contact, name='contact'),
        path('login', views.login, name='login'),
        path('signup', views.signup, name='signup'),
        path('logout', views.logout, name='logout'),
        path('category_course', views.category_course, name='category_course'),
        path('course/<int:cid>/', views.course, name='course'),
        path('subject/<int:sid>/', views.subject, name='subject'),
        path('add_expertise/', views.add_expertise, name='add_expertise'),
        path('tutors/<int:tid>/', views.tutors, name='tutors'),
        path('tutors_detail/<int:t_id>/', views.tutors_detail, name='tutors_detail'),
        path('book-tutor/<int:tutordata_id>/', views.add_tutor_booking, name='add_tutor_booking'),
        path('request_student', views.request_student, name='request_student'),
        path('user-orders/', views.user_orders, name='user_orders'),
        path('success', views.success, name='payment_status'),
        path('storefeedback', views.storefeedback, name='storefeedback'),
        path('forgotpassword', views.forgotpassword, name='forgotpassword'),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)