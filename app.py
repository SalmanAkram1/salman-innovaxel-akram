from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import random
import string
import validators
from sqlalchemy import inspect

# Initialize Flask app and SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'  # Using SQLite for simplicity
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Define the URL model
class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(500), nullable=False)
    short_code = db.Column(db.String(6), unique=True, nullable=False)
    access_count = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"<URL {self.short_code}>"

# Before each request, ensure the tables are created
@app.before_request
def create_tables():
    """Ensure that tables are created before each request"""
    print("Checking/Creating tables before the request...")
    # Use the inspect method to check if the table exists
    inspector = inspect(db.engine)
    if 'url' not in inspector.get_table_names():
        db.create_all()

# Home route (for the root URL "/")
@app.route("/")
def home():
    return jsonify({"message": "Welcome to the URL Shortener API!"})

# Favicon route (to avoid 404 for favicon.ico)
@app.route('/favicon.ico')
def favicon():
    return '', 204  # 204 No Content

# Create Short URL (POST)
@app.route("/shorten", methods=["POST"])
def shorten_url():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Invalid JSON format"}), 400
        
        original_url = data.get("url")
        
        # Validate the URL
        if not original_url or not validators.url(original_url):
            return jsonify({"error": "Invalid URL"}), 400

        # Generate a random short code
        short_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        new_url = URL(url=original_url, short_code=short_code)

        db.session.add(new_url)
        db.session.commit()

        return jsonify({
            "id": new_url.id,
            "url": new_url.url,
            "shortCode": new_url.short_code
        }), 201
    except Exception as e:
        print(f"Error in shorten_url: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Retrieve Original URL (GET)
@app.route("/shorten/<short_code>", methods=["GET"])
def get_url(short_code):
    try:
        url_data = URL.query.filter_by(short_code=short_code).first()
        if url_data:
            url_data.access_count += 1  # Increment access count
            db.session.commit()
            return jsonify({
                "id": url_data.id,
                "url": url_data.url,
                "shortCode": url_data.short_code,
                "accessCount": url_data.access_count
            }), 200
        return jsonify({"error": "URL not found"}), 404
    except Exception as e:
        print(f"Error in get_url: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Update Short URL (PUT)
@app.route("/shorten/<short_code>", methods=["PUT"])
def update_url(short_code):
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Invalid JSON format"}), 400

        new_url = data.get("url")
        
        # Validate the URL
        if not new_url or not validators.url(new_url):
            return jsonify({"error": "Invalid URL"}), 400

        url_data = URL.query.filter_by(short_code=short_code).first()
        if not url_data:
            return jsonify({"error": "URL not found"}), 404

        # Update the URL
        url_data.url = new_url
        db.session.commit()

        return jsonify({
            "id": url_data.id,
            "url": url_data.url,
            "shortCode": url_data.short_code
        }), 200
    except Exception as e:
        print(f"Error in update_url: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Delete Short URL (DELETE)
@app.route("/shorten/<short_code>", methods=["DELETE"])
def delete_url(short_code):
    try:
        url_data = URL.query.filter_by(short_code=short_code).first()
        if url_data:
            db.session.delete(url_data)
            db.session.commit()
            return '', 204  # No content response for successful delete
        return jsonify({"error": "URL not found"}), 404
    except Exception as e:
        print(f"Error in delete_url: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Get URL Statistics (GET)
@app.route("/shorten/<short_code>/stats", methods=["GET"])
def get_statistics(short_code):
    try:
        url_data = URL.query.filter_by(short_code=short_code).first()
        if url_data:
            return jsonify({
                "id": url_data.id,
                "url": url_data.url,
                "shortCode": url_data.short_code,
                "accessCount": url_data.access_count
            }), 200
        return jsonify({"error": "URL not found"}), 404
    except Exception as e:
        print(f"Error in get_statistics: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
