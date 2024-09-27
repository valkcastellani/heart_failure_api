from model import *

# To run: pytest -v test_modelos.py

# Instanciação das Classes
carregador = Carregador()
modelo = Model()
avaliador = Avaliador()

# Parâmetros
url_dadosX = "./MachineLearning/data/X_test_dataset_heart_failures.csv"
colunasX = [
    "Age",
    "Sex",
    "ChestPainType",
    "RestingBP",
    "Cholesterol",
    "FastingBS",
    "RestingECG",
    "MaxHR",
    "ExerciseAngina",
    "Oldpeak",
    "ST_Slope",
]

# Carga dos dados X
datasetX = Carregador.carregar_dados(url_dadosX, colunasX)
arrayX = datasetX.values
X = arrayX[:, :]

# Parâmetros
url_dadosY = "./MachineLearning/data/y_test_dataset_heart_failures.csv"
colunasY = ["HeartDisease"]

# Carga dos dados X
datasetY = Carregador.carregar_dados(url_dadosY, colunasY)
arrayY = datasetY.values
y = arrayY[:, :]

acuracia_desejada = 0.8

# Método para testar o modelo Extra Trees Classifier a partir do arquivo correspondente
def test_modelo_et():
    # Importando o modelo gerado com Extra Trees Classifier
    et_path = "./MachineLearning/models/et_heart_failures_classifier.pkl"
    modelo_et = Model.carrega_modelo(et_path)

    # Obtendo as métricas do modelo gerado com Extra Trees Classifier
    acuracia_et = Avaliador.avaliar(modelo_et, X, y)

    # Testando as métricas do modelo gerado com Extra Trees Classifier
    # Modifique as métricas de acordo com seus requisitos
    assert acuracia_et >= acuracia_desejada
    # assert recall_et >= 0.5
    # assert precisao_et >= 0.5
    # assert f1_et >= 0.5


# Método para testar modelo KNN a partir do arquivo correspondente
def test_modelo_knn():
    # Importando modelo de KNN
    knn_path = "./MachineLearning/models/knn_heart_failures_classifier.pkl"
    modelo_knn = Model.carrega_modelo(knn_path)

    # Obtendo as métricas do KNN
    acuracia_knn = Avaliador.avaliar(modelo_knn, X, y)

    # Testando as métricas do KNN
    # Modifique as métricas de acordo com seus requisitos
    assert acuracia_knn >= acuracia_desejada
    # assert recall_knn >= 0.5
    # assert precisao_knn >= 0.5
    # assert f1_knn >= 0.5


# Método para testar pipeline Random Forest a partir do arquivo correspondente
def test_modelo_rf():
    # Importando pipeline de Random Forest
    rf_path = "./MachineLearning/pipelines/rf_heart_failures_pipeline.pkl"
    modelo_rf = Pipeline.carrega_pipeline(rf_path)

    # Obtendo as métricas do Random Forest
    acuracia_rf = Avaliador.avaliar(modelo_rf, X, y)

    # Testando as métricas do Random Forest
    # Modifique as métricas de acordo com seus requisitos
    assert acuracia_rf >= acuracia_desejada
    # assert recall_rf >= 0.5
    # assert precisao_rf >= 0.5
    # assert f1_rf >= 0.5
