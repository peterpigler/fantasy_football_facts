import pandas as pd

import json
import sqlalchemy
import glob, os



def get_list_from_Table(key,dict):
    temp_list=[]
    for player in dict:
        try:
            for row in player[key]:
                try:
                    if 'TM' in row['team']:
                        break
                except KeyError:
                    pass
                row['player_id'] = player['player_id']
                if key=='scoring':
                    try:
                        del row['av']
                    except:
                        pass
                temp_list.append(row)
        except KeyError:
            continue

    return temp_list

def get_list_from_Fantasy_Table(key,dict):
    temp_list=[]
    for player in dict:
        try:
            for row in player[key]:
                row['player_id'] = player['player_id']

                temp_list.append(row)
        except KeyError:
            continue

    return temp_list
def transform_metric(metric):
    return float(metric.replace('-','.'));

def push_player_information_to_Db(mysource):
    playerdict = json.load(open(mysource))
    Player_Information_Pool = pd.DataFrame(playerdict)
    Player_Information = Player_Information_Pool[
        ['player_id', 'name', 'nick_name', 'full_name', 'position', 'height', 'weight', 'team', 'birth_date',
         'birth_place', 'university', 'weighted_career_AV', 'draft_team', 'draft_class', 'salary', 'picture_URL']]
    engine = sqlalchemy.create_engine()
    Player_Information.to_sql(con=engine, name='player_information', if_exists='append', index=False)


def push_table_to_Db(mysource):
    playerdict = json.load(open(mysource))

    receiving_and_rushing = pd.DataFrame(get_list_from_Table('receiving_and_rushing', playerdict))
    receiving_and_rushing_playoffs = pd.DataFrame(get_list_from_Table('receiving_and_rushing_playoffs', playerdict))
    returns = pd.DataFrame(get_list_from_Table('returns', playerdict))
    scoring_playoffs = pd.DataFrame(get_list_from_Table('scoring_playoffs', playerdict))
    scoring = pd.DataFrame(get_list_from_Table('scoring', playerdict))
    defense = pd.DataFrame(get_list_from_Table('defense', playerdict))
    rushing_and_receiving = pd.DataFrame(get_list_from_Table('rushing_and_receiving', playerdict))
    rushing_and_receiving_playoffs = pd.DataFrame(get_list_from_Table('rushing_and_receiving_playoffs', playerdict))
    kicking = pd.DataFrame(get_list_from_Table('kicking', playerdict))
    passing = pd.DataFrame(get_list_from_Table('passing', playerdict))
    Fantasy = pd.DataFrame(get_list_from_Fantasy_Table('fantasy', playerdict))


    receiving_and_rushing.to_sql(con=engine, name=' receiving_and_rushing', if_exists='append', index=False)
    receiving_and_rushing_playoffs.to_sql(con=engine, name='receiving_and_rushing_playoffs', if_exists='append', index=False)
    returns.to_sql(con=engine, name='returns', if_exists='append', index=False)
    scoring_playoffs.to_sql(con=engine, name='scoring_playoffs', if_exists='append', index=False)
    scoring.to_sql(con=engine, name='scoring', if_exists='append', index=False)
    defense.to_sql(con=engine, name='defense', if_exists='append', index=False)
    rushing_and_receiving.to_sql(con=engine, name=' rushing_and_receiving', if_exists='append', index=False)
    rushing_and_receiving_playoffs.to_sql(con=engine, name='rushing_and_receiving_playoffs', if_exists='append', index=False)
    kicking.to_sql(con=engine, name='kicking', if_exists='append', index=False)
    passing.to_sql(con=engine, name='passing', if_exists='append', index=False)
    Fantasy.to_sql(con=engine, name='fantasy', if_exists='append', index=False)

playerdict = json.load(open('2017_all_player_A.txt'))

Player_Information_Pool=pd.DataFrame(playerdict)

engine = sqlalchemy.create_engine()


for file in glob.glob("2017_all_player_*.txt"):
    push_player_information_to_Db(file)
    push_table_to_Db(file)
    print(file)
