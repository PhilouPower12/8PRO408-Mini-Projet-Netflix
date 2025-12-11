import numpy as py
import pandas as pd
#import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st

#1: Exploration du dataset
#Aperçu général
#print("\nChargement des données...")
df = pd.read_csv("netflix_titles.csv")
#print("\nAperçu des données:")
#print(df.head())
#print("\nDimension du dataset et types de données")
df.info()
#print("\nValeurs manquantes")
#print(df.isnull().sum())
#print("\nValeurs dupliquées: ", df.duplicated().sum())

#Vérification et nettoyage
#print("\nSuppression des lignes vides...")
Avant = len(df)
df.dropna(inplace=True)
#print(f"{Avant - len(df)} lignes supprimées (NA). Il reste {len(df)} lignes.")
#print("\nSuppression des doublons...")
Avant = len(df)
df.drop_duplicates(inplace=True)
#print(f"{Avant - len(df)} doublons supprimés. Il reste {len(df)} lignes.")
#print("\nConversion des dates...")
df["date_added"] = pd.to_datetime(df["date_added"], errors="coerce")
#print("Conversion terminée. Exemple:")
#print(df["date_added"].head())
#print("\nTypes de données apres nettoyage:")
#print(df.dtypes)

#2: Analyse du contenu
#Film vs séries
#print("\nProportion en pourcentage: ")
type = df["type"].value_counts(normalize=True) * 100
#print(type)
#print("\nTendance par année: ")
df["year_added"] = df["date_added"].dt.year
titles = df.groupby(["year_added", "type"]).size().reset_index(name="count")
#print(titles.head())
#Genres principaux (listed_in)
#print("\nFréquence des genres principaux:")
genres = df["listed_in"].dropna().str.split(", ")
genres_exploded = genres.explode()
genre_counts = genres_exploded.value_counts().head(20)
#print(genre_counts)
#print("\nRépartition géographique:")
countries = df["country"].dropna().str.split(", ")
countries_exploded = countries.explode()
country_counts = countries_exploded.value_counts().head(25)
#print(country_counts)
#print("\nTop des acteurs:")
actors = df["cast"].dropna().str.split(", ")
actors_exploded = actors.explode()
top_actors = actors_exploded.value_counts().head(25)
#print(top_actors)
#print("\nTop des réalisateurs:")
directors = df["director"].dropna().str.split(", ")
directors_exploded = directors.explode()
top_directors = directors_exploded.value_counts().head(25)
#print(top_directors)

#Analyse temporelle
#print("\nStatistique par rapport aux années")
#print(df["release_year"].describe())
#print("\nNombre de titres sorties par année")
titles_added_per_year = df["release_year"].value_counts().sort_index()
#print(titles_added_per_year.head(100))

#Application Streamlit
st.title("Analyse exploratoire du catalogue Netflix")

st.markdown("""
Cette application présente une analyse qui explore un base de donnée du catalogue Netflix:
- Exploration du dataset
- Analyse des contenus
- Analyse temporelle
""")

st.sidebar.title("Navigation")
section = st.sidebar.radio(
    "Se diriger vers:",
    [
        "Exploration du dataset",
        "Analyse des contenus",
        "Analyse temporelle",
    ]
)

if section == "Exploration du dataset":
    st.header("Exploration du dataset")

    st.subheader("Aperçu")
    st.dataframe(df.head(100))

elif section == "Analyse des contenus":
    st.header("Analyse des contenus")

    st.subheader("Top 25 des acteurs")
    st.write(top_actors)

    st.subheader("Top 25 des réalisateurs")
    st.write(top_directors)   

    st.subheader("Films vs Séries")
    st.bar_chart(df["type"].value_counts())

    st.subheader("Genres principaux")
    genres = df["listed_in"].dropna().str.split(", ").explode()
    st.bar_chart(genres.value_counts().head(10))

    st.subheader("Top 10 des pays producteurs")
    countries = df["country"].dropna().str.split(", ").explode()
    fig = px.pie(
        names=countries.value_counts().head(10).index,
        values=countries.value_counts().head(10).values
    )
    st.plotly_chart(fig)

elif section == "Analyse temporelle":
    st.header("Analyse temporelle")

    df["date_added"] = pd.to_datetime(df["date_added"], errors="coerce")
    df["year_added"] = df["date_added"].dt.year

    added_per_year = df["year_added"].value_counts().sort_index()

    st.subheader("Ajouts Netflix par année")
    st.dataframe(added_per_year)

    fig = px.line(
        x=added_per_year.index,
        y=added_per_year.values,
        labels={"x": "Année", "y": "Titres ajoutés"},
        title="Ajouts Netflix par année"
    )
    st.plotly_chart(fig)

    st.subheader("Histogramme des années de sortie")
    fig, ax = plt.subplots()
    sns.histplot(df["release_year"], bins=30, ax=ax)
    st.pyplot(fig)
