import pandas as pd
import streamlit as st
import altair as alt
from sqlalchemy import create_engine

# Credenciales de Alwaysdata
usuario = "lurtork_public"
contraseña = "MimbryPaco180493"
host = "mysql-lurtork.alwaysdata.net"
puerto = "3306"
base_datos = "lurtork_portfolio"

# Se conecta a la base de datos en Alwaysdata
engine = create_engine(f"mysql+pymysql://{usuario}:{contraseña}@{host}:{puerto}/{base_datos}")

# Cargar datos desde la tabla
@st.cache_data
def load_data():
    query = "SELECT country, continent, year, lifeExp, pop, gdpPercap FROM datacountriestest"
    return pd.read_sql(query, engine)

df = load_data()

# Streamlit
st.title("Countries database")

st.write("Original table:")
st.dataframe(df)

# Filtros
opciones_continente = ["All"] + list(df["continent"].unique())
continent_filter = st.selectbox("Select continent:", opciones_continente)
year_filter = st.slider("Select year:", int(df["year"].min()), int(df["year"].max()))

if continent_filter == "All":
    filtered_df = df[df["year"] == year_filter]
else:
    filtered_df = df[(df["continent"] == continent_filter) & (df["year"] == year_filter)]


st.write(f"Filtered data for {continent_filter} in {year_filter}:")
st.dataframe(filtered_df)

# Gráfico de expectativa de vida vs PIB per cápita
st.write("Life expectation and GDP Per Capita relation dashboard")

# Cambios en eje X para dinamismo
max_x = float(filtered_df["gdpPercap"].max()) if not filtered_df.empty else 1000

chart = alt.Chart(filtered_df).mark_circle().encode(
    x=alt.X("gdpPercap:Q", scale=alt.Scale(domain=[0, max_x * 1.05]), title="PIB per cápita"),
    y=alt.Y("lifeExp:Q", scale=alt.Scale(zero=False), title="Expectativa de Vida"),
    size=alt.Size("pop:Q", legend=None),
    color=alt.Color("country:N", legend=None),
    tooltip=["country", "gdpPercap", "lifeExp", "pop"]
).interactive()

st.altair_chart(chart, use_container_width=True)