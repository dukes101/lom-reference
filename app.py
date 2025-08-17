from dash import Dash, html, dcc, Output, Input, callback
import plotly.express as px
import plotly.graph_objects as go
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import pandas as pd
import os

dfLeagueStats = (
    pd.read_csv('https://raw.githubusercontent.com/dukes101/lom-reference/refs/heads/main/tpdash_alltimestats.csv')
      .loc[lambda df: ~df['Metric'].isin(['Low Scoring Weeks', 'Playoff Games'])]
)
dfPerformanceCards = pd.read_csv('https://raw.githubusercontent.com/dukes101/lom-reference/refs/heads/main/tpdash_alltimecards.csv')
dfYearbyYear = pd.read_csv('https://raw.githubusercontent.com/dukes101/lom-reference/refs/heads/main/tpdash_yearlystats.csv')
dfYearbyYearAvg = pd.read_csv('https://raw.githubusercontent.com/dukes101/lom-reference/refs/heads/main/tpdash_yearlyavgstats.csv')
dfMostSingleWeekPoints = pd.read_csv('https://raw.githubusercontent.com/dukes101/lom-reference/refs/heads/main/tpdash_bestweeks.csv')
dfLargestWins = pd.read_csv('https://raw.githubusercontent.com/dukes101/lom-reference/refs/heads/main/tpdash_bestwins.csv')
dfLeastSingleWeekPoints = pd.read_csv('https://raw.githubusercontent.com/dukes101/lom-reference/refs/heads/main/tpdash_worstweeks.csv')
dfWorstLosses = pd.read_csv('https://raw.githubusercontent.com/dukes101/lom-reference/refs/heads/main/tpdash_worstlosses.csv')
dfOpponents = pd.read_csv('https://raw.githubusercontent.com/dukes101/lom-reference/refs/heads/main/tpdash_opponents.csv')

## Additional Items
my_list = list(range(len(dfLeagueStats[dfLeagueStats['Team'] == 'Luca']))) #list of metrics
YearByYearList = list(dfYearbyYear.columns)[2:] #yearbyyear columns

app = Dash()

############################################### ALL METRIC GRID STYLING ###############################################
getRowStyle = {
    "styleConditions": [
        {   "condition": "params.data.Rank == '1st' | params.data.Rank == '1st (Tied)'"
            ,"style": {"backgroundColor": "gold"},
        },
        {
            "condition": "params.data.Rank == '2nd' | params.data.Rank == '3rd' | params.data.Rank == '2nd (Tied)' | params.data.Rank == '3rd (Tied)'"
            ,"style": {"backgroundColor": "lightgreen"},
        },
        {
            "condition": "params.data.Rank == '8th' | params.data.Rank == '9th' | params.data.Rank == '10th' | params.data.Rank == '8th (Tied)' | params.data.Rank == '9th (Tied)'"
            ,"style": {"backgroundColor": "#f75352"},
        },
    ],
    "defaultStyle": {"backgroundColor": "grey", "color": "white"},
}

getRowStyleHigh = {
    "styleConditions": [
        {   "condition": "params.data.Rank == '1st'"
            ,"style": {"backgroundColor": "gold"}
        }
]}

getRowStyleLow = {
    "styleConditions": [
        {   "condition": "params.data.Rank == '1st'"
            ,"style": {"backgroundColor": "#f75352"}
        }
]}
############################################### ALL METRIC GRID STYLING ###############################################

app.layout = [

    ## DIV MAIN
    html.Div([

        ## HEADER DASHBOARD TITLE
        html.H1('League of Morons History', className = 'dashboard-header')

        ## DIV LABEL W TEAM DROPDOWN
        ,html.Div([

            html.Label('Moron:', className = 'dropdown-label')

            ,dcc.Dropdown(options=[{'label': i, 'value': i} for i in dfPerformanceCards['Team'].unique()]
                         ,value='Luca'
                         ,id='team-dropdown'
                         ,style={'width': '200px'})
        ],style={'display': 'flex', 'flex-direction': 'row', 'align-items': 'center', 'justify-content': 'center', 'margin-bottom': '20px'})

        ## DIV TOP HALF
        ,html.Div([

            ## DIV LEAGUE STATS
            html.Div([

                html.H2('Performance', className = 'grid-header')

                ## GRID LEAGUE STATS
                ,dag.AgGrid(id='league-stats-grid'
                           ,rowData=dfLeagueStats.to_dict('records')
                           ,columnDefs=[{'field': 'Metric'}, {'field': 'Value'}, {'field': 'Rank'}]
                           ,columnSize="responsiveSizeToFit"
                           ,getRowStyle=getRowStyle
                           ,dashGridOptions={"rowHeight": 30, "headerHeight": 35, "animateRows": False}
                           ,style={'height': '305px'}
            )], className = 'grid')

            ## DIV CARDS
            ,html.Div([

                ## HEADER CARDS
                html.H2('Accolades', className = 'grid-header')

                ## DIV 1ST ROW CARDS
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
                    ,className = 'card')]
                ,className = 'card-row')

                ## DIV 2ND ROW CARDS
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
                    ,className='card')]
                ,className = 'card-row')

                ## DIV 3RD ROW CARDS
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
                    ,className='card')]
                ,className = 'card-row')]
            ,className = 'grid')

            ## DIV OPPONENTS
            ,html.Div([

                html.H2('Head to Head', className = 'grid-header')

                ## GRID OPPONENTS
                ,dag.AgGrid(id='opp-grid'
                           ,rowData=dfOpponents.to_dict('records')
                           ,columnDefs=[{'field': 'Moron'}, {'field': 'Pts For'}, {'field': 'Pts Against'}, {'field': 'Win %'}, {'field': 'Matchups'}]
                           ,columnSize="responsiveSizeToFit"
                           ,dashGridOptions={"rowHeight": 30, "headerHeight": 35, "animateRows": False}
                           ,style={'height': '305px'})
            ],className='grid') ## STYLE OPPONENTS
        ],className='row'), ## STYLE TOP HALF

        ## DIV BOTTOM HALF
        html.Div([

            ## DIV HIGHLIGHTS
            html.Div([

                html.H2('Highlights', className = 'grid-header')

                ## DIV MOST WEEK POINTS
                ,html.Div([
                    
                    html.H4('Highest Weekly Score', className='grid-header-2')

                    ## GRID MOST WEEK POINTS
                    ,dag.AgGrid(id='most-wk-points-grid'
                               ,rowData=dfMostSingleWeekPoints.to_dict('records')
                               ,columnDefs=[{'field': 'Year'}, {'field': 'Week'}, {'field': 'Score'}, {'field': 'Rank'}]
                               ,columnSize="responsiveSizeToFit"
                               ,getRowStyle=getRowStyleHigh
                               ,dashGridOptions={"rowHeight": 30, "headerHeight": 35, "animateRows": False}
                               ,style={'height': '125px'})
                ])

                ## DIV LARGEST WINS
                ,html.Div([

                    html.H4('Largest Wins', className='grid-header-2')

                    ## GRID LARGEST WINS
                    ,dag.AgGrid(id='largest-wins-grid'
                               ,rowData=dfLargestWins.to_dict('records')
                               ,columnDefs=[{'field': 'Year'}, {'field': 'Week'}, {'field': 'Against'}, {'field': 'W Margin'}, {'field': 'Rank'}]
                               ,columnSize="responsiveSizeToFit"
                               ,getRowStyle=getRowStyleHigh
                               ,dashGridOptions={"rowHeight": 30, "headerHeight": 35, "animateRows": False}
                               ,style={'height': '125px'})
                ])
            ],className='grid') ## STYLE HIGHLIGHTS

            ## DIV LOWLIGHTS
            ,html.Div([

                html.H2('Lowlights', className = 'grid-header')

                ## DIV LEAST WEEK POINTS
                ,html.Div([

                    html.H4('Lowest Weekly Score', className='grid-header-2')

                    ## GRID LEAST WEEK POINTS
                    ,dag.AgGrid(id='least-wk-points-grid'
                              ,rowData=dfLeastSingleWeekPoints.to_dict('records')
                              ,columnDefs=[{'field': 'Year'}, {'field': 'Week'}, {'field': 'Score'}, {'field': 'Rank'}]
                              ,columnSize="responsiveSizeToFit"
                              ,getRowStyle=getRowStyleLow
                              ,dashGridOptions={"rowHeight": 30, "headerHeight": 35, "animateRows": False}
                              ,style={'height': '125px'})
                ])

                ## DIV WORST LOSSES
                ,html.Div([

                    html.H4('Worst Losses', className='grid-header-2')

                    ## GRID WORST LOSSES
                    ,dag.AgGrid(id='worst-losses-grid'
                              ,rowData=dfWorstLosses.to_dict('records')
                              ,columnDefs=[{'field': 'Year'}, {'field': 'Week'}, {'field': 'Against'}, {'field': 'L Margin'}, {'field': 'Rank'}]
                              ,columnSize="responsiveSizeToFit"
                              ,getRowStyle=getRowStyleLow
                              ,dashGridOptions={"rowHeight": 30, "headerHeight": 35, "animateRows": False}
                              ,style={'height': '125px'})
                ])
            ],className='grid') ## STYLE LOWLIGHTS
            
            ## DIV YEAR BY YEAR
            ,html.Div([

                html.Div([

                    html.Label('Metric:', className = 'dropdown-label')

                    ,dcc.Dropdown(options=[{'label': col, 'value': col} for col in YearByYearList]
                                 ,value='Points'
                                 ,id='metric-dropdown'
                                 ,style={'width': '200px'})
                ],style={'display': 'flex', 'flex-direction': 'row', 'align-items': 'center', 'justify-content': 'center', 'padding': '5px'})

                ## FIGURE YEAR BY YEAR
                ,dcc.Graph(figure={}
                          ,id='year-by-year-figure'
                          ,style={'height': '400px'}
                          ,config={'responsive': True})
            ],className = 'grid')
        ],className='row') ## STYLE BOTTOM HALF
    ],style={'backgroundColor': 'black'}) ## STYLE MAIN
]

############################################### PERFORMANCE CARDS ###############################################
## CARD CHAMPIONSHIPS
@app.callback(
    Output('championships-value', 'children')
    ,Input('team-dropdown', 'value')
)
def update_championships_value(team):
    championships = dfPerformanceCards[dfPerformanceCards['Team'] == team]['Championships'].iloc[0]
    return str(championships)

## Top 3 Finishes Card
@app.callback(
    Output('top-3-finishes-value', 'children')
    ,Input('team-dropdown', 'value')
)
def update_top3_value(team):
    top3 = dfPerformanceCards[dfPerformanceCards['Team'] == team]['Top 3 Finishes'].iloc[0]
    return str(top3)

## Top 5 Finishes Card
@app.callback(
    Output('top-5-finishes-value', 'children')
    ,Input('team-dropdown', 'value')
)
def update_top5_value(team):
    top5 = dfPerformanceCards[dfPerformanceCards['Team'] == team]['Top 5 Finishes'].iloc[0]
    return str(top5)

## Reg Season Champ Card
@app.callback(
    Output('reg-season-champ-value', 'children')
    ,Input('team-dropdown', 'value')
)
def update_reg_value(team):
    reg = dfPerformanceCards[dfPerformanceCards['Team'] == team]['Reg Champ'].iloc[0]
    return str(reg)

## All Time Record Card
@app.callback(
    Output('record-value', 'children')
    ,Input('team-dropdown', 'value')
)
def update_record_value(team):
    record = dfPerformanceCards[dfPerformanceCards['Team'] == team]['All Time Record'].iloc[0]
    return str(record)

## Playoff Record Card
@app.callback(
    Output('playoff-record-value', 'children')
    ,Input('team-dropdown', 'value')
)
def update_playoff_record_value(team):
    offrecord = dfPerformanceCards[dfPerformanceCards['Team'] == team]['Playoff Record'].iloc[0]
    return str(offrecord)

## Seasons Played Card
@app.callback(
    Output('seasons-value', 'children')
    ,Input('team-dropdown', 'value')
)
def update_seasons_joined_value(team):
    seasons = dfPerformanceCards[dfPerformanceCards['Team'] == team]['Seasons Played'].iloc[0]
    return str(seasons)

## Playoff App Card
@app.callback(
    Output('playoff-app-value', 'children')
    ,Input('team-dropdown', 'value')
)
def update_playoff_value(team):
    playoffapp = dfPerformanceCards[dfPerformanceCards['Team'] == team]['Playoff Appearances'].iloc[0]
    return str(playoffapp)

## Last Place Finishes Card
@app.callback(
    Output('last-place-value', 'children')
    ,Input('team-dropdown', 'value')
)
def update_last_value(team):
    last = dfPerformanceCards[dfPerformanceCards['Team'] == team]['Last Place'].iloc[0]
    return str(last)

############################################### PERFORMANCE CARDS ###############################################

############################################### LEAGUE STATS GRID ###############################################
## League Stats Callback
@callback(
    Output('league-stats-grid', 'rowData')
    ,Input('team-dropdown', 'value')
)

## Updates league stats grid
def update_league_stats_table(team):
  df_team = dfLeagueStats[dfLeagueStats['Team'] == team]
  df_filtered = df_team.iloc[sorted(range(len(df_team)),
                    key=lambda i: (int(df_team.iloc[i]['League Rank'].split()[0][:-2]),
                              0 if '(Tied)' in df_team.iloc[i]['League Rank'] else 1))]
  data = [{'Metric': df_filtered['Metric'].iloc[row], 'Value': df_filtered['Value'].iloc[row], 'Rank': df_filtered['League Rank'].iloc[row]} for row in my_list]
  return data

############################################### LEAGUE STATS GRID ###############################################

############################################### HIGHLIGHTS GRID ###############################################
## Most Week Points Callback
@callback(
    Output('most-wk-points-grid', 'rowData')
    ,Input('team-dropdown', 'value')
)

## Updates Most Week Points Grid
def update_most_week_points_grid(team):
  df_team = dfMostSingleWeekPoints[dfMostSingleWeekPoints['Team'] == team]
  data = [{'Year': df_team['Year'].iloc[row], 'Week': df_team['Week'].iloc[row], 'Score': df_team['Score'].iloc[row], 'Rank': df_team['All Time Rank'].iloc[row]} for row in range(len(df_team))]
  return data

## Largest Wins Callback
@callback(
    Output('largest-wins-grid', 'rowData')
    ,Input('team-dropdown', 'value')
)

## Updates Largest Wins Grid
def update_largest_wins_grid(team):
  df_team = dfLargestWins[dfLargestWins['Team'] == team]
  data = [{'Year': df_team['Year'].iloc[row], 'Week': df_team['Week'].iloc[row], 'Against': df_team['Opponent'].iloc[row], 'W Margin': df_team['Winning Margin'].iloc[row]
           ,'Rank': df_team['All Time Rank'].iloc[row]} for row in range(len(df_team))]
  return data

############################################### HIGHLIGHTS GRID ###############################################

############################################### LOWLIGHTS GRID ###############################################
## Least Week Points Callback
@callback(
    Output('least-wk-points-grid', 'rowData')
    ,Input('team-dropdown', 'value')
)

## Updates Least Week Points Grid
def update_least_week_points_grid(team):
  df_team = dfLeastSingleWeekPoints[dfLeastSingleWeekPoints['Team'] == team]
  data = [{'Year': df_team['Year'].iloc[row], 'Week': df_team['Week'].iloc[row], 'Score': df_team['Score'].iloc[row], 'Rank': df_team['All Time Rank'].iloc[row]} for row in range(len(df_team))]
  return data

## Worst Losses Callback
@callback(
    Output('worst-losses-grid', 'rowData')
    ,Input('team-dropdown', 'value')
)

## Updates Worst Losses Grid
def update_worst_losses_grid(team):
  df_team = dfWorstLosses[dfWorstLosses['Team'] == team]
  data = [{'Year': df_team['Year'].iloc[row], 'Week': df_team['Week'].iloc[row], 'Against': df_team['Opponent'].iloc[row], 'L Margin': df_team['Losing Margin'].iloc[row]
           ,'Rank': df_team['All Time Rank'].iloc[row]} for row in range(len(df_team))]
  return data

############################################### LOWLIGHTS GRID ###############################################

############################################### OPPONENTS GRIDS ###############################################
## Opponent Grid
@callback(
    Output('opp-grid', 'rowData')
    ,Input('team-dropdown', 'value')
)

## Updates opponent table
def update_opp_table(team):
  df_team = dfOpponents[dfOpponents['Team'] == team]
  data = [{'Moron': df_team['Opponent'].iloc[row]
           ,'Pts For': df_team['PointsFor'].iloc[row]
           ,'Pts Against': df_team['PointsAgainst'].iloc[row]
           ,'Win %': df_team['Win %'].iloc[row]
           ,'Matchups': df_team['TotalMatchups'].iloc[row]} for row in range(len(df_team))]
  return data

############################################### OPPONENTS GRIDS ###############################################

############################################### YEAR BY YEAR ###############################################
## Year by Year Figure Callback
@callback(
    Output('year-by-year-figure', 'figure')
    ,Input('team-dropdown', 'value')
    ,Input('metric-dropdown', 'value')
)

## Updates figure based on team and metric selected
def update_year_by_year_figure(team, metric):

  # Filter on team
  dfYearbyYearTeam = dfYearbyYear[dfYearbyYear['Team'] == team]

  # Merge avg data
  dfMerged = pd.merge(dfYearbyYearTeam, dfYearbyYearAvg, on='Year', suffixes=('', '_avg'))

  # Create line
  fig1 = px.line(dfMerged,
                 x='Year',
                 y=[metric,f'{metric}_avg'],
                 template='seaborn')
  fig1.update_xaxes(type='category')
  fig1.update_layout(showlegend=False, xaxis_title=None, yaxis_title=None)

  fig1.data[1].update(name='Average', line_dash='dash')
  return fig1

############################################### YEAR BY YEAR ###############################################

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    app.run(debug=False, host="0.0.0.0", port=port)