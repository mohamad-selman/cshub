from django.urls import path
from app import views

urlpatterns = [
    path('', views.index, name='home'),
    path('login/', views.login_u, name='login'),
    path('logout/', views.logout_u, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('course/<int:cid>/', views.course, name='course'),
    path('results/', views.results, name='results'),
    path('add/<int:cid>/', views.add, name='add'),
    path('submit/<int:cid>/', views.submit, name='submit'),
    path('error/', views.error, name='error'),
    path('vote/<int:cid>/<int:rid>/', views.vote, name='vote'),
    path('report/<int:cid>/<int:rid>/', views.report, name='report'),
    path('submit_report/<int:cid>/<int:rid>/', views.submit_report, name='submit_report'),
    path('admin/reports/', views.admin_report, name='admin_report'),
    path('delete/<int:rid>/', views.delete, name='delete'),
]