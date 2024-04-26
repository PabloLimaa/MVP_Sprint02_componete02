from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from models import Session, Usuario, Agendamento
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
usuario_tag = Tag(name="Usuario", description="Criação de um novo usuário no banco de dados")
agendamento_tag = Tag(name="Agendamento", description="Adição de um agendamento de corte por um usuário no banco de dados")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/usuario', tags=[usuario_tag],
          responses={"200": UsuarioViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_usuario(form: UsuarioSchema):
    """Adiciona um novo Usuario à base de dados

    Retorna uma representação dos usuarios e agendamentos associados.
    """
    print(form)
    usuario = Usuario(
        nome=form.nome,
        email=form.email,
        senha=form.senha,
    )
    
    try:
        # criando conexão com a base
        session = Session()
        # adicionando usuario
        session.add(usuario)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        return apresenta_usuario(usuario), 200
    
    except IntegrityError as e:
        # como a duplicidade do email é a provável razão do IntegrityError
        error_msg = "Usuario de mesmo email e senha já salvo na base :/"
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        return {"mesage": error_msg}, 400

@app.get('/usuarios', tags=[usuario_tag],
         responses={"200": ListagemUsuariosSchema, "404": ErrorSchema})
def get_usuarios():
    """Faz a busca por todos os Usuarios cadastrados

    Retorna uma representação da listagem de usuarios.
    """
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    usuarios = session.query(Usuario).all()

    if not usuarios:
        # se não há usuarios cadastrados
        return {"usuarios": []}, 200
    else:
        # retorna a representação de usuario
        return apresenta_usuarios(usuarios), 200


@app.get('/usuario', tags=[usuario_tag],
         responses={"200": UsuarioViewSchema, "404": ErrorSchema})
def get_usuario(query: UsuarioBuscaPorIDSchema):
    """Faz a busca por um Usuario a partir do id do usuario

    Retorna uma representação dos usuarios e agendamentos associados.
    """
    usuario_id = query.usuario_id
    logger.info(f"Coletando dados sobre usuario #{usuario_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    usuario = session.query(Usuario).filter(Usuario.id == usuario_id).first()

    if not usuario:
        # se o usuario não foi encontrado
        error_msg = "Usuario não encontrado na base :/"
        logger.warning(f"Erro ao buscar usuario '{usuario_id}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.info("Usuario econtrado: %s" % usuario)
        # retorna a representação de usuario
        return apresenta_usuario(usuario), 200


@app.delete('/usuario', tags=[usuario_tag],
            responses={"200": UsuarioDelSchema, "404": ErrorSchema})
def del_usuario(query: UsuarioBuscaPorIDSchema):
    """Deleta um Usuario a partir do ID informado

    Retorna uma mensagem de confirmação da remoção.
    """
    usuario_id = query.usuario_id
    
    session = Session()
    try:
        # Tenta deletar o usuário
        count = session.query(Usuario).filter(Usuario.id == usuario_id).delete()
        session.commit()
        if count:
            return {"message": "Usuario removido com sucesso", "id": usuario_id}
        else:
            return {"message": "Usuario não encontrado na base :/"}, 404
    except Exception as e:
        session.rollback()
        return {"message": "Erro ao deletar o usuário: {}".format(str(e))}, 500
    finally:
        session.close()


@app.post('/agendamento', tags=[agendamento_tag],
          responses={"200": AgendamentoViewSchema, "404": ErrorSchema})
def add_agendamento(form: AgendamentoSchema):
    """Adiciona um novo agendamento de corte feito por um usuário ao banco de dados.
    
    Retorna uma representação do usuário com o novo agendamento adicionado.
    """

    # Validação do ID do usuário
    usuario_id = form.usuario_id

    # Conexão com o banco de dados
    session = Session()

    # Busca pelo usuário
    usuario = session.query(Usuario).filter(Usuario.id == usuario_id).first()

    if not usuario:
         # se usuario não encontrado
        error_msg = "Usuario não encontrado na base"
        return {"mesage": error_msg}, 404

    # # Criação do agendamento
    # agendamento = Agendamento(
    #     id=form.id,
    #     barbeiro_corte=form.barbeiro_corte,
    #     data_corte=form.data_corte,
    #     horario_corte=form.horario_corte,
    #     tipo_corte=form.tipo_corte,
    #     valor_corte=form.valor_corte,
    # )

    # Adiciona o agendamento ao usuário
    # usuario.agendamentos.append(agendamento)

    # session.add(agendamento)
    # session.commit()

    # Retorna a representação do usuário
    return apresenta_usuario(usuario), 200

@app.put('/agendamento/{agendamento_id}', tags=[agendamento_tag],
         responses={"200": AgendamentoSchema, "404": ErrorSchema})
def edit_agendamento(agendamento_id: int, form: AgendamentoSchema):
    """Edita um agendamento de corte existente no banco de dados.

    Retorna a representação do agendamento após a edição.
    """
    # Conexão com o banco de dados
    session = Session()

    # Busca pelo agendamento
    agendamento = session.query(Agendamento).filter(Agendamento.id == agendamento_id).first()

    if not agendamento:
        # se usuario não encontrado
        error_msg = "Agendamento não encontrado na base"
        return {"mesage": error_msg}, 404

    # Atualização dos campos do agendamento
    agendamento.barbeiro_corte = form.barbeiro_corte
    agendamento.data_corte = form.data_corte
    agendamento.horario_corte = form.horario_corte
    agendamento.tipo_corte = form.tipo_corte
    agendamento.valor_corte = form.valor_corte

    session.commit()

    # Retorna a representação do agendamento após a edição
    return agendamento, 200