# On importe les dépendances
import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3

# Definition de couleur HTML
couleur = "color: #1034A6;"
couleur2= "color: blue;"

# Definition titre  Sidebar 1

st.sidebar.markdown("<h1 style='{}'>Descriptives Options</h1>".format(couleur2), unsafe_allow_html=True)

# Definition titre Sidebar 2
st.markdown("<h1 style='{}'>Association Maison des Jeunes</h1>".format(couleur), unsafe_allow_html=True)

# On se connecte à la base de donner pour récupérer la table ass
@st.cache_data
def load_data():
    # Chemin qui mène directement vers la base de données de l'association
    db_chemin = 'C:\\Users\\Mr Koffi\\Desktop\\Deseases\\PAGES\\asso.db'

    # On envoie une equête SQL pour prendre toutes les lignes de la table 'asso'
    select_query = 'SELECT * FROM asso;'

    # Nous créons une Connexion avec la base de données SQLite3
    conn = sqlite3.connect(db_chemin)

    # Chargement des données 
    with conn:
        df = pd.read_sql_query(select_query, conn)

    return df

# Chargons notre table  de données

def main():
   
    # Permet de charger les données
    data = load_data()
    # Vérifier si des données ont été chargées
    if data is not None:
        # Si oui on l'affiche en brute

        C1, C2, = st.columns(2, gap='large')
        with C1:
            st.subheader("1-Données Brutes")
            st.write(data)

        # Rendre les colonnes à choix
        choix_columns = st.sidebar.multiselect("Sélectionnez les colonnes", data.columns)

        with C2:
            # Analyse Univariée
            if st.sidebar.checkbox("Tri à plat"):
               crossed_data1 = data[choix_columns[0]].value_counts().sort_index(ascending=False)
               st.subheader("2-Tri à plat")
               st.write(crossed_data1)



       
       # Analyse Bivarie
        if st.sidebar.checkbox("Analyse Bivariée"):
            crossed_data2 = pd.crosstab(index=data[choix_columns[0]], columns=data[choix_columns[1]], margins=True)
            st.subheader("3-Analyse Bivariée")
            st.write(crossed_data2)


        # Faire un graphique
        if st.sidebar.checkbox("Faire un graphique"):
            chart_type = st.sidebar.selectbox("Sélectionnez le type de graphique", ["A barre", "line", "box", "violin"])
        
            if chart_type == "A barre":
                fig = px.bar(data, x=choix_columns[0], y=choix_columns[1], color=choix_columns[1])


            st.subheader(f"Graphique {chart_type}")
            st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    else:
        st.info("Téléchargez un fichier CSV pour commencer.")

 
   

if __name__ == "__main__":
    main()
