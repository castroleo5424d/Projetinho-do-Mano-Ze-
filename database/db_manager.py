import sqlite3

class DBManager:
    """Gerencia a conexão e operações CRUD no banco de dados SQLite."""
    
    def __init__(self, db_path="database/crm_db.db"): 
        try:
            # Conecta (ou cria) o banco de dados
            self.conn = sqlite3.connect(db_path)
            self.cursor = self.conn.cursor()
            # Este método (create_table) deve estar definido abaixo.
            self.create_table() 
        except sqlite3.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            self.conn = None

    def create_table(self):
        """Cria a tabela CLIENTES se ela não existir."""
        if self.conn:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS clientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    email TEXT,
                    perfil TEXT,             
                    interacoes_historico TEXT
                )
            ''')
            self.conn.commit()

    def insert_cliente(self, nome, email, perfil, historico):
        """Cria (Create) um novo cliente no banco."""
        if self.conn:
            try:
                self.cursor.execute('''
                    INSERT INTO clientes (nome, email, perfil, interacoes_historico) 
                    VALUES (?, ?, ?, ?)
                ''', (nome, email, perfil, historico))
                self.conn.commit()
                return True
            except sqlite3.Error as e:
                print(f"Erro ao inserir cliente: {e}")
                return False

    def get_all_clientes(self):
        """Lê (Read) todos os clientes cadastrados."""
        if self.conn:
            self.cursor.execute("SELECT id, nome, perfil FROM clientes")
            return self.cursor.fetchall()
        return []

    def get_cliente_details(self, cliente_id):
        """Lê (Read) os detalhes completos de um cliente específico."""
        if self.conn:
            self.cursor.execute("SELECT nome, email, perfil, interacoes_historico FROM clientes WHERE id = ?", (cliente_id,))
            return self.cursor.fetchone()
        return None

    def update_cliente(self, cliente_id, nome, email, perfil, historico):
        """Atualiza (Update) os dados de um cliente existente."""
        if self.conn:
            try:
                self.cursor.execute('''
                    UPDATE clientes 
                    SET nome = ?, email = ?, perfil = ?, interacoes_historico = ? 
                    WHERE id = ?
                ''', (nome, email, perfil, historico, cliente_id))
                self.conn.commit()
                return True
            except sqlite3.Error as e:
                print(f"Erro ao atualizar cliente: {e}")
                return False

    def delete_cliente(self, cliente_id):
        """Deleta (Delete) um cliente pelo seu ID."""
        if self.conn:
            try:
                self.cursor.execute("DELETE FROM clientes WHERE id = ?", (cliente_id,))
                self.conn.commit()
                return True
            except sqlite3.Error as e:
                print(f"Erro ao deletar cliente: {e}")
                return False

    def __del__(self):
        """Garante que a conexão seja fechada ao destruir o objeto."""
        if self.conn:
            self.conn.close()