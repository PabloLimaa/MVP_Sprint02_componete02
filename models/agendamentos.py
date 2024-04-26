from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Date, Time, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  models import Base

class Agendamento(Base):

    # A tabela no banco pode seguir um menemônico e 
    # ter um nome diferente do que poderia ser "mais apropriado". Aqui 
    # a tabela que vai representar o agendamento vinculado ao usuario, 
    # que se chama 'usuario_agendamento'.
    __tablename__ = 'usuario_agendamento'

    # Supondo que os atributos seguintes já estejam em conformidade
    # com o menemônico adotado pela empresa, então não há necessidade
    # de fazer a definição de um "nome" de coluna diferente.
    id = Column(Integer, primary_key=True)
    data_insercao = Column(DateTime, default=datetime.now())
    barbeiro_corte = Column(String(255))
    data_corte = Column(String(255))
    horario_corte = Column(String(255))
    tipo_corte = Column(String(100))
    valor_corte = Column(Float)
    

    # Definição do relacionamento entre o agendamento e um usuario.
    # Aqui está sendo definido a coluna 'usuario' que vai guardar
    # a referencia ao usuario, a chave estrangeira que relaciona
    # um usuario ao agendamento.
    usuario_id = Column(Integer, ForeignKey("usuario_lista.pk_usuario"), nullable=False)

    # Estabelecendo o relacionamento entre usuario e agendamento
    usuario = relationship('Usuario')

    def __init__(self, data_corte:Date, data_insercao:Union[DateTime, None] = None):
        """
        Cria um agendamento

        Arguments:
            data_corte: a data de um agendamento.
            data_insercao: data de quando o agendamento foi inserido à base
        """
        self.data_corte = data_corte
        if data_insercao:
            self.data_insercao = data_insercao

    def to_dict(self):
        """
        Retorna a representação em dicionário do Objeto Agendamento.
        """
        return{
            "id": self.id,
            "barbeiro_corte": self.barbeiro_corte,
            "data_corte": self.data_corte,
            "horario_corte": self.horario_corte,
            "tipo_corte": self.tipo_corte,
            "valor_corte": self.valor_corte,
            "data_insercao": self.data_insercao,
            "usuario_id": self.usuario.id
           
        }

    def __repr__(self):
        """
        Retorna uma representação do Agendamento em forma de texto.
        """
        return f"Agendamento(id={self.id}, data_corte='{self.data_corte}')"
