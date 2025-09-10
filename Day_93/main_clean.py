from flask import Flask, render_template, request, jsonify, send_file, flash, redirect, url_for
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import time
import os
from urllib.parse import urljoin, urlparse
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import re

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'pokemon-scraper-secret')

class PokemonScraper:
    def __init__(self):
        self.base_url = "https://pokemondb.net"
        self.pokemon_data = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
    def get_pokemon_list(self, limit=151):
        url = f"{self.base_url}/pokedex/national"
        
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            pokemon_links = []
            pokemon_entries = soup.find_all('span', class_='infocard-lg-data')
            
            for entry in pokemon_entries[:limit]:
                link_element = entry.find('a', class_='ent-name')
                if link_element:
                    pokemon_url = urljoin(self.base_url, link_element['href'])
                    pokemon_name = link_element.text.strip()
                    number_element = entry.find('small')
                    pokemon_number = number_element.text.strip() if number_element else "Unknown"
                    
                    pokemon_links.append({
                        'name': pokemon_name,
                        'number': pokemon_number,
                        'url': pokemon_url
                    })
            
            return pokemon_links[:limit]
            
        except Exception as e:
            return []
    
    def scrape_pokemon_details(self, pokemon_info):
        try:
            response = self.session.get(pokemon_info['url'], timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            data = {
                'number': self.extract_number(pokemon_info['number']),
                'name': pokemon_info['name'],
                'url': pokemon_info['url']
            }
            
            data.update(self.extract_basic_info(soup))
            data.update(self.extract_stats(soup))
            data.update(self.extract_type_info(soup))
            data.update(self.extract_abilities(soup))
            data.update(self.extract_physical_data(soup))
            data.update(self.extract_evolution_info(soup))
            data.update(self.extract_moves_info(soup))
            data.update(self.extract_location_info(soup))
            
            time.sleep(0.5)
            return data
            
        except Exception as e:
            return None
    
    def extract_number(self, number_text):
        numbers = re.findall(r'\d+', str(number_text))
        return int(numbers[0]) if numbers else 0
    
    def extract_basic_info(self, soup):
        data = {}
        
        try:
            data['species'] = soup.find('th', string='Species').find_next('td').text.strip()
        except:
            data['species'] = "Unknown"
        
        try:
            data['generation'] = soup.find('th', string='Generation').find_next('td').text.strip()
        except:
            data['generation'] = "Unknown"
            
        return data
    
    def extract_stats(self, soup):
        stats = {
            'stat_hp': 0,
            'stat_attack': 0,
            'stat_defense': 0,
            'stat_sp_atk': 0,
            'stat_sp_def': 0,
            'stat_speed': 0,
            'stat_total': 0
        }
        
        try:
            base_stats_header = soup.find('h3', string=lambda text: text and 'Base stats' in text)
            if base_stats_header:
                stats_table = base_stats_header.find_next('table', class_='vitals-table')
                if stats_table:
                    rows = stats_table.find_all('tr')
                    for row in rows:
                        th = row.find('th')
                        td = row.find('td')
                        if th and td:
                            stat_name = th.text.strip()
                            stat_value = td.text.strip()
                            
                            try:
                                value = int(stat_value)
                                
                                if stat_name == 'HP':
                                    stats['stat_hp'] = value
                                elif stat_name == 'Attack':
                                    stats['stat_attack'] = value
                                elif stat_name == 'Defense':
                                    stats['stat_defense'] = value
                                elif stat_name == 'Sp. Atk':
                                    stats['stat_sp_atk'] = value
                                elif stat_name == 'Sp. Def':
                                    stats['stat_sp_def'] = value
                                elif stat_name == 'Speed':
                                    stats['stat_speed'] = value
                                elif stat_name == 'Total':
                                    stats['stat_total'] = value
                                    
                            except ValueError:
                                continue
        except:
            pass
            
        return stats
    
    def extract_type_info(self, soup):
        data = {}
        try:
            type_elements = soup.find_all('a', class_='type-icon')
            if type_elements:
                data['type_1'] = type_elements[0].text.strip()
                data['type_2'] = type_elements[1].text.strip() if len(type_elements) > 1 else None
                data['dual_type'] = len(type_elements) > 1
            else:
                data['type_1'] = "Unknown"
                data['type_2'] = None
                data['dual_type'] = False
        except:
            data['type_1'] = "Unknown"
            data['type_2'] = None
            data['dual_type'] = False
        
        return data
    
    def extract_abilities(self, soup):
        data = {}
        abilities = []
        hidden_abilities = []
        
        try:
            abilities_section = soup.find('th', string='Abilities')
            if abilities_section:
                abilities_cell = abilities_section.find_next('td')
                if abilities_cell:
                    ability_links = abilities_cell.find_all('a')
                    for link in ability_links:
                        ability_name = link.text.strip()
                        if '(hidden ability)' in abilities_cell.text:
                            hidden_abilities.append(ability_name)
                        else:
                            abilities.append(ability_name)
        except:
            pass
        
        data['abilities'] = ', '.join(abilities) if abilities else "Unknown"
        data['hidden_abilities'] = ', '.join(hidden_abilities) if hidden_abilities else None
        
        return data
    
    def extract_physical_data(self, soup):
        data = {}
        
        try:
            height_elem = soup.find('th', string='Height').find_next('td')
            height_text = height_elem.text.strip()
            height_match = re.search(r'(\d+\.?\d*)\s*m', height_text)
            data['height_m'] = float(height_match.group(1)) if height_match else 0.0
        except:
            data['height_m'] = 0.0
        
        try:
            weight_elem = soup.find('th', string='Weight').find_next('td')
            weight_text = weight_elem.text.strip()
            weight_match = re.search(r'(\d+\.?\d*)\s*kg', weight_text)
            data['weight_kg'] = float(weight_match.group(1)) if weight_match else 0.0
        except:
            data['weight_kg'] = 0.0
        
        if data['height_m'] > 0:
            data['bmi'] = round(data['weight_kg'] / (data['height_m'] ** 2), 2)
        else:
            data['bmi'] = 0.0
        
        return data
    
    def extract_evolution_info(self, soup):
        data = {}
        
        try:
            evo_chart = soup.find('div', class_='infocard-list-evo')
            if evo_chart:
                evo_links = evo_chart.find_all('a', class_='ent-name')
                evolution_chain = [link.text.strip() for link in evo_links]
                data['evolution_chain'] = ', '.join(evolution_chain)
            else:
                data['evolution_chain'] = "No evolution"
        except:
            data['evolution_chain'] = "Unknown"
        
        return data
    
    def extract_moves_info(self, soup):
        data = {}
        move_count = 0
        
        try:
            moves_section = soup.find('h3', string=lambda text: text and 'Moves learnt by level up' in text)
            if moves_section:
                moves_table = moves_section.find_next('table')
                if moves_table:
                    move_rows = moves_table.find_all('tr')[1:]
                    move_count = len(move_rows)
        except:
            pass
        
        data['total_moves'] = move_count
        return data
    
    def extract_location_info(self, soup):
        data = {}
        
        try:
            location_section = soup.find('h3', string=lambda text: text and 'Where to find' in text)
            if location_section:
                location_data = location_section.find_next('div')
                if location_data:
                    locations = []
                    location_links = location_data.find_all('a')
                    for link in location_links:
                        locations.append(link.text.strip())
                    data['locations'] = ', '.join(locations[:5])
                else:
                    data['locations'] = "Unknown"
            else:
                data['locations'] = "Unknown"
        except:
            data['locations'] = "Unknown"
        
        return data
    
    def scrape_pokemon_batch(self, pokemon_list, max_workers=5):
        self.pokemon_data = []
        completed = 0
        total = len(pokemon_list)
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_pokemon = {
                executor.submit(self.scrape_pokemon_details, pokemon): pokemon 
                for pokemon in pokemon_list
            }
            
            for future in as_completed(future_to_pokemon):
                pokemon_info = future_to_pokemon[future]
                
                try:
                    result = future.result()
                    if result:
                        self.pokemon_data.append(result)
                        completed += 1
                        global scraping_progress
                        scraping_progress['current'] = completed
                        scraping_progress['message'] = f"Scraped: {result['name']} ({completed}/{total})"
                        
                except Exception as exc:
                    pass
        
        scraping_progress['status'] = 'complete'
        scraping_progress['message'] = 'Scraping completed successfully!'
        
        if self.pokemon_data:
            self.save_to_csv('static/pokemon_data.csv')
    
    def save_to_csv(self, filename):
        if not self.pokemon_data:
            return False
        
        try:
            df = pd.DataFrame(self.pokemon_data)
            df.to_csv(filename, index=False)
            return True
        except Exception as e:
            return False

scraper = PokemonScraper()
scraping_progress = {'status': 'idle', 'current': 0, 'total': 0, 'message': ''}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/start_scraping', methods=['POST'])
def start_scraping():
    global scraping_progress
    
    if scraping_progress['status'] == 'scraping':
        return jsonify({'error': 'Scraping already in progress'}), 400
    
    limit = int(request.form.get('limit', 151))
    max_workers = int(request.form.get('max_workers', 5))
    
    def scrape_task():
        global scraping_progress
        scraping_progress = {'status': 'scraping', 'current': 0, 'total': limit, 'message': 'Starting...'}
        
        try:
            pokemon_list = scraper.get_pokemon_list(limit)
            scraping_progress['total'] = len(pokemon_list)
            scraping_progress['message'] = f'Starting to scrape {len(pokemon_list)} Pokemon...'
            
            scraper.scrape_pokemon_batch(pokemon_list, max_workers)
            
        except Exception as e:
            scraping_progress['status'] = 'error'
            scraping_progress['message'] = f'Error: {str(e)}'
    
    thread = threading.Thread(target=scrape_task)
    thread.daemon = True
    thread.start()
    
    return jsonify({'status': 'started', 'message': 'Scraping started successfully'})

@app.route('/progress')
def get_progress():
    return jsonify(scraping_progress)

@app.route('/data')
def view_data():
    if not scraper.pokemon_data:
        flash('No data available. Please run scraping first.', 'warning')
        return redirect(url_for('home'))
    
    return render_template('data.html', pokemon_data=scraper.pokemon_data[:20])

@app.route('/api/pokemon')
def api_pokemon():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))
    search = request.args.get('search', '').lower()
    
    if not scraper.pokemon_data:
        return jsonify({
            'pokemon': [],
            'total': 0,
            'page': page,
            'per_page': per_page,
            'total_pages': 0
        })
    
    filtered_data = scraper.pokemon_data
    if search:
        filtered_data = [
            p for p in scraper.pokemon_data 
            if search in p['name'].lower() or 
               search in str(p['number']) or
               search in p.get('type_1', '').lower() or
               search in p.get('type_2', '').lower()
        ]
    
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    pokemon_page = filtered_data[start_idx:end_idx]
    
    return jsonify({
        'pokemon': pokemon_page,
        'total': len(filtered_data),
        'page': page,
        'per_page': per_page,
        'total_pages': (len(filtered_data) + per_page - 1) // per_page
    })

@app.route('/download')
def download_csv():
    csv_path = 'static/pokemon_data.csv'
    if os.path.exists(csv_path):
        return send_file(csv_path, as_attachment=True, download_name='pokemon_data.csv')
    else:
        flash('No CSV file available. Please run scraping first.', 'error')
        return redirect(url_for('home'))

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    os.makedirs('static', exist_ok=True)
    app.run(debug=True, port=5004)
