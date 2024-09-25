from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from model import Base

# colunas = Age,Sex,ChestPainType,RestingBP,Cholesterol,FastingBS,RestingECG,MaxHR,ExerciseAngina,Oldpeak,ST_Slope,HeartDisease


class Paciente(Base):
    __tablename__ = "pacientes"

    id = Column("pk_paciente", Integer, primary_key=True)
    nome = Column("Name", String(50), nullable=False)
    age = Column("Age", Integer)
    sex = Column("Sex", Integer, nullable=False)  # Sexo = {"Masculino": 0, "Feminino": 1}
    dor = Column("ChestPainType", Integer)
    pressao = Column("RestingBP", Integer)
    colesterol = Column("Cholesterol", Integer)
    glicemia = Column("FastingBS", Integer)
    eletro = Column("RestingECG", Integer)
    frecmax = Column("MaxHR", Integer)
    angina = Column("ExerciseAngina", Integer)
    depressao = Column("Oldpeak", Float)
    inclinacao = Column("ST_Slope", Integer)
    doenca = Column("HeartDisease", Integer, nullable=True)
    data_insercao = Column(DateTime, default=datetime.now())

    def __init__(
        self,
        nome: str,
        age: int,
        sex: int,
        dor: int,
        pressao: int,
        colesterol: int,
        glicemia: int,
        eletro: int,
        frecmax: int,
        angina: int,
        depressao: float,
        inclinacao: int,
        doenca: Union[int, None] = None,
        data_insercao: Union[DateTime, None] = None
    ):
        """
        Cria um Paciente

        Arguments:
            nome: Nome do paciente
            age: Idade do paciente [anos]
            sex: Sexo do paciente [0: Masculino, 1: Feminino]
            dor: Tipo de dor no peito [0: TA - Angina Típica, 1: ATA - Angina Atípica, 2: NAP - Dor Não Anginosa, 3: ASY - Assintomático]
            pressao: Pressão arterial em repouso [mm Hg]
            colesterol: Colesterol sérico [mm/dl]
            glicemia: Glicemia de jejum [1: se FastingBS > 120 mg/dl, 0: caso contrário]
            eletro: Resultados do eletrocardiograma de repouso [0: Normal - Normal, 1: ST - anomalia da onda ST-T (inversões da onda T e/ou elevação ou depressão do ST > 0.05 mV), 2: LVH - mostrando possível ou definida hipertrofia ventricular esquerda pelos critérios de Estes]
            frecmax: Frequência cardíaca máxima atingida [Valor numérico entre 60 e 202]
            angina: Angina induzida por exercício [0: Y - Sim, 1: N - Não]
            depressao: Valor de depressão do segmento ST [Valor numérico medido em depressão]
            inclinacao: Inclinação do segmento ST durante o pico de exercício [0: Up - inclinação ascendente, 1: Flat - plana, 2: Down - inclinação descendente]
            doenca: Classe de saída [1: doença cardíaca, 0: Normal]
            data_insercao: data de quando o paciente foi inserido à base
        """
        self.nome = nome
        self.age = age
        self.sex = sex
        self.dor = dor
        self.pressao = pressao
        self.colesterol = colesterol
        self.glicemia = glicemia
        self.eletro = eletro
        self.frecmax = frecmax
        self.angina = angina
        self.depressao = depressao
        self.inclinacao = inclinacao
        self.doenca = doenca

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao
