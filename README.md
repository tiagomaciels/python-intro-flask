# Python Intro Flask

## Descrição da Aplicação

[2024]Este é um projeto de introdução ao framework Flask em Python. O objetivo é fornecer um exemplo básico de como criar uma aplicação web simples com Flask. O exemplo utilizado foi de uma API para um sistema de e-commerce.

## Tecnologias Utilizadas

- Python
- Flask
- Flask-Login
- Flask-SQLAlchemy
- Flask-CORS
- SQLite

## Configuração do Projeto

1. Clone o repositório:
   ```bash
   git clone https://github.com/tiagomaciels/python-intro-flask.git
   ```
2. Navegue até o diretório do projeto:
   ```bash
   cd python-intro-flask
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Crie o banco de dados e o usuário teste
   Abra o terminal e digite: flask shell

   ```bash
    db.create_all()
    user = User(username="admin", password="123")
    db.session.add(user)
    db.session.commit
    exit()
   ```

   Detalhes dos comandos

   ```bash
   db.create_all():
       Este comando cria todas as tabelas definidas nos modelos (models) no banco de dados.
       Ele verifica os modelos do SQLAlchemy definidos na aplicação e cria as tabelas correspondentes, caso ainda não existam.

   user = User(username="admin", password="123"):
       Cria uma instância do modelo User com os valores fornecidos para os campos username e password.
       Aqui, um usuário com nome de usuário "admin" e senha "123" está sendo criado.

   db.session.add(user):
       Adiciona o objeto user criado anteriormente à sessão do banco de dados.
       Isso prepara o objeto para ser salvo no banco de dados.

   db.session.commit:
       Este comando deveria ser db.session.commit().
       Ele salva todas as alterações pendentes na sessão do banco de dados, ou seja, insere o usuário "admin" no banco.

   exit():
       Sai do Flask Shell, encerrando a interação com o terminal.
   ```

# API Endpoints

## Authentication

- **POST** `/login` - Log in
- **POST** `/logout` - Log out

## Products

- **GET** `/api/products` - Get a list of products
- **GET** `/api/products/{product_id}` - Get product details by ID
- **GET** `/api/products/search` - Search for products
- **POST** `/api/products/add` - Add a new product
- **PUT** `/api/products/update/{product_id}` - Update a product by ID
- **DELETE** `/api/products/delete/{product_id}` - Delete a product by ID

## Cart

- **POST** `/api/cart/add/{product_id}` - Add item to the cart
- **DELETE** `/api/cart/remove/{item_id}` - Remove item from the cart
- **GET** `/api/cart` - View the user's cart
- **POST** `/api/cart/checkout` - Checkout and clear the cart

## Estrutura de Pastas

```
python-intro-flask/
.
├── instance/
│   └── ecommerce.db        # Banco de dados SQLite
├── app.py                  # Arquivo principal da aplicação
├── README.md               # Documentação do projeto
├── requirements.txt        # Dependências do projeto
├── swagger.yaml            # Especificação da API no formato Swagger/OpenAPI
```

## Considerações Finais

Este projeto de API para um sistema de e-commerce é uma introdução básica ao Flask e pode ser expandido conforme necessário.
