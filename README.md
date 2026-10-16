## Como iniciar o projeto?
Para rodar o projeto, abra o terminal na pasta onde está o arquivo manage.py, crie e ative um ambiente virtual executando ```python -m venv venv``` seguido de,

**No Windows:**
```venv\Scripts\activate``` ou,

**No Mac/Linux**
source ```venv/bin/activate``` 


Em seguida, instale as dependências usando ```pip install -r requirements.txt``` ou instale apenas o Django com ```pip install django```. Execute as migrações iniciais do banco de dados com python manage.py migrate e inicie o servidor local rodando ```python manage.py runserver```.


Por fim, basta copiar o link http://127.0.0.1:8000/ que aparece no terminal, colar no seu navegador e pressionar Ctrl + C quando quiser desligar o servidor.
