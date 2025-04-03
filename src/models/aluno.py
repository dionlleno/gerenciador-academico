from datetime import date

class Aluno():
    def __init__(self, nome: str,  data_nascimento: date, matricula: int = None):
        self.__matricula: int = matricula
        self.__nome: str = nome
        self.__data_nascimento: date = data_nascimento
    
    def get_matricula(self) -> int:
        return self.__matricula
    
    def set_matricula(self, matricula: int) -> None:
        self.__matricula = matricula
        
    def get_nome(self) -> str:
        return self.__nome
    
    def set_nome(self, nome: str) -> None:
        self.__nome = nome
        
    def get_data_nascimento(self) -> str:
        return self.__data_nascimento
    
    def set_data_nascimento(self, data_nascimento: str ) -> None:
        self.__data_nascimento = data_nascimento
    
    def __repr__(self) -> str:
        return f"Aluno('{self.__matricula}', '{self.__nome}', '{self.__data_nascimento}')"

    def __str__(self) -> str:
        return (
            "+------- Dados do Aluno -------+\n|\n"
            f"|  Matrícula:          {self.__matricula}\n"
            f"|  Nome:               {self.__nome}\n"
            f"|  Data de Nascimento: {self.__data_nascimento}"
            f"|\n+--------------------------+"
        )