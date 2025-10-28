from controller.controller import Aplication
from flask import Flask

aplication = Aplication()
app = Flask(__name__, template_folder='views')

@app.route('/')
@app.route('/', methods=['GET'])
def inicio():
    """Renderiza a página principal do mapa"""
    return aplication.render('mapa')


@app.route('/api/pontos', methods=['GET'])
def listar_pontos():

    return aplication.api_listar_pontos()

@app.route('/api/pontos', methods=['POST'])
def adicionar_ponto():

    return aplication.api_adicionar_ponto()

@app.route('/api/pontos/<int:ponto_id>', methods=['GET'])
def obter_ponto(ponto_id):
    return aplication.api_obter_ponto(ponto_id)

@app.route('/api/pontos/<int:ponto_id>', methods=['DELETE'])
def deletar_ponto(ponto_id):
    return aplication.api_deletar_ponto(ponto_id)

@app.route('/api/estatisticas', methods=['GET'])
def estatisticas():
    return aplication.api_estatisticas()

@app.route('/api/pontos/export/geojson', methods=['GET'])
def export_geojson():
    return aplication.api_export_geojson()

@app.route('/api/pontos/proximos', methods=['GET'])
def pontos_proximos():

    return aplication.api_pontos_proximos()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8083, debug=True)