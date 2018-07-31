
def getData(dictParametersData):
    import requests

    strTrunk = 'https://api.iextrading.com/1.0/'

    strEndpoint = dictParametersData['strEndpoint']
    if (strEndpoint == 'stock'):
        strType = dictParametersData['strType']
        if(strType == 'chart'):
            strStock = dictParametersData['strStock']
            strPeriod = dictParametersData['strPeriod']

            strBranch = strTrunk + strEndpoint + '/' + strStock + '/' + strType + '/' + strPeriod + '/'
        if (strType == 'company'):
            strStock = dictParametersData['strStock']
            strBranch = strTrunk + strEndpoint + '/' + strStock + '/' + strType + '/'

    if (strEndpoint == '/ref-data/symbols'):
        strBranch = strTrunk + strEndpoint

    r = requests.get(strBranch)
    return r

def getCompanyInfo(strCompanyTicker):
    strEndpoint = 'stock'
    strType = 'company'
    dictParametersData = {'strEndpoint': strEndpoint, 'strStock': strCompanyTicker, 'strType': strType}
    jsonCompanyData = getData(dictParametersData).json()

    return jsonCompanyData

def sDFCompanyInfo(strCompanyTicker):
    import pandas as pd
    import dash_html_components as html
    jsonCompanyData = getCompanyInfo(strCompanyTicker)
    dfCompanyInfo = pd.DataFrame(jsonCompanyData)

    for info in dfCompanyInfo['tags']:
        dfCompanyInfo['tags'][0] = dfCompanyInfo['tags'][0] + ', ' + info

    dfCompanyInfo = dfCompanyInfo[0:1].transpose()

    return dfCompanyInfo

def getStockChart(dictParametersStockChart):
    import pandas as pd

    strEndpoint = 'stock'
    strType = 'chart'

    strStock = dictParametersStockChart['strStock']
    strPeriod = dictParametersStockChart['strPeriod']
    dictParametersData = {'strEndpoint':strEndpoint, 'strStock':strStock,'strType':strType, 'strPeriod':strPeriod}

    dfChrtData = pd.DataFrame(getData(dictParametersData).json())

    return dfChrtData

def getAvailableStocks():
    strBranch = '/ref-data/symbols'
    dictParametersData = {'strEndpoint':strBranch}
    allSymbols = getData(dictParametersData)
    availableStocks = []

    for symbol in allSymbols.json():
        if (symbol['type'] == 'cs' and symbol['isEnabled'] == True):
            availableStocks.append(symbol)

    return availableStocks

def getStockDropdownData(dictRawData, dictParameterLookup):
    dropdownData = []
    labelPosition = dictParameterLookup['label']
    valuePosition = dictParameterLookup['value']
    for dataPoint in dictRawData:

        value = dataPoint[valuePosition]
        label = value + ' - ' + dataPoint[labelPosition]
        dropdownData.append({'label':label , 'value':value})
    return dropdownData

def getPeriodRangeDropdownData():
    lstPeriods = ['1d','1m','3m','6m','ytd', '1y','2y','5y']
    dropdownData = []
    for period in lstPeriods:
        value = period
        label = period
        dropdownData.append({'label':label , 'value':value})
    return dropdownData

def generate_table(dataframe, tableid = '', max_rows=10):
    import dash_html_components as html
    return html.Table(



        [html.Tr([html.Td(dataframe.index[i].title(),className='table_index')] + [
            html.Td(dataframe.iloc[i][col],className='table_value') for col in dataframe.columns
        ], id='') for i in range(min(len(dataframe), max_rows))]
    )

def getStockStats(dftockPrices):
    dfStats = dftockPrices.describe()
    print(dfStats)
    return dfStats


import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from pandas_datareader import data as web
from datetime import datetime as dt
import flask
import os

app = dash.Dash(__name__)
server = app.server
app.title = 'Share Profiler'

app.layout = html.Div([
    html.Div(
        [html.H1('Stock Market Share Profiler', className = 'app-header--title'),
         html.H1('by Rafael Alfinito', className = 'app-header--author')]),
    html.Div([
        html.H3('Available Stocks'),
        dcc.Dropdown(
        id='drpdwnCompany',
        options=getStockDropdownData(getAvailableStocks(),{'label': 'name', 'value': 'symbol'}),
        value=''
    )],className='selector'),
    html.Div([
        html.H3('Period Range'),
        dcc.Dropdown(
        id='drpdwnPeriodRange',
        options=getPeriodRangeDropdownData(),
        value=''
    )],className='selector'),

    html.H3('Stock Price Chart'),
    dcc.Graph(id='my-graph'),

    html.H3('Company Info'),
    html.Div(id='divCompanyInfo'),

    html.H3('Price Stats'),
    html.Div(id='divPriceStats'),

    html.Div(html.A('Data provided for free by IEX.', href='https://iextrading.com/developer', target='_blank',id='attribution')),
    html.Div(html.A('View IEX’s Terms of Use.', href='https://iextrading.com/api-exhibit-a/', target='_blank',id='attribution'))

],id='divBody')



#SET UP THE ICON SHOWN IN THE WEBBROWSER TAB
@server.route('/favicon.ico')
def favicon():
    return flask.send_from_directory(os.path.join(server.root_path, 'static'),
                                     'favicon.ico')


#UPDATE CHARR WHENEVER A NEW COMPANY OR A NEW PERIOD RANGE IS CHOSEN
@app.callback(Output('my-graph', 'figure'), [Input('drpdwnCompany', 'value'), Input('drpdwnPeriodRange', 'value')])
def update_graph(stock_dropdown_value, period_dropdown_value):
    import plotly.graph_objs as go
    dfStockData = getStockChart({'strStock':stock_dropdown_value,'strPeriod':period_dropdown_value})
    goChartData = [
        go.Scatter(
            x=dfStockData['date'],
            y=dfStockData['close']
        )
    ]
    return {
        'data': goChartData
    }

#UPDATE THE COMPANY INFO TABLE WHENEVER A NEW COMPANY IS CHOSEN
@app.callback(Output('divCompanyInfo', 'children'), [Input('drpdwnCompany', 'value')])
def update_table(stock_dropdown_value):
    dfCompanyInfo = sDFCompanyInfo(stock_dropdown_value)
    return generate_table(dfCompanyInfo, 'tblCompanyInfo', dfCompanyInfo.shape[0])

@app.callback(Output('divPriceStats', 'children'), [Input('drpdwnCompany', 'value'), Input('drpdwnPeriodRange', 'value')])
def update_table(stock_dropdown_value, period_dropdown_value):
    dfStockData = getStockChart({'strStock': stock_dropdown_value, 'strPeriod': period_dropdown_value})
    dfStockStats = getStockStats(dfStockData.loc[:,['close']])
    return generate_table(dfStockStats, 'tblCompanyInfo', dfStockStats.shape[0])


if __name__ == '__main__':
    app.run_server()