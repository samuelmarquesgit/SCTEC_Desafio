# SCTEC - Gestão de Empreendimentos (Santa Catarina)

## 📌 Descrição da Solução Desenvolvida
O **SCTEC** é uma aplicação completa (Full-Stack Python) que engloba um **Back-end robusto (API REST)** e um **Front-end interativo (Web App)**, focados exclusivamente no gerenciamento de informações sobre empreendimentos no estado de Santa Catarina. O objetivo principal do projeto é fornecer aos empreendedores e aos gestores uma plataforma segura onde é possível realizar operações padronizadas de CRUD (Criar, Ler, Atualizar, Deletar) de forma extremamente intuitiva, rastreável e eficiente. 

O sistema permite que o usuário gerencie e armazene cadastros completos, incluindo obrigatoriamente: o nome do próprio negócio, o nome do responsável pela criação daquele empreendimento, a cidade na qual reside a sede (com municípios buscados dinamicamente dos dados públicos geográficos do IBGE para garantir exatidão e consistência de dados), o segmento de atuação definido do negócio (*Tecnologia, Indústria, Comércio, Agronegócio, ou Serviços*), o e-mail de contato e o status atualizado (*Ativo / Inativo*). Uma barra lateral de relatórios compila imediatamente esses dados formando um painel de gestão consolidado.

## 🎥 Vídeo Pitch
Assista ao vídeo de apresentação (Pitch Institucional) deste projeto clicando no link abaixo:
- 👉 **[Link para o Vídeo Pitch (Substituir pela URL final)](https://#)**

## 🚀 Tecnologias Utilizadas
**Stack de Back-end (APIs REST e Negócios):**
- **Python 3.10+**: Linguagem central e base para integração dos ambientes.
- **FastAPI**: Framework de altíssimo desempenho para o desenvolvimento das rotas e processamento das requisições RESTful do sistema.
- **Uvicorn**: Servidor local ASGI otimizado para sustentar execuções assíncronas no ambiente de servidor de produção e desenvolvimento.
- **SQLAlchemy e SQLite**: Gerenciamento do banco de dados relacional (ORM) conectado de maneira persistente e limpa ao diretório local da aplicação.
- **Pydantic**: Biblioteca que garante a validação tipada e rigorosa das transações e payloads consumidos internamente.

**Stack de Front-end (Interface Visual):**
- **Streamlit**: Framework que permite compor toda a interface gráfica web e painéis nativamente convertidos e desenhados a partir de código unicamente escrito em Python.
- **Pandas**: Utilizado para o manuseio avançado, higienização inteligente em memória viva e formatação nativa tabular para os *DataGrids* renderizados em tela.
- **HTTPX**: Módulo encarregado da comunicação "cliente > servidor" para consumir a camada remota do nosso Back-end de forma natural.

## 📂 Estrutura Geral do Projeto
A arquitetura foi meticulosamente segmentada provendo um baixo acoplamento:

```text
SCTEC/
├── app/                  # Código fonte do Back-end (API FastAPI)
│   ├── crud.py           # Processamento e regras das tabelas do banco de dados
│   ├── db.py             # Configuração e engine de inicialização (SQLAlchemy)
│   ├── main.py           # Controladores principais (Coração de exposição da API)
│   ├── models.py         # Declaração das entidades espelhadas em tabelas SQL
│   └── schemas.py        # Proteção e contratos de validação de dados de entrada (Pydantic)
├── frontend/             # Código fonte do Front-end (Interface Web)
│   ├── api_client.py     # Cliente gerador das requisições HTTP do Front para o Back
│   └── main.py           # Desenho das telas, formulários e lógica comportamental (Streamlit)
├── data/                 # Armazenamento do banco persistente em SQLite
├── tests/                # Testes de resiliência e validação unitária de componentes internos
├── venv/                 # Ambiente de isolamento das dependências essenciais
├── run_app.py            # Orquestrador automatizado para acionar a solução em forma unificada
├── requirements.txt      # Mapeamento fixo de versões de bibliotecas e dependências (pip)
└── README.md             # Esta documentação central descritiva do projeto tecnológico
```

## ⚙️ Instruções Necessárias para a sua Execução

Para garantir o funcionamento perfeito deste sistema, se assegure de ter a versão mínima de `Python 3.10+` instalada na máquina e visível pela variável `PATH` do sistema.

**Passo a passo (Windows):**

1. Abra um terminal de sua preferência (ex: PowerShell) e adentre a pasta clonada do framework:
   ```powershell
   cd \caminho\onde\voce\baixou\o\SCTEC
   ```

2. Crie e ative a bolha de isolamento de virtualização (Virtual Environment):
   ```powershell
   # Criação explícita do Virtual Environment na subpasta 'venv'
   python -m venv venv
   
   # Ativação do estado isolado
   .\venv\Scripts\Activate.ps1
   ```

3. Em seguida, acione o download dos pacotes e instale as dependências requisitadas para este app no ambiente virtualizado ativado:
   ```powershell
   pip install -r requirements.txt
   ```

4. **Executando a Aplicação Completa:**
   Com a finalidade de providenciar a melhor vivência em modo de desenvolvimento local, deixamos construído previamente um script unificado do sistema (`run_app.py`). Com um único e simplório comando ordenado pelo console as duas camadas virtuais — banco de dados via API e painel de visão do cliente — engatarão ativadas concomitantemente na mesma inicialização:
   ```powershell
   python run_app.py
   ```

**(Método Alternativo: rodando individualmente os processos):**
Caso você decida por efetuar o "Boot", observando especificamente os logs operacionais das aplicações em janelas destacadas individualizadas, ative o terminal de seu próprio venv nas duas interfaces:
- **Janela 1 (Back-end):** Rode `uvicorn app.main:app --reload` (e verifique as documentações na Swagger UI aberta em `http://127.0.0.1:8000/docs`).
- **Janela 2 (Front-end):** Rode concomitantemente `streamlit run frontend/main.py` (acesse via `http://localhost:8501/`).
