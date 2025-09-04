# League of Morons (LOM) Reference
## Overview
This project is an interactive dashboard summarizing 8 years (and counting) of history from my ESPN Fantasy Football League. It pulls raw data directly from the ESPN Fantasy Football API and tracks:
- All-time Performance
- Head-to-Head
- High/Low Lights
- Year-over-Year Stats

The dashboard is built with:
- Python
- Jupyter Notebooks (data ingestion + analysis)
- Dash/Plotly (for interactive dashboard)
- Render (for deployment)

## Notebooks
`ESPN_API_Data_Pull.ipynb`
- Pulls and cleans all matchup data from the ESPN API
- Builds a head-to-head summary
- Consolidates the historical regular season and final standings
 
`Analysis.ipynb`
- Calculates all data sources for the dashboard (performance, accolades, head-to-head, highlights, lowlights, year-over-year stats)

## Data
`headtoheadsummary.csv` - a head-to-head summary of every possible matchup in the league

`matchups_clean.csv` - each row is a unique matchup and the statistics for it

`standings_final.csv` - final standings from every season (hard-coded)

`standings_regular.csv` - regular season final standings from every season

`tpdash_alltimecards.csv`

`tpdash_alltimestats.csv`

`tpdash_bestweeks.csv`

`tpdash_bestwins.csv`

`tpdash_opponents.csv`

`tpdash_worstlosses.csv`

`tpdash_worstweeks.csv`

`tpdash_yearlyavgstats.csv`

`tpdash_yearlystats.csv`
