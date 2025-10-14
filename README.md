# 📚 Sistema de Biblioteca Online — Final Project BD6P

## 🎯 Objetivo
Criar uma aplicação web que permita o gerenciamento de **livros**, **usuários** e **leituras**, com **login**, **upload de arquivos**, **comentários/avaliações** e **geração de relatórios**.

---

## 🧩 CRUDs obrigatórios

### 📘 Livros
- **Campos:**  
  - Título  
  - Autor  
  - Gênero  
  - Ano  
  - Descrição  
  - Imagem da capa (upload)  
  - Arquivo PDF (opcional)

- **Ações:**  
  - Cadastrar  
  - Listar  
  - Editar  
  - Excluir  

- **Ações adicionais:**  
  - Marcar como *“quero ler”*, *“lendo”* ou *“lido”*  
  - Comentar / Avaliar  

---

### 👤 Usuários
- **Campos:**  
  - Nome  
  - E-mail  
  - Senha (hash — **bcrypt**)  
  - Tipo (administrador/leitor)  
  - Foto de perfil (upload opcional)  
  - Biografia / Interesses (opcional)

- **Ações:**  
  - Cadastro  
  - Listagem  
  - Edição  
  - Exclusão  

- **Ações adicionais:**  
  - Ver perfil público  
  - Visualizar histórico de leitura (*“quero ler”*, *“lendo”*, *“lido”*)  
  - Ver estatísticas pessoais de leitura  

---

### 💬 Comentários e Avaliações
- **Campos:**  
  - Livro (relacionamento com `books`)  
  - Usuário (relacionamento com `users`)  
  - Texto do comentário  
  - Nota (1–5 estrelas)  
  - Data  

- **Ações:**  
  - Criar comentário  
  - Editar (pelo próprio autor)  
  - Excluir  
  - Listar comentários por livro  

- **Regras:**  
  - Apenas usuários que marcaram o livro como *“lido”* podem avaliá-lo.  

---

### 📖 Status de Leitura
Gerencia o relacionamento entre **usuário** e **livro**.

- **Campos:**  
  - Usuário (relacionamento com `users`)  
  - Livro (relacionamento com `books`)  
  - Status (`quero ler`, `lendo`, `lido`)  
  - Data de atualização  

- **Ações:**  
  - Criar/atualizar status  
  - Alterar status entre *“quero ler”*, *“lendo”* e *“lido”*  
  - Listar livros por status  

---

### ⭐ Favoritos
Permite ao usuário salvar livros que ele gostou ou quer destacar.

- **Campos:**  
  - Usuário (relacionamento com `users`)  
  - Livro (relacionamento com `books`)  
  - Data de adição  

- **Ações:**  
  - Adicionar livro aos favoritos  
  - Remover dos favoritos  
  - Listar favoritos do usuário  

---


## 🔐 Login e Sessões
- Página de login e cadastro de usuário  
- Hash de senha com **bcrypt**  
- Sessão ativa para controlar quem está logado  
- Opção “lembrar senha”  
- Recuperação de senha via e-mail  

---

## 📁 Upload/Download
- **Upload:**  
  - Imagem da capa do livro  
- **Download:**  
  - Comprovante de leitura ou relatório pessoal (PDF com estatísticas, livros lidos etc.)

---

## 🧠 Recursos diferenciados

### 📖 Gerenciamento de Leitura
- O usuário pode marcar livros como:
  - 🕮 *“Quero ler”* — adiciona à lista de interesse  
  - 📖 *“Lendo”* — mostra livros em andamento  
  - ✅ *“Lido”* — adiciona ao histórico de leituras

### ⭐ Favoritos
- O usuário pode favoritar livros que mais gostou.  
- Listagem de favoritos acessível pelo perfil.  

### 💬 Comentários e Avaliações
- Cada livro pode receber notas e comentários de leitores.  

### 📊 Estatísticas e Relatórios
Painel administrativo com gráficos e dados:
- Número de livros disponíveis  
- Livros mais lidos  
- Gêneros mais populares  
- Usuários mais ativos  

### 🌙 Personalização
- Tema claro/escuro  
- Interface responsiva  

---

## 🖥️ Front-end (mínimo 3 páginas abertas)

### Antes do login
- Página inicial — apresentação da biblioteca  
- Catálogo público — lista de livros disponíveis com busca e filtros  
- Página “Sobre” ou “Contato”  

### Depois do login
- Dashboard (dependendo do tipo de usuário)  
- Páginas:
  - Livros (CRUD completo)  
  - Usuários (CRUD completo — apenas admin)  
  - Comentários e Avaliações  
  - Minhas Leituras (*quero ler*, *lendo*, *lido* e Favoritos)  
  - Estatísticas e relatórios  

---

## 🧱 Arquitetura (MVC)
- **Model:** classes ou schemas de Livro, Usuário, Comentário e Status de Leitura  
- **View:** páginas HTML/CSS  
- **Controller:** rotas e regras de negócio  

---

## 🗄️ Banco de Dados

### Tabelas sugeridas
#### `users`
| Campo | Tipo | Descrição |
|--------|------|------------|
| id | PK | Identificador |
| name | VARCHAR | Nome do usuário |
| email | VARCHAR | E-mail |
| password_hash | VARCHAR | Senha criptografada |
| role | ENUM('admin', 'reader') | Tipo de usuário |
| avatar_url | VARCHAR | Foto de perfil |
| created_at | DATETIME | Data de criação |

#### `books`
| Campo | Tipo | Descrição |
|--------|------|------------|
| id | PK | Identificador |
| title | VARCHAR | Título do livro |
| author | VARCHAR | Autor |
| genre | VARCHAR | Gênero |
| year | INT | Ano |
| description | TEXT | Descrição |
| cover_image | VARCHAR | Imagem da capa |
| pdf_file | VARCHAR | PDF (opcional) |
| created_at | DATETIME | Data de criação |

#### `reading_status`
| Campo | Tipo | Descrição |
|--------|------|------------|
| id | PK | Identificador |
| user_id | FK → users | Usuário |
| book_id | FK → books | Livro |
| status | ENUM('quero ler', 'lendo', 'lido') | Status de leitura |
| updated_at | DATETIME | Última atualização |

#### `comments`
| Campo | Tipo | Descrição |
|--------|------|------------|
| id | PK | Identificador |
| user_id | FK → users | Usuário |
| book_id | FK → books | Livro |
| rating | INT | Nota (1–5) |
| text | TEXT | Comentário |
| created_at | DATETIME | Data de criação |

#### `favorites`
| Campo | Tipo | Descrição |
|--------|------|------------|
| id | PK | Identificador |
| user_id | FK → users | Usuário |
| book_id | FK → books | Livro |
| created_at | DATETIME | Data de adição |

---

## 💡 Diferenciais para Nota Alta
- Filtro de busca (por título, autor, gênero)  
- Paginação na listagem de livros  
- Modo escuro / claro  
- Download de relatório em PDF  
- Painel de estatísticas com gráficos (ex: Chart.js, Recharts)  
- Envio de e-mail para recuperar senha  

---

📚 *Um sistema de leitura digital moderno e interativo, que incentiva a descoberta, o registro e o compartilhamento de experiências literárias.*

---
https://br.freepik.com/<br>
https://storyset.com/search<br>
https://dribbble.com/tags/login-ui<br>
https://uizard.io/templates/mobile-app-templates/book-reading-mobile-app/<br><br>

https://coolors.co/ffffff-fbf8f0-f3ebd9-fea73b-3a3967<br>
https://coolors.co/3a3967-fea73b-cc9a00-05070b-303030-797573-c2b9b5-f3ebd9-fbf8f0-ffffff
