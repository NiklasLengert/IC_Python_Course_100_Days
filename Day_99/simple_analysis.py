import pandas as pd
import matplotlib.pyplot as plt
import requests
from datetime import datetime
import os
import warnings
warnings.filterwarnings('ignore')

def fetch_space_data():
    try:
        response = requests.get("https://api.spacexdata.com/v4/launches")
        if response.status_code == 200:
            data = response.json()
            missions = []
            
            for launch in data:
                if launch.get('date_utc'):
                    try:
                        date = datetime.fromisoformat(launch['date_utc'].replace('Z', '+00:00'))
                        year = date.year
                        
                        if year >= 2006:
                            name = launch.get('name', '').lower()
                            if 'crew' in name or 'dragon' in name:
                                mission_type = 'Human'
                            elif 'starlink' in name:
                                mission_type = 'Satellite'
                            elif 'cargo' in name or 'supply' in name:
                                mission_type = 'Space Station'
                            else:
                                mission_type = 'Satellite'
                            
                            mission = {
                                'Mission': launch.get('name', 'Unknown'),
                                'Year': year,
                                'Type': mission_type,
                                'Status': 'Success' if launch.get('success', False) else 'Failure',
                                'Budget_Million_USD': 62
                            }
                            missions.append(mission)
                    except:
                        continue
            
            return pd.DataFrame(missions)
    except:
        return None

class SimpleSpaceAnalysis:
    def __init__(self):
        self.data = None
        
    def load_data(self):
        if os.path.exists('spacex_missions.csv'):
            self.data = pd.read_csv('spacex_missions.csv')
        else:
            self.data = fetch_space_data()
            if self.data is not None:
                self.data.to_csv('spacex_missions.csv', index=False)
        
        if self.data is None or len(self.data) == 0:
            return False
            
        return True
    
    def create_overview_chart(self):
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('SpaceX Mission Analysis', fontsize=16)
        
        yearly_missions = self.data.groupby('Year').size()
        ax1.plot(yearly_missions.index, yearly_missions.values, marker='o')
        ax1.set_title('Missions per Year')
        ax1.grid(True, alpha=0.3)
        
        success_rate = self.data.groupby('Year').apply(lambda x: (x['Status'] == 'Success').mean() * 100)
        ax2.plot(success_rate.index, success_rate.values, marker='s', color='green')
        ax2.set_title('Success Rate')
        ax2.set_ylim(0, 110)
        ax2.grid(True, alpha=0.3)
        
        type_counts = self.data['Type'].value_counts()
        ax3.pie(type_counts.values, labels=type_counts.index, autopct='%1.1f%%')
        ax3.set_title('Mission Types')
        
        cumulative = yearly_missions.cumsum()
        ax4.plot(cumulative.index, cumulative.values, marker='o', color='purple')
        ax4.set_title('Cumulative Missions')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('spacex_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def generate_summary(self):
        total_missions = len(self.data)
        successful_missions = len(self.data[self.data['Status'] == 'Success'])
        success_rate = (successful_missions / total_missions) * 100
        
        total_investment = self.data['Budget_Million_USD'].sum()
        
        print(f"Total Missions: {total_missions}")
        print(f"Success Rate: {success_rate:.1f}%")
        print(f"Investment: ${total_investment:,.0f}M")
        print(f"Period: {self.data['Year'].min()} - {self.data['Year'].max()}")
        
        for mission_type, count in self.data['Type'].value_counts().items():
            percentage = (count / total_missions) * 100
            print(f"{mission_type}: {count} ({percentage:.1f}%)")
    
    def run_analysis(self):
        if not self.load_data():
            return
            
        self.generate_summary()
        self.create_overview_chart()

if __name__ == "__main__":
    analyzer = SimpleSpaceAnalysis()
    analyzer.run_analysis()
