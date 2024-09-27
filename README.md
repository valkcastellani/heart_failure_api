# Descrição do MVP Heart Failures

Este projeto foi desenvolvido com o objetivo de oferecer uma solução para classificar a probabilidade de um paciente desenvolver uma doença cardíaca, com base em informações obtidas através de exames realizados. O desenvolvimento faz parte do currículo da Pós-Graduação em Engenharia de Software da PUC-Rio, iniciado no módulo de Qualidade de Software, Segurança e Sistemas Inteligentes.

Esta API utiliza o modelo treinado pelo notebook, disponibilizado na pasta **MachineLearning/notebooks** deste repositório, que explora um conjunto de dados de insuficiência cardíaca obtido do site Kaggle (https://www.kaggle.com/datasets/fedesoriano/heart-failure-prediction), voltado para a predição de doenças cardíacas. 

Apesar de conseguir utilizar a API através de linha de comando ou algum aplicativo, o frontend deste MVP foi disponibilizado no endereço https://github.com/valkcastellani/heart_failure_frontend.

---

# Como executar

Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

```
pip3 install -r requirements.txt
```

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

Para executar a API basta executar:

```
flask run --host 0.0.0.0 --port 5000
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte.

```
flask run --host 0.0.0.0 --port 5000 --reload
```

Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução.

---

# Executando a API em Contêineres Docker

## Docker Build e Run

Para construir e executar uma imagem Docker a partir de um Dockerfile, siga os passos abaixo:

1. Construindo a imagem com Docker Build:

   Primeiro, navegue até o diretório onde está localizado o Dockerfile e execute o seguinte comando para construir a imagem:

   ```bash
   docker build -t heart_failures_api:latest .
   ```

   - **heart_failures_api** é o nome da imagem. Nesse caso, foi utilizado no nome da nossa API.
   - **latest** é a tag de identificação da versão da imagem. Nessa caso, foi utilizado latest, pois é a versão mais recente disponibilizada da API.
   - **.** indica que o Dockerfile está no diretório atual.

2. Iniciando a Imagem com Docker Run:

   Após construir a imagem, você pode iniciar um contêiner a partir dessa imagem com o comando:

   ```bash
   docker run -d -p 5000:5000 -v ./database:/app/database heart_failures_api:latest
   ```

   - **-d** inicia o contêiner em modo _detached_ (em segundo plano).
   - **-p 5000:5000** mapeia a porta do host para a porta do contêiner, no formato _porta-do-host:porta-do-contêiner_.
   - **-v ./database:/app/database** monta um volume (mapeando caminhos no formato _/caminho/no/host:/caminho/no/contêiner_), permitindo que dados sejam persistentes no diretório `./database` do host e `/app/database` do contêiner.
   - **heart_failures_api:latest** é a imagem que criamos com o comando _docker build_ no item 1, no format _nome-da-imagem:tag_.

3. Verificando o Contêiner em Execução:

   Para verificar se o contêiner está em execução, use:

   ```bash
   docker ps
   ```

   Ou

   ```bash
   docker container ls -a
   ```

   Isso mostrará uma lista dos contêineres em execução.

## Docker Compose

O Docker Compose simplifica a definição e execução de aplicativos Docker de múltiplos contêineres. Ele usa um arquivo docker-compose.yml para configurar os serviços da sua aplicação.

1. Criando e Iniciando os Serviços:

   Para construir e iniciar todos os serviços definidos no arquivo `docker-compose.yml`, use:

   ```bash
   docker-compose up --build -d
   ```

   - **--build** reconstrói as imagens se necessário.
   - **-d** inicia os contêineres em segundo plano (_detached mode_).

2. Parando os Serviços:

   Para parar e remover os contêineres definidos no arquivo `docker-compose.yml`, execute:

   ```bash
   docker-compose down
   ```

   Isso irá parar todos os contêineres e remover os recursos criados pelo _docker-compose up_.

---

# Testando a API do MVP Heart Failures com PyTest (Testes Unitários)

## Como Rodar os Testes

Para rodar os testes unitários da aplicação, siga os passos abaixo:

1. **Instale as dependências necessárias:**

   Certifique-se de que você possui o `pytest` instalado. Se não tiver, você pode instalá-lo utilizando o pip:

   ```bash
   pip3 install pytest
   ```

2. **Execute os testes:**

   Na raiz do seu projeto, execute o seguinte comando para rodar todos os testes:

   ```bash
   pytest
   ```

3. **Verifique os resultados:**

   O `pytest` exibirá os resultados dos testes diretamente no terminal. Cada teste bem-sucedido será indicado por um ponto (.), enquanto os testes que falharem serão acompanhados de detalhes sobre os erros.

   No caso do arquivo test_modelos.py, o retorno será `FF.`, como mostrado na imagem abaixo:

   ![Execução do PyTest no MVP](https://github.com/valkcastellani/heart_failure_api/blob/master/imagens/pytest-modelos.png)
   
   Isso indica que os modelos ET (ExtraTreesClassifier) e KNN (KNeighborsClassifier) não conseguiram atingir a meta pré-definida de 0,8 (80%) de acurácia.


### Segurança da Informação e Desenvolvimento Seguro

É fundamental implementar a criptografia dos dados trocados entre o frontend e o backend para garantir a segurança das informações pessoais dos pacientes. Dados sensíveis, como resultados de exames, devem ser protegidos durante o transporte e armazenamento, utilizando métodos como HTTPS para comunicação segura e a criptografia de informações no banco de dados. Essas medidas reduzem o risco de interceptação ou acesso indevido às informações.

Além disso, é importante adotar práticas de desenvolvimento seguro, como autenticação robusta, autorização baseada em papéis de usuário e monitoramento de acesso aos dados. Implementar essas medidas no frontend e no backend garante que apenas pessoas autorizadas possam visualizar ou modificar informações confidenciais, assegurando a privacidade e integridade dos dados dos pacientes.

---

# Contribuindo

Se você encontrar qualquer problema ou tiver sugestões para melhorar a API, os testes unitários, sinta-se à vontade para abrir uma _issue_ ou enviar um _pull request_.
