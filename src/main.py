from ttkbootstrap import Window
from ttkbootstrap.constants import *
from ttkbootstrap.widgets import Notebook
from views.aluno_view import AlunoView
from views.disciplina_view import DisciplinaView

class Aplicacao:
    def __init__(self) -> None:
        self.janela = Window(themename="flatly")  # Você pode mudar o tema aqui (ex: "darkly", "superhero", etc.)
        self.janela.title("Gestão Acadêmica")
        self.janela.geometry("650x600")
        self.janela.resizable(True, True)

        # Criar abas com estilo do ttkbootstrap
        self.abas = Notebook(self.janela, bootstyle="info")
        self.abas.pack(fill="both", expand=True)

        # Instanciar telas
        self.aluno_view = AlunoView(self.abas)
        self.disciplina_view = DisciplinaView(self.abas)

        self.janela.mainloop()

if __name__ == "__main__":
    Aplicacao()
