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
    pitstop_data = pd.read_csv('Data\Average_Pitstop.csv')
    fig = px.bar(pitstop_data,x='name',y='milliseconds',
                 labels=dict(name='Circuits',milliseconds='Average Pitstop Time (ms)'))
    fig.update_traces(marker=dict(color= '#646cff'))
    fig.update_xaxes(showticklabels=False)
    graph = fig.to_html(full_html=False)
    context = {'graph': graph}
    return render(request,'pitstop_analysis.html',context)

def circuit_analysis(request):
    circuits_data = pd.read_csv('Data\circuits_m.csv')
    fig1 = px.scatter_geo(data_frame=circuits_data,
                         lat='lat',
                         lon='lng',
                         hover_name="name",
                         hover_data=['location','country'],
                         color='count',
                         color_continuous_scale=px.colors.sequential.Viridis,
                         opacity=0.75,
                         size='count')
    fig1.update_geos(showcountries=True)
    graph1 = fig1.to_html(full_html=False)
    num_races = pd.read_csv(r'Data\num_races.csv')
    fig2 = px.line(num_races,x='Year',y='Races')
    graph2 = fig2.to_html(full_html=False)
    context = {'graph1': graph1,'graph2':graph2}
    return render(request,'circuit_analysis.html',context)

def season_analysis(request):
    year='2011'
    type='Drivers'
    graph1, graph2, graph3, data = season_graph(year,type)
    if (request.method == 'POST'):
        year = request.POST.get('year')
        type = request.POST.get('type')
        graph1, graph2, graph3, data = season_graph(year,type)
    context= {'graph1':graph1,'graph2':graph2,'graph3':graph3,'data':data,'y':year,'t':type}
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
    
    data_c = races_data.where(races_data['year']==int(year)).dropna()
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
        data = data_d.sort_values('points',ascending=False).drop_duplicates(['driverRef']).set_index('Final')
        data = data.sort_index()
        data = data[['code','forename','surname','points','constructor_name','wins']]
        fig1 = px.bar(data_d, x="code", y="points", color='constructorRef',
        animation_frame="name", animation_group="code", range_y=[0,400])
        graph1 = fig1.to_html(full_html=False,auto_play=False)

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
        graph2 = fig2.to_html(full_html=False)
        graph3 = fig3.to_html(full_html=False)
        
    elif (type == 'Constructors'):
        file_path = os.path.join(module_dir,'Colors\\'+ year+'_Constructors.txt')
        f = open(file_path,'r')
        d = f.read()
        color_c =  eval(d)
        c = data_c.groupby(by='constructor_name').max().sort_values('points',ascending=False)
        c['Final'] = range(1,len(c['year'])+1)
        c = c['Final']
        data_c = data_c.merge(c,on='constructor_name').sort_values(['round','Final'])
        data = data_c.sort_values('points',ascending=False).drop_duplicates(['constructor_name']).set_index('Final')
        data = data.sort_index()
        data = data[['constructor_name','points','wins']]
        fig1 = px.bar(data_c, x="constructor_name", y="points",color='constructor_name',
            animation_frame="name", animation_group="constructor_name", range_y=[0,650])
        graph1 = fig1.to_html(full_html=False,auto_play=False)

        fig2 = go.Figure()
        fig3 = go.Figure()

        for i in constructors:
            d = data_c.where(data_c['constructor_name'] == i).dropna()
            
            fig2.add_trace(go.Scatter(x=d['name'],
                                    y=d['points'],
                                    name=i,
                                    mode='lines+markers',
                                    marker=dict(color=color_c[i]['color'],opacity=0.75)))
            
            fig3.add_trace(go.Scatter(x=d['name'],
                                    y=d['position'],
                                    name=i,
                                    mode='lines+markers',
                                    hovertext=d.points,
                                    marker=dict(color=color_c[i]['color'],opacity=0.75)))
        graph2 = fig2.to_html(full_html=False)
        graph3 = fig3.to_html(full_html=False)
    data = data.to_html(classes='styled-table')
    return graph1,graph2,graph3,data