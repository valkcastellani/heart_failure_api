from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import *
from logger import logger
from schemas import *
from flask_cors import CORS


# Instanciando o objeto OpenAPI
info = Info(title="Heart Failure API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# Definindo tags para agrupamento das rotas
home_tag = Tag(
    name="Documentação",
    description="Seleção de documentação: Swagger, Redoc ou RapiDoc",
)

paciente_tag = Tag(
    name="Paciente",
    description="Adição, visualização, remoção e predição de pacientes com doença cardíaca",
)


# Rota home
@app.get("/", tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação."""
    return redirect("/openapi")


# Rota de listagem de pacientes
@app.get(
    "/paciente",
    tags=[paciente_tag],
    responses={"200": PacienteViewSchema, "404": ErrorSchema},
)
def get_pacientes():
    """Lista todos os pacientes cadastrados na base
    Args:
       none

    Returns:
        list: lista de pacientes cadastrados na base
    """
    logger.debug("Coletando dados sobre todos os pacientes")
    # Criando conexão com a base
    session = Session()
    # Buscando todos os pacientes
    pacientes = session.query(Paciente).all()

    if not pacientes:
        # Se não houver pacientes
        return {"pacientes": []}, 200
    else:
        logger.debug(f"%d pacientes econtrados" % len(pacientes))
        print(pacientes)
        return apresenta_pacientes(pacientes), 200


# Métodos baseados por id
# Rota de busca de paciente por id
@app.get(
    "/paciente/<id>",
    tags=[paciente_tag],
    responses={"200": PacienteViewSchema, "404": ErrorSchema},
)
def get_paciente(path: PacienteBuscaSchema):
    """Faz a busca por um paciente cadastrado na base a partir do nome

    Args:
        id (int): id do paciente

    Returns:
        dict: representação do paciente e diagnóstico associado
    """

    logger.debug(f"Coletando dados sobre paciente de ID #{path.id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    paciente = session.query(Paciente).filter(Paciente.id == path.id).first()

    if not paciente:
        # se o paciente não foi encontrado
        error_msg = "Paciente não encontrado na base :/"
        logger.warning(f"Erro ao buscar paciente de ID #'{path.id}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Paciente encontrado: '{paciente.nome}'")
        # retorna a representação de paciente
        return apresenta_paciente(paciente), 200


# Rota de adição de paciente
@app.post(
    "/paciente",
    tags=[paciente_tag],
    responses={"200": PacienteViewSchema, "400": ErrorSchema, "409": ErrorSchema},
)
def predict(form: PacienteSchema):
    """Adiciona um novo paciente à base de dados
    Retorna uma representação dos pacientes e diagnósticos associados.

    Args:
        nome        (str): Nome do paciente
        age         (int): Idade do paciente [anos]
        sex         (int): Sexo do paciente [0: Masculino, 1: Feminino]
        dor         (int): Tipo de dor no peito [0: TA - Angina Típica, 1: ATA - Angina Atípica, 2: NAP - Dor Não Anginosa, 3: ASY - Assintomático]
        pressao     (int): Pressão arterial em repouso [mm Hg]
        colesterol  (int): Colesterol sérico [mm/dl]
        glicemia    (int): Glicemia de jejum [1: se FastingBS > 120 mg/dl, 0: caso contrário]
        eletro      (int): Resultados do eletrocardiograma de repouso [0: Normal - Normal, 1: ST - anomalia da onda ST-T (inversões da onda T e/ou elevação ou depressão do ST > 0.05 mV), 2: LVH - mostrando possível ou definida hipertrofia ventricular esquerda pelos critérios de Estes]
        frecmax     (int): Frequência cardíaca máxima atingida [Valor numérico entre 60 e 202]
        angina      (int): Angina induzida por exercício [0: Y - Sim, 1: N - Não]
        depressao (float): Valor de depressão do segmento ST [Valor numérico medido em depressão]
        inclinacao  (int): Inclinação do segmento ST durante o pico de exercício [0: Up - inclinação ascendente, 1: Flat - plana, 2: Down - inclinação descendente]

    Returns:
        dict: representação do paciente e diagnóstico associado
    """

    # Recuperando os dados do formulário
    nome = form.nome
    age = form.age
    sex = form.sex
    dor = form.dor
    pressao = form.pressao
    colesterol = form.colesterol
    glicemia = form.glicemia
    eletro = form.eletro
    frecmax = form.frecmax
    angina = form.angina
    depressao = form.depressao
    inclinacao = form.inclinacao

    # Preparando os dados para o modelo
    X_input = PreProcessador.preparar_form(form)

    # Carregando modelo
    model_path = "./MachineLearning/pipelines/rf_heart_failures_pipeline.pkl"

    # modelo = Model.carrega_modelo(ml_path)
    modelo = Pipeline.carrega_pipeline(model_path)

    # Realizando a predição
    doenca = int(Model.preditor(modelo, X_input)[0])

    paciente = Paciente(
        nome=nome,
        age=age,
        sex=sex,
        dor=dor,
        pressao=pressao,
        colesterol=colesterol,
        glicemia=glicemia,
        eletro=eletro,
        frecmax=frecmax,
        angina=angina,
        depressao=depressao,
        inclinacao=inclinacao,
        doenca=doenca
    )
    logger.debug(f"Adicionando paciente de nome: '{paciente.nome}'")

    try:
        # Criando conexão com a base
        session = Session()

        # Checando se paciente já existe na base
        if session.query(Paciente).filter(Paciente.nome == form.nome).first():
            error_msg = "Paciente já existente na base :/"
            logger.warning(f"Erro ao adicionar paciente '{paciente.nome}', {error_msg}")
            return {"message": error_msg}, 409

        # Adicionando paciente
        session.add(paciente)
        # Efetivando o comando de adição
        session.commit()
        # Concluindo a transação
        logger.debug(f"Adicionado paciente de nome: '{paciente.nome}'")
        return apresenta_paciente(paciente), 200

    # Caso ocorra algum erro na adição
    except Exception as e:
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar paciente '{paciente.nome}', {error_msg}")
        return {"message": error_msg}, 400


# Rota de remoção de paciente por id
@app.delete(
    "/paciente/<id>",
    tags=[paciente_tag],
    responses={"200": PacienteViewSchema, "404": ErrorSchema},
)
def delete_paciente(path: PacienteBuscaSchema):
    """Remove um paciente cadastrado na base a partir do id

    Args:
        id (int): nome do paciente

    Returns:
        msg: Mensagem de sucesso ou erro
    """

    logger.debug(f"Deletando dados sobre paciente # {path.id}")

    # Criando conexão com a base
    session = Session()

    # Buscando paciente
    paciente = session.query(Paciente).filter(Paciente.id == path.id).first()

    if not paciente:
        error_msg = "Paciente não encontrado na base :/"
        logger.warning(f"Erro ao deletar paciente de ID '{path.id}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        session.delete(paciente)
        session.commit()
        logger.debug(f"Deletado paciente #{paciente.nome}")
        return {"message": f"Paciente {paciente.nome} removido com sucesso!"}, 200


if __name__ == "__main__":
    app.run(debug=True)
