# -*- coding: utf-8 -*-
"""
Created on Sun Sep  3 21:18:38 2023

@author: Alex
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Lecture du fichier CSV
df_premier_league = pd.read_csv("premier_league_all_matches.csv", delimiter=",")

# Affichage des 5 premières lignes
print(df_premier_league.head())

# Séparation des scores en buts à domicile et à l'extérieur
df_premier_league['Home_Goals'] = df_premier_league['Score'].str.split('–').str[0].astype(int)
df_premier_league['Away_Goals'] = df_premier_league['Score'].str.split('–').str[1].astype(int)

# Calcul des victoires, nuls et défaites pour chaque équipe à domicile et à l'extérieur
df_premier_league['Home_Win'] = (df_premier_league['Home_Goals'] > df_premier_league['Away_Goals']).astype(int)
df_premier_league['Away_Win'] = (df_premier_league['Home_Goals'] < df_premier_league['Away_Goals']).astype(int)
df_premier_league['Draw'] = (df_premier_league['Home_Goals'] == df_premier_league['Away_Goals']).astype(int)

# Calcul des points pour chaque équipe à domicile et à l'extérieur
df_premier_league['Home_Points'] = df_premier_league['Home_Win']*3 + df_premier_league['Draw']
df_premier_league['Away_Points'] = df_premier_league['Away_Win']*3 + df_premier_league['Draw']

# Aggrégation des résultats pour chaque équipe à domicile
home_agg = df_premier_league.groupby('Home_Team').agg({
    'Home_Points': 'sum',
    'Home_Goals': 'sum',
    'Away_Goals': 'sum',
    'Home_Win': 'sum',
    'Draw': 'sum'
}).rename(columns={
    'Home_Team': 'Team',
    'Home_Points': 'HomePoints',
    'Home_Goals': 'HomeGoalsFor',
    'Away_Goals': 'HomeGoalsAgainst',
    'Home_Win': 'HomeWins',
    'Draw': 'HomeDraws'
})

# Aggrégation des résultats pour chaque équipe à l'extérieur
away_agg = df_premier_league.groupby('Away_Team').agg({
    'Away_Points': 'sum',
    'Away_Goals': 'sum',
    'Home_Goals': 'sum',
    'Away_Win': 'sum',
    'Draw': 'sum'
}).rename(columns={
    'Away_Team': 'Team',
    'Away_Points': 'AwayPoints',
    'Away_Goals': 'AwayGoalsFor',
    'Home_Goals': 'AwayGoalsAgainst',
    'Away_Win': 'AwayWins',
    'Draw': 'AwayDraws'
})

# Fusion des résultats à domicile et à l'extérieur pour chaque équipe
league_table = pd.concat([home_agg, away_agg], axis=1)

# Calcul du total des points, buts et matches
league_table['TotalPoints'] = league_table['HomePoints'] + league_table['AwayPoints']
league_table['TotalGoalsFor'] = league_table['HomeGoalsFor'] + league_table['AwayGoalsFor']
league_table['TotalGoalsAgainst'] = league_table['HomeGoalsAgainst'] + league_table['AwayGoalsAgainst']
league_table['TotalWins'] = league_table['HomeWins'] + league_table['AwayWins']
league_table['TotalDraws'] = league_table['HomeDraws'] + league_table['AwayDraws']
league_table['TotalLosses'] = 38 - league_table['TotalWins'] - league_table['TotalDraws']  # 38 matches in a PL season

# Tri du tableau en fonction des points totaux, puis de la différence de buts, puis des buts marqués
league_table = league_table.sort_values(by=['TotalPoints', 'TotalGoalsFor', 'TotalGoalsAgainst'], ascending=[False, False, True])
league_table = league_table[['TotalPoints', 'TotalGoalsFor', 'TotalGoalsAgainst', 'TotalWins', 'TotalDraws', 'TotalLosses']]
league_table.reset_index(inplace=True)
league_table.rename(columns={'index': 'Team'}, inplace=True)

league_table

# Équipe avec le plus de buts à domicile
top_home_goals_team = df_premier_league.groupby('Home_Team').Home_Goals.sum().idxmax()
top_home_goals = df_premier_league.groupby('Home_Team').Home_Goals.sum().max()

# Équipe avec le plus de buts à l'extérieur
top_away_goals_team = df_premier_league.groupby('Away_Team').Away_Goals.sum().idxmax()
top_away_goals = df_premier_league.groupby('Away_Team').Away_Goals.sum().max()

top_home_goals_team, top_home_goals, top_away_goals_team, top_away_goals

# Calcul de la différence entre les buts réels et les "expected goals" pour chaque équipe à domicile et à l'extérieur
df_premier_league['Home_Goals_vs_xG'] = df_premier_league['Home_Goals'] - df_premier_league['Home_xG']
df_premier_league['Away_Goals_vs_xG'] = df_premier_league['Away_Goals'] - df_premier_league['Away_xG']

# Aggrégation des résultats pour chaque équipe
teams_xG_diff = df_premier_league.groupby('Home_Team').Home_Goals_vs_xG.sum() + df_premier_league.groupby('Away_Team').Away_Goals_vs_xG.sum()

# Équipe avec la meilleure différence de buts par rapport aux "expected goals"
best_xG_diff_team = teams_xG_diff.idxmax()
best_xG_diff_value = teams_xG_diff.max()

best_xG_diff_team, best_xG_diff_value


# Calcul de l'assistance moyenne pour chaque équipe à domicile
attendance_avg = df_premier_league.groupby('Home_Team').Attendance.mean().sort_values(ascending=False)

# Visualisation
plt.figure(figsize=(15,10))
attendance_avg.plot(kind='bar', color='skyblue')
plt.title('Assistance moyenne par équipe à domicile')
plt.xlabel('Équipe')
plt.ylabel('Assistance moyenne')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# Comptage du nombre de matches arbitrés par chaque arbitre
referee_counts = df_premier_league['Referee'].value_counts()

# Visualisation
plt.figure(figsize=(15,10))
referee_counts.plot(kind='bar', color='lightgreen')
plt.title('Nombre de matches arbitrés par arbitre')
plt.xlabel('Arbitre')
plt.ylabel('Nombre de matches')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


df_premier_league['Cumulative_Home_Points'] = df_premier_league.groupby('Home_Team')['Home_Points'].cumsum()
df_premier_league['Cumulative_Away_Points'] = df_premier_league.groupby('Away_Team')['Away_Points'].cumsum()

# Fusion des points accumulés à domicile et à l'extérieur
home_cumulative = df_premier_league[['Week', 'Home_Team', 'Cumulative_Home_Points']]
away_cumulative = df_premier_league[['Week', 'Away_Team', 'Cumulative_Away_Points']]
home_cumulative.columns = ['Week', 'Team', 'Points']
away_cumulative.columns = ['Week', 'Team', 'Points']
# Fusion des points accumulés à domicile et à l'extérieur et regroupement par semaine
cumulative_points = pd.concat([home_cumulative, away_cumulative])
cumulative_points = cumulative_points.groupby(['Team', 'Week']).sum().groupby(level=0).cumsum().reset_index()

# Sélection des 5 équipes les plus performantes en termes de points totaux
top_teams = league_table['Team'].head(5)

plt.figure(figsize=(14, 8))

for team in top_teams:
    team_data = cumulative_points[cumulative_points['Team'] == team]
    plt.plot(team_data['Week'], team_data['Points'], label=team, marker='o')

plt.title('Performance des équipes au fil des semaines')
plt.xlabel('Semaine')
plt.ylabel('Points cumulés')
plt.legend()
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.tight_layout()
plt.show()


# Extraction de l'année à partir de la colonne "Date"
df_premier_league['Year'] = pd.to_datetime(df_premier_league['Date']).dt.year

# Fonction pour calculer les points par saison
def calculate_season_points(df, start_year):
    season_data = df[(df['Date'] >= f"{start_year}-08-01") & (df['Date'] <= f"{start_year + 1}-05-31")]
    home_points = season_data.groupby('Home_Team')['Home_Points'].sum()
    away_points = season_data.groupby('Away_Team')['Away_Points'].sum()
    total_points = home_points.add(away_points, fill_value=0)
    return total_points

# Calcul des points pour chaque saison
seasons = range(df_premier_league['Year'].min(), df_premier_league['Year'].max())
season_points = {}
for season in seasons:
    season_points[f"{season}/{season+1}"] = calculate_season_points(df_premier_league, season)

season_points_df = pd.DataFrame(season_points)

# Visualisation avec une carte thermique
plt.figure(figsize=(15, 12))
sns.heatmap(season_points_df.sort_values(by=season_points_df.last_valid_index(), axis=1, ascending=False), cmap="YlGnBu", annot=True, fmt=".0f", linewidths=.5, cbar_kws={'label': 'Total Points'})
plt.title('Points accumulés par équipe et par saison')
plt.ylabel('Équipes')
plt.xlabel('Saison')
plt.tight_layout()
plt.show()

# Initialisation des figures
figs = []

# 1. Quelle équipe a marqué le plus de buts à domicile et à l'extérieur?
fig, ax = plt.subplots(figsize=(12, 8))
total_goals.sort_values().plot(kind='barh', ax=ax, color='skyblue')
ax.set_title("Total de buts marqués par équipe")
ax.set_xlabel("Nombre de buts")
figs.append(fig)
plt.close()

# 2. Quelle équipe a le meilleur ratio de buts marqués par rapport aux "expected goals"?
fig, ax = plt.subplots(figsize=(12, 8))
goal_ratio.sort_values().plot(kind='barh', ax=ax, color='lightcoral')
ax.set_title("Ratio de buts marqués par rapport aux 'expected goals' par équipe")
ax.set_xlabel("Ratio")
figs.append(fig)
plt.close()

# 3. Comment l'assistance varie-t-elle en fonction des équipes à domicile?
fig, ax = plt.subplots(figsize=(12, 8))
attendance_avg.sort_values().plot(kind='barh', ax=ax, color='lightgreen')
ax.set_title("Assistance moyenne par équipe à domicile")
ax.set_xlabel("Assistance moyenne")
figs.append(fig)
plt.close()

# 4. Qui sont les arbitres les plus courants et combien de matches ont-ils arbitrés?
fig, ax = plt.subplots(figsize=(12, 8))
referee_counts.head(10).sort_values().plot(kind='barh', ax=ax, color='lightgoldenrodyellow')
ax.set_title("Top 10 des arbitres par nombre de matches arbitrés")
ax.set_xlabel("Nombre de matches")
figs.append(fig)
plt.close()

# 5. Comment la performance des équipes varie-t-elle au fil des semaines?
# (Le code pour cette question est assez long car il implique un suivi des points cumulés pour chaque équipe au fil des semaines.)
teams = df_premier_league['Home_Team'].unique()
fig, ax = plt.subplots(figsize=(14, 10))
for team in teams:
    team_data = df_premier_league[df_premier_league['Home_Team'] == team]
    ax.plot(team_data['Week'], team_data['Home_Points_Cumulative'], label=team)
ax.set_title("Performance des équipes au fil des semaines")
ax.set_xlabel("Semaine")
ax.set_ylabel("Points cumulés")
ax.legend(loc="upper left", bbox_to_anchor=(1,1), ncol=1)
fig.tight_layout()
figs.append(fig)
plt.close()