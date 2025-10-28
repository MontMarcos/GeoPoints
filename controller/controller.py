from math import radians, sin, cos, sqrt, atan2
from flask import render_template, request, jsonify
from data.data import Database 
import logging

def calcular_distancia_haversine(lat1, lng1, lat2, lng2):
    R = 6371000  
    phi1 = radians(lat1)
    phi2 = radians(lat2)
    delta_phi = radians(lat2 - lat1)
    delta_lambda = radians(lng2 - lng1)
    
    a = sin(delta_phi / 2) ** 2 + cos(phi1) * cos(phi2) * sin(delta_lambda / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    return R * c


def formatar_distancia(distancia):
    if distancia >= 1000:
        return f"{distancia / 1000:.2f} km"
    return f"{distancia:.0f} m"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class Aplication:
    def __init__(self):
        self.db = Database()
        self.pages = {
            'mapa': self.render_mapa,
        }
        
        self.categorias = {
            'delegacia': {'nome': 'Delegacia', 'cor': '#0066cc'},
            'posto_fronteira': {'nome': 'Posto de Fronteira', 'cor': '#cc0000'},
            'local_ocorrencia': {'nome': 'Local de Ocorrência', 'cor': '#ff9900'},
            'posto_avancado': {'nome': 'Posto Avançado', 'cor': '#009933'},
            'outros': {'nome': 'Outros', 'cor': '#666666'}
        }
        
        logger.info("Aplicação inicializada com sucesso")
    
    def render(self, page):
        content_function = self.pages.get(page, self.render_mapa)
        return content_function()
    
    def render_mapa(self):
        logger.info("Renderizando página do mapa")
        return render_template('mapa.tpl', categorias=self.categorias)
    
    
    def api_adicionar_ponto(self):
        try:
            dados = request.get_json()
            
            if not dados.get('nome') or not dados.get('latitude') or not dados.get('longitude'):
                logger.warning("Tentativa de adicionar ponto com dados incompletos")
                return jsonify({'erro': 'Dados incompletos: nome, latitude e longitude são obrigatórios'}), 400
            
            try:
                lat = float(dados['latitude'])
                lng = float(dados['longitude'])
            except (ValueError, TypeError):
                logger.warning(f"Coordenadas inválidas recebidas: lat={dados.get('latitude')}, lng={dados.get('longitude')}")
                return jsonify({'erro': 'Coordenadas inválidas: devem ser números'}), 400
            
            if not (-16.0 <= lat <= -15.5 and -48.3 <= lng <= -47.3):
                logger.warning(f"Tentativa de adicionar ponto fora de Brasília: lat={lat}, lng={lng}")
                return jsonify({
                    'erro': 'Coordenadas fora dos limites de Brasília',
                    'detalhes': 'Latitude deve estar entre -16.0 e -15.5, Longitude entre -48.3 e -47.3'
                }), 400
            
            if dados.get('categoria') not in self.categorias:
                logger.warning(f"Categoria inválida: {dados.get('categoria')}")
                return jsonify({
                    'erro': 'Categoria inválida',
                    'categorias_validas': list(self.categorias.keys())
                }), 400
            
            if len(dados['nome']) > 200:
                return jsonify({'erro': 'Nome muito longo (máximo 200 caracteres)'}), 400
            
            if dados.get('descricao') and len(dados['descricao']) > 1000:
                return jsonify({'erro': 'Descrição muito longa (máximo 1000 caracteres)'}), 400
            
            ponto_id = self.db.adicionar_ponto(
                nome=dados['nome'].strip(),
                descricao=dados.get('descricao', '').strip(),
                latitude=lat,
                longitude=lng,
                categoria=dados['categoria']
            )
            
            ponto = self.db.obter_ponto(ponto_id)
            
            logger.info(f"Ponto adicionado: ID={ponto_id}, Nome='{dados['nome']}', Categoria={dados['categoria']}")
            
            return jsonify({
                'sucesso': True,
                'ponto': ponto,
                'mensagem': 'Ponto adicionado com sucesso'
            }), 201
            
        except Exception as e:
            logger.error(f"Erro ao adicionar ponto: {str(e)}", exc_info=True)
            return jsonify({'erro': 'Erro interno do servidor'}), 500
    
    def api_listar_pontos(self):
        try:
            categoria = request.args.get('categoria')
            busca = request.args.get('busca')
            
            pontos = self.db.listar_pontos(categoria=categoria, busca=busca)
            
            logger.info(f"Listagem de pontos: {len(pontos)} encontrado(s) - Filtros: categoria={categoria}, busca={busca}")
            
            return jsonify({
                'sucesso': True,
                'pontos': pontos,
                'total': len(pontos)
            }), 200
            
        except Exception as e:
            logger.error(f"Erro ao listar pontos: {str(e)}", exc_info=True)
            return jsonify({'erro': 'Erro ao listar pontos'}), 500
    
    def api_obter_ponto(self, ponto_id):
        """API: Obtém um ponto específico"""
        try:
            ponto = self.db.obter_ponto(ponto_id)
            
            if not ponto:
                logger.warning(f"Ponto não encontrado: ID={ponto_id}")
                return jsonify({'erro': 'Ponto não encontrado'}), 404
            
            logger.info(f"Ponto obtido: ID={ponto_id}")
            
            return jsonify({
                'sucesso': True,
                'ponto': ponto
            }), 200
            
        except Exception as e:
            logger.error(f"Erro ao obter ponto {ponto_id}: {str(e)}", exc_info=True)
            return jsonify({'erro': 'Erro ao obter ponto'}), 500
    
    def api_deletar_ponto(self, ponto_id):
        try:
            sucesso = self.db.deletar_ponto(ponto_id)
            
            if not sucesso:
                logger.warning(f"Tentativa de deletar ponto inexistente: ID={ponto_id}")
                return jsonify({'erro': 'Ponto não encontrado'}), 404
            
            logger.info(f"Ponto deletado: ID={ponto_id}")
            
            return jsonify({
                'sucesso': True,
                'mensagem': 'Ponto deletado com sucesso'
            }), 200
            
        except Exception as e:
            logger.error(f"Erro ao deletar ponto {ponto_id}: {str(e)}", exc_info=True)
            return jsonify({'erro': 'Erro ao deletar ponto'}), 500
    
    def api_estatisticas(self):
        try:
            stats = self.db.obter_estatisticas()
            
            logger.info("Estatísticas geradas com sucesso")
            
            return jsonify({
                'sucesso': True,
                'estatisticas': stats,
                'categorias': self.categorias
            }), 200
            
        except Exception as e:
            logger.error(f"Erro ao gerar estatísticas: {str(e)}", exc_info=True)
            return jsonify({'erro': 'Erro ao gerar estatísticas'}), 500
    
    def api_export_geojson(self):
        try:
            pontos = self.db.listar_pontos()
            geojson = {
                "type": "FeatureCollection",
                "crs": {
                    "type": "name",
                    "properties": {
                        "name": "urn:ogc:def:crs:OGC:1.3:CRS84"
                    }
                },
                "features": [
                    {
                        "type": "Feature",
                        "geometry": {
                            "type": "Point",
                            "coordinates": [p['longitude'], p['latitude']] 
                        },
                        "properties": {
                            "id": p['id'],
                            "nome": p['nome'],
                            "descricao": p['descricao'],
                            "categoria": p['categoria'],
                            "categoria_nome": self.categorias[p['categoria']]['nome'],
                            "cor": self.categorias[p['categoria']]['cor'],
                            "data_criacao": p['data_criacao']
                        }
                    } for p in pontos
                ]
            }
            
            logger.info(f"GeoJSON exportado: {len(pontos)} pontos")
            
            return jsonify(geojson), 200
            
        except Exception as e:
            logger.error(f"Erro ao exportar GeoJSON: {str(e)}", exc_info=True)
            return jsonify({'erro': 'Erro ao exportar dados'}), 500

    def api_pontos_proximos(self):
        try:
            lat = request.args.get('lat')
            lng = request.args.get('lng')
            
            if not lat or not lng:
                return jsonify({'erro': 'Parâmetros lat e lng são obrigatórios'}), 400
            
            try:
                lat = float(lat)
                lng = float(lng)
                raio = float(request.args.get('raio', 1000))
            except ValueError:
                return jsonify({'erro': 'Coordenadas e raio devem ser números'}), 400
            
            todos = self.db.listar_pontos()
            
            proximos = []
            for p in todos:
                distancia = calcular_distancia_haversine(
                    lat, lng, 
                    p['latitude'], p['longitude']
                )
                
                if distancia <= raio:
                    p['distancia_metros'] = round(distancia, 2)
                    p['distancia_formatada'] = formatar_distancia(distancia)
                    proximos.append(p)
            
            proximos.sort(key=lambda x: x['distancia_metros'])
            
            logger.info(f"Busca por proximidade: {len(proximos)} pontos em raio de {raio}m de ({lat}, {lng})")
            
            return jsonify({
                'sucesso': True,
                'referencia': {'latitude': lat, 'longitude': lng},
                'raio_metros': raio,
                'total_encontrados': len(proximos),
                'pontos': proximos
            }), 200
            
        except Exception as e:
            logger.error(f"Erro na busca por proximidade: {str(e)}", exc_info=True)
            return jsonify({'erro': 'Erro ao buscar pontos próximos'}), 500