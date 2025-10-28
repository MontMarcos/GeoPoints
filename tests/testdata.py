import pytest
from data.data import Database  


@pytest.fixture
def db():
    """Fixture que cria um banco de dados em memória para testes"""
    database = Database(':memory:')
    yield database


class TestDatabase:
    """Testes para operações do banco de dados"""
    
    def test_init_db(self, db):
        """Testa se o banco é inicializado corretamente"""
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='pontos'
        """)
        
        assert cursor.fetchone() is not None
        conn.close()
    
    def test_adicionar_ponto(self, db):
        """Testa adição de um novo ponto"""
        ponto_id = db.adicionar_ponto(
            nome='Delegacia Teste',
            descricao='Descrição de teste',
            latitude=-15.7942,
            longitude=-47.8822,
            categoria='delegacia'
        )
        
        assert ponto_id > 0
        
        ponto = db.obter_ponto(ponto_id)
        assert ponto is not None
        assert ponto['nome'] == 'Delegacia Teste'
        assert ponto['categoria'] == 'delegacia'
    
    def test_listar_pontos_vazio(self, db):
        """Testa listagem quando não há pontos"""
        pontos = db.listar_pontos()
        assert pontos == []
    
    def test_listar_pontos_com_dados(self, db):
        """Testa listagem com múltiplos pontos"""
        db.adicionar_ponto('Ponto 1', 'Desc 1', -15.79, -47.88, 'delegacia')
        db.adicionar_ponto('Ponto 2', 'Desc 2', -15.80, -47.89, 'posto_fronteira')
        
        pontos = db.listar_pontos()
        assert len(pontos) == 2
    
    def test_filtro_por_categoria(self, db):
        """Testa filtro por categoria"""
        db.adicionar_ponto('Delegacia 1', 'Desc', -15.79, -47.88, 'delegacia')
        db.adicionar_ponto('Posto 1', 'Desc', -15.80, -47.89, 'posto_fronteira')
        db.adicionar_ponto('Delegacia 2', 'Desc', -15.81, -47.90, 'delegacia')
        
        delegacias = db.listar_pontos(categoria='delegacia')
        assert len(delegacias) == 2
        assert all(p['categoria'] == 'delegacia' for p in delegacias)
    
    def test_busca_por_texto(self, db):
        """Testa busca por texto no nome ou descrição"""
        db.adicionar_ponto('Delegacia Central', 'Descrição A', -15.79, -47.88, 'delegacia')
        db.adicionar_ponto('Posto Norte', 'Descrição com Central', -15.80, -47.89, 'posto_fronteira')
        db.adicionar_ponto('Outro Local', 'Descrição B', -15.81, -47.90, 'outros')
        
        resultados = db.listar_pontos(busca='Central')
        assert len(resultados) == 2
    
    def test_obter_ponto_inexistente(self, db):
        """Testa busca de ponto que não existe"""
        ponto = db.obter_ponto(999)
        assert ponto is None
    
    def test_atualizar_ponto(self, db):
        """Testa atualização de um ponto"""
        ponto_id = db.adicionar_ponto('Nome Original', 'Desc', -15.79, -47.88, 'delegacia')
        
        sucesso = db.atualizar_ponto(
            ponto_id=ponto_id,
            nome='Nome Atualizado',
            descricao='Nova descrição',
            categoria='posto_fronteira'
        )
        
        assert sucesso is True
        
        ponto = db.obter_ponto(ponto_id)
        assert ponto['nome'] == 'Nome Atualizado'
        assert ponto['categoria'] == 'posto_fronteira'
    
    def test_deletar_ponto(self, db):
        """Testa remoção de um ponto"""
        ponto_id = db.adicionar_ponto('Teste Delete', 'Desc', -15.79, -47.88, 'delegacia')
        
        sucesso = db.deletar_ponto(ponto_id)
        assert sucesso is True
        
        ponto = db.obter_ponto(ponto_id)
        assert ponto is None
    
    def test_deletar_ponto_inexistente(self, db):
        """Testa remoção de ponto que não existe"""
        sucesso = db.deletar_ponto(999)
        assert sucesso is False
    
    def test_estatisticas(self, db):
        """Testa geração de estatísticas"""
        db.adicionar_ponto('D1', 'Desc', -15.79, -47.88, 'delegacia')
        db.adicionar_ponto('D2', 'Desc', -15.80, -47.89, 'delegacia')
        db.adicionar_ponto('P1', 'Desc', -15.81, -47.90, 'posto_fronteira')
        
        stats = db.obter_estatisticas()
        
        assert stats['delegacia'] == 2
        assert stats['posto_fronteira'] == 1
    
    def test_coordenadas_float(self, db):
        """Testa se coordenadas são armazenadas como float"""
        ponto_id = db.adicionar_ponto('Teste', 'Desc', -15.794200, -47.882200, 'delegacia')
        ponto = db.obter_ponto(ponto_id)
        
        assert isinstance(ponto['latitude'], float)
        assert isinstance(ponto['longitude'], float)
        assert ponto['latitude'] == pytest.approx(-15.794200, rel=1e-6)