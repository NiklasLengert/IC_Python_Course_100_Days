import requests
from bs4 import BeautifulSoup
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Test with Bulbasaur
url = "https://pokemondb.net/pokedex/bulbasaur"

try:
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })
    
    response = session.get(url)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    print("=== LOOKING FOR STATS TABLE ===")
    
    # Method 1: Look for "Base stats" header
    base_stats_header = soup.find('h2', string='Base stats')
    if base_stats_header:
        print("Found 'Base stats' header")
        stats_table = base_stats_header.find_next('table')
        if stats_table:
            print("Found table after 'Base stats' header")
            print("Table classes:", stats_table.get('class'))
            rows = stats_table.find_all('tr')
            print(f"Number of rows: {len(rows)}")
            
            for i, row in enumerate(rows):
                cells = row.find_all(['th', 'td'])
                if len(cells) >= 2:
                    print(f"Row {i}: {cells[0].get_text(strip=True)} = {cells[1].get_text(strip=True)}")
    else:
        print("No 'Base stats' header found")
    
    # Method 2: Look for any table with "HP"
    print("\n=== LOOKING FOR TABLES WITH HP ===")
    all_tables = soup.find_all('table')
    print(f"Found {len(all_tables)} tables total")
    
    for i, table in enumerate(all_tables):
        if 'HP' in table.get_text():
            print(f"\nTable {i} contains 'HP':")
            print("Table classes:", table.get('class'))
            rows = table.find_all('tr')
            for j, row in enumerate(rows[:10]):  # First 10 rows
                cells = row.find_all(['th', 'td'])
                if len(cells) >= 2:
                    print(f"  Row {j}: {cells[0].get_text(strip=True)} | {cells[1].get_text(strip=True)}")
    
    print("\n=== LOOKING FOR 'vitals-table' CLASS ===")
    vitals_table = soup.find('table', class_='vitals-table')
    if vitals_table:
        print("Found vitals-table")
        rows = vitals_table.find_all('tr')
        for i, row in enumerate(rows):
            cells = row.find_all(['th', 'td'])
            if len(cells) >= 2:
                print(f"Row {i}: {cells[0].get_text(strip=True)} = {cells[1].get_text(strip=True)}")
    else:
        print("No vitals-table found")

except Exception as e:
    print(f"Error: {e}")
