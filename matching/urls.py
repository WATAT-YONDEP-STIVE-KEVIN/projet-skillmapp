from django.urls import path
from . import views
#
#app_name = 'matching'
#regarder  le setting.py on a utilisé LOGIN_REDIRECT ET LOGOUT_REDIRECT
urlpatterns = [
    #path('', views.matching_view, name='matching'),
    path('dashboard/', views.dashboard_view, name='dashboard_view'),
    path('download/', views.download_pdf, name='download_pdf'),
    path('accueil/', views.accueil, name='accueil'), 
    path('home/', views.home, name='home'), 
    path('aligner/', views.accueil, name='aligner'),
    path('result/', views.accueil, name='result'),
    path('base1/', views.accueil, name='base1'),
    path('match/', views.matching_view, name='matching_page'),
    #path('dashboard/export-pdf/', views.export_dashboard_pdf, name='export_dashboard_pdf'),

]
