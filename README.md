# League of Morons (LOM) Reference
## Overview
This project is an interactive dashboard built from scratch, summarizing 8 years (and counting) of history from my ESPN Fantasy Football League. It pulls raw data directly from the ESPN Fantasy Football API and tracks:
- All-time Performance
- Head-to-Head
- High/Low Lights
- Year-over-Year Stats

The dashboard can be found [here]([https://example.com](https://league-of-morons-reference.onrender.com)) and is built using
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
- Calculates metrics for the dashboard (performance, accolades/cards, head-to-head, highlights, lowlights, year-over-year stats)

## Data
`headtoheadsummary.csv`

This table is a raw head-to-head summary. Refer to `opponents.csv` for a clean version

`matchups_clean.csv`

This **matchups** table records every game played in league history, including both regular season and playoff matchups.  
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

`standings_final.csv`

This table documents the final standings from every season

`standings_regular.csv`

This table documents the regular-season standings from every season

`tpdash_alltimecards.csv`

The table is an **all-time accolades summary** for every team in the league.  
Each row represents a **single team’s career achievements** across all seasons played.  

- **Team** → The fantasy team being summarized  
- **Championships** → Number of league championships won (and years they won)  
- **Top 3 Finishes** → Total times finishing in the top 3 overall  
- **Top 5 Finishes** → Total times finishing in the top 5 overall  
- **Playoff Appearances** → Total playoff berths earned  
- **Seasons Played** → Total seasons the team has participated in  
- **All Time Record** → Combined win–loss-tie record across all games  
- **Playoff Record** → Combined win–loss record in playoff games only  
- **Reg Champ** → Number of regular season first-place finishes  
- **Last Place** → Number of last-place finishes  

`tpdash_alltimestats.csv`

This is an **all-team stats table**, which compares every team across a variety of performance metrics.  
Each row represents the value of a **single metric for a single team**, along with its standing in the league.  

- **Team** → The fantasy team being evaluated  
- **Metric** → The statistic being measured
- **Value** → The team’s value for that specific metric  
- **League Rank** → The team’s ranking for that metric compared to all league members 

`tpdash_bestweeks.csv`

This table tracks each team’s **best single-week performances**, capturing the games where scoring output was at its highest.  
Each row represents one of the **top 3 highest-scoring weeks for a given team**, with the following details:  

- **Year** → Season when the high score occurred  
- **Week** → Specific week of the matchup  
- **Team** → The team that posted the high score  
- **Score** → Total points scored by the team that week  
- **Opponent** → The opposing team in that matchup  
- **All Time Rank** → Ranking of the score compared to the *highest scores in league history*

`tpdash_bestwins.csv`

This table tracks each team's **best wins**.  
Each row represents one of the **top 3 best wins for a given team**, with details about when and how it happened:  

- **Year** → Season when the win occurred  
- **Week** → Specific week of the matchup  
- **Team** → The team that won  
- **Opponent** → The opposing team that loss  
- **Winning Margin** → Point differential (Team’s score – Opponent’s score)  
- **All Time Rank** → Overall ranking of the win compared to *every win in league history* 

`tpdash_opponents.csv`

The table tracks the **head-to-head matchup statistics** between every pair of teams in the league.  
Each row represents a **unique team vs. opponent combination** and provides the following stats:

- **Team** → The team being evaluated  
- **Opponent** → The opposing team in the matchup history  
- **PointsFor** → Total points scored by *Team* across all games vs. that opponent  
- **PointsAgainst** → Total points scored by *Opponent* in those games  
- **Win %** → The percentage of games won by *Team* against that opponent  
- **Total Matchups** → How many times the two teams have faced each other over the league’s history  

`tpdash_worstweeks.csv`

This table tracks each team’s **worst single-week performances**, capturing the games where scoring output was at its lowest.  
Each row represents one of the **top 3 lowest-scoring weeks for a given team**, with the following details:  

- **Year** → Season when the low score occurred  
- **Week** → Specific week of the matchup  
- **Team** → The team that posted the low score  
- **Score** → Total points scored by the team that week  
- **Opponent** → The opposing team in that matchup  
- **All Time Rank** → Ranking of the score compared to the *lowest scores in league history*

`tpdash_worstlosses.csv`

This table tracks each team's **worst losses**, highlighting the biggest defeats in league history.  
Each row represents one of the **top 3 worst losses for a given team**, with details about when and how it happened:  

- **Year** → Season when the loss occurred  
- **Week** → Specific week of the matchup  
- **Team** → The team that suffered the loss  
- **Opponent** → The opposing team that delivered the loss  
- **Losing Margin** → Point differential (Opponent’s score – Team’s score)  
- **All Time Rank** → Overall ranking of the loss compared to *every loss in league history*   

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
