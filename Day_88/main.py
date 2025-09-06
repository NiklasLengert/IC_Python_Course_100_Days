from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Sample cafe data
cafes_data = [
    {
        'id': 1,
        'name': 'Central Perk',
        'map_url': 'https://www.google.com/maps/search/Central+Perk+coffee+New+York+NY',
        'img_url': 'https://images.unsplash.com/photo-1559925393-8be0ec4767c8?w=400',
        'location': 'New York, NY',
        'seats': 20,
        'has_toilet': True,
        'has_wifi': True,
        'has_sockets': True,
        'can_take_calls': True,
        'coffee_price': '$3.50'
    },
    {
        'id': 2,
        'name': 'The Grind Coffee',
        'map_url': 'https://www.google.com/maps/search/The+Grind+Coffee+San+Francisco+CA',
        'img_url': 'https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?w=400',
        'location': 'San Francisco, CA',
        'seats': 35,
        'has_toilet': True,
        'has_wifi': True,
        'has_sockets': True,
        'can_take_calls': False,
        'coffee_price': '$4.00'
    },
    {
        'id': 3,
        'name': 'Laptop Lounge',
        'map_url': 'https://www.google.com/maps/search/Laptop+Lounge+coffee+Austin+TX',
        'img_url': 'https://images.unsplash.com/photo-1445116572660-236099ec97a0?w=400',
        'location': 'Austin, TX',
        'seats': 50,
        'has_toilet': True,
        'has_wifi': True,
        'has_sockets': True,
        'can_take_calls': True,
        'coffee_price': '$2.75'
    },
    {
        'id': 4,
        'name': 'Code & Coffee',
        'map_url': 'https://www.google.com/maps/search/Code+Coffee+cafe+Portland+OR',
        'img_url': 'https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=400',
        'location': 'Portland, OR',
        'seats': 25,
        'has_toilet': False,
        'has_wifi': True,
        'has_sockets': True,
        'can_take_calls': False,
        'coffee_price': '$3.25'
    },
    {
        'id': 5,
        'name': 'Remote Work Hub',
        'map_url': 'https://www.google.com/maps/search/Remote+Work+Hub+cafe+Denver+CO',
        'img_url': 'https://images.unsplash.com/photo-1521017432531-fbd92d768814?w=400',
        'location': 'Denver, CO',
        'seats': 60,
        'has_toilet': True,
        'has_wifi': True,
        'has_sockets': True,
        'can_take_calls': True,
        'coffee_price': '$3.00'
    }
]

@app.route('/')
def home():
    return render_template('index.html', cafes=cafes_data)

@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    if request.method == 'POST':
        new_cafe = {
            'id': len(cafes_data) + 1,
            'name': request.form['name'],
            'map_url': request.form['map_url'],
            'img_url': request.form['img_url'],
            'location': request.form['location'],
            'seats': int(request.form['seats']),
            'has_toilet': 'has_toilet' in request.form,
            'has_wifi': 'has_wifi' in request.form,
            'has_sockets': 'has_sockets' in request.form,
            'can_take_calls': 'can_take_calls' in request.form,
            'coffee_price': request.form['coffee_price']
        }
        cafes_data.append(new_cafe)
        flash('Cafe added successfully!', 'success')
        return redirect(url_for('home'))
    
    return render_template('add_cafe.html')

@app.route('/cafe/<int:cafe_id>')
def cafe_detail(cafe_id):
    cafe = next((c for c in cafes_data if c['id'] == cafe_id), None)
    if not cafe:
        flash('Cafe not found!', 'error')
        return redirect(url_for('home'))
    return render_template('cafe_detail.html', cafe=cafe)

@app.route('/search')
def search():
    query = request.args.get('q', '').lower()
    wifi_required = request.args.get('wifi') == 'on'
    sockets_required = request.args.get('sockets') == 'on'
    calls_allowed = request.args.get('calls') == 'on'
    
    filtered_cafes = []
    
    for cafe in cafes_data:
        if query and query not in cafe['name'].lower() and query not in cafe['location'].lower():
            continue
        if wifi_required and not cafe['has_wifi']:
            continue
        if sockets_required and not cafe['has_sockets']:
            continue
        if calls_allowed and not cafe['can_take_calls']:
            continue
        
        filtered_cafes.append(cafe)
    
    return render_template('search_results.html', cafes=filtered_cafes, query=query)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
