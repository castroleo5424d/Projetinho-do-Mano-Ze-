import tkinter as tk
from database.db_manager import DBManager 
from gui.app_gui import AppGUI 
import os
import sys

# Define o caminho para a pasta 'database'
# Isso é importante para que o script encontre a classe DBManager 
sys.path.append(os.path.join(os.path.dirname(__file__), 'database'))

if __name__ == "__main__":
    # Garante que o diretório 'database' exista antes de tentar criar o arquivo .db
    os.makedirs('database', exist_ok=True)
    
    # 1. Inicializa o banco de dados (cria o arquivo crm_db.db e a tabela)
    db_manager = DBManager()
    
    # Verifica se a conexão foi estabelecida antes de prosseguir
    if db_manager.conn is None:
         print("A aplicação não pode iniciar sem a conexão com o banco de dados.")
         exit()

    # 2. Inicializa a janela principal do Tkinter
    root = tk.Tk()
    root.title("CRM - Gestão de Clientes")
    root.geometry("700x550") # Define um tamanho inicial para a janela

    # 3. Cria a interface gráfica, passando o gerenciador do banco
    app = AppGUI(root, db_manager)
    
    # 4. Inicia o loop principal da aplicação gráfica
    root.mainloop()