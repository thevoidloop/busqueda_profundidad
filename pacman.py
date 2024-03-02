from flask import Flask, request, jsonify
import networkx as nx
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.visitados = set()

def crear_tablero_personalizado(filas, columnas, conexiones):


    G = nx.Graph()
    
    for nodo_info in conexiones:
        nodo = tuple(nodo_info[0])
        G.add_node(nodo)
        
        for vecino_info in nodo_info[1]:
            vecino = tuple(vecino_info)
            G.add_edge(nodo, vecino)
    
    # return G
    
    # G = nx.Graph()
    # for i in range(filas):
    #     for j in range(columnas):
    #         nodo = (i, j)
    #         G.add_node(nodo)
    #         for vecino in conexiones.get(nodo, []):
    #             G.add_edge(nodo, vecino)

    return G

def dfs_tablero(G, stack):

    while True:
        if not stack:
            ultimo_nodo_visitado = nodo_actual if 'nodo_actual' in locals() else None

            stack.append(ultimo_nodo_visitado)
            app.visitados = set()

        nodo_actual = stack.pop()

        if nodo_actual not in app.visitados:
            app.visitados.add(nodo_actual)
            vecinos = G.neighbors(nodo_actual)
            
            for vecino in vecinos:
                if vecino not in app.visitados and vecino not in stack:
                    stack.append(vecino)
            
            yield nodo_actual, stack

@app.route('/dfs_tablero', methods=['POST'])
def endpoint_dfs_tablero():
    data = request.json
    op = data.get("op")

    if op == "Next":
        try:
            nodo_actual, stack = next(app.generador_dfs) 
        except StopIteration:
            return jsonify({"error": "Pila agotada"}), 400
        return jsonify({"nodo_actual": nodo_actual, "stack": stack})    
    return jsonify({"msj": "Sin interaccion"})


@app.route('/conf', methods=['POST'])
def endpoint_conf():
    data = request.json
    no_filas = data.get("noFilas", 0)
    no_columnas = data.get("noColums", 0)
    conexiones = {}

    # for nodo in data.get("conexiones", []):
    #     conexiones[tuple(nodo['nodo'])] = {tuple(conexion) for conexion in nodo['conexiones']}

    conexiones = [ (tuple(nodo['nodo']), [tuple(conexion) for conexion in nodo['conexiones']]) for nodo in data.get("conexiones", []) ]
    
    print(conexiones);

    app.tablero_grafo = crear_tablero_personalizado(no_filas, no_columnas, conexiones)
    app.stack_inicial = [tuple(data.get("inicio", (0, 0)))]
    app.generador_dfs = dfs_tablero(app.tablero_grafo, app.stack_inicial)

    return jsonify({"Numero de Filas": no_filas, "Numero de Columnas": no_columnas, "Inicio": app.stack_inicial[0]})

if __name__ == '__main__': 
    app.run(host='0.0.0.0', port=5000)
