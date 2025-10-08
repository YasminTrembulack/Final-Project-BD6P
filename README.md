# Final-Project-BD6P

# 📚 Sistema de Biblioteca Online

## 🎯 Objetivo
Criar uma aplicação web que permita o gerenciamento de **livros**, **usuários** e **empréstimos**, com **login**, **upload de arquivos** e **geração de relatórios**.

---

## 🧩 CRUDs obrigatórios

### Livros
- **Campos:**  
  - Título  
  - Autor  
  - Gênero  
  - Ano  
  - Status (disponível/emprestado)  
  - Imagem da capa (upload)
- **Ações:**  
  - Cadastrar  
  - Listar  
  - Editar  
  - Excluir

### Usuários
- **Campos:**  
  - Nome  
  - E-mail  
  - Senha (hash)  
  - Tipo (administrador/leitor)
- **Ações:**  
  - Cadastro  
  - Listagem  
  - Edição  
  - Exclusão

### Empréstimos
- **Campos:**  
  - Livro  
  - Usuário  
  - Data de retirada  
  - Data de devolução  
  - Status
- **Ações:**  
  - Registrar empréstimo  
  - Listar  
  - Editar (devolução)  
  - Excluir

---

## 🔐 Login e Sessões
- Página de login e cadastro de usuário  
- Hash obrigatório (**bcrypt** ou similar)  
- Sessão ativa para controlar quem está logado  
- Função “lembrar senha”

---

## 📁 Upload/Download
- **Upload:**  
  - Imagem da capa do livro  
  - PDF do livro digitalizado
- **Download:**  
  - Gerar comprovante de empréstimo em PDF com:  
    - Dados do usuário  
    - Livro emprestado  
    - Datas de retirada e devolução

---

## 🖥️ Front-end (mínimo 3 páginas abertas)

### Antes do login
- Página inicial — apresentação da biblioteca  
- Página de catálogo público — lista de livros disponíveis  
- Página “Sobre” ou “Contato”

### Depois do login
- Dashboard (dependendo do tipo de usuário)  
- Páginas de CRUD:  
  - Livros  
  - Usuários  
  - Empréstimos

---

## 🧱 Arquitetura (MVC)
- **Model:** classes ou schemas de Livro, Usuário e Empréstimo  
- **View:** páginas HTML/CSS  
- **Controller:** rotas e regras de negócio

---

## 🗄️ Banco de Dados
### Tabelas sugeridas
- **users**  
- **books**  
- **loans**

### Relacionamentos
- Um usuário pode ter vários empréstimos  
- Um livro pode aparecer em vários empréstimos, mas **apenas um ativo por vez**

---

## 💡 Diferenciais para nota alta
- Filtro de busca (por título, autor, gênero)  
- Paginação na listagem de livros  
- Envio de e-mail ao realizar empréstimo  
- Painel de estatísticas (número de livros emprestados, usuários ativos)  
- Download de relatório em PDF
