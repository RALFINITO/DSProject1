
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

import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from pandas_datareader import data as web
from datetime import datetime as dt

app = dash.Dash()
# print(getAvailableStocks())
app.layout = html.Div([
    html.H1('Available Stocks'),
    dcc.Dropdown(
        id='drpdwnCompany',
        options=getStockDropdownData(getAvailableStocks(),{'label': 'name', 'value': 'symbol'}),
        value=''
    ),
    html.H1('Period Range'),
    dcc.Dropdown(
        id='drpdwnPeriodRange',
        options=getPeriodRangeDropdownData(),
        value=''
    ),
    dcc.Graph(id='my-graph')
])

@app.callback(Output('my-graph', 'figure'), [Input('drpdwnCompany', 'value'), Input('drpdwnPeriodRange', 'value')])

def update_graph(stock_dropdown_value, period_dropdown_value):
    import plotly.graph_objs as go
    print(getCompanyInfo(stock_dropdown_value))
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


if __name__ == '__main__':
    app.run_server()

# strStock = 'aapl'
# strPeriod = '3m'
# dictParametersStockChart = {'strStock':strStock, 'strPeriod':strPeriod}
# print(getStockChart(dictParametersStockChart).content)

# print(getAvailableStocks())