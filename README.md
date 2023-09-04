# Matches de Premiere League entre 2018 et 2023



# Analyse des données de la Premier League

Cette documentation couvre l'analyse des données de la Premier League. Nous aborderons cinq questions principales concernant les performances des équipes, les arbitres, et l'assistance. Pour chaque question, nous fournirons le code Python utilisé pour obtenir les résultats, ainsi qu'une explication détaillée pour les débutants.


## Quelle équipe a marqué le plus de buts à domicile et à l'extérieur?
```python

home_goals = df_premier_league.groupby('Home_Team')['Home_Goals'].sum()
away_goals = df_premier_league.groupby('Away_Team')['Away_Goals'].sum()
total_goals = home_goals.add(away_goals, fill_value=0)
top_scorer_team = total_goals.idxmax()
top_scorer_goals = total_goals.max()
top_scorer_team, top_scorer_goals

```

## Quelle équipe a le meilleur ratio de buts marqués par rapport aux "expected goals"?
```python

home_goals = df_premier_league.groupby('Home_Team')['Home_Goals'].sum()
home_xgoals = df_premier_league.groupby('Home_Team')['Home_Expected_Goals'].sum()
away_goals = df_premier_league.groupby('Away_Team')['Away_Goals'].sum()
away_xgoals = df_premier_league.groupby('Away_Team')['Away_Expected_Goals'].sum()
total_goals = home_goals.add(away_goals, fill_value=0)
total_xgoals = home_xgoals.add(away_xgoals, fill_value=0)
goal_ratio = total_goals / total_xgoals
best_ratio_team = goal_ratio.idxmax()
best_ratio_value = goal_ratio.max()
best_ratio_team, best_ratio_value

```

## Comment l'assistance varie-t-elle en fonction des équipes à domicile?
```python

average_attendance = df_premier_league.groupby('Home_Team')['Attendance'].mean().sort_values(ascending=False)
average_attendance

```

## Qui sont les arbitres les plus courants et combien de matches ont-ils arbitrés?
```python

referee_counts = df_premier_league['Referee'].value_counts()
referee_counts.head(10)

```

## Comment la performance des équipes varie-t-elle au fil des semaines?
```python

df_premier_league['Week'] = pd.to_datetime(df_premier_league['Date']).dt.isocalendar().week
df_premier_league['Home_Points_Cumulative'] = df_premier_league.groupby(['Home_Team', 'Week'])['Home_Points'].cumsum()
df_premier_league['Away_Points_Cumulative'] = df_premier_league.groupby(['Away_Team', 'Week'])['Away_Points'].cumsum()
df_premier_league[['Home_Team', 'Week', 'Home_Points_Cumulative', 'Away_Team', 'Away_Points_Cumulative']].head(10)

```

# Conclusion

Grâce à cette analyse, nous avons pu obtenir des informations précieuses sur les performances des équipes, l'efficacité des arbitres et la popularité des équipes en termes d'assistance. Ces insights peuvent être utilisés par les clubs, les médias, et les fans pour mieux comprendre les dynamiques de la Premier League.
