from collections import defaultdict
from math import trunc
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash_html_components.Tr import Tr
import plotly.express as px
import pandas as pd
from datetime import date, datetime, timedelta
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from threading import Timer
import webbrowser

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP],suppress_callback_exceptions=True)

#attendance={'2021-06-24': {'DPS212': '22:12', 'DPS211': '22:13', 'CLD214': '22:24', 'CLD213': '21:06'}, '2021-06-25': {'DPS211': '22:26', 'CLD214': '22:26', 'HRM211': '22:26', 'DPS212': '22:23'}, '2021-06-26': {'CLD214': '17:13'}, '2021-06-30': {'CLD214': '21:20'}, '2021-07-01': {'CLD213': '11:59', 'CLD214': '11:58'}, '2021-07-04': {'HRM213': '12:57', 'CLD214': '12:27', 'DPS211': '12:57'}, 
#'2021-07-09': {'DPS211': '21:53', 'HRM213': '21:53', 'CLD214': '21:52'}, '2021-07-10': {'DPS212': '11:04', 'CLD214': '11:03', 'DPS211': '11:03', 'HRM213': '11:03'}}



def get_date_count(attendance):
    dates=list(attendance.keys())
    count=[len(x) for x in attendance.values() ]
    return dates,count

def monthdisplay(dates,count):
    df_monthly = pd.DataFrame({
        "Dates": dates,
        "Count": count,
    })
    return df_monthly

def findmissingdates(d):
    d=[datetime.strptime(x, '%Y-%m-%d').date() for x in d]
    date_set = set(d[0] + timedelta(x) for x in range((d[-1] - d[0]).days))
    missingdates = sorted(date_set - set(d))
    missingdates=[str(x) for x in missingdates]
    return missingdates

def getdepartmentnames(deptshort):
    deptname={'DPS':'DevOps','CLD':'Cloud','HRM':'Human Resources','BIA':'business analysts','FIN':'finance','NET':'networking'}
    deptnames=[]
    for name in deptshort:
        deptnames.append(deptname[name])
    return deptnames

def getdeptavg(avginp,totday):
    deptavg=defaultdict(lambda:0)
    count=defaultdict(lambda:0)
    for key,value in avginp.items():
        deptavg[key[:3]]+=(value/totday)
        count[key[:3]]+=1
    for key,val in deptavg.items():
        deptavg[key]=val/count[key]

    deptname=getdepartmentnames(list(deptavg.keys()))
    deptavgval=list(deptavg.values())
    return deptname,deptavgval



# all app renders

navbar = dbc.Navbar(
    [
        html.H1(
            dbc.Row(
                [
                    dbc.Col(dbc.NavbarBrand("Project - One", className="ml-2")),
                ],
                align="center",
                no_gutters=True,
            ),
        ),
    ],
    color="dark",
    dark=True,
    sticky='top',
)

nav = dbc.Nav(
    [
      dbc.Container( html.Div([
            dcc.Tabs(id="tabs",
                     value='tab-1',
                     children=[
                         dcc.Tab(label='Overall Statistics', value='tab-1'),
                         dcc.Tab(label='Department Wise', value='tab-2'),
                         dcc.Tab(label='Employee Attendance', value='tab-3'),
                     ]),
            html.Br(),
            #dcc.Graph(id='date-line'),
            html.Div(id='date-line')
            
        ]),
    fluid=True,
      )
    ],
    horizontal='center',
)

@app.callback(
    [ Output('output-container-date-picker-range', 'children'),
    Output('output-empid', 'children'),
    Output('output-empie', 'children')],
    [dash.dependencies.Input('my-date-picker-range', 'start_date'),
     dash.dependencies.Input('my-date-picker-range', 'end_date'),
      dash.dependencies.Input('empid', 'value')])
def update_output(start_date, end_date,empid1):
    string_prefix = 'You have selected: '
    if (start_date is not None) and  (end_date is not None):
        #print('entered')
        start_date_object = date.fromisoformat(start_date)
        start_date_string = start_date_object.strftime('%d %m, %Y')
        string_prefix = string_prefix + 'Start Date: ' + start_date_string + ' | '
        end_date_object = date.fromisoformat(end_date)
        end_date_string = end_date_object.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'End Date: ' + end_date_string
        totday=0
        presday=0
        start_date=datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date=datetime.strptime(end_date, '%Y-%m-%d').date()
        for key,val in attendance.items():
            currdate=datetime.strptime(key, '%Y-%m-%d').date()
            if currdate >= start_date and currdate<= end_date:
                if empid1 in val:
                    presday+=1
                totday+=1
        #print(presday,totday)
        labels = ['Absent','Present']
        values = [totday-presday,presday]
        colors=['#EF553B','#00CC96']
        fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
        fig.update_traces(marker=dict(colors=colors))
        figdcc=dcc.Graph(
        id='empid-graph',
        figure=fig
        )
        return string_prefix,empid1,figdcc
    else:
        raise dash.exceptions.PreventUpdate

@app.callback(
    [ Output('dept-output-date-picker-range', 'children'),
    Output('dept-output', 'children')],
    [dash.dependencies.Input('dept-date-picker-range', 'start_date'),
    dash.dependencies.Input('dept-date-picker-range', 'end_date'),
    ])
def update_output_dept(start_date, end_date):
    string_prefix = 'You have selected: '
    if (start_date is not None) and  (end_date is not None):
        #print('entered')
        start_date_object = date.fromisoformat(start_date)
        start_date_string = start_date_object.strftime('%d %m, %Y')
        string_prefix = string_prefix + 'Start Date: ' + start_date_string + ' | '
        end_date_object = date.fromisoformat(end_date)
        end_date_string = end_date_object.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'End Date: ' + end_date_string
        totday=0
        start_date=datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date=datetime.strptime(end_date, '%Y-%m-%d').date()
        empavg=defaultdict(lambda :0)
        for key,val in attendance.items():
            currdate=datetime.strptime(key, '%Y-%m-%d').date()
            if currdate >= start_date and currdate<= end_date:
                for empid1 in val:
                    empavg[empid1]+=1
                totday+=1
        #print(empavg,totday)
        deptnames,deptavg=getdeptavg(empavg,totday)
        #print(deptnames,deptavg)
        allcards=[]
        for i in range(len(deptnames)):
            labels = ['Absent','Present']
            colors=['#EF553B','#00CC96']
            values = [1-deptavg[i],deptavg[i]]
            fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
            fig.update_traces(marker=dict(colors=colors))
            card1 = dbc.Card(
                        [
                            dbc.CardHeader(deptnames[i]),
                            dbc.CardBody(
                                [
                                    #html.H4(deptnames[i], className="card-title"),
                                    dcc.Graph(
                                        figure=fig,
                                    ),
                                ]
                            ),
                        ],outline=True,
                        style={'flex': '0 0 33.333333%'},
                    )
            allcards.append(card1)
        index=0
        row = html.Div(
            [
                dbc.Row([

                    dbc.Col(children=[currcard for currcard in allcards],style={'display':'contents'})

                ],justify="center",style={'margin':'1rem'},)
            ])
        return string_prefix,row
    else:
        raise dash.exceptions.PreventUpdate

@app.callback(Output('date-line', 'children'), [Input('tabs', 'value')])
def show_clicks(tab):
    if tab=='tab-1':
        fig = px.bar(monthdisplay(dates,count), x="Dates", y="Count")
        fig.update_xaxes(
            rangebreaks=[dict(values=missingdates)],
            #rangeslider_visible=True,
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="This Month", step="month", stepmode="todate"),
                    dict(count=1, label="1 Month", step="month", stepmode="backward"),
                    dict(count=3, label="3 months", step="month", stepmode="backward"),
                    dict(count=6, label="6 Months", step="month", stepmode="backward"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(label='overall',step="all")
                ])
            )
        )
        fig.update_layout(
            yaxis={'tickformat': ',d'}
        )
        graph=dcc.Graph(
            id='monthly-graph',
            figure=fig
        )
        return html.Div([graph,
        ])

    if tab=='tab-2':
        row = html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(html.Div([html.H5("Select Date Range"),dcc.DatePickerRange(
                                id='dept-date-picker-range',
                                min_date_allowed=firstdate,
                                max_date_allowed=lastdate,
                                initial_visible_month=lastdate,
                                end_date=lastdate
                                )
                                ])
                                , width=4),
                    ],
                    justify="center",style={'margin':'2rem'},
                ),
                dbc.Row(
                    [
                       dbc.Col(dbc.Alert(html.H5(id='dept-output-date-picker-range')), width=8),
                    ], 
                    justify="center",style={'margin':'2rem'},
                ),                
                dbc.Row(
                    [
                       dbc.Col(html.Div(id='dept-output')),
                    ], 
                    justify="center",style={'margin':'2rem'},
                ),
            ])
        return html.Div(row)
        
    if tab=='tab-3':
        initial_visible_month=lastdate,
        end_date=lastdate
        row = html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(html.Div([html.H5("Enter Employee ID"),dbc.Input(id="empid", type="text", placeholder="",)]), width=4),
                        dbc.Col(html.Div([html.H5("Select Date Range"),dcc.DatePickerRange(
                                id='my-date-picker-range',
                                min_date_allowed=firstdate,
                                max_date_allowed=lastdate,
                                initial_visible_month=lastdate,
                                end_date=lastdate
                                )
                                ])
                                , width=4),
                    ],
                    justify="center",style={'margin':'2rem'},
                ),
                dbc.Row(
                    [
                       dbc.Col(dbc.Alert(html.H5(id='output-container-date-picker-range')), width=8),
                    ], 
                    justify="center",style={'margin':'2rem'},
                ),
                dbc.Row(
                    [
                       dbc.Col(dbc.Alert([html.H3(id='output-empid',style={'display':'inline',}),html.H3('Attendance details',style={'display':'inline','margin-left':'2rem'}),], color="info"), width=8),
                    ], 
                    justify="center",style={'margin':'2rem'},
                ),
                dbc.Row(
                    [
                       dbc.Col(html.Div(id='output-empie')),
                    ], 
                    justify="center",style={'margin':'2rem'},
                ),
            ])    
        return html.Div(row)



app.layout = html.Div(children=[
    navbar,
    nav,
    
])


def open_browser():
      webbrowser.open_new('http://127.0.0.1:5002/')

def start_dash(attendance_copy):
    global attendance,dates,count,missingdates,firstdate,lastdate
    attendance=attendance_copy
    print(attendance)
    # data function calls
    dates,count=get_date_count(attendance)
    missingdates=findmissingdates(dates)
    firstdate=datetime.strptime(list(attendance.keys())[0], '%Y-%m-%d').date()
    lastdate=datetime.strptime(list(attendance.keys())[-1], '%Y-%m-%d').date()
    #if __name__ == '__main__':
    Timer(1, open_browser).start()
    app.run_server(port=5002)