# Importing required functions 
import os
import pandas as pd
import matplotlib
import seaborn as sns
matplotlib.use('Agg')
import matplotlib.pyplot as plt 
from flask import Flask, render_template , request, jsonify, redirect, url_for
import csv
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from datetime import datetime

# Flask constructor 
app = Flask(__name__) 

df = pd.read_csv("London_Air_Quality.csv")
#Formatea el campo fecha por datime, ya que la fuent viene con formato object
df['Date'] = pd.to_datetime(df['Date'])
features = ['CO', 'NO2', 'SO2', 'O3', 'PM2.5','PM10','AQI']

def filtrar_fecha(fecha_inicio, fecha_fin):
	#Filtrar el AQI por un rango de fecha
	#fecha_inicio = '2024-06-01'
	#fecha_fin = '2024-06-30'
	df_filtrado = df[(df['Date'].dt.date >= fecha_inicio) & (df['Date'].dt.date <= fecha_fin)].copy()
	return df_filtrado

def entrenar_modelo(df_filtrado):
	#Agregar una columna del día de las muestras tomadas
	df_filtrado['Date'] = pd.to_datetime(df_filtrado['Date'])
	df_filtrado['Dia'] = df_filtrado['Date'].dt.day

	#Seleccionar el muestreo de los datos para entrenar
	# Seleccionar características relevantes para la predicción
	#features = ['CO', 'NO2', 'SO2', 'O3', 'PM2.5','PM10','AQI']
	X = df_filtrado[features] # Variables independientes
	y = df_filtrado['Dia']   # Variable objetivo

	# Dividir los datos en conjuntos de entrenamiento (80%) y prueba (20%)
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

	#Cramos los modelos
	from sklearn.ensemble import RandomForestRegressor
	model = RandomForestRegressor(n_estimators=100, random_state=42)


	# Entrenar cada modelo
	model.fit(X_train, y_train)  # Entrenar el modelo

	from sklearn.metrics import mean_squared_error, r2_score
	y_pred = model.predict(X_test)  # Hacer predicciones
	rmse = mean_squared_error(y_test, y_pred)  # Error cuadrático medio
	r2 = r2_score(y_test, y_pred)  # Coeficiente de determinación

	return model

def get_plot(model,X_test, y_pred):
	#Graficar Prediccion
	# Get the names of the features
	import matplotlib.pyplot as plt
	features = X_test.columns
	filenames = []
	# Loop through each feature and create a scatter plot
	for feature in features:
		plt.figure(figsize=(8, 6)) # Create a new figure for each plot
		plt.scatter(y_pred, X_test[feature], label="Prediccion")
		plt.legend()
		plt.title(f"Relación entre {feature} en un mes") # Dynamic title
		plt.xlabel('Día') # Dynamic x-axis label
		plt.ylabel(feature)
		# Save the figure in the static directory 
		filename = f'plot_{feature}.png'
		plt.savefig(os.path.join('static', 'images', filename))
		filenames.append(filename)
	return filenames


# Root URL 
@app.get('/')
def single_converter():
	# Filtrar datos por fechas específicas
    fecha_inicio = datetime(2024, 6, 1).date()
    fecha_fin = datetime(2024, 6, 30).date()
    df_filtrado = filtrar_fecha(fecha_inicio, fecha_fin)

    # Entrenar el modelo
    model= entrenar_modelo(df_filtrado)

    # Generar gráficos
    filenames = get_plot(model, df_filtrado[features], model.predict(df_filtrado[features]))

    # Pasar las métricas al template
    return render_template('index.html')

###########  ENTRA AL FORMULARIO
@app.route('/calcular', methods=['GET', 'POST'])
def calcular():
	datos = request.get_json()
	fecha_in = datetime(2024, 5, 1).date()
	fecha_fi = datetime(2024, 5, 30).date()
	#fecha_in = datetime.strftime(datos['fechaIni'], '%Y-%m-%d')
	#fecha_fi = datetime.strptime(datos['fechaFin'], '%Y-%m-%d')
	df_filtrado = filtrar_fecha(fecha_in, fecha_fi)
	model= entrenar_modelo(df_filtrado)
	get_plot(model, df_filtrado[features], model.predict(df_filtrado[features]))
	resultado = 'Con exito'
	return jsonify(prediccion=resultado)
	#return redirect(url_for('index'))
	#return render_template('image_gallery.html', prediccion=resultado)
	#return redirect(url_for('index.html'))
	#convertir las cadenas a objeto datetime
	#try:
	#fecha_in = datetime.strftime(datos['fechaIni'], '%Y-%m-%d').date()
	#fecha_fi = datetime.strptime(datos['fechaFin'], '%Y-%m-%d').date()
	#except ValueError:
	#	return jsonify({'error': 'Fecha no proporcionada'}), 400
	#fechaI = datetime.strptime(fecha_str, '%Y-%m-%d').date()
	#return jsonify({'fecha': fecha.isoformat()})
    #df_filtrado = filtrar_fecha(fecha_in, fecha_fi)

    # Entrenar el modelo
    #model= entrenar_modelo(df_filtrado)

    # Generar gráficos
    #get_plot(model, df_filtrado[features], model.predict(df_filtrado[features]))

@app.after_request
def add_header(response):
    response.cache_control.no_store = True
    return response

# Main Driver Function 
if __name__ == '_main_': 
	# Run the application on the local development server 
	app.run(debug=True)