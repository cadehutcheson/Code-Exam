import socket
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
import time

# Set the IP address and port of the server
#IP_ADDRESS = input("Enter IP:")
IP_ADDRESS = ''
if IP_ADDRESS == '': IP_ADDRESS = '192.168.56.1'  # Replace with the IP address of the server

PORT = 21567




players_list = players.get_players()


while True:
    player_name = input("Enter a player's name: ")
    player_name = player_name.title()
    print(player_name)
    #quit if 'q' si entered
    if player_name == 'q':
        exit

    player = [player for player in players_list if player['full_name'] == player_name][0]
    if player is None:
        print("Invalid Name")
        pass

    # Get the player's career stats
    stats = playercareerstats.PlayerCareerStats(player_id=player['id'])

    stats_dict = stats.get_dict()
    #print(stats_dict)

    career_totals = next(rs for rs in stats_dict['resultSets'] if rs['name'] == 'CareerTotalsRegularSeason')
    season_totals = next(rs for rs in stats_dict['resultSets'] if rs['name'] == 'SeasonTotalsRegularSeason')
    # Get the first row of the result set (there should only be one)
    career_totals_row = career_totals['rowSet'][0]
    season_totals_row = season_totals['rowSet'][0]

    
    # Get the index of the 'PTS' column
    pts_index = career_totals['headers'].index('PTS')
    ast_index = career_totals['headers'].index('AST')

    seasons_index = season_totals['headers'].index('SEASON_ID')
    s_points_index = season_totals['headers'].index('PTS')
    s_assists_index = season_totals['headers'].index('AST')

    # Extract the total points scored from the row
    total_points = career_totals_row[pts_index]
    total_assists = career_totals_row[ast_index]

    season_years=""
    season_points=""
    season_assists=""
    for i in range(len(season_totals['rowSet']) -1):
        if season_totals['rowSet'][i][seasons_index] == season_totals['rowSet'][i+1][seasons_index]:
            continue
        season_years += (str(season_totals['rowSet'][i][seasons_index])) + ","
        season_points += (str(season_totals['rowSet'][i][s_points_index])) + ","
        season_assists += (str(season_totals['rowSet'][i][s_assists_index])) + ","
    
    season_years += (str(season_totals['rowSet'][-1][seasons_index]))
    season_points += (str(season_totals['rowSet'][-1][s_points_index]))
    season_assists += (str(season_totals['rowSet'][-1][s_assists_index]))

    print(f"Total regular season points scored: {total_points}")
    print(f"Total regular season assists: {total_assists}")

    print("Seasons played: ", season_years)
    print("Season totals - points: ", season_points)
    print("Season totals - assists: ", season_assists)

    if total_points <= 0:
        print("Invalid points")
        pass

    data = f"{player_name}_{total_points}_{total_assists}/{season_years}_{season_points}_{season_assists}" 
    # Read data from the terminal and send it to the server
    
    while True:
        print()
        try:
        #connect to IP & port
        # Create a socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((IP_ADDRESS, PORT))
            data = f"{player_name}_{total_points}_{total_assists}/{season_years}_{season_points}_{season_assists}"
            print("connected! ", player_name, " stats sent to ", IP_ADDRESS)
            data_bytes = data.encode()
            sock.send(data_bytes)
            break
        except:
            print("Could not Connect")
            time.sleep(10)

    # Close the socket
sock.close()

