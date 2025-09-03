# Dependencies
from dash import Dash, html, dcc, Output, Input, callback
import plotly.express as px
import plotly.graph_objects as go
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import pandas as pd
import os

# Data Reads (from github)
dfLeagueStats = pd.read_csv('https://raw.githubusercontent.com/dukes101/lom-reference/refs/heads/main/tpdash_alltimestats.csv')
dfPerformanceCards = pd.read_csv('https://raw.githubusercontent.com/dukes101/lom-reference/refs/heads/main/tpdash_alltimecards.csv')
dfYearbyYear = pd.read_csv('https://raw.githubusercontent.com/dukes101/lom-reference/refs/heads/main/tpdash_yearlystats.csv')
dfYearbyYearAvg = pd.read_csv('https://raw.githubusercontent.com/dukes101/lom-reference/refs/heads/main/tpdash_yearlyavgstats.csv')
dfMostSingleWeekPoints = pd.read_csv('https://raw.githubusercontent.com/dukes101/lom-reference/refs/heads/main/tpdash_bestweeks.csv')
dfLargestWins = pd.read_csv('https://raw.githubusercontent.com/dukes101/lom-reference/refs/heads/main/tpdash_bestwins.csv')
dfLeastSingleWeekPoints = pd.read_csv('https://raw.githubusercontent.com/dukes101/lom-reference/refs/heads/main/tpdash_worstweeks.csv')
dfWorstLosses = pd.read_csv('https://raw.githubusercontent.com/dukes101/lom-reference/refs/heads/main/tpdash_worstlosses.csv')
dfOpponents = pd.read_csv('https://raw.githubusercontent.com/dukes101/lom-reference/refs/heads/main/tpdash_opponents.csv')

# Initialize Dash App
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Row Styles
# Performance Grid
rowstylepg = {
    "styleConditions": [
        {   "condition": "params.data.Rank == '1st' | params.data.Rank == '1st (Tied)'"
            ,"style": {"backgroundColor": "gold"},
        },
        {
            "condition": "params.data.Rank == '2nd' | params.data.Rank == '2nd (Tied)'"
            ,"style": {"backgroundColor": "silver"},
        },
        {
            "condition": "params.data.Rank == '3rd' | params.data.Rank == '3rd (Tied)'"
            ,"style": {"backgroundColor": "#CD7F32"},
        },
        {
            "condition": "params.data.Rank == '10th'"
            ,"style": {"backgroundColor": "red"},
        }
    ],
    "defaultStyle": {"backgroundColor": "#8d8f91", "color": "white"},
}

# Highlights & Lowlights Grids
rowstylelights = {
    "styleConditions": [
        {   "condition": "params.data.Rank == '1st'"
            ,"style": {"backgroundColor": "gold"}
        },
        {   "condition": "params.data.Rank == '2nd'"
            ,"style": {"backgroundColor": "silver"}
        },
        {   "condition": "params.data.Rank == '3rd'"
            ,"style": {"backgroundColor": "#CD7F32"}
        },
], "defaultStyle": {"backgroundColor": "#8d8f91", "color": "white"},
}

# H2H Grid
rowstyleh2h = {
    "styleConditions": [
    # If win % > 50, highlight green
        {   "condition": "params.data.WinPct > 50"
            ,"style": {"backgroundColor": "lightgreen"},
        },
    # If win % < 50, highlight red
        {
            "condition": "params.data.WinPct < 50"
            ,"style": {"backgroundColor": "red"}
        }
    ],
    "defaultStyle": {"backgroundColor": "#8d8f91", "color": "white"},
}

# App Layout
app.layout = dbc.Container(
    [
        # Dashboard Title (full width)
        html.H1('League of Morons History', className = 'dashboard-header')
        
        # Label + Dropdown (full width)
        ,html.Div([
            html.Label('Moron:', className = 'dropdown-label')
            ,dcc.Dropdown(
                options=[{'label': i, 'value': i} for i in dfPerformanceCards['Team'].unique()]
                ,value='Luca'
                ,id='team-dropdown'
                ,style={'width': '150px'}
            )
        ],style={'display': 'flex'
                ,'flex-direction': 'row'
                ,'justify-content': 'center' # center of screen
                ,'margin-bottom': '20px'
                ,'backgroundColor': 'black'})
        
        # League Stats + Cards + H2H
        ,dbc.Row(
            [
                dbc.Col( # League Stats
                    html.Div([
                        html.H2('Performance', className = 'grid-header')
                        ,dag.AgGrid(id='league-stats-grid'
                            ,rowData=dfLeagueStats.to_dict('records')
                            ,columnDefs=[{'field': 'Metric'}, {'field': 'Value'}, {'field': 'Rank'}]
                            ,columnSize="responsiveSizeToFit"
                            ,getRowStyle=rowstylepg
                            ,dashGridOptions={"rowHeight": 30, "headerHeight": 35, "animateRows": False}
                            ,style={'height': '305px'}
                        )
                    ],className = 'grid'
                    ),xs=12, md=4
                )
                ,dbc.Col( # Cards
                    html.Div([
                        html.H2('Accolades', className = 'grid-header')
                            ,html.Div([
                                #1,1
                                dbc.Card(
                                    dbc.CardBody([html.H3("CHAMP", className='card-title')
                                                 ,html.P(id='championships-value', className='card-text')])
                                                 ,className = 'card')
                    
                                #1,2
                                ,dbc.Card(
                                    dbc.CardBody([html.H3("TOP 3", className='card-title')
                                                 ,html.P(id='top-3-finishes-value', className='card-text')])
                                                 ,className = 'card')
                    
                                #1,3                
                                ,dbc.Card(
                                    dbc.CardBody([html.H3("TOP 5", className='card-title')
                                                 ,html.P(id='top-5-finishes-value', className='card-text')])
                                                 ,className = 'card')
                            ],className = 'card-row'
                            )
                            ,html.Div([
                                #2,1
                                dbc.Card(
                                    dbc.CardBody([html.H3("REG CHAMP", className='card-title')
                                                 ,html.P(id='reg-season-champ-value', className="card-text")])
                                                 ,className = 'card')
                                #2,2
                                ,dbc.Card(
                                    dbc.CardBody([html.H3("RECORD", className='card-title')
                                                 ,html.P(id='record-value', className="card-text")])
                                                 ,className = 'card')
                    
                                #2,3
                                ,dbc.Card(
                                    dbc.CardBody([html.H3("PO RECORD", className='card-title')
                                                 ,html.P(id='playoff-record-value', className="card-text")])
                                                 ,className='card')
                            ],className = 'card-row'
                            )
                            ,html.Div([
                                #3,1
                                dbc.Card(
                                    dbc.CardBody([html.H3("SEASONS", className='card-title')
                                                 ,html.P(id='seasons-value', className="card-text")])
                                                 ,className='card')
                    
                                #3,2
                                ,dbc.Card(
                                    dbc.CardBody([html.H3("PO APP", className='card-title')
                                                 ,html.P(id='playoff-app-value', className="card-text")])
                                                 ,className='card')
                    
                                #3,3
                                ,dbc.Card(
                                    dbc.CardBody([html.H3("LAST PLACE", className='card-title')
                                                 ,html.P(id='last-place-value', className="card-text")])
                                                 ,className='card')
                            ],className = 'card-row')
                    ],className = 'grid'
                    ),xs=12, md=4
                )
                ,dbc.Col( # H2H
                    html.Div([
                        html.H2('Head to Head', className = 'grid-header')
                        ,dag.AgGrid(id='opp-grid'
                            ,rowData=dfOpponents.to_dict('records')
                            ,columnDefs=[{'field': 'Moron'}, {'field': 'Pts For'}, {'field': 'Pts Against'}, {'field': 'WinPct', 'headerName': 'Win %'}, {'field': 'Matchups'}]
                            ,columnSize="responsiveSizeToFit"
                            ,getRowStyle=rowstyleh2h
                            ,dashGridOptions={"rowHeight": 30, "headerHeight": 35, "animateRows": False}
                            ,style={'height': '305px'})
                    ],className='grid'
                    ),xs=12, md=4
                )
            ]
        )
        
        # Highlights + Lowlights + Graph
        ,dbc.Row(
            [
                dbc.Col( # Highlights
                    html.Div([
                        html.H2('Highlights', className = 'grid-header')
                        ,html.Div([
                            html.H4('Highest Weekly Score', className='grid-header-2')
                            ,dag.AgGrid(
                                id='most-wk-points-grid'
                                ,rowData=dfMostSingleWeekPoints.to_dict('records')
                                ,columnDefs=[{'field': 'Year'}, {'field': 'Week'}, {'field': 'Score'}, {'field': 'Rank'}]
                                ,columnSize="responsiveSizeToFit"
                                ,getRowStyle=rowstylelights
                                ,dashGridOptions={"rowHeight": 30, "headerHeight": 35, "animateRows": False}
                                ,style={'height': '125px'})
                        ])
                        ,html.Div([
                            html.H4('Largest Wins', className='grid-header-2')
                            ,dag.AgGrid(
                                id='largest-wins-grid'
                                ,rowData=dfLargestWins.to_dict('records')
                                ,columnDefs=[{'field': 'Year'}, {'field': 'Week'}, {'field': 'Against'}, {'field': 'W Margin'}, {'field': 'Rank'}]
                                ,columnSize="responsiveSizeToFit"
                                ,getRowStyle=rowstylelights
                                ,dashGridOptions={"rowHeight": 30, "headerHeight": 35, "animateRows": False}
                                ,style={'height': '125px'})
                        ])
                    ],className='grid'
                    ),xs=12, md=4
                )
                ,dbc.Col( # Lowlights
                    html.Div([
                        html.H2('Lowlights', className = 'grid-header')
                        ,html.Div([
                            html.H4('Lowest Weekly Score', className='grid-header-2')
                            ,dag.AgGrid(
                                id='least-wk-points-grid'
                                ,rowData=dfLeastSingleWeekPoints.to_dict('records')
                                ,columnDefs=[{'field': 'Year'}, {'field': 'Week'}, {'field': 'Score'}, {'field': 'Rank'}]
                                ,columnSize="responsiveSizeToFit"
                                ,getRowStyle=rowstylelights
                                ,dashGridOptions={"rowHeight": 30, "headerHeight": 35, "animateRows": False}
                                ,style={'height': '125px'})
                        ])
                        ,html.Div([
                            html.H4('Worst Losses', className='grid-header-2')
                            ,dag.AgGrid(
                                id='worst-losses-grid'
                                ,rowData=dfWorstLosses.to_dict('records')
                                ,columnDefs=[{'field': 'Year'}, {'field': 'Week'}, {'field': 'Against'}, {'field': 'L Margin'}, {'field': 'Rank'}]
                                ,columnSize="responsiveSizeToFit"
                                ,getRowStyle=rowstylelights
                                ,dashGridOptions={"rowHeight": 30, "headerHeight": 35, "animateRows": False}
                                ,style={'height': '125px'})
                        ])
                    ],className='grid'
                    ),xs=12, md=4
                )
                ,dbc.Col( # Graph
                    html.Div([
                        html.Div([
                            html.Label('Yearly Stats', className = 'dropdown-label')
                            ,dcc.Dropdown(
                                options=[{'label': col, 'value': col} for col in list(dfYearbyYear.columns)[2:]]
                                ,value='Points'
                                ,id='metric-dropdown'
                                ,style={'width': '200px'})
                        ],style={'display': 'flex', 'flex-direction': 'row', 'align-items': 'center', 'justify-content': 'center', 'padding': '5px'}
                        )
                        ,dcc.Graph(
                            figure={}
                            ,id='year-by-year-figure'
                            ,style={'height': '400px'}
                            ,config={'responsive': True})
                    ],className = 'grid'
                    ),xs=12, md=4
                )
            ]
        )
    ],fluid=True
    ,style={'backgroundColor': 'black'}
)

# Callbacks for Cards
@app.callback(
    Output('championships-value', 'children')
    ,Input('team-dropdown', 'value')
)
def update_championships_value(team):
    championships = dfPerformanceCards[dfPerformanceCards['Team'] == team]['Championships'].iloc[0]
    return str(championships)

@app.callback(
    Output('top-3-finishes-value', 'children')
    ,Input('team-dropdown', 'value')
)
def update_top3_value(team):
    top3 = dfPerformanceCards[dfPerformanceCards['Team'] == team]['Top 3 Finishes'].iloc[0]
    return str(top3)

@app.callback(
    Output('top-5-finishes-value', 'children')
    ,Input('team-dropdown', 'value')
)
def update_top5_value(team):
    top5 = dfPerformanceCards[dfPerformanceCards['Team'] == team]['Top 5 Finishes'].iloc[0]
    return str(top5)

@app.callback(
    Output('reg-season-champ-value', 'children')
    ,Input('team-dropdown', 'value')
)
def update_reg_value(team):
    reg = dfPerformanceCards[dfPerformanceCards['Team'] == team]['Reg Champ'].iloc[0]
    return str(reg)

@app.callback(
    Output('record-value', 'children')
    ,Input('team-dropdown', 'value')
)
def update_record_value(team):
    record = dfPerformanceCards[dfPerformanceCards['Team'] == team]['All Time Record'].iloc[0]
    return str(record)

@app.callback(
    Output('playoff-record-value', 'children')
    ,Input('team-dropdown', 'value')
)
def update_playoff_record_value(team):
    offrecord = dfPerformanceCards[dfPerformanceCards['Team'] == team]['Playoff Record'].iloc[0]
    return str(offrecord)

@app.callback(
    Output('seasons-value', 'children')
    ,Input('team-dropdown', 'value')
)
def update_seasons_joined_value(team):
    seasons = dfPerformanceCards[dfPerformanceCards['Team'] == team]['Seasons Played'].iloc[0]
    return str(seasons)

@app.callback(
    Output('playoff-app-value', 'children')
    ,Input('team-dropdown', 'value')
)
def update_playoff_value(team):
    playoffapp = dfPerformanceCards[dfPerformanceCards['Team'] == team]['Playoff Appearances'].iloc[0]
    return str(playoffapp)

@app.callback(
    Output('last-place-value', 'children')
    ,Input('team-dropdown', 'value')
)
def update_last_value(team):
    last = dfPerformanceCards[dfPerformanceCards['Team'] == team]['Last Place'].iloc[0]
    return str(last)

# Callback for League Stats Grid
@callback(
    Output('league-stats-grid', 'rowData')
    ,Input('team-dropdown', 'value')
)

def update_league_stats_table(team):
  df_team = dfLeagueStats[dfLeagueStats['Team'] == team]
  df_filtered = df_team.iloc[sorted(range(len(df_team)),
                    key=lambda i: (int(df_team.iloc[i]['League Rank'].split()[0][:-2]),
                              0 if '(Tied)' in df_team.iloc[i]['League Rank'] else 1))]
  data = [{'Metric': df_filtered['Metric'].iloc[row]
          ,'Value': df_filtered['Value'].iloc[row]
          ,'Rank': df_filtered['League Rank'].iloc[row]} for row in list(range(len(dfLeagueStats[dfLeagueStats['Team'] == 'Luca'])))]
  return data

# Callbacks for Highlights
@callback(
    Output('most-wk-points-grid', 'rowData')
    ,Input('team-dropdown', 'value')
)

def update_most_week_points_grid(team):
  df_team = dfMostSingleWeekPoints[dfMostSingleWeekPoints['Team'] == team]
  data = [{'Year': df_team['Year'].iloc[row], 'Week': df_team['Week'].iloc[row], 'Score': df_team['Score'].iloc[row], 'Rank': df_team['All Time Rank'].iloc[row]} for row in range(len(df_team))]
  return data

@callback(
    Output('largest-wins-grid', 'rowData')
    ,Input('team-dropdown', 'value')
)

def update_largest_wins_grid(team):
  df_team = dfLargestWins[dfLargestWins['Team'] == team]
  data = [{'Year': df_team['Year'].iloc[row], 'Week': df_team['Week'].iloc[row], 'Against': df_team['Opponent'].iloc[row], 'W Margin': df_team['Winning Margin'].iloc[row]
           ,'Rank': df_team['All Time Rank'].iloc[row]} for row in range(len(df_team))]
  return data

# Callbacks for Lowlights
@callback(
    Output('least-wk-points-grid', 'rowData')
    ,Input('team-dropdown', 'value')
)

def update_least_week_points_grid(team):
  df_team = dfLeastSingleWeekPoints[dfLeastSingleWeekPoints['Team'] == team]
  data = [{'Year': df_team['Year'].iloc[row], 'Week': df_team['Week'].iloc[row], 'Score': df_team['Score'].iloc[row], 'Rank': df_team['All Time Rank'].iloc[row]} for row in range(len(df_team))]
  return data

@callback(
    Output('worst-losses-grid', 'rowData')
    ,Input('team-dropdown', 'value')
)

def update_worst_losses_grid(team):
  df_team = dfWorstLosses[dfWorstLosses['Team'] == team]
  data = [{'Year': df_team['Year'].iloc[row], 'Week': df_team['Week'].iloc[row], 'Against': df_team['Opponent'].iloc[row], 'L Margin': df_team['Losing Margin'].iloc[row]
           ,'Rank': df_team['All Time Rank'].iloc[row]} for row in range(len(df_team))]
  return data

# Callback for H2H
@callback(
    Output('opp-grid', 'rowData')
    ,Input('team-dropdown', 'value')
)

def update_opp_table(team):
  df_team = dfOpponents[dfOpponents['Team'] == team]
  data = [{'Moron': df_team['Opponent'].iloc[row]
           ,'Pts For': df_team['PointsFor'].iloc[row]
           ,'Pts Against': df_team['PointsAgainst'].iloc[row]
           ,'WinPct': df_team['Win %'].iloc[row]
           ,'Matchups': df_team['TotalMatchups'].iloc[row]} for row in range(len(df_team))]
  return data

# Callback for Figure
@callback(
    Output('year-by-year-figure', 'figure')
    ,Input('team-dropdown', 'value')
    ,Input('metric-dropdown', 'value')
)

def update_year_by_year_figure(team, metric):

  # Filter on team
  dfYearbyYearTeam = dfYearbyYear[dfYearbyYear['Team'] == team]

  # Merge avg data
  dfMerged = pd.merge(dfYearbyYearTeam, dfYearbyYearAvg, on='Year', suffixes=('', '_avg'))

  # Create line
  fig1 = px.line(dfMerged,
                 x='Year',
                 y=[metric,f'{metric}_avg'],
                 template='plotly_dark')
  fig1.update_xaxes(type='category')
  fig1.update_layout(showlegend=False, xaxis_title=None, yaxis_title=None)

  fig1.data[1].update(name='Average', line_dash='dash')
  return fig1

# Render requirements
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    app.run(debug=False, host="0.0.0.0", port=port)