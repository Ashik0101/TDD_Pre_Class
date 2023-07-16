import pytest
from flask import Flask,jsonify,request

weather_data = {
    'San Francisco': {'temperature': 14, 'weather': 'Cloudy'},
    'New York': {'temperature': 20, 'weather': 'Sunny'},
    'Los Angeles': {'temperature': 24, 'weather': 'Sunny'},
    'Seattle': {'temperature': 10, 'weather': 'Rainy'},
    'Austin': {'temperature': 32, 'weather': 'Hot'},
}


def create_app():
    app = Flask(__name__)
    
    @app.route("/weather/<string:city>",methods=['GET'])
    def get_city_data(city):
        if city in weather_data:
            return jsonify(weather_data[city]),200
        else:
            return jsonify({'msg':'Invalid city name!'}),400
    return app



# define a fixture for creating an instance of our flask app
@pytest.fixture
def app():
    return create_app()

# define a fixture for creating a test client
@pytest.fixture
def client(app):
    return app.test_client()

def test_get_city_data(client):
    response = client.get("/weather/Delhi")
    assert response.status_code == 400
    assert response.json == {'msg':'Invalid city name!'}
