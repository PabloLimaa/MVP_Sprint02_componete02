from pydantic import BaseModel
from typing import Optional, List
from models.agendamentos import Agendamento
from models.usuario import Usuario

class AgendamentoSchema(BaseModel):
    """ Define como um novo agendamento a ser inserido deve ser representado
    """
    usuario_id: int = 1
    barbeiro_corte: str = "Carlos Henrique"
    data_corte: str = "14/10/2024"
    horario_corte: str = "10:00"
    tipo_corte: str = "Máquina e Tesoura"
    valor_corte: float = 50.0


class AgendamentoViewSchema(BaseModel):
    """ Define como um agendamento será retornado.
    """
    usuario_id: int = 1
    barbeiro_corte: str = "Carlos Henrique"
    data_corte: str = "10/10/2024"
    horario_corte: str = "10:00"
    tipo_corte: str = "Máquina e Tesoura"
    valor_corte: float = 50.0

def apresenta_agendamento(agendamento: Agendamento):
    """ Retorna uma representação do agendamento seguindo o schema definido em
    
    AgendamentoViewSchema.
    """
    return {
        "usuario_id": agendamento.usuario_id,
        "barbeiro_corte": agendamento.barbeiro_corte,
        "data_corte": agendamento.data_corte,
        "horario_corte": agendamento.horario_corte,
        "tipo_corte": agendamento.tipo_corte,
        "valor_corte": agendamento.valor_corte,
    }


