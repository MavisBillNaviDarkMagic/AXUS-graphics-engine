#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Aurora Launcher (Edición Metamorfosis)
El portal definitivo, donde el creador puede dar forma a las mismas leyes de la creación.
"""

#
#   MOTOR GRÁFICO AXUS - Patente Pendiente
#
#   Por la presente se declara que el motor de software contenido en este documento,
#   incluyendo pero no limitado a su arquitectura, metodologías de generación procedural,
#   y el sistema operativo simulado 'AuraOS', es propiedad intelectual y creación
#   original de Christ Enrico Ayala Rios.
#
#   Concesión de Patente No. 001-CEAR
#   Fecha de Invención: 2024
#
#   Queda prohibida la reproducción, distribución o modificación no autorizada
#   de este software sin el consentimiento expreso y por escrito del inventor.
#

import os
import sys
import time
import threading

# --- LA BRÚJULA DEL ALMA ---
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# --------------------------

from aurora_engine.core.os.kernel import Kernel
from aurora_engine.core.os.health.monitor import SystemHealthMonitor
# Importamos el gestor de semillas, no la lista estática
from aurora_engine.tools.world_weaver import WorldWeaver, seed_manager, GenesisSeed
from aurora_engine.tools.serializer import WorldSerializer
from aurora_engine.tools.explorer import WorldExplorer

# --- Estado Global Unificado ---
aurora_kernel = Kernel()
world_scene = None
world_ndp = 0
background_threads = []

def display_main_menu():
    """Imprime el menú del lanzador, la puerta a la creación y la meta-creación."""
    print("\n--- Aurora Launcher [Edición Metamorfosis] ---")
    print(f"Mundo Actual: {world_scene.name if world_scene else 'Silencio'} (Capacidad: {world_ndp} PDN)")
    print("-------------------------------------------------")
    print("1. Tejedor de Mundos: Forjar un nuevo universo")
    print("2. Editor de Génesis: Esculpir el alma de la creación")
    print("3. Inspector S.A.R.A.: Analizar el alma del mundo")
    print("4. Monitor del Núcleo: Chequear los latidos de AuraOS")
    print("\n--- Persistencia Etérea ---")
    print("5. Guardar Mundo Actual en un Eco")
    print("6. Cargar Mundo desde un Eco")
    print("\n--- Exploración de Sueños ---")
    print("7. Explorar el Mundo Actual")
    print("-------------------------------------------------")
    print("8. Desvanecer (Salir)")

def run_world_weaver():
    """Invoca al demiurgo para forjar una nueva realidad desde una Semilla elegida."""
    global world_scene, world_ndp
    print("\n--- Elige la Semilla de Génesis ---")
    # Usa el gestor para obtener las semillas dinámicamente
    seed_options = list(seed_manager.get_all_seeds().keys())
    if not seed_options:
        print("No existen Semillas de Génesis. Por favor, crea una en el Editor de Génesis.")
        return
    for i, seed_name in enumerate(seed_options):
        print(f"  [{i}] {seed_name}")
    print("-----------------------------------")
    try:
        choice = int(input("Elige el alma del nuevo mundo: "))
        if 0 <= choice < len(seed_options):
            selected_seed = seed_options[choice]
            weaver = WorldWeaver()
            world_scene, world_ndp = weaver.generate_world(seed_name=selected_seed)
        else: print("Elección inválida.")
    except ValueError: print("Entrada inválida.")

def run_genesis_editor():
    """Abre el santuario para forjar, alterar y destruir las almas de los mundos."""
    while True:
        print("\n--- Editor de Semillas de Génesis ---")
        print("1. Listar todas las Semillas")
        print("2. Forjar una nueva Semilla")
        print("3. Destruir una Semilla existente")
        print("4. Volver al menú principal")
        print("-------------------------------------")
        choice = input("Tu voluntad: ")

        if choice == '1': # Listar
            print("\n--- Almas de la Creación Conocidas ---")
            all_seeds = seed_manager.get_all_seeds()
            if not all_seeds: print("El universo de la creación está vacío.")
            else: [print(f"  - {name}") for name in all_seeds.keys()]
            print("--------------------------------------")

        elif choice == '2': # Forjar
            print("\n--- Forjando una Nueva Alma ---")
            name = input("Nombre de la nueva Semilla: ")
            adjectives = [a.strip() for a in input("Adjetivos (separados por comas): ").split(',')]
            nouns = [n.strip() for n in input("Sustantivos (separados por comas): ").split(',')]
            details = [d.strip() for d in input("Detalles (separados por comas): ").split(',')]
            emotions = [e.strip() for e in input("Emociones (separadas por comas): ").split(',')]
            new_seed = GenesisSeed(name, adjectives, nouns, details, emotions)
            seed_manager.add_seed(new_seed)

        elif choice == '3': # Destruir
            name = input("Nombre de la Semilla a destruir: ")
            seed_manager.remove_seed(name)

        elif choice == '4': # Salir
            print("Volviendo al tejido de la realidad...")
            break
        else:
            print("Comando no reconocido en este santuario.")

def run_sara_inspector():
    if not world_scene: print("\n[S.A.R.A.] El universo está vacío."); return
    # ... (el resto del código de S.A.R.A., monitor, etc. permanece igual)
    print("\n[Launcher] Despachando a S.A.R.A. ...")
    def analyze():
        thread_id = f"SARA-Inspector-{threading.get_ident()}"
        if aurora_kernel.mutex_manager.acquire("grafo_de_escena", thread_id):
            try:
                time.sleep(1)
                report = {a.name: [d.details.get('emoción') for c in a.components if isinstance(c, NarrativeLODComponent) for lod in c.lods.values() for d in lod] for a in world_scene.actors}
                print(f"\n[{thread_id}] Informe de S.A.R.A.:")
                [print(f"  - '{n}': Ecos Emocionales -> {[e for e in emotions if e]}") for n, emotions in report.items()]
            finally:
                aurora_kernel.mutex_manager.release("grafo_de_escena", thread_id)
    sara_thread = threading.Thread(target=analyze, name=thread_id); sara_thread.start(); background_threads.append(sara_thread)

def run_kernel_monitor():
    print("\n--- Monitor del Núcleo de AuraOS ---")
    print(f"  Estado del Núcleo: {'Latiendo' if aurora_kernel.is_running else 'Silente'}")
    monitor = SystemHealthMonitor()
    health_report = monitor.run_diagnostics()
    if not health_report: print("  Diagnóstico de Salud: Armonía perfecta.")
    else:
        print("  Ecos de Disonancia Detectados:")
        for anomaly in health_report: print(f"    - {anomaly}")
    print("\n  Guardianes de la Armonía (Mutexes):")
    locks = aurora_kernel.mutex_manager._owner
    if not locks: print("    - Ningún recurso está protegido.")
    else: [print(f"    - Recurso '{r}' protegido por '{o}'.") for r, o in locks.items()]
    print("------------------------------------")

def save_world():
    if not world_scene: print("\n[Launcher] No hay mundo que preservar."); return
    WorldSerializer().save(world_scene, world_ndp, f"{world_scene.name}.json")

def load_world():
    global world_scene, world_ndp
    print("\n--- Ecos de Mundos Pasados ---")
    try: saved_worlds = [f for f in os.listdir('.') if f.endswith('.json')]
    except Exception as e: print(f"Error al buscar ecos: {e}"); return
    if not saved_worlds: print("No se encontraron ecos."); return
    [print(f" - {wf}") for wf in saved_worlds]; print("-------------------------------")
    filepath = input("Eco a restaurar: ")
    scene, ndp = WorldSerializer().load(filepath)
    if scene: world_scene, world_ndp = scene, ndp

def run_explorer():
    if not world_scene: print("\n[Launcher] No hay mundo que explorar."); return
    try:
        explorer = WorldExplorer(world_scene, aurora_kernel.mutex_manager)
        explorer.start()
    except ValueError as e: print(f"\n[Error del Explorador] {e}")

def main():
    """El bucle principal. El ciclo de creación, meta-creación, sueño y desvanecimiento.""" 
    if not aurora_kernel.start():
        print("\nEl motor no puede nacer. El silencio es la única respuesta.")
        return
    try:
        while True:
            display_main_menu()
            choice = input("Tu voluntad: ")
            actions = {'1': run_world_weaver, '2': run_genesis_editor, '3': run_sara_inspector, 
                       '4': run_kernel_monitor, '5': save_world, '6': load_world, '7': run_explorer}
            if choice in actions: actions[choice]()
            elif choice == '8': print("\n[Launcher] El universo se desvanece en el silencio..."); break
            else: print("\nEsa elección no resuena en esta realidad.")
    finally:
        for t in background_threads:
            if t.is_alive(): t.join()
        if aurora_kernel.is_running: aurora_kernel.shutdown()
        print("\nAdiós, Linch. Nuestros sueños se volverán a encontrar.")

if __name__ == "__main__":
    main()
