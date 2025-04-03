from tkinter import Frame, Label, Entry, Button, messagebox, ttk, Scrollbar, END
from services.disciplina_service import DisciplinaService
from services.aluno_service import AlunoService

class DisciplinaView:
    def __init__(self, parent):
        self.service = DisciplinaService()
        self.service_aluno = AlunoService()
        self.definir_estilos()
        
        aba = Frame(parent, background=self.estilos['aba_bg'])
        parent.add(aba, text="DISCIPLINA")
        
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
        frame_meio.place(relx=0, rely=0.26, relwidth=1, relheight=0.25)
        
        frame_inferior = Frame(
            aba, bd=4, background=self.estilos['frame_bg'],
            highlightthickness=2,
            highlightcolor=self.estilos['frame_hl_act'],
            highlightbackground=self.estilos['frame_hl']
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
                frame_superior, text=texto, font=self.estilos['bt_font'],
                background=self.estilos['bt_bg'], border=2, activebackground=self.estilos['bt_bg_act'], foreground=self.estilos['bt_fg'], activeforeground=self.estilos['bt_fg_act'],
                command=comando
            ).place(relx=relx, rely=rely, relwidth=0.12, relheight=0.15)
        
        botoes_inferior = [
            ("BUSCAR",        self.buscar_aluno,    0.66, 0.06, 0.12, 0.08),
            ("LIMPAR",        self.limpar_aluno,    0.79, 0.06, 0.12, 0.08),
            ("MATRICULAR",    self.matricular, 0.02, 0.16, 0.18, 0.08),
            ("DESMATRICULAR", self.desmatricular, 0.21, 0.16, 0.18, 0.08),
        ]
        for texto, comando, relx, rely, relwidth, relheight in botoes_inferior:
            Button(
                frame_inferior, text=texto, font=self.estilos['bt_font'],
                background=self.estilos['bt_bg'], border=2, activebackground=self.estilos['bt_bg_act'], foreground=self.estilos['bt_fg'], activeforeground=self.estilos['bt_fg_act'],
                command=comando
            ).place(relx=relx, rely=rely, relwidth=relwidth, relheight=relheight)
        
        labels_superior = [
            ("MATRICULA:", 0.03, 0.06),
            ("NOME:", 0.03, 0.32),
            ("TURNO:", 0.03, 0.58), ("SALA:", 0.27, 0.58)
        ]
        for texto, x, y in labels_superior:
            Label(
                frame_superior, text=texto, font=self.estilos['lb_font'],
                background=self.estilos['lb_bg'], foreground=self.estilos['lb_fg'], 
                activeforeground=self.estilos['lb_fg_act']
            ).place(relx=x, rely=y)
        
        labels_inferior = [
            ("MAT.:"       , 0.03, 0.00),
            ("NOME:"       , 0.14, 0.00),
            ("DATA NASC.:" , 0.45, 0.00)
        ]
        for texto, x, y in labels_inferior:
            Label(
                frame_inferior, text=texto, font=self.estilos['lb_font'],
                background=self.estilos['lb_bg'], foreground=self.estilos['lb_fg'], 
                activeforeground=self.estilos['lb_fg_act']
            ).place(relx=x, rely=y)
        
        self.entry_matricula = self.criar_entry(frame_superior, 0.02, 0.16)
        self.entry_nome      = self.criar_entry(frame_superior, 0.02, 0.42)
        self.entry_turno     = self.criar_entry(frame_superior, 0.02, 0.68)
        self.entry_sala      = self.criar_entry(frame_superior, 0.26, 0.68)
        self.entry_aluno_matricula = self.criar_entry_aluno(frame_inferior, 0.02, 0.06, width=0.10)
        self.entry_aluno_nome = self.criar_entry_aluno(frame_inferior, 0.13, 0.06, width=0.30)
        self.entry_aluno_data_nascimento = self.criar_entry_aluno(frame_inferior, 0.44, 0.06)
        
        self.lista_disc = ttk.Treeview(frame_meio, height=3, columns=("col1", "col2", "col3", "col4"))
        self.lista_aluno = ttk.Treeview(frame_inferior, height=3, columns=("col1", "col2", "col3"))
        self.configurar_lista_disc(frame_meio)
        self.configurar_lista_aluno(frame_inferior)
        
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
    
    def criar_entry(self, parent, x, y, width=0.23, height=0.15):
        entry = Entry(
            parent, font=self.estilos['entry_font'],
            foreground=self.estilos['entry_fg'], background=self.estilos['entry_bg'],
            border=2, highlightbackground=self.estilos['entry_bg']
        )
        entry.place(relx=x, rely=y, relwidth=width, relheight=height)
        return entry

    def criar_entry_aluno(self, parent, x, y, width=0.15, height=0.08):
        entry = Entry(
            parent, font=self.estilos['entry_font'],
            foreground=self.estilos['entry_fg'], background=self.estilos['entry_bg'],
            border=2, highlightbackground=self.estilos['entry_bg']
        )
        entry.place(relx=x, rely=y, relwidth=width, relheight=height)
        return entry
    
    def configurar_lista_disc(self, frame):
        self.lista_disc.heading("#0", text="")
        self.lista_disc.heading("#1", text="MAT.")
        self.lista_disc.heading("#2", text="NOME")
        self.lista_disc.heading("#3", text="TURNO")
        self.lista_disc.heading("#4", text="SALA")
        self.lista_disc.column("#0", width=1)
        self.lista_disc.column("#1", width=50)
        self.lista_disc.column("#2", width=350)
        self.lista_disc.column("#3", width=75)
        self.lista_disc.column("#4", width=75)
        self.lista_disc.place(relx=0, rely=0.01, relwidth=0.98, relheight=0.90)
        
        scrool_disc_x = Scrollbar(frame, orient="horizontal", command=self.lista_disc.xview)
        scrool_disc_x.place(relx=0, rely=0.90, relwidth=0.98, relheight=0.1)
        self.lista_disc.configure(xscrollcommand=scrool_disc_x.set)
        
        scrool_disc_y = Scrollbar(frame, orient="vertical", command=self.lista_disc.yview)
        scrool_disc_y.place(relx=0.98, rely=0.01, relwidth=0.02, relheight=0.99)
        self.lista_disc.configure(yscrollcommand=scrool_disc_y.set)
        
        self.lista_disc.bind("<Double-1>", self.on_double_click)
        self.lista_disc.bind("<Return>", self.on_double_click)
        self.lista_disc.bind("<Shift Delete>", self.on_shift_del)
    
    def configurar_lista_aluno(self, frame):
        self.lista_aluno.heading("#0", text="")
        self.lista_aluno.heading("#1", text="MAT.")
        self.lista_aluno.heading("#2", text="NOME")
        self.lista_aluno.heading("#3", text="DATA_NASC.")
        self.lista_aluno.column("#0", width=1)
        self.lista_aluno.column("#1", width=50)
        self.lista_aluno.column("#2", width=400)
        self.lista_aluno.column("#3", width=100)
        self.lista_aluno.place(relx=0, rely=0.25, relwidth=0.98, relheight=0.71)
        
        scrool_aluno_x = Scrollbar(frame, orient="horizontal", command=self.lista_aluno.xview)
        scrool_aluno_x.place(relx=0, rely=0.96, relwidth=0.98, relheight=0.04)
        self.lista_aluno.configure(xscrollcommand=scrool_aluno_x.set)
        
        scrool_aluno_y = Scrollbar(frame, orient="vertical", command=self.lista_aluno.yview)
        scrool_aluno_y.place(relx=0.98, rely=0.25, relwidth=0.02, relheight=0.75)
        self.lista_aluno.configure(yscrollcommand=scrool_aluno_y.set)
        
        self.lista_aluno.bind("<Double-1>", self.on_double_click_aluno)
        self.lista_aluno.bind("<Return>", self.on_double_click_aluno)
    
    def listagem(self):
        self.limpar_lista_disc()
        for disciplina in self.service.listar():
            self.lista_disc.insert("", END, values=(
                disciplina.get_matricula(),
                disciplina.get_nome(),
                disciplina.get_turno(),
                disciplina.get_sala()
            ))
    
    def listagem_aluno(self, matricula):
        self.limpar_lista_aluno()
        matriculados = self.service.listar_matriculados(matricula)
        if matriculados:
            for aluno in matriculados:
                self.lista_aluno.insert("", END, values=(
                    aluno.get_matricula(),
                    aluno.get_nome(),
                    aluno.get_data_nascimento()
                ))
    
    def buscar(self) -> None:
        matricula = self.entry_matricula.get()
        nome = self.entry_nome.get()
        if matricula:
            self.limpar()
            disciplina = self.service.buscar_por_matricula(matricula=matricula)
            if disciplina:
                self.entry_matricula.insert(END, disciplina.get_matricula())
                self.entry_nome.insert(END, disciplina.get_nome())
                self.entry_turno.insert(END, disciplina.get_turno())
                self.entry_sala.insert(END, disciplina.get_sala())
                self.listagem_aluno(matricula)
            else:
                return messagebox.showerror("ATENÇÃO!", "Digite uma matricula valida, nenhuma disciplina foi encontrada.")
        elif nome:
            self.limpar_aluno()
            for item in self.lista_disc.get_children():
                self.lista_disc.delete(item)
            for item in self.lista_aluno.get_children():
                self.lista_aluno.delete(item)
            disciplinas = self.service.buscar_por_nome(nome)
            if disciplinas:
                for disciplina in disciplinas:
                    self.lista_disc.insert("", END, values=(
                        disciplina.get_matricula(),
                        disciplina.get_nome(),
                        disciplina.get_turno(),
                        disciplina.get_sala()))
            else:
                return messagebox.showerror("ATENÇÃO!", "Digite um nome valido, nenhum aluno foi encontrado.")
        else:
            return messagebox.showerror("ATENÇÃO!", "Digite uma matricula ou nome validos, nenhum aluno foi encontrado.")
    
    def buscar_aluno(self) -> None:
        matruicula_aluno = self.entry_aluno_matricula.get()
        if matruicula_aluno:
            self.limpar_aluno()
            aluno = self.service_aluno.buscar_por_matricula(matruicula_aluno)
            if aluno:
                self.entry_aluno_matricula.insert(END, aluno.get_matricula())
                self.entry_aluno_nome.insert(END, aluno.get_nome())
                self.entry_aluno_data_nascimento.insert(END, aluno.get_data_nascimento())
            else:
                return messagebox.showerror("ATENÇÃO!", "Digite uma matricula valida, nenhum aluno foi encontrado.")
            
        else: return messagebox.showerror("ATENÇÃO!", "Digite uma matricula valida, nenhum aluno foi encontrado.")
        
    def limpar(self) -> None:
        self.entry_matricula.delete(0, END)
        self.entry_nome.delete(0,END)
        self.entry_turno.delete(0, END)
        self.entry_sala.delete(0, END)
        self.limpar_aluno()
        self.limpar_lista_aluno()
        self.listagem()
        
    def limpar_aluno(self) -> None:
        self.entry_aluno_matricula.delete(0, END)
        self.entry_aluno_nome.delete(0,END)
        self.entry_aluno_data_nascimento.delete(0, END)
    
    def limpar_lista_disc(self) -> None:
        for item in self.lista_disc.get_children():
            self.lista_disc.delete(item)
    
    def limpar_lista_aluno(self) -> None:
        for item in self.lista_aluno.get_children():
            self.lista_aluno.delete(item)
    
    def adicionar(self) -> None:
        nome = self.entry_nome.get()
        turno = self.entry_turno.get()
        sala = self.entry_sala.get()
        msg = self.service.adicionar(nome=nome, turno=turno, sala=sala)
        self.listagem()
        return messagebox.showinfo(message="Disciplina adicionada com sucesso." if msg else "Dados invalidos, favor digitar dados validos.")
    
    def atualizar(self) -> None:
        matricula = self.entry_matricula.get()
        nome = self.entry_nome.get()
        turno = self.entry_turno.get()
        sala = self.entry_sala.get()
        if matricula and nome and turno and sala:
            self.service.atualizar(matricula=matricula, nome=nome, turno=turno, sala=sala, alunos=[])
            self.limpar()
            return messagebox.showinfo(message="Disciplina atualizado com sucesso.")
        else:
            return messagebox.showinfo(message="Selecione uma disciplina da listagem.")
    
    def excluir(self) -> None:
        matricula = self.entry_matricula.get()
        if messagebox.askyesno(title="EXCLUIR", message=f"Deseja realmente excluir o aluno com a matricula '{matricula}'?"):
            self.service.excluir(matricula=matricula)
            self.limpar()
            return messagebox.showinfo(message="A disciplina foi excluida.")
        else:
            return messagebox.showinfo(message="O aluno não foi excluido.")
    
    def matricular(self):
        matricula = self.entry_matricula.get()
        matricula_aluno = self.entry_aluno_matricula.get()
        if matricula_aluno is None:
            self.limpar_aluno()
            return messagebox.showinfo(message="Matricula do alunos é invalida.")
        if matricula is None:
            self.limpar()
            return messagebox.showinfo(message="Matricula da disciplina é invalida.")
        msg = self.service.matricular(matricula_disciplina=matricula, matricula_aluno=matricula_aluno)
        self.limpar_aluno()
        self.listagem_aluno(matricula=matricula)
        return messagebox.showinfo(message=msg)
        
    def desmatricular(self):
        matricula = self.entry_matricula.get()
        matricula_aluno = self.entry_aluno_matricula.get()
        if matricula_aluno is None:
            self.limpar_aluno()
            return messagebox.showinfo(message="Matricula do alunos é invalida.")
        if matricula is None:
            self.limpar()
            return messagebox.showinfo(message="Matricula da disciplina é invalida.")
        msg = self.service.desmatricular(matricula_disciplina=matricula, matricula_aluno=matricula_aluno)
        self.limpar_aluno()
        self.listagem_aluno(matricula=matricula)
        return messagebox.showinfo(message=msg)
    
    def on_shift_del(self, event) -> None:
        indice = self.lista_disc.selection()
        item = self.lista_disc.item(indice, "values")
        matricula = item[0]
        if messagebox.askyesno(title="EXCLUIR", message=f"Deseja realmente excluir a disciplina com a matricula '{matricula}'?"):
            self.service.excluir(matricula=matricula)
            self.limpar()
            return messagebox.showinfo(message="A disciplina foi excluida.")
        else:
            return messagebox.showinfo(message="A disciplina não foi excluida.")
    
    def on_double_click(self, event) -> None:
        indice = self.lista_disc.selection()
        itens = self.lista_disc.item(indice, "values")
        if itens and indice:
            self.limpar()
            self.listagem_aluno(itens[0])
            self.entry_matricula.insert(END, itens[0])
            self.entry_nome.insert(END, itens[1])
            self.entry_turno.insert(END, itens[2])
            self.entry_sala.insert(END, itens[3])
    
    def on_double_click_aluno(self, event) -> None:
        indice = self.lista_aluno.selection()
        itens = self.lista_aluno.item(indice, "values")
        if itens and indice:
            self.limpar_aluno()
            self.entry_aluno_matricula.insert(END, itens[0])
            self.entry_aluno_nome.insert(END, itens[1])
            self.entry_aluno_data_nascimento.insert(END, itens[2])
