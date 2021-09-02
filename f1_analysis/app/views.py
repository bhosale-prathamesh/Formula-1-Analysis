from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

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
    fig.update_traces(marker=dict(color= '#646cff'))
    graph = fig.to_html(full_html=False, default_height=500, default_width=700)
    context = {'graph': graph}
    return render(request,'pitstop_analysis.html',context)

def circuit_analysis(request):
    return render(request,'circuit_analysis.html')

def season_analysis(request):
    year='2011'
    type='Drivers'
    graph1, graph2, graph3 = season_graph(year,type)
    if (request.method == 'POST'):
        year = request.POST.get('year')
        type = request.POST.get('type')
        graph1, graph2, graph3 = season_graph(year,type)
    context= {'y':year,'t':type,'graph1':graph1,'graph2':graph2,'graph3':graph3}
    return render(request,'season_analysis.html',context)

def season_graph(year,type):
    races_data = pd.read_csv(r'Data\races.csv')
    diverstanding_data = pd.read_csv('Data\driver_standings.csv')
    drivers_data = pd.read_csv('Data\drivers.csv')
    constructorstanding_data = pd.read_csv('Data\constructor_standings.csv')
    constructors_data = pd.read_csv('Data\constructors.csv')
    constructor_race_data = pd.read_csv('Data\constructor_results.csv')
    qualifying_data = pd.read_csv('Data\qualifying.csv')
    qualifying_data.rename(columns ={'position':'quali_position'},inplace=True)
    constructors_data.drop(columns=['url'],inplace=True)
    constructors_data.rename(columns={'name':'constructor_name','nationality':'constructor_nationality'},inplace=True)
    
    data_c = races_data.where(races_data['year']==2011).dropna()
    data_c =     data_c.merge(constructorstanding_data,on='raceId').dropna()
    data_c =     data_c.merge(constructors_data,on='constructorId').dropna()
    data_c.drop(columns=['date','time','url','constructorStandingsId','constructorId','constructor_nationality','raceId'],inplace=True)
    data_c =     data_c.sort_values(['round','position'])

    data_d = races_data.where(races_data['year']==int(year)).dropna()
    data_d = data_d.merge(diverstanding_data,on='raceId').dropna()
    data_d = data_d.merge(drivers_data,on='driverId').dropna()        
    data_d.drop(columns=['date','time','url_x','url_y','driverStandingsId','dob','number','nationality'],inplace=True)
    data_d = data_d.sort_values(['round','position'])
    data_d = data_d.merge(qualifying_data,on=['raceId','driverId'])
    data_d.drop(columns=['qualifyId','raceId','driverId'],inplace=True)
    data_d = data_d.merge(constructors_data,on='constructorId')
    data_d = data_d.sort_values(['round','position'])
    constructors = data_c['constructor_name'].unique()
    drivers = data_d['code'].unique()
    module_dir = os.path.dirname(__file__)  # get current directory

    if (type == 'Drivers'): 
        file_path = os.path.join(module_dir,'Colors\\'+ year+'_Drivers.txt')
        f = open(file_path,'r')
        d = f.read()
        f.close()
        color_d =  eval(d)
        c = data_d.groupby(by='code').max().sort_values('points',ascending=False)
        c['Final'] = range(1,len(c['year'])+1)
        c = c['Final']
        data_d = data_d.merge(c,on='code').sort_values(['round','Final'])
        fig1 = px.bar(data_d, x="code", y="points", color='constructorRef',
        animation_frame="name", animation_group="code", range_y=[0,400])
        graph1 = fig1.to_html(full_html=False, default_height=500, default_width=700)

        fig2 = go.Figure()
        fig3 = go.Figure()

        for i in drivers:
            d = data_d.where(data_d['code'] == i).dropna()
            
            fig2.add_trace(go.Scatter(x=d['name'],
                                    y=d['points'],
                                    name=i,
                                    mode='lines+markers',
                                    marker=dict(color=color_d[i]['color'],
                                                opacity=0.75),
                                    line=dict(dash=color_d[i]['dash'])))
            
            fig3.add_trace(go.Scatter(x=d['name'],
                                    y=d['position'],
                                    name=i,
                                    mode='lines+markers',
                                    hovertext=d.points,
                                    marker=dict(color=color_d[i]['color'],
                                                opacity=0.75),
                                    line=dict(dash=color_d[i]['dash'])))
        graph2 = fig2.to_html(full_html=False, default_height=500, default_width=700)
        graph3 = fig3.to_html(full_html=False, default_height=500, default_width=700)
        
    elif (type == 'Constructors'):
        
        f = open('colors/'+year+'_Constructors.txt','r')
        d = f.read()
        color_c =  eval(d)
        c = data_c.groupby(by='constructor_name').max().sort_values('points',ascending=False)
        c['Final'] = range(1,len(c['year'])+1)
        c = c['Final']
        data_c = data_c.merge(c,on='constructor_name').sort_values(['round','Final'])

        fig3 = px.bar(data_c, x="constructor_name", y="points",color='constructor_name',
            animation_frame="name", animation_group="constructor_name", range_y=[0,650])
        graph1 = fig3.to_html(full_html=False, default_height=500, default_width=700)
    
    return graph1,graph2,graph3

