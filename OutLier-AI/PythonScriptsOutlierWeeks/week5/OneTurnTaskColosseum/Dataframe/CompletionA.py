import pandas as pd
from nba_api.stats.endpoints import playercareerstats

# Fetch player career stats using the NBA API
history = playercareerstats.PlayerCareerStats(player_id='303999')

# Convert the data into a DataFrame
df = history.get_data_frames()[0]

# assuming df is the DataFrame returned from history.get_data_frames()[0]
unique_league_ids = df['LEAGUE_ID'].unique()

print(unique_league_ids)


# Convert the DataFrame to JSON
json_data = df.to_json()

# Convert the DataFrame to a dictionary
dict_data = df.to_dict()

# Print the DataFrame, JSON, and dictionary
print("DataFrame:\n", df)
print("JSON:\n", json_data)
print("Dictionary:\n", dict_data)
