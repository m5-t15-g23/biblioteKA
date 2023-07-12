<h1 align="center">
  Biblioteka API
</h1>

<p align = "center">
Biblioteka é uma API escrita em Django feita para o controle de estoque e gerenciamento de emprestimos de livros para estudantes.
</p>

<p align="center">
  <a href="#endpoints">Endpoints</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
</p>

## **Endpoints**

A API tem um total de 19 endpoints, sendo: <br/>
Usuários Estudantes - podendo cadastrar seu perfil, relizar empréstimos de livros e segui-los a fim de receber notificações, etc... <br/>
Usuário Colaboradores - podendo registrar novos livros, listar usuários, listar empréstimo, bloquear usuários, etc..

<blockquote> Para utilizar o WorkSpace do Insomnia, basta importa-lo do Repositório.
Dentro do Insmonia temos variáveis de ambiente que precisam ser preenchidas corretamente, segue indicação:
	"colaborator_token": Campo Request => [USERS][Login] POST Colaborator | Campo Filter: $.access,
	"student_token": Campo Request => [USERS][Login] POST Student | Campo Filter: $.access,
	"student_token2": Campo Request => [USERS][Login] POST Student 2 | Campo Filter: $.access,
	"student_to_recive_email_token": Campo Request => [USERS][Login] POST Student To Recieve Email | Campo Filter: $.access
</blockquote>
 <img alt="JSON" title="JSON" src="./assets/insomnia_fullfill_variables_enviroment.png" />

<br>

A url base da API é https://biblioteka.up.railway.app/api

## Rotas que não precisam de autenticação

<h2 align ='center'> Registrando usuários </h2>

Para diferenciar o usuário colaborador do estudante, basta passar o campo is_colaborator como true, caso não seja passado, o mesmo é por padrão false.

`POST /users/ - FORMATO DA REQUISIÇÃO`
`Colaborador`
```json
{
	"email": "colaborator1@mail.com",
	"username": "colaborator1",
	"first_name": "colabo1",
	"last_name": "rator1",
	"password": "1234",
	"is_colaborator": true
}
```
Formato da Resposta
`POST /users/ - FORMATO DA RESPOSTA - STATUS 201`
```json
{
	"id": 1,
	"email": "colaborator1@mail.com",
	"username": "colaborator1",
	"first_name": "colabo1",
	"last_name": "rator1",
	"is_colaborator": true
}
```

`POST /users/ - FORMATO DA REQUISIÇÃO`
`Estudante`
```json
{
	"email": "colaborator1@mail.com",
	"username": "colaborator1",
	"first_name": "colabo1",
	"last_name": "rator1",
	"password": "1234",
}
```
Formato da Resposta
`POST /users/ - FORMATO DA RESPOSTA - STATUS 201`
```json
{
	"id": 1,
	"email": "colaborator1@mail.com",
	"username": "colaborator1",
	"first_name": "colabo1",
	"last_name": "rator1",
	"is_colaborator": false
}
```

<h2 align ='center'> Logando usuários </h2>

As funcionalidade de autenticação na API foram feitar utilizando a biblitoeca drf-simplejwt. Logo teremos dois tipos de tokens, sendo eles: access e refresh. <br/>
Utilizamos o access token para as validações de autenticação

`POST /users/login/ - FORMATO DA REQUISIÇÃO`
```json
{
	"username": "colaborator1",
	"password": "1234",
}
```
Formato da Resposta
`POST /users/login/ - FORMATO DA RESPOSTA - STATUS 200`
```json
{
	"refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY4OTcyMDYyMiwiaWF0IjoxNjg5MTE1ODIyLCJqdGkiOiI3NzhiOTYzZjJlZmI0NDNlOGVkYTA3NTg2ODVjYjY0MiIsInVzZXJfaWQiOjF9.Judxl50VyHENLSQkpXPBTWFj8SCQ4S-KWS1vgcSH1is",
	"access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg5MTY5ODIyLCJpYXQiOjE2ODkxMTU4MjIsImp0aSI6IjcxZDlhOGUzMzgxZDRjNDdiZTY1Yzc1ZDYzMTE2NGNmIiwidXNlcl9pZCI6MX0.K6J6vtjuGjcaKW4YhgC5PbbANnbdRm_KJbB6G5tiAlc"
}
```

<h2 align ='center'> Listando Livros </h2>

Para listar o usuário não precisa estar logado. <br/>
A listagem de todos os livros vem paginada, sendo 5 livros por página. <br/>
Podemos aqui também listar livros por id, adicionando um id de book como url params na rota.

`POST /books/ - FORMATO DA REQUISIÇÃO`
Sem body.

Formato da Resposta
`POST /books/ - FORMATO DA RESPOSTA - STATUS 200`
```json
{
	"count": 1,
	"next": null,
	"previous": null,
	"results": [
		{
			"id": 1,
			"title": "Clean Code",
			"author": "Robert C. Martin",
			"description": "How to write clean code",
			"publication_year": "2023-07-11",
			"page_numbers": 500,
			"language": "English",
			"genre": "Education",
			"disponibility": true
		}
	]
}
```
`POST /books/:book_id/ - FORMATO DA REQUISIÇÃO`
Sem body.

Formato da Resposta
`POST /books/:book_id/ - FORMATO DA RESPOSTA - STATUS 200`
```json
  {
    "id": 1,
    "title": "Clean Code",
    "author": "Robert C. Martin",
    "description": "How to write clean code",
    "publication_year": "2023-07-11",
    "page_numbers": 500,
    "language": "English",
    "genre": "Education",
    "disponibility": true
  }
```

## Rotas que precisam de autenticação

<h2 align ='center'> Criando Livros </h2>

Essa é uma rota exclusiva de Colaboradores. <br/>
As criações das cópias de cada livro, são geradas através desse mesmo endpoint, através do campo copies_number, que ditará a quatidade de cópias criadas para cada livro.

`POST /books/ - FORMATO DA REQUISIÇÃO`
```json
{
	"title": "Clean Code",
	"author": "Robert C. Martin",
	"description": "How to write clean code",
	"page_numbers": 500,
	"language": "English",
	"genre": "Education",
	"copies_number": 3
}
```

Formato da Resposta
`POST /books/ - FORMATO DA RESPOSTA - STATUS 201`
```json
{
	"id": 1,
	"title": "Clean Code",
	"author": "Robert C. Martin",
	"description": "How to write clean code",
	"publication_year": "2023-07-11",
	"page_numbers": 500,
	"language": "English",
	"genre": "Education",
	"disponibility": true
}
```

<h2 align ='center'> Listando Cópias </h2>

Essa é uma rota exclusiva de Colaboradores.

`GET /copies/ - FORMATO DA REQUISIÇÃO`
Sem body.

Formato da Resposta
`GET /copies/ - FORMATO DA RESPOSTA - STATUS 200`
```json
{
	"count": 3,
	"next": null,
	"previous": null,
	"results": [
		{
			"id": 1,
			"book_id": 1,
			"book_title": "Clean Code",
			"is_avaliable": false
		},
		{
			"id": 2,
			"book_id": 1,
			"book_title": "Clean Code",
			"is_avaliable": true
		},
		{
			"id": 3,
			"book_id": 1,
			"book_title": "Clean Code",
			"is_avaliable": true
		}
	]
}
```

<h2 align ='center'> Seguindo Livros </h2>

Essa é uma rota exclusiva de Estudantes. <br/>
Todas as vezes que a disponibilidade de um livro for alterada, o estudante que o segue, receberá em seu email, uma mensagem o avisando do novo stauts de disponibilidade do livro.

`POST /follow/:book_id/ - FORMATO DA REQUISIÇÃO`
Sem body

Formato da Resposta
`POST /follow/:book_id/ - FORMATO DA RESPOSTA - STATUS 201`
```json
{
	"id": 1,
	"student_id": 2,
	"student_username": "student",
	"book_followed_id": 1,
	"book_followed_title": "Clean Code"
}
```

<h2 align ='center'> Listando livros Seguidos </h2>

Essa é uma rota exclusiva de Estudantes. <br/>
A listagem dos livros seguidos vem paginada, sendo 5 por página. <br/>

`GET /follow/ - FORMATO DA REQUISIÇÃO`
Sem body

Formato da Resposta
`GET /follow/ - FORMATO DA RESPOSTA - STATUS 200`
```json
{
	"count": 1,
	"next": null,
	"previous": null,
	"results": [
		{
			"id": 1,
			"student_id": 2,
			"student_username": "student",
			"book_followed_id": 1,
			"book_followed_title": "Clean Code"
		}
	]
}
```

<h2 align ='center'> Listando todos os livros seguidos pelos Estudantes</h2>

Essa é uma rota exclusiva de Colaboradores. <br/>
A listagem dos livros seguidos vem paginada, sendo 5 por página. <br/>

`GET /follow/colaborator/ - FORMATO DA REQUISIÇÃO`
Sem body

Formato da Resposta
`GET /follow/colaborator/ - FORMATO DA RESPOSTA - STATUS 200`
```json
{
	"count": 1,
	"next": null,
	"previous": null,
	"results": [
		{
			"id": 1,
			"student_id": 2,
			"student_username": "student",
			"book_followed_id": 1,
			"book_followed_title": "Clean Code"
		}
	]
}
```

<h2 align ='center'> Deixando de seguir livros </h2>

Essa é uma rota exclusiva de Estudantes. <br/>


`GET /unfollow/:book_id/ - FORMATO DA REQUISIÇÃO`
Sem body

Formato da Resposta
`GET /unfollow/:book_id/ - FORMATO DA RESPOSTA - STATUS 204`
Sem body

<h2 align ='center'> Criando empréstimos</h2>

Essa é uma rota exclusiva de Estudantes. <br/>
O emprésitmo é realizado utilizando um id de livro, porém, a nivél de código, é utilizada a primeira cópia disponivél referente ao livro. <br/>
Cada empréstimo tem um período fixo de duração, sendo de 30 dias a partir da data de criação, caso o dia de retorno seja um sábado ou domingo, o mesmo passará a ser a próxima segunda feria após a data de retorno estipulada em 30 dias. Assim que 00:00 da data de retonro for atiginda, o empréstimo será interpretado como atrasado.<br/>
Formato das datas: Ano/Mês/Dia. <br/>
Um estudante só poder ter até 3 empréstimos simultâneos, a partir do terceiro empréstimo, seu campo stauts_for_loan ficará como false. <br/>
Caso todas as cópias de um livro sejam empretadas, o livro passará a não estar disponivel, causando alteração no seu campo disponibility para false, e enviando emails para todos os estudantes que seguem o mesmo, os avisando da alteração.


`POST /loans/:book_id/ - FORMATO DA REQUISIÇÃO`
Sem body

Formato da Resposta
`POST /loans/:book_id/ - FORMATO DA RESPOSTA - STATUS 201`
```json
{
	"id": 1,
	"loan_date": "2023-07-11",
	"loan_return": "2023-08-10",
	"is_active": true,
	"returned_at": null,
	"user_id": 2,
	"user_email": "student@mail.com",
	"user_username": "student",
	"copy_id": 1,
	"book_title": "Clean Code"
}
```

Formato da Resposta caso o usuário esteja bloqueado
`POST /loans/:book_id/ - FORMATO DA RESPOSTA - STATUS 201`
```json
{
	"detail": "User alredy have max number of loans: 3"
}
```

Formato da Resposta caso o livro não esteja disponível
`POST /loans/:book_id/ - FORMATO DA RESPOSTA - STATUS 201`
```json
{
	"detail": "This book is not available, follow to checkavailability status."
}
```
<h2 align ='center'> Listando todos os empréstimos </h2>

Essa é uma rota exclusiva de Colaboradores. <br/>
A listagem dos emprésitmos vem paginada, sendo 5 por página. <br/>

`GET /loans/ - FORMATO DA REQUISIÇÃO`
Sem body

Formato da Resposta
`GET /loans/ - FORMATO DA RESPOSTA - STATUS 200`
```json
{
	"count": 1,
	"next": null,
	"previous": null,
	"results": [
		{
			"id": 1,
			"loan_date": "2023-07-11",
			"loan_return": "2023-08-10",
			"is_active": true,
			"returned_at": null,
			"user_id": 2,
			"user_email": "student@mail.com",
			"user_username": "student",
			"copy_id": 1,
			"book_title": "Clean Code"
		}
	]
}
```

<h2 align ='center'> Listando todos os empréstimos por id de estudante </h2>

Essa é uma rota exclusiva de Colaboradores. <br/>
A listagem dos emprésitmos vem paginada, sendo 5 por página. <br/>

`GET /loans/student/:student_id - FORMATO DA REQUISIÇÃO`
Sem body

Formato da Resposta
`GET /loans/student/:student_id - FORMATO DA RESPOSTA - STATUS 200`
```json
{
	"count": 1,
	"next": null,
	"previous": null,
	"results": [
		{
			"id": 1,
			"loan_date": "2023-07-11",
			"loan_return": "2023-08-10",
			"is_active": true,
			"returned_at": null,
			"user_id": 2,
			"user_email": "student@mail.com",
			"user_username": "student",
			"copy_id": 1,
			"book_title": "Clean Code"
		}
	]
}
```

<h2 align ='center'> Listando todos os empréstimos de um estudante </h2>

Essa é uma rota exclusiva de Estudantes. <br/>
A listagem dos emprésitmos vem paginada, sendo 5 por página. <br/>

`GET /loans/student/:student_id/ - FORMATO DA REQUISIÇÃO`
Sem body

Formato da Resposta
`GET /loans/student/:student_id/ - FORMATO DA RESPOSTA - STATUS 200`
```json
{
	"count": 1,
	"next": null,
	"previous": null,
	"results": [
		{
			"id": 1,
			"loan_date": "2023-07-11",
			"loan_return": "2023-08-10",
			"is_active": true,
			"returned_at": null,
			"user_id": 2,
			"user_email": "student@mail.com",
			"user_username": "student",
			"copy_id": 1,
			"book_title": "Clean Code"
		}
	]
}
```

<h2 align ='center'> Listando todos os empréstimos de uma cópia </h2>

Essa é uma rota exclusiva de Colaboradores. <br/>
A listagem dos emprésitmos vem paginada, sendo 5 por página. <br/>

`GET /loans/copy/:copy_id/ - FORMATO DA REQUISIÇÃO`
Sem body

Formato da Resposta
`GET /loans/copy/:copy_id/ - FORMATO DA RESPOSTA - STATUS 200`
```json
{
	"count": 1,
	"next": null,
	"previous": null,
	"results": [
		{
			"id": 1,
			"loan_date": "2023-07-11",
			"loan_return": "2023-08-10",
			"is_active": true,
			"returned_at": null,
			"user_id": 2,
			"user_email": "student@mail.com",
			"user_username": "student",
			"copy_id": 1,
			"book_title": "Clean Code"
		}
	]
}
```

<h2 align ='center'> Listando todos os empréstimos de um estudante </h2>

Essa é uma rota exclusiva de Estudantes. <br/>
A listagem dos emprésitmos vem paginada, sendo 5 por página. <br/>

`GET /loans/student/:student_id/ - FORMATO DA REQUISIÇÃO`
Sem body

Formato da Resposta
`GET /loans/student/:student_id/ - FORMATO DA RESPOSTA - STATUS 200`
```json
{
	"count": 1,
	"next": null,
	"previous": null,
	"results": [
		{
			"id": 1,
			"loan_date": "2023-07-11",
			"loan_return": "2023-08-10",
			"is_active": true,
			"returned_at": null,
			"user_id": 2,
			"user_email": "student@mail.com",
			"user_username": "student",
			"copy_id": 1,
			"book_title": "Clean Code"
		}
	]
}
```

<h2 align ='center'> Devolução de Empréstimos </h2>

Essa é uma rota exclusiva de Estudantes. <br/>
Ao devolver um livro, o empréstimo passará a não estar mais ativado, ocasionando na alteração do campo is_active do mesmo, se tornado false. <br/>
Caso, a devolução do empréstimo seja de um livro que não está disponivél, ou seja, todas as cópias alugadas, o mesmo passará a ser disponível, ocasioando em envio de emails para os usuários que seguem o livro.

`GET /loans/loans/:loan_id/checkout/ - FORMATO DA REQUISIÇÃO`
Sem body

Formato da Resposta
`GET /loans/loans/:loan_id/checkout/ - FORMATO DA RESPOSTA - STATUS 200`
```json
{
	"id": 1,
	"loan_date": "2023-07-11",
	"loan_return": "2023-08-10",
	"is_active": false,
	"returned_at": "2023-07-11",
	"user_id": 2,
	"user_email": "student@mail.com",
	"user_username": "student",
	"copy_id": 1,
	"book_title": "Clean Code"
}
```

<h2 align ='center'> Bloqueio de Estudantes com empréstimos atrasados </h2>

Essa é uma rota exclusiva de Colaboradores. <br/>

`PATCH /loans/loans/:loan_id/checkout/ - FORMATO DA REQUISIÇÃO`
```json
{
	"status_for_loan": false
}
```

Formato da Resposta caso o estudante não tenha empréstimos
`PATCH /users/:user_id/ - FORMATO DA RESPOSTA - STATUS 200`
```json
{
	"detail": "User didn't have loans yet"
}
```
Formato da Resposta caso o estudante tenha empréstimos não atrasados
`PATCH /users/:user_id/ - FORMATO DA RESPOSTA - STATUS 200`
```json
{
	"detail": "User first loan is already in permited period"
}
```
Formato da Resposta caso o estudante já esteja bloqueado
`PATCH /users/:user_id/ - FORMATO DA RESPOSTA - STATUS 200`
```json
{
	"detail": "User already blocked"
}
```
Formato da Resposta caso estudante possua empréstimos atrasados
`PATCH /users/:user_id/ - FORMATO DA RESPOSTA - STATUS 200`
```json
{
	"id": 5,
	"email": "studenttoblock@mail.com",
	"username": "studenttoblock",
	"first_name": "stutoblock",
	"last_name": "denttoblock",
	"is_colaborator": false,
	"status_for_loan": false
}
```
