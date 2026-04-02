import pandas as pd
import streamlit as st
from sqlalchemy import create_engine

# Credenciales de Alwaysdata
usuario = "lurtork_public"
contraseña = "MimbryPaco180493"
host = "mysql-lurtork.alwaysdata.net"
puerto = "3306"
base_datos = "lurtork_portfolio"

# Crear motor de conexión
engine = create_engine(f"mysql+pymysql://{usuario}:{contraseña}@{host}:{puerto}/{base_datos}")

# Cargar datos desde la tabla
@st.cache_data
def load_data():
    query = "SELECT country, continent, year, lifeExp, pop, gdpPercap FROM datacountriestest"
    return pd.read_sql(query, engine)

df = load_data()

# --- Streamlit UI ---
st.title("📊 Datos de Países (AlwaysData)")

st.write("Tabla original:")
st.dataframe(df)

# Filtros interactivos
continent_filter = st.selectbox("Selecciona continente:", df["continent"].unique())
year_filter = st.slider("Selecciona año:", int(df["year"].min()), int(df["year"].max()))

filtered_df = df[(df["continent"] == continent_filter) & (df["year"] == year_filter)]

st.write(f"Datos filtrados para {continent_filter} en {year_filter}:")
st.dataframe(filtered_df)

# Gráfico de expectativa de vida vs PIB per cápita
st.write("Relación entre expectativa de vida y PIB per cápita:")
st.scatter_chart(filtered_df, x="gdpPercap", y="lifeExp", size="pop", color="country")