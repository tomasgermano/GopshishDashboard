#Configurar API_KEY (la sacan de gophish y url de gophish en la funcion ConnectToGophish()
#EJEMPLO:
# api_key = 'fm39949rj9943f49f49f494fmfm39949rj9943f49f49f494f'
# api = Gophish(api_key, host='https://srv:port', verify=False)
# En el resto de las funciones se leen o escriben archivos csv parametrizados dentro de las func

import cufflinks as cf
import pandas as pd
import urllib3
from gophish import Gophish
import dash
from dash import dcc
import dash_bootstrap_components as dbc
from dash import html
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input,Output,State
from dash import dash_table

cf.set_config_file(sharing='public', theme='ggplot', offline=True)
#-------------- Traer datos de Gophish --------------------"
def connectToGophish():
    urllib3.disable_warnings()
    api_key = 'API_KEY'
    api = Gophish(api_key, host='https://host:port', verify=False)
    return api
#-----------Genero CSV por tipo de resultado---------------"
def campaignResultToCSV(api):
    archivo = open('Gophish_Stats.csv', 'w')
    cabecera = "camp_nombre" + "," + "ID" + "," + "mail" + "," + "nombre" + "," + "sector" + "," + "resultado" + "\n"
    archivo.write(cabecera)
    for campaign in api.campaigns.get():
        ID = [campaign.id]
        for numero in ID:
            campNumero = api.campaigns.get(campaign_id=numero)
            results = campaign.results
            for result in results:
                verbose = campaign.name + "," + str(numero) + "," + result.email + " , " + result.first_name + " " + result.last_name + " , " + result.position + " , " + result.status + "\n"
                archivo.write(verbose)
    archivo.close()
def readCSV():
    flujo = pd.read_csv('Gophish_Stats.csv', encoding="ISO-8859-1")
    return flujo
def resultadoxEstado(flujo):
    cuentaResult=flujo.groupby(['resultado'], as_index=False)['resultado'].value_counts()
    cuentaResult.to_csv('Gophish_Stats_ResultxEstado.csv')
    ResultxEstado = pd.read_csv('Gophish_Stats_ResultxEstado.csv', encoding="ISO-8859-1")
    return ResultxEstado
def resultadoxNombre(flujo):
    cuentaResultxNombre=flujo.groupby(['nombre','resultado'], as_index=False)['camp_nombre','resultado'].value_counts()
    cuentaResultxNombre.to_csv('Gophish_Stats_ResultxNombre.csv')
    ResultxNombre = pd.read_csv('Gophish_Stats_ResultxNombre.csv', encoding="ISO-8859-1")
    return ResultxNombre
def resultadoxSector(flujo):
    cuentaResultxSector=flujo.groupby(['sector','resultado'], as_index=False)['camp_nombre','resultado'].value_counts()
    cuentaResultxSector.to_csv('Gophish_Stats_ResultxSector.csv')
    ResultxSector = pd.read_csv('Gophish_Stats_ResultxSector.csv', encoding="ISO-8859-1")
    return ResultxSector
def listadoCamp(flujo):
    listado=flujo.groupby(['camp_nombre'])['camp_nombre'].count()
    listado.to_csv('Gophish_Listado_Campanias.csv')
    ResultadoCampanias = pd.read_csv('Gophish_Listado_Campanias.csv', encoding="ISO-8859-1")
    return ResultadoCampanias

api=connectToGophish()
campaignResultToCSV(api)
flujo=readCSV()
ResultxEstado = resultadoxEstado(flujo)
ResultxNombre = resultadoxNombre(flujo)
ResultxSector = resultadoxSector(flujo)
ListadoCampanias = listadoCamp(flujo)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
#objetos para layout
radioitems_campania = dcc.RadioItems(
    id='RadioItemEstados',options=[
           {'label': 'Emails Abiertos ', 'value': ' Email Opened'},
           {'label': 'Links Clickeados ', 'value': ' Clicked Link'},
           {'label': 'Datos Cargados ', 'value': ' Submitted Data'}
                ], value=' Email Opened', labelClassName='p-1')
tabla_resultados = dash_table.DataTable(
    id='tabla1',
    data=flujo.to_dict('records'),
    columns=[{"name": i, "id": i, "deletable": False, "selectable": False} for i in flujo.columns],
    style_cell_conditional=[
            {'if': {'column_id': 'ID'},'width': '5%'},
            {'if': {'column_id': 'resultado'},'width': '10%'},],
    style_header={
        'backgroundColor': 'dodgerblue',
        'color': 'white',
        'fontWeight': 'bold',},
    style_cell={'textAlign': 'left','color':'grey','font_size': '10px'},
    style_table={"overflowX": "auto"},
    style_as_list_view=True,
    editable=False,
    filter_action="native",  # agrega un filtro por texto
    sort_action="native",
    sort_mode="multi",
    page_action='none',
    virtualization=True,)

#layout
app.layout=\
    dbc.Container\
    ([
        dbc.Row([dbc.Col(html.Nav(html.H2(" Reportes Gophish", className='text-center text-primary p-1 text-white'),className='navbar navbar-expand-lg navbar-dark bg-dark text-center')),
                ], className='pb-3'), #Header
        dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(html.H5("Lista Resultado General")),
                        dbc.CardBody(tabla_resultados),
                        ],style={"marginTop": 0, "marginBottom": 0, 'height':540},), #Tabla general
                        ],width={'size':8, 'order':'last'},),
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(html.H5("Resultado General")),
                        dbc.CardBody(
                            dcc.Graph(id='GrafGral', figure={}
                                      ),style={"marginTop": 0, "marginBottom": 0, 'height':540},),
                            ]),
                        ],width={'size':4, 'order':'first'},),
            ], className='pt-3'), #Tabla y Grafica Pie general
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("Filtro por estado"), ),
                    dbc.CardBody([dbc.Col(radioitems_campania)]), ]),  # Tarjeta titulo
                ]),
            ], className='pt-3'),
        dbc.Row([
                dbc.Col(
                    dbc.Card([
                        dbc.CardHeader(html.H6('Resultados por Sector')),
                        dbc.CardBody(dbc.Col(dcc.Graph(id='GrafSector', figure={}),)),
                    ]),),
            ], className='pt-3'), #result x sector
        dbc.Row([
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader(html.H6('Resultados por Usuario')),
                    dbc.CardBody(dbc.Col(dcc.Graph(id='GrafUsuario', figure={}), )),
                ]), ),
            ], className='pt-3 pb-3'), #result x Usuario
    ], fluid=True, className='px-5')

@app.callback(
    Output(component_id='GrafGral', component_property='figure'),
    Output(component_id='GrafSector', component_property='figure'),
    Output(component_id='GrafUsuario', component_property='figure'),
    Input(component_id='RadioItemEstados',component_property='value'),)
def updateGraf(valueRI): #valor del radioitem, valor del dropdown
    ResultxEstado_pie = px.pie(data_frame=ResultxEstado,values='count',names='resultado',hole=.4)

    #filtro los resultados para utilizar en el if = el result va al value del radio item y filtra
    dataSectorEmailOpen = ResultxSector.query("resultado==' Email Opened'")
    dataNombreEmailOpen = ResultxNombre.query("resultado==' Email Opened'")
    dataSectorClickLink = ResultxSector.query("resultado==' Clicked Link'")
    dataNombreClickLink = ResultxNombre.query("resultado==' Clicked Link'")
    dataSectorSubData = ResultxSector.query("resultado==' Submitted Data'")
    dataNombreSubData = ResultxNombre.query("resultado==' Submitted Data'")
    if valueRI == ' Clicked Link':
        ResultxSector_bar = px.bar(data_frame= dataSectorClickLink,x = 'sector',y = 'count')
        ResultxNombre_bar = px.bar(data_frame=dataNombreClickLink,x='nombre',y='count')
    elif valueRI == ' Email Opened':
        ResultxSector_bar = px.bar(data_frame= dataSectorEmailOpen,x = 'sector',y = 'count')
        ResultxNombre_bar = px.bar(data_frame=dataNombreEmailOpen,x='nombre',y='count')
    elif valueRI == ' Submitted Data':
        ResultxSector_bar = px.bar(data_frame= dataSectorSubData,x = 'sector',y = 'count')
        ResultxNombre_bar = px.bar(data_frame=dataNombreSubData,x='nombre',y='count')

    ResultxSector_bar.update_xaxes(categoryorder='total descending')
    ResultxNombre_bar.update_xaxes(categoryorder='total descending')
    ResultxEstado_pie.update_layout(legend=dict(orientation="h", yanchor="top"))

    return (ResultxEstado_pie,ResultxSector_bar,ResultxNombre_bar)

if __name__ == "__main__":
    app.run_server()
