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
`headtoheadsummary.csv` - a head-to-head summary of every possible matchup in the leagu

`matchups_clean.csv`

This **matchups** records every game played in league history, including both regular season and playoff matchups.  
Each row represents a **unique weekly matchup** between two teams, with detailed results:  

- **Year** → Season of the matchup  
- **Week** → Specific week of the season  
- **Team** → The team being evaluated  
- **Score** → Total points scored by the team  
- **Opponent** → The opposing team  
- **Opponent_Score** → Points scored by the opponent  
- **Score_Margin** → Point differential (Score – Opponent_Score)  
- **Outcome** → Win, loss, or tie for the team  
- **Type** → Matchup type (Regular Season or Playoffs)  
- **Top_Scoring_Week** → Binary indicator (1 if this was the highest score for the given week)  
- **Low_Scoring_Week** → Binary indicator (1 if this was the lowest score for the given week)  

This table is the **foundation of the league’s history**, enabling detailed head-to-head analysis, tracking playoff runs, and highlighting record-breaking weeks.

`standings_final.csv` - final standings from every season (hard-coded)

`standings_regular.csv` - regular season final standings from every season

`tpdash_alltimecards.csv` - accolades for each team

`tpdash_alltimestats.csv` - statistics for each team and where they rank all time

`tpdash_bestweeks.csv` - a teams top 3 weeks in terms of total points scored

`tpdash_bestwins.csv` - a teams top 3 largest wins in terms of scoring margin

`tpdash_opponents.csv`

The table tracks the **head-to-head matchup statistics** between every pair of teams in the league.  
Each row represents a **unique team vs. opponent combination** and provides the following stats:

- **Team** → The team being evaluated  
- **Opponent** → The opposing team in the matchup history  
- **PointsFor** → Total points scored by *Team* across all games vs. that opponent  
- **PointsAgainst** → Total points scored by *Opponent* in those games  
- **Win %** → The percentage of games won by *Team* against that opponent  
- **Total Matchups** → How many times the two teams have faced each other over the league’s history  

`tpdash_worstlosses.csv`

This table tracks each team's **worst losses**, highlighting the biggest defeats in league history.  
Each row represents one of the **top 3 worst losses for a given team**, with details about when and how it happened:  

- **Year** → Season when the loss occurred  
- **Week** → Specific week of the matchup  
- **Team** → The team that suffered the loss  
- **Opponent** → The opposing team that delivered the loss  
- **Losing Margin** → Point differential (Opponent’s score – Team’s score)  
- **All Time Rank** → Overall ranking of the loss compared to *every loss in league history* 

`tpdash_worstweeks.csv`

This table tracks each team’s **worst single-week performances**, capturing the games where scoring output was at its lowest.  
Each row represents one of the **top 3 lowest-scoring weeks for a given team**, with the following details:  

- **Year** → Season when the low score occurred  
- **Week** → Specific week of the matchup  
- **Team** → The team that posted the low score  
- **Score** → Total points scored by the team that week  
- **Opponent** → The opposing team in that matchup  
- **All Time Rank** → Ranking of the score compared to the *lowest scores in league history*  

`tpdash_yearlyavgstats.csv`

This table tracks **yearly averages**, which provides context for evaluating performance across different seasons.  
Each row represents a **single season** and summarizes league-wide averages for that year. The table includes:  

- **Year** → The season being summarized  
- **Points** → Total points scored by the team that year  
- **PPG** → Average points per game across the season  
- **Wins** → Total number of wins  
- **Score Margin** → Average point differential per game (Points For – Points Against)  
- **Win %** → Winning percentage for the season  
- **Reg. Finishing Position** → Final standing after the regular season  
- **Final Finishing Position** → Overall finish after playoffs  

This table powers the **dotted average reference line** in the year-by-year visual, allowing users to compare a team’s performance in any given season to the league’s long-term averages. 

`tpdash_yearlystats.csv`

This table tracks **yearly stats**, which breaks down each team’s performance on a season-by-season basis.  
Unlike the average metrics table, this version is **team-specific**: each row represents one team’s stats for a given year.  

- **Team** → The fantasy team being summarized  
- **Year** → The season being summarized  
- **Points** → Total points scored that year  
- **PPG** → Average points per game across the season  
- **Wins** → Total number of wins  
- **Score Margin** → Average point differential per game (Points For – Points Against)  
- **Win %** → Winning percentage for the season  
- **Reg. Finishing Position** → Standing after the regular season  
- **Final Finishing Position** → Overall finish after playoffs 

This table powers the **solid lines** in the year-by-year visual, allowing users to view their performance for a specific metric over the years
