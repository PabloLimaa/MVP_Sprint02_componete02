from pydantic import BaseModel
from typing import Optional, List
from models.usuario import Usuario
from models.agendamentos import Agendamento

class UsuarioSchema(BaseModel):
    """ Define como um novo usuario a ser inserido deve ser representado
    """
    nome: str = "Pablo Lima"
    email: str = "pablo@gmail.com"
    senha: str = "123456"

class UsuarioViewSchema(BaseModel):
    """ Define como um usuario será retornado.
    """
    id: int = 1
    nome: str = "Pablo Lima"
    email: str = "pablo@gmail.com"

class UsuarioBuscaPorEmailSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
    
    feita apenas com base no email do usuario.
    """
    termo: str = "pablo@gmail.com"


class UsuarioBuscaPorIDSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
    
    feita apenas com base no ID do usuario.
    """
    usuario_id: int = 1

class ListagemUsuariosSchema(BaseModel):
    """ Define como uma listagem de usuarios será retornada.
    """
    usuarios:List[UsuarioViewSchema]


def apresenta_usuarios(usuarios: List[Usuario]):
    """ Retorna uma representação do usuario seguindo o schema definido em
    
    ListagemUsuariosSchema.
    """
    result = []
    for usuario in usuarios:
        result.append({
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
        })

    return {"usuarios": result}


class UsuarioDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
    
    de remoção.
    """
    mesage: str
    nome: str
    

def apresenta_usuario(usuario: Usuario):
    """ Retorna uma representação do usuario seguindo o schema definido em
    
    UsuarioViewSchema.
    """
    return {
        "id": usuario.id,
        "nome": usuario.nome,
        "email": usuario.email,  
    }
