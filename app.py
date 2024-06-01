from extract_weather_data import get_coordinates, get_weather, unity_transform, create_weather_index, insert_weather_data
from extract_directions_data import get_directions, get_gmaps
from geopy.geocoders import Nominatim
import streamlit as st
import pandas as pd
import sqlite3

def get_weather_data_from_db(db_path):
    # Conectar ao banco de dados
    conn = sqlite3.connect("database/desafio_escola_dnc.db")
    query = "SELECT * FROM tbl_weather;"
    df_weather = pd.read_sql_query(query, conn)
    conn.close()
    
    return df_weather

weather_city_text = st.text_area("Dados de clima\nInsira a cidade")
weather_country_text = st.text_area("Insira o país")
directions_origin_text = st.text_area("Dados da rota\nInsira a origem da rota")
directions_destination_text = st.text_area("Insira o destino da rota")
directions_mode_selectbox = st.selectbox("Escolha o modo de viagem",
                                         ("driving", "walking", "bicycling", "transit")
                                         )

st.button("Confirmar", type="primary")
if st.button("Confirmar", type="primary"):
    if not weather_city_text:
        st.error("O campo 'Dados de clima - Cidade' está vazio.")
    elif not weather_country_text:
        st.error("O campo 'Dados de clima - País' está vazio.")
    elif not directions_origin_text:
        st.error("O campo 'Dados da rota - Origem' está vazio.")
    elif not directions_destination_text:
        st.error("O campo 'Dados da rota - Destino' está vazio.")
    else:
        # Se todos os campos estiverem preenchidos, execute a lógica desejada
        st.success("Todos os campos foram preenchidos corretamente.")
        try:
            coordinates = get_coordinates(weather_city_text, weather_country_text)

            df = pd.DataFrame(coordinates)
            df_weather = get_weather_data_from_db("database/desafio_escola_dnc.db")
            if weather_city_text in in df_weather['city'].values:
            
                df_cidade_usuario = df_weather[df_weather['city'] == weather_city_text]
                st.warning('A cidade já existe. ', icon="⚠️")
            
            df = create_weather_index(df)

            df_weather = df.apply(lambda x: get_weather(x), axis=1)
            df = pd.concat([df, pd.json_normalize(df_weather)], axis=1)

            df = unity_transform(df)

            insert_weather_data(df)

            directions = get_directions(directions_origin_text, directions_destination_text, directions_mode_selectbox)
            st.write("Direções:")
            st.write(directions)
        except Exception as e:
            st.error(f"Erro ao obter direções: {e}")

def verifica_cidade(lat, long, cidade, pais):
    geolocator = Nominatim(user_agent="DesafioEscolaDNC")
    location = geolocator.reverse((lat, long))
    address = location.raw['address']
    
    if cidade.lower() in address.get('city', '').lower() and pais.lower() in address.get('country', '').lower():
        return True
    else:
        return False

# Exemplo de uso
latitude = 40.7128
longitude = -74.0060
cidade = "New York"
pais = "United States"
resultado = verifica_cidade(latitude, longitude, cidade, pais)
if resultado:
    pass
else:
    pass