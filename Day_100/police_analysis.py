import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import warnings
warnings.filterwarnings('ignore')

class PoliceDataAnalyzer:
    def __init__(self):
        self.police_data = None
        self.census_data = None
        
    def load_police_data(self):
        try:
            url = "https://raw.githubusercontent.com/washingtonpost/data-police-shootings/master/v2/fatal-police-shootings-data.csv"
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            from io import StringIO
            self.police_data = pd.read_csv(StringIO(response.text))
            
            self.police_data['date'] = pd.to_datetime(self.police_data['date'])
            self.police_data['year'] = self.police_data['date'].dt.year
            
            return True
        except:
            return False
    
    def create_census_data(self):
        try:
            base_url = "https://api.census.gov/data/2022/acs/acs1"
            
            race_codes = {
                'White': 'B02001_002E',
                'Black': 'B02001_003E', 
                'Asian': 'B02001_005E',
                'Hispanic': 'B03003_003E'
            }
            
            census_rows = []
            
            for race_name, code in race_codes.items():
                url = f"{base_url}?get=NAME,{code}&for=state:*"
                response = requests.get(url, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    rows = data[1:]
                    
                    for row in rows:
                        state_name = row[0]
                        population = int(row[1]) if row[1] and row[1] != 'null' else 0
                        
                        if population > 0:
                            census_rows.append({
                                'state': state_name,
                                'race': race_name,
                                'population': population
                            })
            
            if census_rows:
                self.census_data = pd.DataFrame(census_rows)
                return True
            return False
                
        except:
            return False
    
    def analyze_by_race(self):
        race_mapping = {
            'W': 'White',
            'B': 'Black', 
            'H': 'Hispanic',
            'A': 'Asian',
            'N': 'Native American',
            'O': 'Other'
        }
        
        self.police_data['race_mapped'] = self.police_data['race'].map(race_mapping)
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        
        race_counts = self.police_data['race_mapped'].value_counts()
        ax1.bar(race_counts.index, race_counts.values, color='darkred', alpha=0.7)
        ax1.set_title('Police Fatalities by Race')
        ax1.tick_params(axis='x', rotation=45)
        
        yearly_trends = self.police_data.groupby(['year', 'race_mapped']).size().unstack(fill_value=0)
        yearly_trends.plot(kind='line', ax=ax2, marker='o')
        ax2.set_title('Yearly Trends by Race')
        ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        age_race = self.police_data.groupby('race_mapped')['age'].mean()
        ax3.bar(age_race.index, age_race.values, color='steelblue', alpha=0.7)
        ax3.set_title('Average Age by Race')
        ax3.tick_params(axis='x', rotation=45)
        
        armed_status = pd.crosstab(self.police_data['race_mapped'], self.police_data['armed_with'])
        armed_status.plot(kind='bar', stacked=True, ax=ax4, alpha=0.8)
        ax4.set_title('Armed Status by Race')
        ax4.tick_params(axis='x', rotation=45)
        ax4.legend(title='Armed Status', bbox_to_anchor=(1.05, 1), loc='upper left')
        
        plt.tight_layout()
        plt.savefig('police_analysis_by_race.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return race_counts

    def analyze_by_state(self):
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        
        state_counts = self.police_data['state'].value_counts().head(15)
        ax1.barh(state_counts.index[::-1], state_counts.values[::-1], color='navy', alpha=0.7)
        ax1.set_title('Top 15 States - Police Fatalities')
        
        monthly_data = self.police_data.groupby(self.police_data['date'].dt.month).size()
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        ax2.plot(months, monthly_data.values, marker='o', color='red', linewidth=2)
        ax2.set_title('Monthly Distribution')
        ax2.tick_params(axis='x', rotation=45)
        
        yearly_total = self.police_data.groupby('year').size()
        ax3.plot(yearly_total.index, yearly_total.values, marker='s', color='green', linewidth=2)
        ax3.set_title('Yearly Totals')
        ax3.grid(True, alpha=0.3)
        
        threat_level = self.police_data['threat_type'].value_counts()
        ax4.pie(threat_level.values, labels=threat_level.index, autopct='%1.1f%%', startangle=90)
        ax4.set_title('Threat Level Distribution')
        
        plt.tight_layout()
        plt.savefig('police_analysis_by_state.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return state_counts
    
    def create_combined_analysis(self):
        police_by_race = self.police_data['race_mapped'].value_counts()
        
        if self.census_data is None:
            return None
            
        us_population_by_race = self.census_data.groupby('race')['population'].sum().to_dict()
        
        comparison_data = []
        for race in ['White', 'Black', 'Hispanic', 'Asian']:
            if race in police_by_race.index and race in us_population_by_race:
                police_count = police_by_race[race]
                population = us_population_by_race[race]
                rate_per_million = (police_count / population) * 1000000
                
                comparison_data.append({
                    'Race': race,
                    'Police_Fatalities': police_count,
                    'Population': population,
                    'Rate_Per_Million': rate_per_million,
                    'Population_Percentage': (population / sum(us_population_by_race.values())) * 100,
                    'Fatality_Percentage': (police_count / police_by_race.sum()) * 100
                })
        
        comparison_df = pd.DataFrame(comparison_data)
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        x_pos = np.arange(len(comparison_df))
        width = 0.35
        
        ax1.bar(x_pos - width/2, comparison_df['Population_Percentage'], width, 
                label='Population %', alpha=0.7, color='skyblue')
        ax1.bar(x_pos + width/2, comparison_df['Fatality_Percentage'], width, 
                label='Fatality %', alpha=0.7, color='red')
        
        ax1.set_xlabel('Race')
        ax1.set_ylabel('Percentage')
        ax1.set_title('Population vs Police Fatality Percentages')
        ax1.set_xticks(x_pos)
        ax1.set_xticklabels(comparison_df['Race'])
        ax1.legend()
        
        ax2.bar(comparison_df['Race'], comparison_df['Rate_Per_Million'], 
                color=['lightblue', 'darkred', 'orange', 'green'], alpha=0.8)
        ax2.set_ylabel('Rate per Million')
        ax2.set_title('Police Fatality Rate per Million by Race')
        ax2.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig('combined_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return comparison_df
    
    def generate_insights(self):
        total_cases = len(self.police_data)
        date_range = f"{self.police_data['date'].min().strftime('%Y-%m-%d')} to {self.police_data['date'].max().strftime('%Y-%m-%d')}"
        
        race_counts = self.police_data['race_mapped'].value_counts()
        most_affected_race = race_counts.index[0]
        
        armed_percentage = (self.police_data['armed_with'] != 'unarmed').mean() * 100
        avg_age = self.police_data['age'].mean()
        
        top_state_data = self.police_data['state'].value_counts()
        top_state = top_state_data.index[0]
        top_state_count = top_state_data.iloc[0]
        
        return {
            'total_cases': total_cases,
            'date_range': date_range,
            'avg_age': avg_age,
            'armed_percentage': armed_percentage,
            'top_state': top_state,
            'top_state_count': top_state_count,
            'most_affected_race': most_affected_race,
            'race_counts': race_counts
        }
    
    def run_complete_analysis(self):
        if not self.load_police_data():
            return None
            
        self.create_census_data()
        race_counts = self.analyze_by_race()
        insights = self.generate_insights()
        self.analyze_by_state() 
        comparison_df = self.create_combined_analysis()
        
        return {
            'insights': insights,
            'race_counts': race_counts,
            'comparison_df': comparison_df
        }

if __name__ == "__main__":
    analyzer = PoliceDataAnalyzer()
    analyzer.run_complete_analysis()