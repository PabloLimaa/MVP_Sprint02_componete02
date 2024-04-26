from sqlalchemy import Column, String, Integer, DateTime, Float, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  models import Base, Agendamento

class Usuario(Base):

    # Comentário de aula: a tabela no banco pode seguir um menemônico e 
    # ter um nome diferente do que poderia ser "mais apropriado". Aqui 
    # a tabela que vai representar o produto, se chama 'usuario_lista',
    # supondo o cenário em que o sufixo "usuario" é utilizado para 
    # indicar que é uma tabela de Usuarios.
    __tablename__ = 'usuario_lista'

    # O nome de uma coluna também pode ter no banco um nome diferente
    # como é apresentado aqui no caso do Usuario.id que no banco será 
    # usuario_lista.pk_usuario, o sufixo pk está sendo utilizado para 
    # indicar que é uma chave primária
    id = Column("pk_usuario", Integer, primary_key=True)

    # Supondo que os atributos seguintes já estejam em conformidade
    # com o menemônico adotado pela empresa, então não há necessidade
    # de fazer a definição de um "nome" de coluna diferente.
    nome = Column(String(140))  # 140 é o número máximo de caracteres
    email = Column(String(255), unique=True, nullable=False)
    senha = Column(String(150), nullable=False)

    # A data de inserção será o instante de inserção caso não tenha
    # um valor definido pelo usuário
    data_insercao = Column(DateTime, default=datetime.now())

    # Criando um requisito de unicidade envolvendo uma par de informações
    __table_args__ = (UniqueConstraint("email", "senha", name="usuario_unique_id"),)

    # Estabelecendo o relacionamento entre usuario e agendamento
    agendamentos = relationship('Agendamento')

    def __init__(self, nome, email, senha,
                 data_insercao:Union[DateTime, None] = None):
        """
        Cria um usuario

        Arguments:
            nome: nome do usuario.
            email: email do usuario.
            senha: senha do usuario.
            data_insercao: data de quando o usuario foi inserido à base
        """
        self.nome = nome
        self.email = email
        self.senha = senha

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao

    def to_dict(self):
        """
        Retorna a representação em dicionário do Objeto usuario.
        """
        return{
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "senha": self.senha,
            "data_insercao": self.data_insercao,
            "agendamentos": [c.to_dict() for c in self.agendamentos]
        }

    def __repr__(self):
        """
        Retorna uma representação do Usuario em forma de texto.
        """
        return f"User(id={self.id}, nome='{self.nome}', email={self.email}, senha='{self.senha}')"

    def adiciona_agendamento(self, agendamentos:Agendamento):
        """ 
        Adiciona um novo agendamento para o Usuario
        """
        self.agendamentos.append(agendamentos)
