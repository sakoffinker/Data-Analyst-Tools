############CETTE APPLICATION A POUR OBJECTIF D'AUTOMATISER LE PROCESSUS DE RECODAGE DES DONNES ##############################
# Voici les dépendances de notre application. PYTHON C'est PUISSANT, PYTHON C'est la Vie.

import streamlit as st
import pandas as pd


# Style css que nous allons appliquer à nos bouttons

st.markdown("""
    <style>
        #button-after {
            color: blue;
            background-color: transparent;
            border: 4px white;
            padding: 16px 32px;
            cursor: pointer;
        }
    </style>
""", unsafe_allow_html=True)


# Dans cette partie, nous définissons des couleurs que nous utiliserons pour nos titres et textes
couleur = "color: #1034A6;"
couleur2= "color: green;"
couleur3= "color: blue;"


# Début de notre application de récodage de données

def main():
    st.markdown("<h1 style='{}'>Application de Recodage Données</h2>".format(couleur2), unsafe_allow_html=True)
    st.markdown("<h6 style='{}'>Collecter des données, c'est un gros problème pour le chercheur, mais les recoder, c'est encore une autre. Cette application a pour objectif de vous libérer de l'étape du recodage qui peux parfois devenir très laborieux. Mais n'oubliez pas de coder parfois pour ne pas en perdre le reflexe. </h6>".format(couleur2), unsafe_allow_html=True)

    # Méthode qui permet de charger les données de types csv, xlsx, xls,json.
    # On contrle avec des conditions le type de fichier que l'utilisateur va charger.
    # Cela nous permettra de définir des méthode de téléchargement adaptées à chaque fichiers.
    st.sidebar.markdown("<h1 style='{}'>MASTER RECODER OPTIONS</h2>".format(couleur2), unsafe_allow_html=True)
    donnees_chargees = st.sidebar.file_uploader("Choisissez le fichier CSV à recoder", type=["csv", "xlsx", "xls", "json"])
    if donnees_chargees is not None:
        if donnees_chargees.name.endswith('.csv'):
            df = pd.read_csv(donnees_chargees)
        elif donnees_chargees.name.endswith('.xlsx') or donnees_chargees.name.endswith('.xls'):
            df = pd.read_excel(donnees_chargees)
        elif donnees_chargees.name.endswith('.json'):
            df = pd.read_json(donnees_chargees)
        else:
            st.error("Erreur, les formats pris en charges sont: CSV, Excel ou JSON.")
            return
        

        # Il est important d'afficher un aperçu des données auxquelles on a affaire
        st.markdown("<h3 style='{}'>1- Structure des données</h3>".format(couleur2), unsafe_allow_html=True)
        st.dataframe(df.head())

        # On donne la possibilité de sélectionner les variables à recoder
        st.sidebar.markdown("<h4 style='{}'>I-COLONNE À RECODER</h4>".format(couleur2), unsafe_allow_html=True)
        colonne_selectionnee = st.sidebar.selectbox("Colonne à recoder :", df.columns)

        # Une fois la variable à recoder sélectionnée, on affiche les modalités qu'elle contients
        st.markdown("<h4 style='{}'>2- Les modalité de la Colonne sectionnée</h4>".format(couleur2), unsafe_allow_html=True)
        valeur_unique = df[colonne_selectionnee].unique()
        st.write(valeur_unique)

        # Ensuite on recode les modalités une à une.
        # On écris dans le formulaire la nouvelle modalité puis on clique sur entrer.
        # Pour chaque modalité définie, on l'enrégistre à un dictionnaire python initialisé à 0
        st.markdown("<h4 style='{}'>3- Recodez les modalités maintenant:</h4>".format(couleur2), unsafe_allow_html=True)
        dictionnaire_de_recodage = {}
        for Value in valeur_unique:
            nouvelle_valeur = st.text_input(f"Définissez une Nouvelle valeur pour '{Value}':", Value)
            dictionnaire_de_recodage[Value] = nouvelle_valeur

        # Puis on applique les modifications à notre table d'origine
        df[colonne_selectionnee] = df[colonne_selectionnee].map(dictionnaire_de_recodage)

        # Affichages des données après les avoir recodé en auto auto.
        st.markdown("<h4 style='{}'>4- Données après recodage:</h4>".format(couleur2), unsafe_allow_html=True)
        st.dataframe(df)

        # Une autre routine quand on est data scientiste ou analyste, il faut regrouper les modalités pour rendre les données plus interprétable.
        # Plus de modalités, c'est pas facile pour le cerveau

        # Alors ici, on donne la possibilité de sélectionner les variables que nous voulons regrouper.
        st.sidebar.markdown("<h3 style='{}'>II-REGROUPEMENT DE MODALITES</h3>".format(couleur2), unsafe_allow_html=True)
        composition_groupe = st.sidebar.multiselect("Sélectionnez les modalités à regrouper :", valeur_unique)
        
        # Maintenant on définis un nom pour l'ensemble.
        if composition_groupe:
            nom_du_groupe = st.sidebar.text_input("Nom du nouveau groupe:")
            df[colonne_selectionnee] = df[colonne_selectionnee].apply(lambda x: nom_du_groupe if x in composition_groupe else x)

            # Affichage des données après le regroupement
            st.subheader("5- Données après regroupement:")
            st.dataframe(df)


        # Après les modifications, on télécharge la nouvelles version des données.
        
        st.markdown("<h6 style='{}'>Votre nouvelle table est tout prêt, vous pouvez à présent procécder à son téléchargement. Pour ce faire, cliquez sur le bouton ci-dessous. Il sera enrégistré dans votre répertoire de travail que celui dans lequel se trouve votre application.</h6>".format(couleur2), unsafe_allow_html=True)
        if st.button("TELECHARGER LA NOUVELLE VERSION DE VOS DONNEES", key="button-after"):
            st.markdown('<span id="button-after"></span>', unsafe_allow_html=True)
            if donnees_chargees.name.endswith('.csv'):
                df.to_csv("donnees_recodes_regroupes.csv", index=False)
            elif donnees_chargees.name.endswith('.xlsx') or donnees_chargees.name.endswith('.xls'):
                df.to_excel("donnees_recodes_regroupes.xls", index=False)
            elif donnees_chargees.name.endswith('.json'):
                df.to_json("donnees_recodes_regroupes.json", orient='records', lines=True)

            st.success("La nouvelles version de vos données a été téléchargé avec succès.")
    


if __name__ == "__main__":
    main()


# FIN DE NOTRE APPLICATION. MERCI DE PARTAGER VOS CODES AU CAS OU VOUS LA RENDEZ PLUS BELLE ET RAJOUTEZ D'AUTRES FONCTIONNALITES
