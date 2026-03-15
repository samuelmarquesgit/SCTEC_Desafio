import streamlit as st
import pandas as pd
from api_client import APIClient
import time
import httpx
import re

@st.cache_data
def get_municipios_sc():
    try:
        response = httpx.get("https://servicodados.ibge.gov.br/api/v1/localidades/estados/SC/municipios", timeout=5.0)
        response.raise_for_status()
        municipios = [m["nome"] for m in response.json()]
        return sorted(municipios)
    except Exception:
        # Fallback de algumas cidades caso a API do IBGE falhe
        return sorted(["Florianópolis", "Joinville", "Blumenau", "São José", "Criciúma", "Chapecó", "Itajaí", "Jaraguá do Sul", "Lages", "Palhoça", "Balneário Camboriú", "Tubarão", "Brusque"])

# Configuração da página
st.set_page_config(
    page_title="SCTEC - Empreendimentos SC",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Estilo CSS customizado para um visual "premium"
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #007bff;
        color: white;
    }
    .status-active {
        color: #28a745;
        font-weight: bold;
    }
    .status-inactive {
        color: #dc3545;
        font-weight: bold;
    }
    .card {
        padding: 1.5rem;
        border-radius: 10px;
        background-color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Inicializa o cliente da API
api = APIClient()

import os
LOGO_PATH = os.path.join(os.path.dirname(__file__), "logoSCTEC.png")

# Sidebar
if os.path.exists(LOGO_PATH):
    st.sidebar.image(LOGO_PATH, use_container_width=True)
else:
    st.sidebar.title("🏗️ SCTEC")
st.sidebar.subheader("Gestão de Empreendimentos SC")

menu = st.sidebar.radio(
    "Navegação",
    ["Dashboard", "Cadastrar Novo", "Gerenciar"]
)

# Check de conexão com o Backend
connected = api.check_health()
if not connected:
    st.sidebar.error("⚠️ Backend Offline")
else:
    st.sidebar.success("✅ Backend Online")

# Segmentos de atuação
SEGMENTOS = ["Tecnologia", "Comércio", "Indústria", "Serviços", "Agronegócio"]
MUNICIPIOS_SC = get_municipios_sc()

# --- PÁGINA: DASHBOARD ---
if menu == "Dashboard":
    st.title("📊 Painel de Empreendimentos")
    
    col1, col2, col3 = st.columns(3)
    
    # Filtros
    with st.expander("🔍 Filtros de Busca"):
        f_col1, f_col2 = st.columns(2)
        with f_col1:
            filtro_municipio = st.selectbox("Município", ["Todos"] + MUNICIPIOS_SC)
        with f_col2:
            filtro_segmento = st.selectbox("Segmento", ["Todos"] + SEGMENTOS)
            
    params = {}
    if filtro_municipio != "Todos": params["municipio_sc"] = filtro_municipio
    if filtro_segmento != "Todos": params["segmento_atuacao"] = filtro_segmento
    
    data = api.get_empreendimentos(params=params)
    
    if data:
        df = pd.DataFrame(data)
        
        # Métricas
        col1.metric("Total", len(df))
        col1.metric("Ativos", len(df[df['status_ativo'] == True]))
        
        # Exibição
        st.subheader("Lista de Empreendimentos")
        
        # Formata para exibição
        display_df = df.copy()
        display_df['Status'] = display_df['status_ativo'].map({True: "✅ Ativo", False: "❌ Inativo"})
        display_df = display_df.drop(columns=['status_ativo'])
        
        st.dataframe(
            display_df[['nome_empreendimento', 'nome_empreendedor', 'municipio_sc', 'segmento_atuacao', 'contato', 'Status']],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("Nenhum empreendimento encontrado.")

# --- PÁGINA: CADASTRAR ---
elif menu == "Cadastrar Novo":
    st.title("➕ Novo Empreendimento")
    st.markdown("Preencha as informações abaixo para cadastrar um novo empreendimento em Santa Catarina.")
    
    with st.form("cadastro_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        
        with c1:
            nome_e = st.text_input("Nome do Empreendimento*", placeholder="Ex: Tech Floripa")
            nome_p = st.text_input("Responsável*", placeholder="Nome do empreendedor")
            municipio = st.selectbox("Município (SC)*", MUNICIPIOS_SC)
        
        with c2:
            segmento = st.selectbox("Segmento*", SEGMENTOS)
            contato = st.text_input("E-mail ou Contato*", placeholder="Ex: contato@empresa.com")
            status_ativo = st.toggle("Status Ativo", value=True)
            
        descricao = st.text_area("Descrição (opcional)", placeholder="Breve resumo sobre o negócio...")
        
        submit = st.form_submit_button("Finalizar Cadastro")
        
        if submit:
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            
            if not all([nome_e, nome_p, municipio, segmento, contato]):
                st.error("Por favor, preencha todos os campos obrigatórios (*).")
            elif "@" in contato and not re.match(email_pattern, contato):
                st.error("O formato do e-mail inserido é inválido.")
            else:
                payload = {
                    "nome_empreendimento": nome_e,
                    "nome_empreendedor": nome_p,
                    "municipio_sc": municipio,
                    "segmento_atuacao": segmento,
                    "contato": contato,
                    "status_ativo": status_ativo,
                    "descricao": descricao
                }
                with st.spinner("Enviando dados..."):
                    success = api.create_empreendimento(payload)
                    if success:
                        st.success(f"✅ '{nome_e}' cadastrado com sucesso!")
                        time.sleep(1)
                    else:
                        st.error("Erro ao cadastrar. Verifique o backend.")

# --- PÁGINA: GERENCIAR ---
elif menu == "Gerenciar":
    st.title("⚙️ Gerenciamento")
    
    data = api.get_empreendimentos()
    if not data:
        st.warning("Sem dados para gerenciar.")
    else:
        df = pd.DataFrame(data)
        escolha = st.selectbox("Selecione um empreendimento para gerenciar:", df['nome_empreendimento'].tolist())
        
        item = df[df['nome_empreendimento'] == escolha].iloc[0]
        
        st.divider()
        st.subheader(f"Editando: {item['nome_empreendimento']}")
        
        col_ed1, col_ed2 = st.columns(2)
        
        with col_ed1:
            edit_nome = st.text_input("Nome", value=item['nome_empreendimento'])
            edit_resp = st.text_input("Responsável", value=item['nome_empreendedor'])
            
            idx_mun = MUNICIPIOS_SC.index(item['municipio_sc']) if item['municipio_sc'] in MUNICIPIOS_SC else 0
            edit_cid = st.selectbox("Município", MUNICIPIOS_SC, index=idx_mun)
            
        with col_ed2:
            idx_seg = SEGMENTOS.index(item['segmento_atuacao']) if item['segmento_atuacao'] in SEGMENTOS else 0
            edit_seg = st.selectbox("Segmento", SEGMENTOS, index=idx_seg)
            edit_cont = st.text_input("Contato", value=item['contato'])
            edit_status = st.toggle("Ativo", value=item['status_ativo'], key="edit_toggle")
            
        edit_desc = st.text_area("Descrição", value=item['descricao'] or "")
        
        b1, b2, _ = st.columns([1, 1, 2])
        
        with b1:
            if st.button("Salvar Alterações"):
                upd_payload = {
                    "nome_empreendimento": edit_nome,
                    "nome_empreendedor": edit_resp,
                    "municipio_sc": edit_cid,
                    "segmento_atuacao": edit_seg,
                    "contato": edit_cont,
                    "status_ativo": edit_status,
                    "descricao": edit_desc
                }
                if api.update_empreendimento(item['id'], upd_payload):
                    st.success("Alterações salvas!")
                    st.rerun()
        
        with b2:
            if st.button("Excluir", type="secondary"):
                if api.delete_empreendimento(item['id']):
                    st.warning("Empreendimento removido.")
                    st.rerun()

st.sidebar.markdown("---")
st.sidebar.caption("Desenvolvido para o desafio SCTEC")
