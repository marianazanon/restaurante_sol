# Restaurante Sol

## <img src="/restaurante_app/static/restaurante_app/img/django_logo.png" width="300"/> ##


## Tecnologias Utilizadas

### Conheça o Django
- Django é um framework web em Python de alto nível que incentiva o desenvolvimento rápido e um design limpo e pragmático. Criado por desenvolvedores experientes, ele cuida de grande parte dos problemas do desenvolvimento web, permitindo que você se concentre em escrever seu aplicativo sem precisar reinventar a roda. É gratuito e de código aberto.

- Ridiculamente rápido: Django foi projetado para ajudar os desenvolvedores a levar aplicações do conceito à conclusão o mais rápido possível.

- Reassurantemente seguro: O Django leva a segurança a sério e ajuda os desenvolvedores a evitar muitos erros de segurança comuns.

- Extremamente escalável: Alguns dos sites mais movimentados da web aproveitam a capacidade do Django de escalar de forma rápida e flexível.

 ## Grupo:
 
 ### Mariana Zanon, Gabriel Reis Batista, Luiz Cláudio Brito e Maria Vitória Moura Paiva

## Pré-requisitos

- Docker
- Docker Compose

## Como executar a aplicação

Siga os passos abaixo para configurar e executar a aplicação:

1. **Configure o arquivo `.env`**

   Essas variáveis serão utilizadas pelo Docker para criar o banco de Dados MySQL do projeto. O banco será criado pelo Docker, só preciamos fornecer as credenciais para a aplicação acessar

   Crie um arquivo `.env` no root do projeto com as seguintes variáveis de ambiente:

   ```env
   MYSQL_ROOT_PASSWORD=crie_uma_senha_de_root
   DB_NAME=nome_do_banco_a_ser_criado
   DB_USER=usuario_do_banco_a_ser_criado => Não usar 'root'
   DB_PASSWORD=senha_do_banco_a_ser_criado
   DB_HOST=db
   DB_PORT=3306

   # Senhas adicionais
   GERENTE_PASSWORD=sua_senha_de_gerente
   FUNCIONARIO_PASSWORD=sua_senha_de_funcionario
   SUPERUSER_PASSWORD=sua_senha_de_superuser
   ```

   Os usuários criados pelo sistema para acessar o dashboard após a primeira migração serão: admin, gerente e funcionario. Para acessar como admin utilize a senha do super usuário.

4. **Construa e execute os contêiners**

   No root do projeto, execute o seguinte comando para construir e iniciar os contêineres Docker:

   ```sh
   docker-compose up --build
   ```

5. **Rode as migrações**

   Após os contêineres serem iniciados, abra outro terminal e execute o seguinte comando para rodar as migrações do banco de dados:

   ```sh
   docker-compose exec web python manage.py makemigrations restaurante_app
   docker-compose exec web python manage.py migrate
   ```
   No Windows:

   ```sh
   cd gerenciador_de_restaurante
   docker-compose exec web sh
   python manage.py makemigrations restaurante_app
   python manage.py migrate
   ```

6. **Acesse a aplicação**

   Após rodar as migrações, você pode acessar a aplicação através do seu navegador no endereço:

   ```
   http://localhost:1337
   ```
   Acesse com um dos seguintes usuários:
    - admin: super usuário
    - gerente: permissão de write,read e edit
    - funcionario: read e write na tabela de produtos e vendas.

   a senha foi fornecida no .env nos campos SUPERUSER_PASSWORD (admin), FUNCIONARIO_PASSWORD (funcionario) e GERENTE_PASSWORD (gerente)

## Comandos Úteis

- **Parar os contêineres**

  ```sh
  docker-compose down
  ```

- **Acessar o shell do contêiner web**

  ```sh
  docker-compose exec web sh
  ```

- **Deleter o Banco**

  ```sh
   docker-compose exec web python manage.py delete_database
  ```

  No Windows:

  ```sh
   docker-compose exec web sh
   python manage.py delete_database
  ```
