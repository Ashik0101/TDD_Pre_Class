import pytest   #import pytest
from que2 import create_app  # import create_app from que2 file

@pytest.fixture
def app():
   return create_app()


@pytest.fixture
def client(app):
   return app.test_client()

def test_create_weather_data(client):
   # test for create weather data
   city_data = {'city_name':'Delhi','temperature':20,'weather':'Cloudy'}
   response = client.post("/weather/create",json=city_data)
   assert response.status_code == 201
   assert response.json == {'msg': 'City data created successfully'}

   # test for already present city data
   city_data = {'city_name':'Seattle','temperature':20,'weather':'Cloudy'}
   response = client.post("/weather/create",json=city_data)
   assert response.status_code == 400
   assert response.json == {'msg':"City data already exists!"}

   # test for missing fields
   city_data = {'city_name':'Punjab','temperature':20}
   response = client.post("/weather/create",json=city_data)
   assert response.status_code == 400
   assert response.json == {'msg':"Please provide all the fields!"}
   
   # check for incorrect temperature type
   city_data = {'city_name':'Mumbai','temperature':'20','weather':'Cloudy'}
   response = client.post("/weather/create",json=city_data)
   assert response.status_code == 400
   assert response.json == {'msg':"Incorrect Temperature format!"}

def test_update_weather_data(client):
   # test for successful update
   city_data = {'temperature':200,'weather':'Hot'}
   response = client.patch("/weather/update/Seattle",json=city_data)
   assert response.status_code == 200
   assert response.json == {'msg':'Data updated successfully!'}

   # test for successful update of only temperature field
   city_data = {'temperature':200}
   response = client.patch("/weather/update/Seattle",json=city_data)
   assert response.status_code == 200
   assert response.json == {'msg':'Data updated successfully!'}

   # test for successful update of only weather field
   city_data = {'weather':"Rainy"}
   response = client.patch("/weather/update/Seattle",json=city_data)
   assert response.status_code == 200
   assert response.json == {'msg':'Data updated successfully!'}

   # test for incorrect format of temperature
   city_data = {'temperature':'200','weather':'Hot'}
   response = client.patch("/weather/update/Seattle",json=city_data)
   assert response.status_code == 400
   assert response.json == {'msg':"Incorrect Temperature format!"}

   # test for incorrect weather condition
   city_data = {'temperature':200,'weather':'Hottttty'}
   response = client.patch("/weather/update/Seattle",json=city_data)
   assert response.status_code == 400
   assert response.json == {'msg':'Incorrect weather!'}


def test_delete_weather_data(client):
   # check for invalid city name
   response = client.delete("/weather/delete/Chennai")
   assert response.status_code == 404
   assert response.json == {'msg':"City doesn't exist!"}

   # check for valid city name
   response = client.delete("/weather/delete/Seattle")
   assert response.status_code == 200
   assert response.json == {'msg':"City data deleted!"}

def test_read_weather_data(client):
   response = client.get("/weather")
   assert response.status_code == 200