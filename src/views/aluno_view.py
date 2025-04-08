from tkinter import Frame, Label, Entry, Button, messagebox, ttk, Scrollbar, END
from services.aluno_service import AlunoService

class AlunoView:
    def __init__(self, parent):
        self.service = AlunoService()
        
        aba = Frame(parent)
        parent.add(aba, text="ALUNOS")
        
        frame_superior = Frame(
            aba, bd=4, highlightthickness=2
        )
        frame_superior.place(relx=0, rely=0.01, relwidth=1, relheight=0.25)
        
        frame_meio = Frame(
            aba, bd=4, highlightthickness=2
        )
        frame_meio.place(relx=0, rely=0.26, relwidth=1, relheight=0.25)
        
        frame_inferior = Frame(
            aba, bd=4, highlightthickness=2
        )
        frame_inferior.place(relx=0, rely=0.51, relwidth=1, relheight=0.48)
        
        botoes_superior = [
            ("BUSCAR",    self.buscar,    0.27, 0.16),
            ("LIMPAR",    self.limpar,    0.40, 0.16),
            ("ADICIONAR", self.adicionar, 0.60, 0.16),
            ("ATUALIZAR", self.atualizar, 0.73, 0.16),
            ("EXCLUIR",   self.excluir,   0.86, 0.16),
        ]
        
        for texto, comando, relx, rely in botoes_superior:
            Button(
                frame_superior, text=texto, border=2,
                command=comando
            ).place(relx=relx, rely=rely, relwidth=0.12, relheight=0.15)
        
        botoes_inferior = [
            ("BUSCAR",        self.buscar,    0.66, 0.06, 0.12, 0.08),
            ("LIMPAR",        self.limpar,    0.79, 0.06, 0.12, 0.08),
            ("MATRICULAR",    self.limpar, 0.02, 0.16, 0.18, 0.08),
            ("DESMATRICULAR", self.limpar, 0.21, 0.16, 0.18, 0.08),
        ]
        for texto, comando, relx, rely, relwidth, relheight in botoes_inferior:
            Button(
                frame_inferior, text=texto, border=2,
                command=comando
            ).place(relx=relx, rely=rely, relwidth=relwidth, relheight=relheight)
        
        labels_superior = [
            ("MATRICULA:"         , 0.03, 0.06, 0.12, 0.10),
            ("NOME:"              , 0.03, 0.32, 0.10, 0.10),
            ("DATA DE NASCIMENTO:", 0.03, 0.58, 0.20, 0.10),
        ]
        for texto, x, y, width, height in labels_superior:
            Label(
                frame_superior, text=texto
            ).place(relx=x, rely=y, relwidth=width, relheight=height)
        
        labels_inferior = [
            ("MAT.:"       , 0.03, 0.00),
            ("NOME:"       , 0.14, 0.00),
            ("DATA NASC.:" , 0.45, 0.00)
        ]
        for texto, x, y in labels_inferior:
            Label(
                frame_inferior, text=texto
            ).place(relx=x, rely=y)
        
        self.entry_matricula = self.criar_entry(frame_superior, 0.02, 0.16)
        self.entry_nome = self.criar_entry(frame_superior, 0.02, 0.42, 0.23)
        self.entry_data_nascimento = self.criar_entry(frame_superior, 0.02, 0.68, 0.23)
        
        self.entry_nota_matricula = self.criar_entry_nota(frame_inferior, 0.02, 0.06, width=0.10)
        self.entry_nota_valor = self.criar_entry_nota(frame_inferior, 0.13, 0.06, width=0.10)
        
        self.lista_aluno = ttk.Treeview(frame_meio, height=3, columns=("col1", "col2", "col3"))
        self.lista_nota = ttk.Treeview(frame_inferior, height=3, columns=("col1", "col2", "col3", "col4"))
        self.configurar_lista_aluno(frame_meio)
        self.configurar_lista_nota(frame_inferior)
        
        self.listagem_aluno()
    
    def criar_entry(self, parent, x, y, width=0.15):
        entry = Entry(
            parent, border=2
        )
        entry.place(relx=x, rely=y, relwidth=width, relheight=0.15)
        return entry
    
    def criar_entry_nota(self, parent, x, y, width=0.15, height=0.08):
        entry = Entry(
            parent, border=2
        )
        entry.place(relx=x, rely=y, relwidth=width, relheight=height)
        return entry
    
    def configurar_lista_aluno(self, frame):
        self.lista_aluno.heading("#1", text="MAT.")
        self.lista_aluno.heading("#2", text="NOME")
        self.lista_aluno.heading("#3", text="DATA_NASC.")
        self.lista_aluno.column("#0", width=1)
        self.lista_aluno.column("#1", width=50)
        self.lista_aluno.column("#2", width=400)
        self.lista_aluno.column("#3", width=100)
        self.lista_aluno.place(relx=0, rely=0.01, relwidth=0.98, relheight=0.90)
        
        scrool_x = Scrollbar(frame, orient="horizontal", command=self.lista_aluno.xview)
        scrool_x.place(relx=0, rely=0.90, relwidth=0.98, relheight=0.01)
        self.lista_aluno.configure(xscrollcommand=scrool_x.set)
        
        scrool_y = Scrollbar(frame, orient="vertical", command=self.lista_aluno.yview)
        scrool_y.place(relx=0.98, rely=0.01, relwidth=0.02, relheight=0.99)
        self.lista_aluno.configure(yscrollcommand=scrool_y.set)
        self.lista_aluno.bind("<Double-1>", self.on_double_click)
        self.lista_aluno.bind("<Return>", self.on_double_click)
        self.lista_aluno.bind("<Shift Delete>", self.on_shift_del)
    
    def configurar_lista_nota(self, frame):
        self.lista_nota.heading("#0", text="")
        self.lista_nota.heading("#1", text="MAT.")
        self.lista_nota.heading("#2", text="NOME")
        self.lista_nota.heading("#3", text="DATA_NASC.")
        self.lista_nota.column("#0", width=1)
        self.lista_nota.column("#1", width=50)
        self.lista_nota.column("#2", width=400)
        self.lista_nota.column("#3", width=100)
        self.lista_nota.place(relx=0, rely=0.25, relwidth=0.98, relheight=0.71)
        
        scrool_nota_x = Scrollbar(frame, orient="horizontal", command=self.lista_nota.xview)
        scrool_nota_x.place(relx=0, rely=0.96, relwidth=0.98, relheight=0.04)
        self.lista_nota.configure(xscrollcommand=scrool_nota_x.set)
        
        scrool_nota_y = Scrollbar(frame, orient="vertical", command=self.lista_nota.yview)
        scrool_nota_y.place(relx=0.98, rely=0.25, relwidth=0.02, relheight=0.75)
        self.lista_nota.configure(yscrollcommand=scrool_nota_y.set)
    
    def listagem_aluno(self):
        for item in self.lista_aluno.get_children():
            self.lista_aluno.delete(item)
        for aluno in self.service.listar():
            self.lista_aluno.insert("", END, values=(aluno.get_matricula(), aluno.get_nome(), aluno.get_data_nascimento()))
            
    def listagem_nota(self):
        for item in self.lista_nota.get_children():
            self.lista_nota.delete(item)
        for aluno in self.service.listar():
            self.lista_nota.insert("", END, values=(aluno.get_matricula(), aluno.get_nome(), aluno.get_data_nascimento()))
    
    def buscar(self) -> None:
        matricula = self.entry_matricula.get()
        nome = self.entry_nome.get()
        if matricula:
            self.limpar()
            aluno = self.service.buscar_por_matricula(matricula=matricula)
            if aluno:
                self.entry_matricula.insert(END, aluno.get_matricula())
                self.entry_nome.insert(END, aluno.get_nome())
                self.entry_data_nascimento.insert(END, aluno.get_data_nascimento())
            else:
                return messagebox.showerror("ATENÇÃO!", "Digite uma matricula valida, nenhum aluno foi encontrado.")
        elif nome:
            for item in self.lista.get_children():
                self.lista.delete(item)
            alunos = self.service.buscar_por_nome(nome=nome)
            if alunos:
                for aluno in alunos:
                    self.lista.insert("", END, values=(aluno.get_matricula(), aluno.get_nome(), aluno.get_data_nascimento()))
            else:
                return messagebox.showerror("ATENÇÃO!", "Digite um nome valido, nenhum aluno foi encontrado.")
        else:
            return messagebox.showerror("ATENÇÃO!", "Digite uma matricula ou nome validos, nenhum aluno foi encontrado.")

    def limpar(self) -> None:
        self.entry_matricula.delete(0, END)
        self.entry_nome.delete(0,END)
        self.entry_data_nascimento.delete(0, END)
        self.listagem()
        
    def adicionar(self) -> None:
        nome = self.entry_nome.get()
        data_nascimento = self.entry_data_nascimento.get()
        msg = self.service.adicionar(nome=nome, data_nascimento=data_nascimento)
        self.listagem()
        return messagebox.showinfo(message="Aluno adicionado com sucesso." if msg else "Dados invalidos, favor digitar dados validos.")
    
    def atualizar(self) -> None:
        matricula = self.entry_matricula.get()
        nome = self.entry_nome.get()
        data_nascimento = self.entry_data_nascimento.get()
        if matricula and nome and data_nascimento:
            self.service.atualizar(matricula=matricula, nome=nome, data_nascimento=data_nascimento)
            self.limpar()
            return messagebox.showinfo(message="Aluno atualizado com sucesso.")
        else:
            return messagebox.showinfo(message="Selecione um aluno da listagem.")
    
    def excluir(self) -> None:
        matricula = self.entry_matricula.get()
        if messagebox.askyesno(title="EXCLUIR", message=f"Deseja realmente excluir o aluno com a matricula '{matricula}'?"):
            self.service.excluir(matricula=matricula)
            self.limpar()
            return messagebox.showinfo(message="O aluno foi excluido.")
        else:
            return messagebox.showinfo(message="O aluno não foi excluido.")
    
    def on_shift_del(self, event) -> None:
        indice = self.lista.selection()
        item = self.lista.item(indice, "values")
        matricula = item[0]
        if messagebox.askyesno(title="EXCLUIR", message=f"Deseja realmente excluir o aluno com a matricula '{matricula}'?"):
            self.service.excluir(matricula=matricula)
            self.limpar()
            return messagebox.showinfo(message="O aluno foi excluido.")
        else:
            return messagebox.showinfo(message="O aluno não foi excluido.")
    
    def on_double_click(self, event) -> None:
        indice = self.lista.selection()
        itens = self.lista.item(indice, "values")
        self.limpar()
        self.entry_matricula.insert(END, itens[0])
        self.entry_nome.insert(END, itens[1])
        self.entry_data_nascimento.insert(END, itens[2])
