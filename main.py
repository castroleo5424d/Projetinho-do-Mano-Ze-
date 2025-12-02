import tkinter as tk
from database.db_manager import DBManager 
from gui.app_gui import AppGUI 
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), 'database'))

if __name__ == "__main__":
    # Garante que o diretório 'database' exista antes de tentar criar o arquivo .db
    os.makedirs('database', exist_ok=True)
    
    db_manager = DBManager()
    
    if db_manager.conn is None:
         print("A aplicação não pode iniciar sem a conexão com o banco de dados.")
         exit()

    root = tk.Tk()
    root.title("CRM - Gestão de Clientes")
    root.geometry("700x550") # Define um tamanho inicial para a janela

    app = AppGUI(root, db_manager)
    
    root.mainloop()
