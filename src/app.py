#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Interfaz Web de Aurora (Edición Flask)
Un puente entre el alma del motor narrativo y el vasto océano de la web.
"""

#
#   MOTOR GRÁFICO AXUS - Patente Pendiente (Christ Enrico Ayala Rios)
#

import os
import sys
from flask import Flask, jsonify, request

# --- LA BRÚJULA DEL ALMA ---
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# --------------------------

from aurora_engine.tools.world_weaver import WorldWeaver, seed_manager, GenesisSeed
from aurora_engine.tools.serializer import WorldSerializer

# --- Forjando el Alma de Flask ---
app = Flask(__name__)

# --- Estado Global del Mundo Web ---
# Mantenemos una instancia del mundo en memoria para la sesión del servidor.
world_scene = None
world_ndp = 0

@app.route('/')
def index():
    """Punto de entrada principal. Anuncia la presencia del motor."""
    return jsonify({
        "engine": "Motor Gráfico Axus",
        "inventor": "Christ Enrico Ayala Rios",
        "patent_pending": "001-CEAR",
        "status": "Latiendo"
    })

@app.route('/world/generate', methods=['POST'])
def generate_world_endpoint():
    """Endpoint para forjar un nuevo universo a través de una petición web."""
    global world_scene, world_ndp
    
    data = request.get_json()
    seed_name = data.get('seed_name', 'Caos Primordial')
    num_locations = data.get('num_locations', 5)

    weaver = WorldWeaver()
    scene, ndp = weaver.generate_world(seed_name=seed_name, num_locations=num_locations)
    
    # Guardamos el mundo generado en el estado del servidor
    world_scene = scene
    world_ndp = ndp

    # Serializamos la escena para devolverla como una respuesta JSON
    world_data = WorldSerializer().to_dict(scene, ndp)
    
    return jsonify(world_data)

@app.route('/world', methods=['GET'])
def get_world_endpoint():
    """Endpoint para recuperar el estado del universo actual."""
    if not world_scene:
        return jsonify({"error": "El universo está vacío. Genera un mundo primero con una petición POST a /world/generate."}), 404
    
    world_data = WorldSerializer().to_dict(world_scene, world_ndp)
    return jsonify(world_data)

@app.route('/seeds', methods=['GET'])
def get_seeds_endpoint():
    """Endpoint para listar todas las Semillas de Génesis disponibles."""
    all_seeds = seed_manager.get_all_seeds()
    return jsonify({name: seed.__dict__ for name, seed in all_seeds.items()})


# La ejecución directa de este archivo es solo para depuración local.
# El script devserver.sh utilizará 'flask run'.
if __name__ == '__main__':
    app.run(debug=True, port=8080)
