# Matches de Premiere League entre 2018 et 2023



# Analyse des données de la Premier League

Cette documentation couvre l'analyse des données de la Premier League. Nous aborderons cinq questions principales concernant les performances des équipes, les arbitres, et l'assistance. Pour chaque question, nous fournirons le code Python utilisé pour obtenir les résultats, ainsi qu'une explication détaillée pour les débutants.


## Quelle équipe a marqué le plus de buts à domicile et à l'extérieur?
```python

home_goals = df_premier_league.groupby('Home_Team')['Home_Goals'].sum()
away_goals = df_premier_league.groupby('Away_Team')['Away_Goals'].sum()
total_goals = home_goals.add(away_goals, fill_value=0)

# Génération du graphe
fig, ax = plt.subplots(figsize=(12, 8))
total_goals.sort_values().plot(kind='barh', ax=ax, color='skyblue')
ax.set_title("Total de buts marqués par équipe")
ax.set_xlabel("Nombre de buts")
plt.tight_layout()
plt.show()

```

## Quelle équipe a le meilleur ratio de buts marqués par rapport aux "expected goals"?
```python

home_xgoals = df_premier_league.groupby('Home_Team')['Home_xG'].sum()
away_xgoals = df_premier_league.groupby('Away_Team')['Away_xG'].sum()
total_xgoals = home_xgoals.add(away_xgoals, fill_value=0)
goal_ratio = total_goals / total_xgoals

# Génération du graphe
fig, ax = plt.subplots(figsize=(12, 8))
goal_ratio.sort_values().plot(kind='barh', ax=ax, color='lightcoral')
ax.set_title("Ratio de buts marqués par rapport aux 'expected goals' par équipe")
ax.set_xlabel("Ratio")
plt.tight_layout()
plt.show()

```

## Comment l'assistance varie-t-elle en fonction des équipes à domicile?
```python

average_attendance = df_premier_league.groupby('Home_Team')

# Génération du graphe
fig, ax = plt.subplots(figsize=(12, 8))
average_attendance.plot(kind='barh', ax=ax, color='lightgreen')
ax.set_title("Assistance moyenne par équipe à domicile")
ax.set_xlabel("Assistance moyenne")
plt.tight_layout()
plt.show()
```

## Qui sont les arbitres les plus courants et combien de matches ont-ils arbitrés?
```python

referee_counts = df_premier_league['Referee'].value_counts()

# Génération du graphe pour les 10 arbitres les plus courants
fig, ax = plt.subplots(figsize=(12, 8))
referee_counts.head(10).sort_values().plot(kind='barh', ax=ax, color='lightgoldenrodyellow')
ax.set_title("Top 10 des arbitres par nombre de matches arbitrés")
ax.set_xlabel("Nombre de matches")
plt.tight_layout()
plt.show()

```

## Comment la performance des équipes varie-t-elle au fil des semaines?
```python

df_premier_league['Week'] = pd.to_datetime(df_premier_league['Date']).dt.isocalendar().week
df_premier_league['Home_Points_Cumulative'] = df_premier_league.groupby(['Home_Team', 'Week'])['Home_Points'].cumsum()
df_premier_league['Away_Points_Cumulative'] = df_premier_league.groupby(['Away_Team', 'Week'])['Away_Points'].cumsum()

# Calcul des points cumulés par semaine pour chaque équipe
cumulative_points = {}
for team in teams:
    cumulative_points[team] = {
        'Weeks': [],
        'Points': []
    }
    for week in df_premier_league['Week'].unique():
        home_points = df_premier_league[(df_premier_league['Home_Team'] == team) & (df_premier_league['Week'] == week)]['Home_Points_Cumulative'].sum()
        away_points = df_premier_league[(df_premier_league['Away_Team'] == team) & (df_premier_league['Week'] == week)]['Away_Points_Cumulative'].sum()
        
        # If both home and away points exist for that week, take the average
        if home_points and away_points:
            cumulative_points[team]['Weeks'].append(week)
            cumulative_points[team]['Points'].append((home_points + away_points) / 2)
        elif home_points:
            cumulative_points[team]['Weeks'].append(week)
            cumulative_points[team]['Points'].append(home_points)
        elif away_points:
            cumulative_points[team]['Weeks'].append(week)
            cumulative_points[team]['Points'].append(away_points)

last_week = df_premier_league['Week'].max()
top_teams = df_premier_league[df_premier_league['Week'] == last_week].groupby('Home_Team')['Home_Points_Cumulative'].sum().nlargest(5).index.tolist()

# Génération du graphe linéaire montrant l'évolution des points cumulés pour les 5 meilleures équipes au fil des semaines
fig, ax = plt.subplots(figsize=(14, 10))
for team, data in cumulative_points.items():
    if team in top_teams:
        ax.plot(data['Weeks'], data['Points'], label=team, linewidth=2)
ax.set_title("Performance des 5 meilleures équipes au fil des semaines")
ax.set_xlabel("Semaine")
ax.set_ylabel("Points cumulés")
ax.legend(loc="upper left")
fig.tight_layout()
plt.show()

```

# Conclusion

Grâce à cette analyse, nous avons pu obtenir des informations précieuses sur les performances des équipes, l'efficacité des arbitres et la popularité des équipes en termes d'assistance. Ces insights peuvent être utilisés par les clubs, les médias, et les fans pour mieux comprendre les dynamiques de la Premier League.
