# **🗺️ GeoPoints PF \- Sistema de Mapeamento de Pontos de Interesse**

Este repositório contém o código-fonte para o **GeoPoints PF**, um sistema de gerenciamento e visualização de Pontos de Interesse (POI) em um mapa interativo, desenvolvido com **Python (Flask)** para o *backend* e **JavaScript (Leaflet)** para o *frontend*.

O projeto simula uma ferramenta interna utilizada pela Polícia Federal para georreferenciamento e análise de dados espaciais.

## **🌟 Melhoria Implementada: Edição de Pontos de Interesse no Mapa**

Para esta candidatura, a funcionalidade adicionada foi a **Edição de Pontos de Interesse (POIs) diretamente pelo *popup* do mapa**.

Anteriormente, o *popup* de um ponto só permitia a visualização de dados e a exclusão. Com a alteração, o usuário agora pode:

1. Clicar em um ponto existente.  
2. Clicar em um novo botão "📝 **Editar Ponto**" (a ser implementado no mapa.js).  
3. Um formulário é carregado dentro do *popup*, permitindo alterar o **Nome**, a **Descrição** e a **Categoria** do POI.  
4. O formulário utiliza uma nova rota de API (*endpoint*) no *backend* para persistir as alterações no banco de dados SQLite.

### **🎯 Por que esta Melhoria? (Alinhamento com a Vaga)**

A escolha desta melhoria foi motivada por três fatores, alinhados com os objetivos de um estágio no SEGEO/DITEC/PF:

1. **Usabilidade e Produtividade (Foco na Tarefa):** A capacidade de editar informações no local aumenta a usabilidade do mapa. Em um contexto operacional da PF, a agilidade na atualização de dados georreferenciados é crucial.  
2. **Integração *Full Stack*:** A implementação exigiu modificações em todas as camadas do sistema:  
   * **Frontend (JavaScript/HTML):** Criação da interface de edição no *popup* (mapa.js, mapa.tpl).  
   * **Backend (Python/Flask):** Criação do método para atualizar dados no banco (data.py) e exposição de uma nova rota na API (controller.py, route.py).  
3. **Habilidade Técnica:** Demonstra proficiência em:  
   * Conhecimento de **JavaScript** e manipulação de eventos (requisito da vaga).  
   * Comunicação **Assíncrona (Fetch API)** para requisições de atualização.  
   * Design de *endpoints* **RESTful** no **Flask** (conhecimento de Python e framework web é um diferencial).  
   * Consultas e atualizações no **SQLite** (gerenciado pela classe Database).

### **🛠️ Passos de Implementação (Alterações Principais)**

1. **data/data.py (Database Class):**  
   * Será necessário adicionar o método atualizar\_ponto(self, ponto\_id, nome, descricao, categoria) para executar a *query* UPDATE no SQLite.  
   * *Exemplo de Query:* UPDATE pontos SET nome \= ?, descricao \= ?, categoria \= ? WHERE id \= ?  
2. **controller/controller.py (Aplication Class):**  
   * Adicionar o método api\_atualizar\_ponto(self, ponto\_id) para:  
     * Receber os dados do request.get\_json().  
     * Validar coordenadas e limites (já há lógica de validação de limites e categorias implementada).  
     * Chamar o método db.atualizar\_ponto().  
     * Retornar uma resposta JSON adequada (Status 200/400/404).  
3. **route.py (Flask Routes):**  
   * Adicionar a rota para manipulação da edição:  
     Python  
     @app.route('/api/pontos/\<int:ponto\_id\>', methods=\['PUT'\])  
     def atualizar\_ponto(ponto\_id):  
         return aplication.api\_atualizar\_ponto(ponto\_id)

   * *Nota: O método HTTP PUT é ideal para a atualização completa de recursos (POIs).*  
4. **mapa.js (Frontend Logic):**  
   * Modificar createPopupContent(ponto) para incluir o botão de edição.  
   * Implementar a função showEditPointForm(ponto) para carregar a interface de edição dentro do *popup*.  
   * Implementar a função submitEditPoint(event, pontoId) para enviar os dados do formulário via fetch com o método PUT.

---

## **💻 Configuração e Execução**

O projeto é baseado em Python (Flask) e utiliza SQLite para persistência de dados.

### **Pré-requisitos**

* Conhecimento básico de Python, JavaScript, CSS e HTML (requisitos da vaga)  
* Python 3.x  
* Flask (assumido como dependência)

---
### **Passos**

1. **Clone o repositório:**  
   Bash  
   git clone https://github.com/MontMarcos/GeoPoints.git  
   cd GeoPoints

2. **Crie e ative o ambiente virtual (.venv):**  
   Bash  
   python \-m venv .venv  
   source .venv/bin/activate    

3. **Instale as dependências:**  
   Bash  
   pip install -r requirements.txt

4. **Execute a aplicação:**  
   Bash  
   python route.py

5. Acesse:  
   A aplicação estará disponível em na porta 8083

---

## **📁 Estrutura do Projeto**

A estrutura segue o padrão do Flask e está bem organizada:

ESTAGIA\_PROJETO/  
├── .venv/                         \# Ambiente virtual Python  
├── controller/  
│   ├── controller.py              \# Lógica de negócio (API e Renderização)  
│   └── ...  
├── data/  
│   └── data.py                    \# Camada de Acesso a Dados (SQLite)  
├── static/  
│   ├── css/  
│   │   └── styles.css             \# Estilos CSS  
│   └── js/  
│       └── mapa.js                \# Lógica Frontend (Leaflet, AJAX)  
├── views/  
│   └── mapa.tpl                   \# Template HTML (Jinja2)  
├── pontos_interesse.db            \# Banco de dados SQLite  
└── route.py                       \# Configuração e Rotas do Flask

---

Deseja que eu elabore o código Python (controller.py, data.py, route.py) e JavaScript (mapa.js) necessário para implementar essa funcionalidade de edição?
