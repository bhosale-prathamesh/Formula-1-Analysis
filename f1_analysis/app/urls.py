from django.urls import path
from . import views 

urlpatterns = [
    path('',views.home,name='Home'),
    path('pitstop_analysis/',views.pitstop_analysis,name='Pitstop_Analysis'),
    path('circuit_analysis/',views.circuit_analysis,name='Circuit_Analysis'),
    path('season_analysis/',views.season_analysis,name='Season_Analysis')
]