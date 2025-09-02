from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import os

app = Flask(__name__)

# Connect to Database
db_path = os.path.join(os.path.dirname(__file__), 'instance', 'cafes.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
db = SQLAlchemy(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    __tablename__ = 'cafe'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)
    
    def to_dict(self):
        """Convert cafe object to dictionary for JSON serialization"""
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


# HTTP GET - Read Record
@app.route('/random', methods=['GET'])
def random_cafe():
    cafe = Cafe.query.order_by(func.random()).first()
    if cafe:
        return jsonify(cafe.to_dict())
    else:
        return jsonify({"error": "No cafes found"}), 404

@app.route('/debug', methods=['GET'])
def debug_info():
    db_path = app.config['SQLALCHEMY_DATABASE_URI']
    cafe_count = Cafe.query.count()
    table_name = Cafe.__tablename__
    actual_db_path = os.path.join(os.path.dirname(__file__), 'instance', 'cafes.db')
    return jsonify({
        "database_uri": db_path,
        "actual_db_path": actual_db_path,
        "db_file_exists": os.path.exists(actual_db_path),
        "cafe_count": cafe_count,
        "table_name": table_name,
        "instance_path": app.instance_path
    })

@app.route('/all', methods=['GET'])
def all_cafes():
    cafes = Cafe.query.all()
    print(f"DEBUG: Found {len(cafes)} cafes in database")
    print(f"DEBUG: First few cafe names: {[cafe.name for cafe in cafes[:5]]}")
    if cafes:
        return jsonify([cafe.to_dict() for cafe in cafes])
    else:
        return jsonify({"error": "No cafes found"}), 404
    
@app.route('/search', methods=['GET'])
def search_cafes():
    query = request.args.get('query')
    loc = request.args.get('loc')
    
    if query:
        cafes = Cafe.query.filter(Cafe.name.ilike(f'%{query}%')).all()
        if cafes:
            return jsonify([cafe.to_dict() for cafe in cafes])
    
    if loc:
        cafes = Cafe.query.filter(Cafe.location.ilike(f'%{loc}%')).all()
        if cafes:
            return jsonify([cafe.to_dict() for cafe in cafes])
    
    return jsonify({"error": "No cafes found"}), 404

# HTTP POST - Create Record
@app.route('/add', methods=['POST'])
def add_cafe():
    new_cafe = Cafe(
        name=request.json.get("name"),
        map_url=request.json.get("map_url"),
        img_url=request.json.get("img_url"),
        location=request.json.get("location"),
        seats=request.json.get("seats"),
        has_toilet=request.json.get("has_toilet"),
        has_wifi=request.json.get("has_wifi"),
        has_sockets=request.json.get("has_sockets"),
        can_take_calls=request.json.get("can_take_calls"),
        coffee_price=request.json.get("coffee_price"),
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(new_cafe.to_dict()), 201

# HTTP PUT/PATCH - Update Record
@app.route('/update-price/<int:cafe_id>', methods=['PATCH', 'GET'])
def update_price(cafe_id):
    try:
        cafe = db.session.execute(db.select(Cafe).where(Cafe.id == cafe_id)).scalar_one_or_none()
        
        if cafe is None:
            return jsonify({"error": "Cafe not found"}), 404
        
        new_price = request.args.get('new_price')
        
        if new_price is None:
            return jsonify({"error": "Missing required parameter: new_price"}), 400
        
        cafe.coffee_price = new_price
        db.session.commit()
        
        return jsonify({
            "success": "Successfully updated the price.",
            "cafe": cafe.to_dict()
        }), 200
        
    except AttributeError:
        return jsonify({"error": "Cafe not found"}), 404
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# HTTP DELETE - Delete Record
@app.route('/report-closed/<int:cafe_id>', methods=['DELETE'])
def delete_cafe(cafe_id):
    try:
        cafe = Cafe.query.get(cafe_id)
        
        if cafe is None:
            return jsonify({"error": "Cafe not found"}), 404
        
        cafe_name = cafe.name
        
        db.session.delete(cafe)
        db.session.commit()
        
        return jsonify({
            "success": f"Successfully deleted {cafe_name}."
        }), 200
        
    except AttributeError:
        return jsonify({"error": "Cafe not found"}), 404
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True)
