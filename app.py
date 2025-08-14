from dash import Dash, html, dcc, Output, Input, callback
import plotly.express as px
import plotly.graph_objects as go
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import pandas as pd
import os

dfLeagueStats = pd.read_csv('https://raw.githubusercontent.com/dukes101/lom-reference/refs/heads/main/tpdash_alltimestats.csv')
dfPerformanceCards = pd.read_csv('https://raw.githubusercontent.com/dukes101/lom-reference/refs/heads/main/tpdash_alltimecards.csv')
dfYearbyYear = pd.read_csv('https://raw.githubusercontent.com/dukes101/lom-reference/refs/heads/main/tpdash_yearlystats.csv')
dfYearbyYearAvg = pd.read_csv('https://raw.githubusercontent.com/dukes101/lom-reference/refs/heads/main/tpdash_yearlyavgstats.csv')
dfMostSingleWeekPoints = pd.read_csv('https://raw.githubusercontent.com/dukes101/lom-reference/refs/heads/main/tpdash_bestweeks.csv')
dfLargestWins = pd.read_csv('https://raw.githubusercontent.com/dukes101/lom-reference/refs/heads/main/tpdash_bestwins.csv')
dfLeastSingleWeekPoints = pd.read_csv('https://raw.githubusercontent.com/dukes101/lom-reference/refs/heads/main/tpdash_worstweeks.csv')
dfWorstLosses = pd.read_csv('https://raw.githubusercontent.com/dukes101/lom-reference/refs/heads/main/tpdash_worstlosses.csv')
dfOpponents = pd.read_csv('https://raw.githubusercontent.com/dukes101/lom-reference/refs/heads/main/tpdash_opponents.csv')

## Other Items
my_list = list(range(len(dfLeagueStats[dfLeagueStats['Team'] == 'Luca Hurst']))) #list of metrics
YearByYearList = list(dfYearbyYear.columns)[2:] #yearbyyear columns

app = Dash()

############################################### ALL METRIC GRID STYLING ###############################################
getRowStyle = {
    "styleConditions": [
        {
            "condition": "params.data.Rank == '1st' | params.data.Rank == '2nd' | params.data.Rank == '3rd' | params.data.Rank == '1st (Tied)' | params.data.Rank == '2nd (Tied)' | params.data.Rank == '3rd (Tied)' ",
            "style": {"backgroundColor": "lightgreen"},
        },
        {
            "condition": "params.data.Rank == '8th' | params.data.Rank == '9th' | params.data.Rank == '10th' | params.data.Rank == '8th (Tied)' | params.data.Rank == '9th (Tied)' ",
            "style": {"backgroundColor": "#f75352"},
        },
    ],
    "defaultStyle": {"backgroundColor": "grey", "color": "white"},
}
############################################### ALL METRIC GRID STYLING ###############################################

app.layout = [

    ## DIV MAIN
    html.Div([

        ## HEADER DASHBOARD TITLE
        html.H1('League of Morons History', style={'color': 'white', 'textAlign': 'center', 'padding': '20px', 'backgroundColor': 'black'}),

        ## DIV LABEL W TEAM DROPDOWN
        html.Div([

            html.Label('Select Moron:', style={'font-size': '20px', 'font-weight': 'bold', 'margin-right': '10px', 'margin-left': '5px', 'color': 'black'}),

            dcc.Dropdown(
                options=[{'label': i, 'value': i} for i in dfPerformanceCards['Team'].unique()],
                value='Luca Hurst',
                id='team-dropdown',
                style={'width': '200px'}
                )
            ],
            style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center', 'flex-direction': 'row'}), # DIV for dropdown

        ## DIV TOP HALF
        html.Div([

            ## DIV LEAGUE STATS
            html.Div([

                html.H2('Performance', style={'color': 'black', 'textAlign': 'center', 'border': '5px solid #ddd', 'borderRadius': '5px'}),

                ## GRID LEAGUE STATS
                dag.AgGrid(
                    id='league-stats-grid',
                    rowData=dfLeagueStats.to_dict('records'),
                    columnDefs=[{'field': 'Metric'}, {'field': 'Value'}, {'field': 'Rank'}],
                    columnSize="responsiveSizeToFit",
                    getRowStyle=getRowStyle,
                    dashGridOptions={"rowHeight": 39, "headerHeight": 45, "animateRows": False}
                    )
                ],
                style={'display': 'flex', 'flex-direction': 'column', 'alignItems': 'center', 'backgroundColor': 'white', 'border': '5px solid #ddd', 'width': '33%'}
                ),

            ## DIV CARDS
            html.Div([

                ## HEADER CARDS
                html.H2('Accolades', style={'color': 'black', 'textAlign': 'center', 'border': '5px solid #ddd', 'borderRadius': '5px'}),

                ## DIV 1ST ROW CARDS
                html.Div([

                    dbc.Card(

                        dbc.CardBody(
                            [
                                html.H3("CHAMP", className="card-title", style={'color': 'black', 'textAlign': 'center'}),
                                html.P(id='championships-value', className="card-text",
                                      style={'color': 'black', 'textAlign': 'center', 'font-size': 20}),
                                ]
                            ), style={'border': '2px solid #ddd', 'borderRadius': '2px', 'height': '100px', 'margin': '10px', 'flex': '1', 'minWidth': '0'}
                        ),
                    dbc.Card(

                        dbc.CardBody(
                            [
                                html.H3("TOP 3", className="card-title", style={'color': 'black', 'textAlign': 'center'}),
                                html.P(id='top-3-finishes-value', className="card-text",
                                      style={'color': 'black', 'textAlign': 'center', 'font-size': 20}),
                                ]
                            ), style={'border': '2px solid #ddd', 'borderRadius': '2px', 'height': '100px', 'margin': '10px', 'flex': '1', 'minWidth': '0'}
                        ),
                    dbc.Card(

                        dbc.CardBody(
                            [
                                html.H3("TOP 5", className="card-title", style={'color': 'black', 'textAlign': 'center'}),
                                html.P(id='top-5-finishes-value', className="card-text",
                                      style={'color': 'black', 'textAlign': 'center', 'font-size': 20}),
                                ]
                            ), style={'border': '2px solid #ddd', 'borderRadius': '2px', 'height': '100px', 'margin': '10px', 'flex': '1', 'minWidth': '0'}
                        ),
                    ],
                         style={'display': 'flex'
                               ,'justifyContent': 'space-around'
                               ,'backgroundColor': 'white'
                               #,'border': '5px solid #ddd'
                               ,'alignItems': 'stretch'
                               ,'width': '100%'  # <-- make container full width
                               ,'boxSizing': 'border-box'  # <-- include padding/border in width
                               ,'border': '2px solid red'}),

                ## DIV 2ND ROW CARDS
                html.Div([

                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H3("REG. CHAMP", className="card-title", style={'color': 'black', 'textAlign': 'center'}),
                                html.P(id='reg-season-champ-value', className="card-text",
                                      style={'color': 'black', 'textAlign': 'center', 'fontSize': 20}),
                                ]
                            ), style={'border': '2px solid #ddd', 'borderRadius': '2px', 'height': '100px', 'margin': '10px', 'flex': '1', 'minWidth': '0'}
                        ),
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H3("RECORD", className="card-title", style={'color': 'black', 'textAlign': 'center'}),
                                html.P(id='record-value', className="card-text",
                                      style={'color': 'black', 'textAlign': 'center', 'fontSize': 20}),
                                ]
                            ), style={'border': '2px solid #ddd', 'borderRadius': '2px', 'height': '100px', 'margin': '10px', 'flex': '1', 'minWidth': '0'}
                        ),
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H3("PLAYOFF RECORD", className="card-title", style={'color': 'black', 'textAlign': 'center'}),
                                html.P(id='playoff-record-value', className="card-text",
                                      style={'color': 'black', 'textAlign': 'center', 'fontSize': 20}),
                                ]
                            ), style={'border': '2px solid #ddd', 'borderRadius': '2px', 'height': '100px', 'margin': '10px', 'flex': '1', 'minWidth': '0'}
                        ),
                    ],
                         style={'display': 'flex'
                               ,'justifyContent': 'space-around'
                               ,'backgroundColor': 'white'
                               #,'border': '5px solid #ddd'
                               ,'alignItems': 'stretch'
                               ,'width': '100%'  # <-- make container full width
                               ,'boxSizing': 'border-box'  # <-- include padding/border in width
                               ,'border': '2px solid red'}),

                ## DIV 3RD ROW CARDS
                html.Div([

                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H3("SEASONS", className="card-title", style={'color': 'black', 'textAlign': 'center'}),
                                html.P(id='seasons-value', className="card-text",
                                      style={'color': 'black', 'textAlign': 'center', 'fontSize': 20}),
                                ]
                            ), style={'border': '2px solid #ddd', 'borderRadius': '2px', 'height': '100px', 'margin': '10px', 'flex': '1', 'minWidth': '0'}
                        ),
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H3("PLAYOFF APP.", className="card-title", style={'color': 'black', 'textAlign': 'center'}),
                                html.P(id='playoff-app-value', className="card-text",
                                      style={'color': 'black', 'textAlign': 'center', 'fontSize': 20}),
                                ]
                            ), style={'border': '2px solid #ddd', 'borderRadius': '2px', 'height': '100px', 'margin': '10px', 'flex': '1', 'minWidth': '0'}
                        ),
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H3("LAST PLACE", className="card-title", style={'color': 'black', 'textAlign': 'center'}),
                                html.P(id='last-place-value', className="card-text",
                                      style={'color': 'black', 'textAlign': 'center', 'fontSize': 20}),
                                ]
                            ), style={'border': '2px solid #ddd', 'borderRadius': '2px', 'height': '100px', 'margin': '10px', 'flex': '1', 'minWidth': '0'}
                        ),
                    ],
                         style={'display': 'flex'
                               ,'justifyContent': 'space-around'
                               ,'backgroundColor': 'white'
                               #,'border': '5px solid #ddd'
                               ,'alignItems': 'stretch'
                               ,'width': '100%'  # <-- make container full width
                               ,'boxSizing': 'border-box'  # <-- include padding/border in width
                               ,'border': '2px solid red'}
                         )
                ],
                     style={'display': 'flex', 'flex-direction': 'column', 'alignItems': 'center', 'backgroundColor': 'white', 'border': '5px solid #ddd', 'flex': '1'}), ## STYLE CARDS

            ## DIV YEAR BY YEAR
            html.Div([

                html.Div([

                    html.H2('Year by Year Stats', style={'color': 'black', 'textAlign': 'center', 'border': '5px solid #ddd', 'borderRadius': '5px'}),

                    html.Div([

                        html.Label('Metric:', style={'font-size': '20px', 'font-weight': 'bold', 'color': 'black'}),

                        dcc.Dropdown(
                            options=[{'label': col, 'value': col} for col in YearByYearList],
                            value='Points',
                            id='metric-dropdown',
                            style={'width': '200px'}
                            )
                        ],
                             style={'display': 'flex', 'flex-direction': 'row', 'align-items': 'center', 'margin-left': '20px'}),
                    ],
                         style={'display': 'flex', 'flex-direction': 'row'}),

                ## FIGURE YEAR BY YEAR
                dcc.Graph(
                    figure={},
                    id='year-by-year-figure',
                    style={'width': '100%', 'height': '420px'},
                    config={'responsive': True}
                    )
                ],
                     style={'display': 'flex', 'flex-direction': 'column', 'alignItems': 'center', 'backgroundColor': 'white', 'border': '5px solid #ddd', 'flex': '1'}) ## STYLE FIGURE
        ],
                 style={'display': 'flex', 'flex-direction': 'row'}), ## STYLE TOP HALF

        ## DIV BOTTOM HALF
        html.Div([

            ## DIV HIGHLIGHTS
            html.Div([

                html.H2('Highlights', style={'color': 'black', 'textAlign': 'center', 'border': '5px solid #ddd', 'borderRadius': '5px'}),

                ## DIV MOST WEEK POINTS
                html.Div([

                  html.H4('Highest Weekly Score', style={'color': 'black', 'textAlign': 'center'}),

                  ## GRID MOST WEEK POINTS
                  dag.AgGrid(
                      id='most-wk-points-grid',
                      rowData=dfMostSingleWeekPoints.to_dict('records'),
                      columnDefs=[{'field': 'Year'}, {'field': 'Week'}, {'field': 'Score'}, {'field': 'All Time Rank'}],
                      columnSize="responsiveSizeToFit",
                      dashGridOptions={"rowHeight": 30, "headerHeight": 35, "animateRows": False},
                      style={'height': '150px'}
                      )
                  ],
                        style={'width': '100%'}),

                ## DIV LARGEST WINS
                html.Div([

                    html.H4('Largest Wins', style={'color': 'black', 'textAlign': 'center'}),

                    ## GRID LARGEST WINS
                    dag.AgGrid(
                        id='largest-wins-grid',
                        rowData=dfLargestWins.to_dict('records'),
                        columnDefs=[{'field': 'Year'}, {'field': 'Week'}, {'field': 'Against'}, {'field': 'Winning Margin'}, {'field': 'All Time Rank'}],
                        columnSize="responsiveSizeToFit",
                        dashGridOptions={"rowHeight": 30
                                         ,"headerHeight": 35
                                         ,"animateRows": False},
                        style={'height': '150px'}
                        )
                    ],
                         style={'width': '100%'})
                ],
                     style={'display': 'flex', 'flex-direction': 'column', 'alignItems': 'center', 'backgroundColor': 'white', 'border': '5px solid #ddd', 'width': '33%'}), ## STYLE HIGHLIGHTS

            ## DIV LOWLIGHTS
            html.Div([

                html.H2('Lowlights', style={'color': 'black', 'textAlign': 'center', 'border': '5px solid #ddd', 'borderRadius': '5px'}),

                ## DIV LEAST WEEK POINTS
                html.Div([

                  html.H4('Lowest Weekly Score', style={'color': 'black', 'textAlign': 'center'}),

                  ## GRID LEAST WEEK POINTS
                  dag.AgGrid(
                      id='least-wk-points-grid',
                      rowData=dfLeastSingleWeekPoints.to_dict('records'),
                      columnDefs=[{'field': 'Year'}, {'field': 'Week'}, {'field': 'Score'}, {'field': 'All Time Rank'}],
                      columnSize="responsiveSizeToFit",
                      dashGridOptions={"rowHeight": 30, "headerHeight": 35, "animateRows": False},
                      style={'height': '150px'}
                      )
                  ],
                        style={'width': '100%'}),

                ## DIV WORST LOSSES
                html.Div([

                    html.H4('Worst Losses', style={'color': 'black', 'textAlign': 'center'}),

                    ## GRID WORST LOSSES
                    dag.AgGrid(
                        id='worst-losses-grid',
                        rowData=dfWorstLosses.to_dict('records'),
                        columnDefs=[{'field': 'Year'}, {'field': 'Week'}, {'field': 'Against'}, {'field': 'Losing Margin'}, {'field': 'All Time Rank'}],
                        columnSize="responsiveSizeToFit",
                        dashGridOptions={"rowHeight": 30, "headerHeight": 35, "animateRows": False},
                        style={'height': '150px'}
                        )
                    ],
                         style={'width': '100%'})
                ],
                     style={'display': 'flex', 'flex-direction': 'column', 'alignItems': 'center', 'backgroundColor': 'white', 'border': '5px solid #ddd', 'width': '33%'}), ## STYLE LOWLIGHTS

            ## DIV OPPONENTS
            html.Div([

                html.H2('Head to Head', style={'color': 'black', 'textAlign': 'center', 'border': '5px solid #ddd', 'borderRadius': '5px'}), ## HEADER OPPONENTS

                html.Div([

                    html.H4('Stats Against Morons', style={'color': 'black', 'textAlign': 'center'}),

                    ## GRID OPPONENTS
                    dag.AgGrid(
                        id='opp-grid',
                        rowData=dfOpponents.to_dict('records'),
                        columnDefs=[{'field': 'Moron'}, {'field': 'Pts For'}, {'field': 'Pts Against'}, {'field': 'Win %'}, {'field': 'Matchups'}],
                        columnSize="responsiveSizeToFit",
                        dashGridOptions={"rowHeight": 30, "headerHeight": 35, "animateRows": False},
                        style={'height': '308px'}
                        )
                    ],
                          style={'width': '100%'})
                ],
                     style={'display': 'flex', 'flex-direction': 'column', 'alignItems': 'center', 'backgroundColor': 'white', 'border': '5px solid #ddd', 'width': '33%'}) ## STYLE OPPONENTS
            ],
                 style={'display': 'flex', 'flex-direction': 'row'}) ## STYLE BOTTOM HALF
        ],
             style={'backgroundColor': 'white'}) ## STYLE MAIN
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
  data = [{'Year': df_team['Year'].iloc[row], 'Week': df_team['Week'].iloc[row], 'Score': df_team['Score'].iloc[row], 'All Time Rank': df_team['All Time Rank'].iloc[row]} for row in range(len(df_team))]
  return data

## Largest Wins Callback
@callback(
    Output('largest-wins-grid', 'rowData')
    ,Input('team-dropdown', 'value')
)

## Updates Largest Wins Grid
def update_largest_wins_grid(team):
  df_team = dfLargestWins[dfLargestWins['Team'] == team]
  data = [{'Year': df_team['Year'].iloc[row], 'Week': df_team['Week'].iloc[row], 'Against': df_team['Opponent'].iloc[row], 'Winning Margin': df_team['Winning Margin'].iloc[row]
           ,'All Time Rank': df_team['All Time Rank'].iloc[row]} for row in range(len(df_team))]
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
  data = [{'Year': df_team['Year'].iloc[row], 'Week': df_team['Week'].iloc[row], 'Score': df_team['Score'].iloc[row], 'All Time Rank': df_team['All Time Rank'].iloc[row]} for row in range(len(df_team))]
  return data

## Worst Losses Callback
@callback(
    Output('worst-losses-grid', 'rowData')
    ,Input('team-dropdown', 'value')
)

## Updates Worst Losses Grid
def update_worst_losses_grid(team):
  df_team = dfWorstLosses[dfWorstLosses['Team'] == team]
  data = [{'Year': df_team['Year'].iloc[row], 'Week': df_team['Week'].iloc[row], 'Against': df_team['Opponent'].iloc[row], 'Losing Margin': df_team['Losing Margin'].iloc[row]
           ,'All Time Rank': df_team['All Time Rank'].iloc[row]} for row in range(len(df_team))]
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

#if __name__ == '__main__':
#    app.run(debug=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    app.run(debug=False, host="0.0.0.0", port=port)