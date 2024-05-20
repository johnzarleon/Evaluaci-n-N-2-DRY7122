import requests
from geopy.geocoders import Nominatim

# Configuración
API_KEY = 'f054c94d-7010-4f4e-991f-f29526a78497'
BASE_URL = 'https://graphhopper.com/api/1/route'
geolocator = Nominatim(user_agent="route_planner")

# Función para obtener coordenadas geográficas de una ciudad
def obtener_coordenadas(ciudad):
    location = geolocator.geocode(ciudad)
    if location:
        return (location.latitude, location.longitude)
    else:
        return None

# Función para obtener la ruta entre dos puntos geográficos
def obtener_ruta(coordenadas_origen, coordenadas_destino):
    parametros = {
        'point': [f"{coordenadas_origen[0]},{coordenadas_origen[1]}", f"{coordenadas_destino[0]},{coordenadas_destino[1]}"],
        'vehicle': 'car',
        'locale': 'es',
        'instructions': 'true',
        'calc_points': 'true',
        'key': API_KEY
    }
    respuesta = requests.get(BASE_URL, params=parametros)
    datos = respuesta.json()
    return datos

# Función principal
def main():
    while True:
        ciudad_origen = input("Ciudad de Origen: ")
        if ciudad_origen.lower() == 'q':
            break
        ciudad_destino = input("Ciudad de Destino: ")
        if ciudad_destino.lower() == 'q':
            break

        coordenadas_origen = obtener_coordenadas(ciudad_origen)
        coordenadas_destino = obtener_coordenadas(ciudad_destino)
        
        if not coordenadas_origen or not coordenadas_destino:
            print("No se pudieron obtener las coordenadas de las ciudades. Verifique los nombres ingresados.")
            continue
        
        ruta = obtener_ruta(coordenadas_origen, coordenadas_destino)
        if 'paths' in ruta and ruta['paths']:
            path = ruta['paths'][0]
            distancia_km = path['distance'] / 1000  # Convertir de metros a kilómetros
            duracion_segundos = path['time'] / 1000  # Convertir de milisegundos a segundos
            duracion_horas = int(duracion_segundos // 3600)
            duracion_minutos = int((duracion_segundos % 3600) // 60)
            duracion_segundos = int(duracion_segundos % 60)
            consumo_combustible = distancia_km * 0.1  # Ejemplo: 10 km/l

            print(f"Distancia: {distancia_km:.2f} km")
            print(f"Duración: {duracion_horas} horas, {duracion_minutos} minutos, {duracion_segundos} segundos")
            print(f"Combustible requerido: {consumo_combustible:.2f} litros")
            print("Narrativa del viaje:")
            for instruccion in path['instructions']:
                print(f"- {instruccion['text']}")
        else:
            print("No se pudo calcular la ruta. Verifique las ciudades ingresadas.")

if __name__ == "__main__":
    main()
