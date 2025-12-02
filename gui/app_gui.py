import tkinter as tk
from tkinter import ttk, messagebox

class AppGUI(tk.Frame):
    """Interface Gráfica do Usuário (GUI) para o CRM."""
    
    def __init__(self, master, db_manager):
        super().__init__(master)
        self.master = master
        self.db_manager = db_manager
        self.selected_cliente_id = None # Inicializa o ID do cliente selecionado
        self.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.create_widgets()
        self.load_clientes_list()

    def create_widgets(self):
        # Frame Principal - Gerenciamento de Clientes
        main_frame = ttk.LabelFrame(self, text="📊 Gestão de Clientes (CRUD)")
        main_frame.pack(pady=10, padx=10, fill="x")

        # --- Campos de Entrada ---
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(padx=5, pady=5, fill="x")

        # Nome, Email, Perfil, Histórico (Campos iguais aos anteriores)
        ttk.Label(form_frame, text="Nome:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.nome_entry = ttk.Entry(form_frame, width=30)
        self.nome_entry.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(form_frame, text="Email:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.email_entry = ttk.Entry(form_frame, width=30)
        self.email_entry.grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Label(form_frame, text="Perfil:").grid(row=0, column=2, sticky="w", padx=5, pady=2)
        self.perfil_entry = ttk.Entry(form_frame, width=20)
        self.perfil_entry.grid(row=0, column=3, padx=5, pady=2)

        ttk.Label(form_frame, text="Histórico:").grid(row=2, column=0, sticky="nw", padx=5, pady=2)
        self.historico_text = tk.Text(form_frame, height=4, width=45)
        self.historico_text.grid(row=2, column=1, columnspan=3, padx=5, pady=2)

        # --- Botões ---
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        # Botões para CRUD
        ttk.Button(button_frame, text="➕ Adicionar Cliente", command=self.add_cliente).pack(side="left", padx=5)
        ttk.Button(button_frame, text="✏️ Atualizar Cliente", command=self.update_cliente_data).pack(side="left", padx=5)
        ttk.Button(button_frame, text="🗑️ Excluir Cliente", command=self.delete_selected_cliente, style='Danger.TButton').pack(side="left", padx=5)
        ttk.Button(button_frame, text="🔄 Limpar Campos", command=self.clear_entries).pack(side="left", padx=5)
        
        # Estilo para o botão de exclusão
        style = ttk.Style()
        style.configure('Danger.TButton', foreground='red', font=('Arial', 10, 'bold'))

        # --- Tabela de Visualização (Treeview) ---
        ttk.Label(self, text="📋 Clientes Cadastrados:").pack(pady=(10, 5), anchor="w")
        
        tree_frame = ttk.Frame(self)
        tree_frame.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(tree_frame, columns=("ID", "Nome", "Perfil"), show="headings", selectmode="browse")
        self.tree.heading("ID", text="ID", anchor="w")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Perfil", text="Perfil")
        
        self.tree.column("ID", width=50, stretch=tk.NO)
        self.tree.column("Nome", width=250)
        self.tree.column("Perfil", width=150)
        
        # Scrollbar
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side='right', fill='y')
        self.tree.pack(fill="both", expand=True)
        
        # Vincula o evento de clique na linha para mostrar detalhes
        self.tree.bind('<<TreeviewSelect>>', self.show_cliente_details)

    def clear_entries(self):
        """Limpa os campos de entrada do formulário e a seleção."""
        self.nome_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.perfil_entry.delete(0, tk.END)
        self.historico_text.delete('1.0', tk.END)
        self.selected_cliente_id = None # Limpa o ID selecionado
        self.tree.selection_remove(self.tree.selection()) # Remove a seleção visual

    def add_cliente(self):
        """Coleta dados do formulário e insere no banco."""
        nome = self.nome_entry.get()
        # ... (restante da coleta de dados)
        email = self.email_entry.get()
        perfil = self.perfil_entry.get()
        historico = self.historico_text.get('1.0', tk.END).strip()
        
        if not nome:
            messagebox.showerror("Erro", "O campo Nome é obrigatório!")
            return

        if self.db_manager.insert_cliente(nome, email, perfil, historico):
            messagebox.showinfo("Sucesso", f"Cliente '{nome}' adicionado com sucesso!")
            self.clear_entries()
            self.load_clientes_list()
        else:
            messagebox.showerror("Erro", "Não foi possível adicionar o cliente.")

    def update_cliente_data(self):
        """Coleta dados do formulário e atualiza o cliente selecionado no banco."""
        if self.selected_cliente_id is None:
            messagebox.showwarning("Aviso", "Selecione um cliente na lista para atualizar.")
            return

        nome = self.nome_entry.get()
        email = self.email_entry.get()
        perfil = self.perfil_entry.get()
        historico = self.historico_text.get('1.0', tk.END).strip()
        
        if not nome:
            messagebox.showerror("Erro", "O campo Nome é obrigatório!")
            return
            
        confirm = messagebox.askyesno(
            "Confirmação de Atualização", 
            f"Tem certeza que deseja ATUALIZAR os dados do cliente '{nome}' (ID: {self.selected_cliente_id})?"
        )
        
        if confirm:
            if self.db_manager.update_cliente(self.selected_cliente_id, nome, email, perfil, historico):
                messagebox.showinfo("Sucesso", f"Cliente '{nome}' atualizado com sucesso!")
                self.load_clientes_list() # Recarrega a lista para mostrar a alteração
            else:
                messagebox.showerror("Erro", "Não foi possível atualizar o cliente.")

    def delete_selected_cliente(self):
        """Deleta o cliente selecionado no banco."""
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Aviso", "Selecione um cliente na lista para excluir.")
            return

        values = self.tree.item(selected_item, 'values')
        cliente_id = values[0]
        cliente_nome = values[1]
        
        confirm = messagebox.askyesno(
            "Confirmação de Exclusão", 
            f"Tem certeza que deseja EXCLUIR o cliente '{cliente_nome}' (ID: {cliente_id})?"
        )
        
        if confirm:
            if self.db_manager.delete_cliente(cliente_id):
                messagebox.showinfo("Sucesso", f"Cliente '{cliente_nome}' excluído permanentemente.")
                self.clear_entries()
                self.load_clientes_list()
            else:
                messagebox.showerror("Erro", "Falha ao excluir o cliente.")

    def load_clientes_list(self):
        """Busca os clientes no banco e exibe no Treeview."""
        # Limpa o Treeview
        for i in self.tree.get_children():
            self.tree.delete(i)
            
        clientes = self.db_manager.get_all_clientes()
        for cliente in clientes:
            self.tree.insert("", tk.END, values=cliente)

    def show_cliente_details(self, event):
        """Exibe os detalhes completos do cliente selecionado no formulário."""
        selected_item = self.tree.focus()
        if not selected_item:
            return

        values = self.tree.item(selected_item, 'values')
        cliente_id = values[0]
        
        details = self.db_manager.get_cliente_details(cliente_id)
        
        if details:
            nome, email, perfil, historico = details
            
            # Limpa e preenche os campos do formulário com os detalhes
            self.clear_entries()
            self.nome_entry.insert(0, nome)
            self.email_entry.insert(0, email)
            self.perfil_entry.insert(0, perfil)
            self.historico_text.insert('1.0', historico)
            
            # Armazena o ID para permitir a atualização/exclusão
            self.selected_cliente_id = cliente_id