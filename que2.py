
from flask import Flask, jsonify, request
import json
weather_data = {
    'San Francisco': {'temperature': 14, 'weather': 'Cloudy'},
    'New York': {'temperature': 20, 'weather': 'Sunny'},
    'Los Angeles': {'temperature': 24, 'weather': 'Sunny'},
    'Seattle': {'temperature': 10, 'weather': 'Rainy'},
    'Austin': {'temperature': 32, 'weather': 'Hot'},
}



def create_app():
   app = Flask(__name__)
   
   #create route
   @app.route('/weather/create',methods=['POST'])
   def create_weather_data():
      data = request.json
      city_name = data.get('city_name')
      temperature = data.get('temperature')
      weather = data.get('weather')
      if city_name is None or temperature is None or weather is None:
         return jsonify({'msg':"Please provide all the fields!"}),400
      if weather not in ['Cloudy', 'Sunny', 'Rainy', 'Hot']:
         return jsonify({'msg':'Incorrect weather!'}),400
      if not isinstance(temperature,(float,int)):
         return ({'msg':"Incorrect Temperature format!"}),400
      if city_name in weather_data:
         return jsonify({'msg':"City data already exists!"}),400
      
      weather_data[city_name] = {'temperature':temperature,'weather':weather}
      return jsonify({'msg': 'City data created successfully'}),201
   

   #update route
   @app.route("/weather/update/<string:city>",methods=['PATCH'])
   def update_weather_data(city):
      data = request.json
      new_temp = data.get('temperature')
      new_weather = data.get('weather')

      if new_temp is not None:
         if not isinstance(new_temp,(float,int)):
            return ({'msg':"Incorrect Temperature format!"}),400
         weather_data[city]['temperature'] = new_temp
      if new_weather is not None:
         if new_weather not in ['Cloudy', 'Sunny', 'Rainy', 'Hot']:
            return jsonify({'msg':'Incorrect weather!'}),400
         weather_data[city]['weather'] = new_temp
      return jsonify({'msg':'Data updated successfully!'}),200

   # delete route
   @app.route('/weather/delete/<string:city>',methods=['DELETE'])
   def delete_weather_data(city):
      print('city is :',city)
      if city not in weather_data:
         return jsonify({'msg':"City doesn't exist!"}),404
      del weather_data[city]
      return jsonify({'msg':"City data deleted!"}),200


   # read route
   @app.route("/weather",methods=['GET'])
   def read_weather_data():
      return jsonify(weather_data),200

   return app



