from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import plotly.express as px

# Create your views here.
def home(request):
    return render(request,'home.html')

def pitstop_analysis(request):
    pitstop_data = pd.read_csv('Data\pit_stops.csv')
    pitstop_data = pitstop_data.where(pitstop_data['milliseconds']<50000).dropna()
    pitstop_data = pitstop_data.groupby(by='raceId').mean()
    races_data = pd.read_csv(r'Data\races.csv')
    pitstop_data = pd.merge(races_data,pitstop_data,on='raceId',how='outer')
    pitstop_data = pitstop_data.groupby(by='circuitId').mean()
    circuits_data = pd.read_csv('Data\circuits.csv')
    pitstop_data = pd.merge(circuits_data,pitstop_data,on='circuitId',how='outer').dropna().reset_index()
    pitstop_data = pitstop_data[['name','milliseconds']]
    fig = px.bar(pitstop_data,x='name',y='milliseconds',width=1280, height = 720,
                 labels=dict(name='Circuit Name',milliseconds='Average Pitstop Time (ms)'))
    
    graph = fig.to_html(full_html=False, default_height=500, default_width=700)
    context = {'graph': graph}
    return render(request,'pitstop_analysis.html',context)

def circuit_analysis(request):
    return render(request,'circuit_analysis.html')

def season_analysis(request):
    return render(request,'season_analysis.html')