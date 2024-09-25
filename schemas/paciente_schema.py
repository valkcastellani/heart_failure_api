from pydantic import BaseModel
from typing import Optional, List
from model.paciente import Paciente
import json
import numpy as np


class PacienteSchema(BaseModel):
    """Define como um novo paciente a ser inserido deve ser representado"""

    nome: str = "John Connor"
    age: int = 42
    sex: int = 0
    dor: int = 3
    pressao: int = 105
    colesterol: int = 0
    glicemia: int = 1
    eletro: int = 0
    frecmax: int = 128
    angina: int = 0
    depressao: float = -1.5
    inclinacao: int = 2


class PacienteViewSchema(BaseModel):
    """Define como um paciente será retornado"""

    id: int = 1
    nome: str = "John Connor"
    age: int = 42
    sex: int = 0
    dor: int = 3
    pressao: int = 105
    colesterol: int = 0
    glicemia: int = 1
    eletro: int = 0
    frecmax: int = 128
    angina: int = 0
    depressao: float = -1.5
    inclinacao: int = 2
    doenca: int = 0


class PacienteBuscaSchema(BaseModel):
    """Define como deve ser a estrutura que representa a busca.
    Ela será feita com base no id do paciente.
    """

    id: int = 1


class ListaPacientesSchema(BaseModel):
    """Define como uma lista de pacientes será representada"""

    pacientes: List[PacienteSchema]


class PacienteDelSchema(BaseModel):
    """Define como um paciente para deleção será representado"""

    nome: str = "John Connor"


# Apresenta apenas os dados de um paciente
def apresenta_paciente(paciente: Paciente):
    """Retorna uma representação do paciente seguindo o schema definido em
    PacienteViewSchema.
    """
    return {
        "id": paciente.id,
        "nome": paciente.nome,
        "age": paciente.age,
        "sex": paciente.sex,
        "dor": paciente.dor,
        "pressao": paciente.pressao,
        "colesterol": paciente.colesterol,
        "glicemia": paciente.glicemia,
        "eletro": paciente.eletro,
        "frecmax": paciente.frecmax,
        "angina": paciente.angina,
        "depressao": paciente.depressao,
        "inclinacao": paciente.inclinacao,
        "doenca": paciente.doenca,
    }


# Apresenta uma lista de pacientes
def apresenta_pacientes(pacientes: List[Paciente]):
    """Retorna uma representação do paciente seguindo o schema definido em
    PacienteViewSchema.
    """
    result = []
    for paciente in pacientes:
        result.append(
            {
                "id": paciente.id,
                "nome": paciente.nome,
                "age": paciente.age,
                "sex": paciente.sex,
                "dor": paciente.dor,
                "pressao": paciente.pressao,
                "colesterol": paciente.colesterol,
                "glicemia": paciente.glicemia,
                "eletro": paciente.eletro,
                "frecmax": paciente.frecmax,
                "angina": paciente.angina,
                "depressao": paciente.depressao,
                "inclinacao": paciente.inclinacao,
                "doenca": paciente.doenca,
            }
        )

    return {"pacientes": result}
