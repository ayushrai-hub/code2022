import pandas as pd
from nba_api.stats.endpoints import playercareerstats

# Fetch player career stats
history = playercareerstats.PlayerCareerStats(player_id='303999')
df = history.get_data_frames()[0]

# Get unique values as a list
unique_league_ids_list = df['LEAGUE_ID'].unique().tolist()
print("Unique LEAGUE_ID values as list:")
print(unique_league_ids_list)

