from tkinter import Tk
from tkinter import ttk
from views.aluno_view import AlunoView
from views.disciplina_view import DisciplinaView

class Aplicacao:
    def __init__(self) -> None:
        self.janela = Tk()
        self.janela.title("Gestão Acadêmica")
        self.janela.geometry("650x600")
        self.janela.resizable(False, False)
        
        # Configurar estilo
        self.estilo = ttk.Style()
        self.estilo.theme_use("clam")  # Define um tema moderno

        # Personalizar a aba do Notebook
        self.estilo.configure("TNotebook", background="#FFFFFF", borderwidth=2)

        # Personalizar abas não selecionadas
        self.estilo.configure(
            "TNotebook.Tab",
            background="#DFEDF1",
            foreground="#00A7F8",
            #padding=[10, 5],
            font=("Arial", 10, "bold")
        )

        # Personalizar aba selecionada
        self.estilo.map(
            "TNotebook.Tab",
            background=[("selected", "#00A7F8")],
            foreground=[("selected", "#FFFFFF")],
        )

        # Criar abas
        self.abas = ttk.Notebook(self.janela)
        self.abas.place(relx=0.00, rely=0.00, relwidth=1.00, relheight=1.00)

        # Instanciar telas
        self.aluno_view = AlunoView(self.abas)
        self.disciplina_view = DisciplinaView(self.abas)

        self.janela.mainloop()

if __name__ == "__main__":
    Aplicacao()
