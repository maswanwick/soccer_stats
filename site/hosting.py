#########################
# Import the dependencies
#########################
import psycopg2
import pandas as pd
from json import loads
from flask import Flask, render_template

import warnings
warnings.filterwarnings('ignore')

#########################
# Return DataFrame for given SQL statement
#########################
def getDataFrameFromDB(sql):
    conn = psycopg2.connect(
        database=f"soccer_stats", user='postgres', password='postgres', host='127.0.0.1', port='5432'
    )

    conn.autocommit = True

    cursor = conn.cursor()

    df = pd.read_sql(sql, cursor.connection)

    return df

#########################
# Setup the Flask app
#########################
hosting = Flask(__name__)

#########################
# Base route
#########################
@hosting.route("/")
def home():
    return render_template('site.html');

#########################
# Returns the list of leagues.  Used to build dropdown
#########################
@hosting.route("/api/v1.0/leagues")
def getLeagues():
    sql = '''
        SELECT
            league_id,
            league
        FROM
            "league"
        ORDER BY
            league
    '''
    league_df = getDataFrameFromDB(sql)
    league_df.loc[-1] = [-1, 'ALL']
    league_df.index = league_df.index + 1
    league_df = league_df.sort_index()
    json_data = league_df.to_json(orient='records')
    return loads(json_data)
    
#########################
# Returns list of teams for a given league.  Used to build dropdown
# If leagueId = -1, return all teams
#########################
@hosting.route("/api/v1.0/leagues/<leagueId>/teams")
def getTeamsForLeague(leagueId):
    sql = '''
        SELECT
            team_id,
            team
        FROM
            "team"
    '''

    if (leagueId != '-1'):
        sql += f'''
            WHERE
                league_id = '{leagueId}'
        '''

    sql += '''
        ORDER BY
            team
    '''
    team_df = getDataFrameFromDB(sql)
    team_df.loc[-1] = [-1, 'ALL']
    team_df.index = team_df.index + 1
    team_df = team_df.sort_index()
    json_data = team_df.to_json(orient='records')
    return loads(json_data)

#########################
# Returns list of positions.  Used to build dropdown
#########################
@hosting.route("/api/v1.0/positions")
def getPositions():
    sql = '''
        SELECT
            position_id,
            position
        FROM
            "position"
    '''

    position_df = getDataFrameFromDB(sql)
    position_df.loc[-1] = [-1, 'ALL']
    position_df.index = position_df.index + 1
    position_df = position_df.sort_index()
    json_data = position_df.to_json(orient='records')
    return loads(json_data)

#########################
# Returns data for the photo and demographic data for the provided player.
#########################
@hosting.route("/api/v1.0/player_data/<playerId>")
def getPlayerPhotoAndDemographics(playerId):
    sql = f'''
        SELECT
            p.photo_url,
            CASE WHEN p.jersey_number = -1 THEN 'N/A' ELSE (p.jersey_number)::text END as jersey_number,
            CASE WHEN p.height = 0 THEN 'N/A' ELSE (p.height)::text END as height,
            CASE WHEN p.weight = 0 THEN 'N/A' ELSE (p.weight)::text END as weight,
            TO_CHAR(p.birthdate, 'YYYY-MM-DD') as birthdate,
            n.nationality
        FROM
            "player_data" as p
        INNER JOIN
            "nationality" as n
        ON
            n.nationality_id = p.nationality_id
        WHERE
            p.player_id = '{playerId}'
    '''
    player_df = getDataFrameFromDB(sql)
    player_df.index = player_df.index + 1
    player_df = player_df.sort_index()
    json_data = player_df.to_json(orient='records')
    return loads(json_data)

#########################
# Returns statistics for the given league, team, and position
# If all parameters = -1, return all data
# If leagueId is provided, but teamId is -1, return all data for a given league
# If positionId is provided, filter by position
#########################
@hosting.route("/api/v1.0/player_stats/<leagueId>/<teamId>/<positionId>")
def getPlayerStats(leagueId, teamId, positionId):
    sql = '''
        SELECT
            pd.player_id,
            pd.player_name,
            t.team,
            p.position,
            pd.goals,
            pd.assists,
            pd.yellow_cards,
            pd.red_cards,
            pd.shots,
            pd.shots_on_goal,
            pd.saves,
            pd.clean_sheets,
            pd.goals_against
        FROM
            "player_data" as pd
        INNER JOIN
            "team" as t
        ON
            t.team_id = pd.team_id
        INNER JOIN
            "position" as p
        ON
            p.position_id = pd.position_id
        INNER JOIN
            "league" as l
        ON
            l.league_id = t.league_id
    '''
    # if one of the filters is specified, need a 'where' clause
    if (leagueId != '-1') or (teamId != '-1') or (positionId != '-1'):
        conditionAdded = False
        sql += 'WHERE '

        # all teams for a specified league
        if (leagueId != '-1') and (teamId == '-1'):
            conditionAdded = True
            sql += f" t.league_id = '{leagueId}'"
        
        # specific team selected
        if (teamId != '-1'):
            conditionAdded = True
            sql += f" pd.team_id = '{teamId}'"

        # specific position selected
        if (positionId != '-1'):
            if (conditionAdded == True):
                sql += " AND "
            sql += f" pd.position_id = '{positionId}'"

    sql += '''
        ORDER BY
            l.league,
            t.team,
            pd.player_name
    '''
    
    player_stats_df = getDataFrameFromDB(sql)
    player_stats_df.index = player_stats_df.index + 1
    player_stats_df = player_stats_df.sort_index()
    json_data = player_stats_df.to_json(orient='records')
    return loads(json_data)


if __name__ == '__main__':
    hosting.run(port=8000, debug=True)