import pandas as pd
import requests
from datetime import datetime

def fetch_space_data():
    try:
        spacex_url = "https://api.spacexdata.com/v4/launches"
        response = requests.get(spacex_url)
        
        if response.status_code == 200:
            spacex_data = response.json()
            return process_spacex_data(spacex_data)
        else:
            return None
            
    except Exception as e:
        return None

def process_spacex_data(data):
    missions = []
    
    for launch in data:
        if launch.get('date_utc'):
            try:
                date = datetime.fromisoformat(launch['date_utc'].replace('Z', '+00:00'))
                year = date.year
                
                if year >= 2006:
                    mission = {
                        'Mission': launch.get('name', 'Unknown'),
                        'Year': year,
                        'Country': 'USA',
                        'Type': determine_mission_type(launch),
                        'Status': 'Success' if launch.get('success', False) else 'Failure',
                        'Budget_Million_USD': 62
                    }
                    missions.append(mission)
            except:
                continue
    
    return pd.DataFrame(missions)

def determine_mission_type(launch):
    name = launch.get('name', '').lower()
    
    if 'crew' in name or 'dragon' in name:
        return 'Human'
    elif 'starlink' in name:
        return 'Satellite'
    elif 'cargo' in name or 'supply' in name:
        return 'Space Station'
    else:
        return 'Satellite'

if __name__ == "__main__":
    data = fetch_space_data()
    if data is not None:
        data.to_csv('spacex_missions.csv', index=False)
