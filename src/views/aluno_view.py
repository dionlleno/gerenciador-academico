from tkinter import Frame, Label, Entry, Button, messagebox, ttk, Scrollbar, END
from services.aluno_service import AlunoService

class AlunoView:
    def __init__(self, parent):
        self.service = AlunoService()
        self.definir_estilos()
        
        aba = Frame(parent, background=self.estilos['aba_bg'])
        parent.add(aba, text="ALUNOS")
        
        frame_superior = Frame(
            aba, bd=4, background=self.estilos['frame_bg'],
            highlightthickness=2,
            highlightcolor=self.estilos['frame_hl_act'],
            highlightbackground=self.estilos['frame_hl']
        )
        frame_superior.place(relx=0, rely=0.01, relwidth=1, relheight=0.25)
        
        frame_meio = Frame(
            aba, bd=4, background=self.estilos['frame_bg'],
            highlightthickness=2,
            highlightcolor=self.estilos['frame_hl_act'],
            highlightbackground=self.estilos['frame_hl']
        )
        frame_meio.place(relx=0, rely=0.26, relwidth=1, relheight=0.74)
        
        frame_inferior = Frame(
            aba, bd=4, background=self.estilos['frame_bg'],
            highlightthickness=2,
            highlightcolor=self.estilos['frame_hl_act'],
            highlightbackground=self.estilos['frame_hl']
        )
        frame_inferior.place(relx=0, rely=0.26, relwidth=1, relheight=0.74)
        
        botoes = [
            ("BUSCAR", self.buscar, 0.27),
            ("LIMPAR", self.limpar, 0.40),
            ("ADICIONAR", self.adicionar, 0.60),
            ("ATUALIZAR", self.atualizar, 0.73),
            ("EXCLUIR", self.excluir, 0.86),
        ]
        for texto, comando, pos in botoes:
            Button(
                frame_superior, text=texto, font=self.estilos['bt_font'],
                background=self.estilos['bt_bg'], border=2, activebackground=self.estilos['bt_bg_act'], foreground=self.estilos['bt_fg'], activeforeground=self.estilos['bt_fg_act'],
                command=comando
            ).place(relx=pos, rely=0.16, relwidth=0.12, relheight=0.15)
        
        labels = [
            ("MATRICULA:", 0.03, 0.06),
            ("NOME:", 0.03, 0.32),
            ("DATA DE NASCIMENTO:", 0.03, 0.58)
        ]
        for texto, x, y in labels:
            Label(
                frame_superior, text=texto, font=self.estilos['lb_font'],
                background=self.estilos['lb_bg'], foreground=self.estilos['lb_fg'], 
                activeforeground=self.estilos['lb_fg_act']
            ).place(relx=x, rely=y)
        
        self.entry_matricula = self.criar_entry(frame_superior, 0.02, 0.16)
        self.entry_nome = self.criar_entry(frame_superior, 0.02, 0.42, 0.23)
        self.entry_data_nascimento = self.criar_entry(frame_superior, 0.02, 0.68, 0.23)
        
        self.lista = ttk.Treeview(frame_inferior, height=3, columns=("col1", "col2", "col3"))
        self.configurar_lista(frame_inferior)
        
        self.listagem()

    def definir_estilos(self):
        self.estilos = {
            "aba_bg": "#DFEDF1",
            "frame_bg": "#DFEDF1",
            "frame_hl": "#00A7F8",
            "frame_hl_act": "#00A7F8",
            "bt_bg": "#00A7F8",
            "bt_fg": "#FFFFFF",
            "bt_bg_act": "#FFFFFF",
            "bt_fg_act": "#00A7F8",
            "bt_font": ("Arial", 10, "bold"),
            "lb_bg": "#DFEDF1",
            "lb_fg": "#00A7F8",
            "lb_fg_act": "#00A7F8",
            "lb_font": ("Arial", 10, "bold"),
            "entry_bg": "#FAFAFA",
            "entry_fg": "#666666",
            "entry_font": ("Arial", 10, "bold")
        }
    
    def criar_entry(self, parent, x, y, width=0.15):
        entry = Entry(
            parent, font=self.estilos['entry_font'],
            foreground=self.estilos['entry_fg'], background=self.estilos['entry_bg'],
            border=2, highlightbackground=self.estilos['entry_bg']
        )
        entry.place(relx=x, rely=y, relwidth=width, relheight=0.15)
        return entry
    
    def configurar_lista(self, frame_inferior):
        self.lista.heading("#1", text="MAT.")
        self.lista.heading("#2", text="NOME")
        self.lista.heading("#3", text="DATA_NASC.")
        self.lista.column("#0", width=1)
        self.lista.column("#1", width=50)
        self.lista.column("#2", width=400)
        self.lista.column("#3", width=100)
        self.lista.place(relx=0, rely=0.01, relwidth=0.98, relheight=0.97)
        
        scrool_x = Scrollbar(frame_inferior, orient="horizontal", command=self.lista.xview)
        scrool_x.place(relx=0, rely=0.96, relwidth=0.98, relheight=0.03)
        self.lista.configure(xscrollcommand=scrool_x.set)
        
        scrool_y = Scrollbar(frame_inferior, orient="vertical", command=self.lista.yview)
        scrool_y.place(relx=0.98, rely=0.01, relwidth=0.02, relheight=0.98)
        self.lista.configure(yscrollcommand=scrool_y.set)
        self.lista.bind("<Double-1>", self.on_double_click)
        self.lista.bind("<Return>", self.on_double_click)
        self.lista.bind("<Shift Delete>", self.on_shift_del)
    
    def listagem(self):
        for item in self.lista.get_children():
            self.lista.delete(item)
        for aluno in self.service.listar():
            self.lista.insert("", END, values=(aluno.get_matricula(), aluno.get_nome(), aluno.get_data_nascimento()))
            
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
