import fastf1
import fastf1.events
import pandas as pd
from datetime import datetime
from fastf1.ergast import Ergast

ergast = Ergast()

fastf1.Cache.enable_cache('./cache')
pd.set_option('display.max_columns', None)

def getConstructorStandings(year):
    response = ergast.get_constructor_standings(season=year)
    standings = response.content[0]
    selected_columns = ['positionText', 'points', 'wins', 'constructorName', 'constructorNationality']
    standings = standings[selected_columns]
    return standings

def getDriverStandings(year):
    response = ergast.get_driver_standings(season=year)
    standings = response.content[0]
    standings['driverName'] = standings['givenName'] + ' ' + standings['familyName']
    selected_columns = ['position','points', 'wins', 'driverCode', 'driverName', 'driverNumber', 'constructorIds']
    standings = standings[selected_columns]
    return standings

def getDriverInfoByGP(year: int, gp: str, session: str, id: str):
    session = loadSession(year, gp, session)
    driver = session.get_driver(id)  # example: "VER"
    selected_columns = ['FullName','Abbreviation','DriverNumber','TeamName','CountryCode','Status','Position','Points']
    return driver[selected_columns].to_frame().T  

def getRemainingGP():
    with fastf1.Cache.disabled():
        remaining = fastf1.get_events_remaining(dt= datetime.now(), include_testing=False, backend=None, force_ergast=False)
        selected_columns = ['EventName', 'Location', 'Session5DateUtc']
        return remaining[selected_columns]
     
def getGPInfoByName(gp,year):
    with fastf1.Cache.disabled():
        schedule = fastf1.events.get_event_schedule(year)
        event = schedule.get_event_by_name(gp)
        selected = event[['EventName', 'Location','RoundNumber',  'Session5DateUtc']]
        return selected
        
def getGPSessionResult(year, gp, session):
    session = loadSession(year, gp, session)
    results = session.results[['Abbreviation', 'Points', 'GridPosition', 'Status']]
    print (results)
    return results



def getSchedule(year):
    with fastf1.Cache.disabled():
        schedule = fastf1.events.get_event_schedule(year)
        schedule = schedule[schedule['RoundNumber'] != 0]
        selected_columns = schedule[[ 'RoundNumber','EventName','Country','Session5DateUtc']]
        return selected_columns
        
def loadSession(year,gp,session):
     with fastf1.Cache.disabled():
        session = fastf1.get_session(year, gp,session) #GP has a list of words to identify which it is, session has to be one of Q(qualy),R(race),FP1/2/3(free practice)
        session.load()
        return session

        
