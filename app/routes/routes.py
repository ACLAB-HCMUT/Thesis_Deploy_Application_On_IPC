from flask import jsonify, request
from app.controllers.controllers import get_all_data, get_data_by_field

def init_routes(app):
    
    @app.route('/ping', methods=['GET'])
    def ping():
        return jsonify({"message": "Server is running"}), 200

    @app.route('/api/data', methods=['GET'])
    def fetch_all_data():
        try:
            data = get_all_data()
            return jsonify(data), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/api/data/<field>/<value>', methods=['GET'])
    def fetch_data_by_field(field, value):
        try:
            data = get_data_by_field(field, value)
            if data:
                return jsonify(data), 200
            else:
                return jsonify({"message": "No data found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500
