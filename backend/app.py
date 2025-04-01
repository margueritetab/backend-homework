import pathlib as pl
import numpy as np
import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

data = pl.Path(__file__).parent.absolute() / 'data'

# Charger les données CSV
associations_df = pd.read_csv(data / 'associations_etudiantes.csv')
evenements_df = pd.read_csv(data / 'evenements_associations.csv')

## Vous devez ajouter les routes ici : 

# Route pour vérifier si le serveur est actif
@app.route('/api/alive', methods=['GET'])
def check_alive():
    return jsonify({"message": "Alive"}), 200

# Route pour obtenir la liste de toutes les associations
@app.route('/api/associations', methods=['GET'])
def get_associations():
    association_ids = associations_df['id'].tolist()
    return jsonify(association_ids), 200

# Route pour obtenir les détails d'une association
@app.route('/api/association/<int:id>', methods=['GET'])
def get_association(id):
    association = associations_df[associations_df['id'] == id]
    if association.empty:
        return jsonify({"error": "Association not found"}), 404
    return jsonify(association.to_dict(orient='records')[0]), 200

# Route pour obtenir la liste de tous les événements
@app.route('/api/evenements', methods=['GET'])
def get_evenements():
    evenement_ids = evenements_df['id'].tolist()
    return jsonify(evenement_ids), 200

# Route pour obtenir les détails d'un événement
@app.route('/api/evenement/<int:id>', methods=['GET'])
def get_evenement(id):
    evenement = evenements_df[evenements_df['id'] == id]
    if evenement.empty:
        return jsonify({"error": "Event not found"}), 404
    return jsonify(evenement.to_dict(orient='records')[0]), 200

# Route pour obtenir les événements d'une association spécifique
@app.route('/api/association/<int:id>/evenements', methods=['GET'])
def get_evenements_association(id):
    events = evenements_df[evenements_df['association_id'] == id]
    if events.empty:
        return jsonify({"error": "No events found for this association"}), 404
    return jsonify(events.to_dict(orient='records')), 200

# Route pour obtenir les associations par type
@app.route('/api/associations/type/<string:type>', methods=['GET'])
def get_associations_by_type(type):
    filtered_associations = associations_df[associations_df['type'].str.lower() == type.lower()]
    if filtered_associations.empty:
        return jsonify({"error": "No associations found for this type"}), 404
    return jsonify(filtered_associations['id'].tolist()), 200


if __name__ == '__main__':
    app.run(debug=False)
