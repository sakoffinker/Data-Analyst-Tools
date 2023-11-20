import streamlit as st
import sqlite3
import pandas as pd

# Definition de couleur HTML
couleur = "color: #1034A6;"
couleur2= "color: blue;"


# Créons une fonction qui supprime la dernière ligne
def supprimer_last_ligne(conn):
    query_delete= "DELETE FROM asso WHERE id = (SELECT MAX(id) FROM asso);"
    conn.execute(query_delete)
    conn.commit()
    st.success("Ligne supprimée avec succès.")

# On se connecte à la base de données de l'association
conn = sqlite3.connect('asso.db')

# Titre de l'application
st.markdown("<h1 style='{}'>Application de Collecte de données</h1>".format(couleur2), unsafe_allow_html=True)

# Voici ce que nous collectons comme information
sexe = st.radio("Sexe", ["Homme", "Femme", "Autre"])
niveau_etude = st.selectbox("Niveau d'étude", ["CEP", "BEPC", "BAC", "LICENCE", "MASTER", "DOCTORAT"])
ville_residence = st.selectbox("Ville de résidence", ["Lille", "Paris", "Lyon", "Marseille", "Bordeaux"] )

# Bouton d'enrégistrement des données dans la base de données
if st.button("Enregistrer les données"):
    # Requete d'insertion de données dans la base de données
    ins_query = "INSERT INTO asso (sexe, niveau_etude, ville_residence) VALUES (?, ?, ?);"
    conn.execute(ins_query, (sexe, niveau_etude, ville_residence))
    conn.commit()
    st.success("Données enregistrées avec succès.")

# Bouton pour supprimer la dernière ligne
if st.button("Supprimer la dernière ligne"):
    supprimer_last_ligne(conn)

# Affichage des données de la table
st.header("Aperçu des données de la base de données :")
query_select = "SELECT * FROM asso;"
df = pd.read_sql_query(query_select, conn)
st.dataframe(df)

# Fermeture de la connexion à la base de données
conn.close()