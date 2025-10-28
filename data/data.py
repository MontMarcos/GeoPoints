import sqlite3
import json
from datetime import datetime

class Database:    
    def __init__(self, db_path='pontos_interesse.db'):
        self.db_path = db_path
        self.init_db()
    
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row 
        return conn
    
    def init_db(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pontos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                descricao TEXT,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL,
                categoria TEXT NOT NULL,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def adicionar_ponto(self, nome, descricao, latitude, longitude, categoria):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO pontos (nome, descricao, latitude, longitude, categoria)
            VALUES (?, ?, ?, ?, ?)
        ''', (nome, descricao, latitude, longitude, categoria))
        
        ponto_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return ponto_id
    
    def listar_pontos(self, categoria=None, busca=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = 'SELECT * FROM pontos WHERE 1=1'
        params = []
        
        if categoria:
            query += ' AND categoria = ?'
            params.append(categoria)
        
        if busca:
            query += ' AND (nome LIKE ? OR descricao LIKE ?)'
            busca_param = f'%{busca}%'
            params.extend([busca_param, busca_param])
        
        query += ' ORDER BY data_criacao DESC'
        
        cursor.execute(query, params)
        pontos = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return pontos
    
    def obter_ponto(self, ponto_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM pontos WHERE id = ?', (ponto_id,))
        ponto = cursor.fetchone()
        
        conn.close()
        return dict(ponto) if ponto else None
    
    def atualizar_ponto(self, ponto_id, nome, descricao, categoria):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE pontos 
            SET nome = ?, descricao = ?, categoria = ?
            WHERE id = ?
        ''', (nome, descricao, categoria, ponto_id))
        
        conn.commit()
        conn.close()
        
        return cursor.rowcount > 0
    
    def deletar_ponto(self, ponto_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM pontos WHERE id = ?', (ponto_id,))
        
        conn.commit()
        conn.close()
        
        return cursor.rowcount > 0
    
    def obter_estatisticas(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT categoria, COUNT(*) as total
            FROM pontos
            GROUP BY categoria
        ''')
        
        stats = {row['categoria']: row['total'] for row in cursor.fetchall()}
        
        conn.close()
        return stats