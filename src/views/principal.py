from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from services.aluno_service import AlunoService
from services.disciplina_service import DisciplinaService

class FuncoesAluno():
    def __init__(self) -> None:
        self.aluno_service = AlunoService()
        
    def aluno_limpar_tela(self) -> None:
        self.entry_aluno_matricula.delete(0, END)
        self.entry_aluno_nome.delete(0, END)
        self.entry_aluno_data_nascimento.delete(0, END)
    
    def aluno_adicionar(self) -> None:
        nome = self.entry_aluno_nome.get()
        data_nascimento = self.entry_aluno_data_nascimento.get()
        self.aluno_service.cadastrar_aluno(nome=nome, data_nascimento=data_nascimento)
        self.aluno_listagem()
    
    def aluno_buscar(self) -> None:
        matricula = self.entry_aluno_matricula.get()
        nome = self.entry_aluno_nome.get()
        if nome:
            self.self.lista_aluno.delete(*self.self.lista_aluno.get_children())
            alunos = self.aluno_service.buscar_aluno_nome(nome)
            for aluno in alunos:
                self.self.lista_aluno.insert("", END, values=(aluno.get_matricula(), aluno.get_nome(), aluno.get_data_nascimento()))
        elif matricula:
            self.aluno_limpar_tela()
            aluno = self.aluno_service.buscar_aluno_matricula(matricula=matricula)
            if aluno:  # Verifica se encontrou um aluno
                self.entry_aluno_matricula.insert(END, aluno.get_matricula())
                self.entry_aluno_nome.insert(END, aluno.get_nome())
                self.entry_aluno_data_nascimento.insert(END, aluno.get_data_nascimento())
        else:
            print("Aluno não encontrado.")
    
    def aluno_atualizar(self) -> None:
        matricula = self.entry_aluno_matricula.get()
        nome = self.entry_aluno_nome.get()
        data_nascimento = self.entry_aluno_data_nascimento.get()
        self.aluno_service.atualizar_aluno(matricula=matricula, novo_nome=nome, nova_data_nascimento=data_nascimento)
        self.aluno_limpar_tela()
        self.aluno_listagem()
    
    def aluno_excluir(self) -> None:
        matricula = self.entry_aluno_matricula.get().strip()
        if not matricula:
            messagebox.showwarning("Aviso", "Informe a matrícula do aluno para excluir.")
            return

        resposta = messagebox.askyesno("Confirmação", "Tem certeza que deseja excluir este aluno?")
        if resposta:
            self.aluno_service.excluir_aluno(matricula=matricula)
            self.aluno_limpar_tela()
            self.aluno_listagem()
    
    def aluno_listagem(self) -> None:
        self.lista_aluno.delete(*self.lista_aluno.get_children())
        alunos = self.aluno_service.listar_alunos()
        for aluno in alunos:
            self.lista_aluno.insert("", END, values=(aluno.get_matricula(), aluno.get_nome(), aluno.get_data_nascimento()))
    
    def aluno_on_double_click(self, event) -> None:
        indice = self.lista_aluno.selection()
        itens = self.lista_aluno.item(indice, 'values')
        self.aluno_limpar_tela()
        self.aluno_entry_matricula.insert(END, itens[0])
        self.aluno_entry_nome.insert(END, itens[1])
        self.aluno_entry_data_nascimento.insert(END, itens[2])

class FuncoesDisciplina():
    def __init__(self) -> None:
        self.disc_service = DisciplinaService()
        
    def disc_limpar_tela(self) -> None:
        self.entry_disc_matricula.delete(0, END)
        self.entry_disc_nome.delete(0, END)
        self.entry_disc_turno.delete(0, END)
        self.entry_disc_sala.delete(0, END)
    
    def disc_adicionar(self) -> None:
        nome = self.entry_disc_nome.get()
        turno = self.entry_disc_turno.get()
        sala = self.entry_disc_sala.get()
        alunos = []
        
        self.disc_service.adicionar_disciplina(nome=nome, turno=turno, sala=sala, alunos=alunos)
        self.disc_listagem()
    
    def disc_buscar(self) -> None:
        matricula = self.entry_disc_matricula.get()
        nome = self.entry_disc_nome.get()
        if nome:
            self.self.lista_disc.delete(*self.self.lista_disc.get_children())
            discs = self.disc_service.obter_disciplina()
            for disc in discs:
                self.self.lista_aluno.insert("", END, values=())
        elif matricula:
            self.disc_limpar_tela()
            disc = self.disc_service.obter_disciplina(matricula=matricula)
            if disc:  # Verifica se encontrou um aluno
                self.entry_disc_matricula.insert(END,)
                self.entry_disc_nome.insert(END,)
        else:
            print("Aluno não encontrado.")
    
    def disc_atualizar(self) -> None:
        matricula = self.entry_disc_matricula.get()
        nome = self.entry_disc_nome.get()
        self.disc_service.atualizar_disciplina()
        self.disc_limpar_tela()
        self.disc_listagem()
    
    def disc_excluir(self) -> None:
        matricula = self.entry_disc_matricula.get().strip()
        if not matricula:
            messagebox.showwarning("Aviso", "Informe a matrícula do aluno para excluir.")
            return

        resposta = messagebox.askyesno("Confirmação", "Tem certeza que deseja excluir este aluno?")
        if resposta:
            self.disc_service.excluir_disciplina(matricula=matricula)
            self.disc_limpar_tela()
            self.disc_listagem()
    
    def disc_listagem(self) -> None:
        self.lista_disc.delete(*self.lista_disc.get_children())
        discs = self.disc_service.listar_disciplinas()
        for disc in discs:
            self.lista_disc.insert("", END, values=())
    
    def disc_on_double_click(self, event) -> None:
        indice = self.lista_disc.selection()
        itens = self.lista_disc.item(indice, 'values')
        self.disc_limpar_tela()
        self.disc_entry_matricula.insert(END, itens[0])
        self.disc_entry_nome.insert(END, itens[1])
        self.disc_entry_data_nascimento.insert(END, itens[2])


class Aplicacao(FuncoesAluno,FuncoesDisciplina):
    def __init__(self) -> None:
        super(FuncoesAluno).__init__()
        super(FuncoesDisciplina).__init__()
        self.janela = Tk()
        self.criar_tela()
        
        self.abas = ttk.Notebook(self.janela)
        self.abas.place(relx=0.00, rely=0.00, relwidth=1.00, relheight=1.00)
        
        self.criar_aba_aluno()
        self.criar_aba_nota()
        
        #self.aluno_listagem()
        #self.disc_listagem()
        self.criar_menu()
        self.janela.mainloop()

    def criar_tela(self) -> None:
        bg_color = "#DFEDF1"
        self.janela.title("Menu Principal")
        self.janela.configure(background=bg_color)
        self.janela.geometry("700x600")
        self.janela.resizable(True, True)
        self.janela.maxsize(width=1000, height=1000)
        self.janela.minsize(width=700, height=700)
        
    def criar_aba_aluno(self) -> None:
        # ABA
        aba_bg_color     = "#DFEDF1"
        aba_bg_highlight = "#00A7F8"
        # BUTTON
        bt_bg_color = "#00A7F8"
        bt_fg_color = "#FFFFFF"
        bt_font  = ("verdana", 10, "bold")
        # FRAME
        fr_bg_color     = "#DFEDF1"
        fr_bg_highlight = "#00A7F8"
        # LABEL
        lb_font       = ("verdana", 10, "bold")
        lb_title_font = ("verdana", 12, "bold")
        lb_bg_color      = "#DFEDF1"
        lb_fg_color      = "#00A7F8"
        # ENTRY -> CAIXA DE ENTRADA DE DADOS
        ent_bg_color     = "#FAFAFA"
        ent_bg_highlight = "#FAFAFA"
        ent_fg_color     = "#666666"
        ent_font   = ("verdana", 10, "bold")
        
        aba_aluno = Frame(self.abas)
        aba_aluno.configure(background=aba_bg_color, highlightthickness=2, highlightcolor=aba_bg_highlight, borderwidth=2)
        self.abas.add(aba_aluno, text="ALUNOS")
        
        
        # FRAME -> SUPERIOR
        frame_superior = Frame(aba_aluno, bd=4, bg=fr_bg_color, highlightbackground=fr_bg_highlight, highlightthickness=2)
        frame_superior.place(relx=0.01,rely=0.01, relwidth=0.98, relheight=0.25)
        # FRAME -> INFERIOR
        frame_inferior = Frame(aba_aluno, bd=4, bg=fr_bg_color, highlightbackground=fr_bg_highlight, highlightthickness=2)
        frame_inferior.place(relx=0.01, rely=0.25, relwidth=0.98, relheight=0.74)
        # BUTTON
        # BUTTON -> BUSCAR UM ITEM
        bt_aluno_buscar    = Button(frame_superior, background=bt_bg_color, font=bt_font, text="BUSCAR", foreground=bt_fg_color, command=self.aluno_buscar)
        bt_aluno_buscar.place(relx=0.27, rely=0.16, relwidth=0.12, relheight=0.15)
        # BUTTON -> LIMPAR CAIXAS DE ENTRADA
        bt_aluno_limpar    = Button(frame_superior, background=bt_bg_color, font=bt_font, bd=2, text="LIMPAR", foreground=bt_fg_color, command=self.aluno_limpar_tela)
        bt_aluno_limpar.place(relx=0.41, rely=0.16, relwidth=0.12, relheight=0.15)
        # BUTTON -> ADICIONAR NOVO ITEM
        bt_aluno_adicionar = Button(frame_superior, background=bt_bg_color, font=bt_font, bd=2, text="ADICIONAR", foreground=bt_fg_color, command=self.aluno_adicionar)
        bt_aluno_adicionar.place(relx=0.60, rely=0.16, relwidth=0.12, relheight=0.15)
        # BUTTON -> ATUALIZAR ITEM
        bt_aluno_atualizar = Button(frame_superior, background=bt_bg_color, font=bt_font, text="ATUALIZAR", foreground=bt_fg_color, command=self.aluno_atualizar)
        bt_aluno_atualizar.place(relx=0.73, rely=0.16, relwidth=0.12, relheight=0.15)
        # BUTTON -> EXCLUIR ITEM
        bt_aluno_excluir   = Button(frame_superior, background=bt_bg_color, font=bt_font, text="EXCLUIR", foreground=bt_fg_color, command=self.aluno_excluir)
        bt_aluno_excluir.place(relx=0.86, rely=0.16, relwidth=0.12, relheight=0.15)
        # LABEL -> MATRICULA
        lb_aluno_matricula       = Label(frame_superior, background=lb_bg_color, font=lb_font, text="MATRICULA:", foreground=lb_fg_color)
        lb_aluno_matricula.place(relx=0.03, rely=0.06)
        # LABEL -> NOME
        lb_aluno_nome            = Label(frame_superior, background=lb_bg_color, font=lb_font, text="NOME:", foreground=lb_fg_color)
        lb_aluno_nome.place(relx=0.03, rely=0.32)
        # LABEL -> DATA_NASCIMENTO
        lb_aluno_data_nascimento = Label(frame_superior, background=lb_bg_color, font=lb_font, text="DATA DE NASCIMENTO:", foreground=lb_fg_color)
        lb_aluno_data_nascimento.place(relx=0.03, rely=0.58)
        # LABEL -> TITULO DOS FRAMES
        lb_aluno_titulo_superior    = Label(frame_superior, background=lb_bg_color, font=lb_title_font, foreground=lb_fg_color, text="ALUNO")
        lb_aluno_titulo_superior.place(relx=0.46, rely=0.00)
        lb_aluno_titulo_inferior    = Label(frame_inferior, background=lb_bg_color, font=lb_title_font, foreground=lb_fg_color, text="LISTA")
        lb_aluno_titulo_inferior.place(relx=0.46, rely=0.23)
        # ENTRY -> MATRICULA
        self.entry_aluno_matricula       = Entry(frame_superior, font=ent_font, foreground=ent_fg_color,background=ent_bg_color, border=2, highlightbackground=ent_bg_highlight)
        self.entry_aluno_matricula.place(relx=0.02, rely=0.16, relwidth=0.15, relheight=0.15)
        # ENTRY -> NOME
        self.entry_aluno_nome            = Entry(frame_superior, font=ent_font, foreground=ent_fg_color,background=ent_bg_color, border=2, highlightbackground=ent_bg_highlight)
        self.entry_aluno_nome.place(relx=0.02, rely=0.42, relwidth=0.23, relheight=0.15)
        # ENTRY -> DATA_NASCIMENTO
        self.entry_aluno_data_nascimento = Entry(frame_superior, font=ent_font, foreground=ent_fg_color,background=ent_bg_color, border=2, highlightbackground=ent_bg_highlight)
        self.entry_aluno_data_nascimento.place(relx=0.02, rely=0.68, relwidth=0.23, relheight=0.15)
        # CAIXA DE LISTAGEM -> LISTAR ALUNOS
        self.lista_aluno = ttk.Treeview(frame_inferior, height=3, columns=("col1", "col2", "col3"))
        ## CAIXA DE LISTAGEM -> DEFININDO CABEÇALHO
        self.lista_aluno.heading("#0", text="")
        self.lista_aluno.heading("#1", text="MATRICULA")
        self.lista_aluno.heading("#2", text="NOME")
        self.lista_aluno.heading("#3", text="DATA_NASC.")
        # CAIXA DE LISTAGEM -> DEFININDO LARGURA
        self.lista_aluno.column("#0", width=1)
        self.lista_aluno.column("#1", width=40)
        self.lista_aluno.column("#2", width=350)
        self.lista_aluno.column("#3", width=109)
        # CAIXA DE LISTAGEM -> DEFININDO POSIÇÂO
        self.lista_aluno.place(relx=0.00, rely=0.00, relwidth=0.98, relheight=1.00)
        # CAIXA DE LISTAGEM -> DEFININDO BARRA DE ROLAGEM
        scrool_list = Scrollbar(frame_inferior, orient="vertical")
        scrool_list.place(relx=0.98, rely=0.00, relwidth=0.02, relheight=1.00)
        self.lista_aluno.configure(yscrollcommand=scrool_list.set)
        self.lista_aluno.bind("<Double-1>", self.aluno_on_double_click)

    def criar_aba_nota(self) -> None:
        # ABA
        aba_bg_color     = "#DFEDF1"
        aba_bg_highlight = "#00A7F8"
        # BUTTON
        bt_bg_color = "#00A7F8"
        bt_fg_color = "#FFFFFF"
        bt_font  = ("verdana", 10, "bold")
        # FRAME
        fr_bg_color     = "#DFEDF1"
        fr_bg_highlight = "#00A7F8"
        # LABEL
        lb_font       = ("verdana", 10, "bold")
        lb_title_font = ("verdana", 12, "bold")
        lb_bg_color      = "#DFEDF1"
        lb_fg_color      = "#00A7F8"
        # ENTRY -> CAIXA DE ENTRADA DE DADOS
        ent_bg_color     = "#FAFAFA"
        ent_bg_highlight = "#FAFAFA"
        ent_fg_color     = "#666666"
        ent_font   = ("verdana", 10, "bold")
        
        aba_nota = Frame(self.abas)
        aba_nota.configure(background=aba_bg_color, highlightthickness=2, highlightcolor=aba_bg_highlight, borderwidth=2)
        self.abas.add(aba_nota, text="NOTAS")
        
        
        # FRAME -> SUPERIOR
        frame_superior = Frame(aba_nota, bd=4, bg=fr_bg_color, highlightbackground=fr_bg_highlight, highlightthickness=2)
        frame_superior.place(relx=0.01,rely=0.01, relwidth=0.98, relheight=0.25)
        # FRAME -> MEIO
        frame_meio = Frame(aba_nota, bd=4, bg=fr_bg_color, highlightbackground=fr_bg_highlight, highlightthickness=2)
        frame_meio.place(relx=0.01, rely=0.25, relwidth=0.98, relheight=0.50)
        # FRAME -> INFERIOR
        frame_inferior = Frame(aba_nota, bd=4, bg=fr_bg_color, highlightbackground=fr_bg_highlight, highlightthickness=2)
        frame_inferior.place(relx=0.01, rely=0.51, relwidth=0.98, relheight=0.74)
        # BUTTON
        # BUTTON -> BUSCAR UM ITEM
        bt_disc_buscar    = Button(frame_superior, background=bt_bg_color, font=bt_font, text="BUSCAR", foreground=bt_fg_color, command=self.disc_buscar)
        bt_disc_buscar.place(relx=0.27, rely=0.16, relwidth=0.12, relheight=0.15)
        # BUTTON -> LIMPAR CAIXAS DE ENTRADA
        bt_disc_limpar    = Button(frame_superior, background=bt_bg_color, font=bt_font, bd=2, text="LIMPAR", foreground=bt_fg_color, command=self.disc_limpar_tela)
        bt_disc_limpar.place(relx=0.41, rely=0.16, relwidth=0.12, relheight=0.15)
        # BUTTON -> ADICIONAR NOVO ITEM
        bt_disc_adicionar = Button(frame_superior, background=bt_bg_color, font=bt_font, bd=2, text="ADICIONAR", foreground=bt_fg_color, command=self.disc_adicionar)
        bt_disc_adicionar.place(relx=0.60, rely=0.16, relwidth=0.12, relheight=0.15)
        # BUTTON -> ATUALIZAR ITEM
        bt_disc_atualizar = Button(frame_superior, background=bt_bg_color, font=bt_font, text="ATUALIZAR", foreground=bt_fg_color, command=self.disc_atualizar)
        bt_disc_atualizar.place(relx=0.73, rely=0.16, relwidth=0.12, relheight=0.15)
        # BUTTON -> EXCLUIR ITEM
        bt_disc_excluir   = Button(frame_superior, background=bt_bg_color, font=bt_font, text="EXCLUIR", foreground=bt_fg_color, command=self.disc_excluir)
        bt_disc_excluir.place(relx=0.86, rely=0.16, relwidth=0.12, relheight=0.15)
        # LABEL -> MATRICULA
        lb_disc_disc_matricula       = Label(frame_superior, background=lb_bg_color, font=lb_font, text="MATRICULA:", foreground=lb_fg_color)
        lb_disc_disc_matricula.place(relx=0.03, rely=0.06)
        # LABEL -> NOME
        lb_disc_disc_nome           = Label(frame_superior, background=lb_bg_color, font=lb_font, text="NOME:", foreground=lb_fg_color)
        lb_disc_disc_nome.place(relx=0.03, rely=0.32)
        # LABEL -> TURNO
        lb_disc_disc_turno = Label(frame_superior, background=lb_bg_color, font=lb_font, text="TURNO:", foreground=lb_fg_color)
        lb_disc_disc_turno.place(relx=0.03, rely=0.58)
        # LABEL -> TURNO
        lb_disc_disc_turno = Label(frame_superior, background=lb_bg_color, font=lb_font, text="SALA:", foreground=lb_fg_color)
        lb_disc_disc_turno.place(relx=0.28, rely=0.58)
        # LABEL -> TITULO DOS FRAMES
        lb_titulo_superior    = Label(frame_superior, background=lb_bg_color, font=lb_title_font, foreground=lb_fg_color, text="DISCIPLINA")
        lb_titulo_superior.place(relx=0.46, rely=0.00)
        lb_titulo_meio    = Label(frame_meio, background=lb_bg_color, font=lb_title_font, foreground=lb_fg_color, text="DISCIPLINAS")
        lb_titulo_meio.place(relx=0.46, rely=0.50)
        lb_titulo_inferior    = Label(frame_inferior, background=lb_bg_color, font=lb_title_font, foreground=lb_fg_color, text="MATRICULADOS")
        lb_titulo_inferior.place(relx=0.46, rely=0.50)
        # ENTRY -> MATRICULA
        entry_disc_matricula       = Entry(frame_superior, font=ent_font, foreground=ent_fg_color,background=ent_bg_color, border=2, highlightbackground=ent_bg_highlight)
        entry_disc_matricula.place(relx=0.02, rely=0.16, relwidth=0.15, relheight=0.15)
        # ENTRY -> NOME
        entry_disc_nome            = Entry(frame_superior, font=ent_font, foreground=ent_fg_color,background=ent_bg_color, border=2, highlightbackground=ent_bg_highlight)
        entry_disc_nome.place(relx=0.02, rely=0.42, relwidth=0.23, relheight=0.15)
        # ENTRY -> TURNO
        entry_disc_turno = Entry(frame_superior, font=ent_font, foreground=ent_fg_color,background=ent_bg_color, border=2, highlightbackground=ent_bg_highlight)
        entry_disc_turno.place(relx=0.02, rely=0.68, relwidth=0.23, relheight=0.15)
        # ENTRY -> SALA
        entry_disc_sala = Entry(frame_superior, font=ent_font, foreground=ent_fg_color,background=ent_bg_color, border=2, highlightbackground=ent_bg_highlight)
        entry_disc_sala.place(relx=0.27, rely=0.68, relwidth=0.23, relheight=0.15)
        
        
        # CAIXA DE LISTAGEM -> LISTAR ALUNOS
        self.lista_disc = ttk.Treeview(frame_meio, height=3, columns=("col1", "col2", "col3", "col4"))
        ## CAIXA DE LISTAGEM -> DEFININDO CABEÇALHO
        self.lista_disc.heading("#0", text="")
        self.lista_disc.heading("#1", text="MATRICULA")
        self.lista_disc.heading("#2", text="NOME")
        self.lista_disc.heading("#3", text="TURNO")
        self.lista_disc.heading("#4", text="SALA")
        # CAIXA DE LISTAGEM -> DEFININDO LARGURA
        self.lista_disc.column("#0", width=1)
        self.lista_disc.column("#1", width=40)
        self.lista_disc.column("#2", width=350)
        self.lista_disc.column("#3", width=55)
        self.lista_disc.column("#3", width=54)
        # CAIXA DE LISTAGEM -> DEFININDO POSIÇÂO
        self.lista_disc.place(relx=0.00, rely=0.00, relwidth=0.98, relheight=1.00)
        # CAIXA DE LISTAGEM -> DEFININDO BARRA DE ROLAGEM
        scrool_list_disc = Scrollbar(frame_inferior, orient="vertical")
        scrool_list_disc.place(relx=0.98, rely=0.00, relwidth=0.02, relheight=1.00)
        self.lista_disc.configure(yscrollcommand=scrool_list_disc.set)
        self.lista_disc.bind("<Double-1>", self.disc_on_double_click)
        
        # CAIXA DE LISTAGEM -> LISTAR ALUNOS
        self.lista_disc_aluno = ttk.Treeview(frame_inferior, height=3, columns=("col1", "col2", "col3"))
        ## CAIXA DE LISTAGEM -> DEFININDO CABEÇALHO
        self.lista_disc_aluno.heading("#0", text="")
        self.lista_disc_aluno.heading("#1", text="MATRICULA")
        self.lista_disc_aluno.heading("#2", text="NOME")
        self.lista_disc_aluno.heading("#3", text="DATA_NASC.")
        # CAIXA DE LISTAGEM -> DEFININDO LARGURA
        self.lista_disc_aluno.column("#0", width=1)
        self.lista_disc_aluno.column("#1", width=40)
        self.lista_disc_aluno.column("#2", width=350)
        self.lista_disc_aluno.column("#3", width=109)
        # CAIXA DE LISTAGEM -> DEFININDO POSIÇÂO
        self.lista_disc_aluno.place(relx=0.00, rely=0.00, relwidth=0.98, relheight=1.00)
        # CAIXA DE LISTAGEM -> DEFININDO BARRA DE ROLAGEM
        scrool_list_disc_aluno = Scrollbar(frame_inferior, orient="vertical")
        scrool_list_disc_aluno.place(relx=0.98, rely=0.00, relwidth=0.02, relheight=1.00)
        self.lista_disc_aluno.configure(yscrollcommand=scrool_list_disc_aluno.set)
        #self.lista_disc_aluno.bind("<Double-1>", self.disc_on_double_click)

    def criar_menu(self) -> None:
        menubar = Menu(self.janela)
        self.janela.config(menu=menubar)
        menu_opcao = Menu(menubar)
        menu_manipulacao = Menu(menubar)
        
        def quit() -> None: self.janela.destroy()
        
        menubar.add_cascade(label="Manipular", menu=menu_manipulacao)
        menubar.add_cascade(label="Opções", menu=menu_opcao)
        menu_opcao.add_command(label="Sair", command=quit)
        menu_manipulacao.add_command(label="Limpar Tela", command=self.aluno_limpar_tela)
