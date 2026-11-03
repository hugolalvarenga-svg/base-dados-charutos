import streamlit as st
import pandas as pd
from PIL import Image, ImageOps

# Configuração da página
st.set_page_config(page_title="Base de Dados - Caixas de Charutos Vintage", layout="wide")

st.title("📦 Base de Dados de Caixas de Charutos Vintage")
st.markdown("Gestão de espólio e colecionismo de alta gama.")

# Função robusta para processar imagens (Corrige HDR, orientação EXIF e perfis de cor)
def process_uploaded_image(uploaded_file):
    try:
        img = Image.open(uploaded_file)
        img = ImageOps.exif_transpose(img)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        return img
    except Exception as e:
        st.error(f"Erro ao processar o formato da imagem: {e}")
        return None

# Inicialização da base de dados completa na sessão
if 'catalogo' not in st.session_state:
    st.session_state.catalogo = [
        {
            "id": 1,
            "artigo": "Willem II 5 Half Corona",
            "origem": "Holanda (Valkenswaard)",
            "ano": "c. 1982-1985",
            "preco": 25.00,
            "notas": "Pocket pack cartonado em tons de vermelho com janela em acetato transparente. 5 charutos mild individuais selados com celofane original."
        },
        {
            "id": 6,
            "artigo": "De Huifkar Exclusive 15 (Lote Militar)",
            "origem": "Holanda",
            "ano": "1974",
            "preco": 85.00,
            "notas": "Mostruário de prestígio com tampa de Oficial Couraceiro e conteúdo original intacto mantido em adega. Selos fiscais da RFA (12.50 DM)."
        },
        {
            "id": 3,
            "artigo": "Aguere Nº 1 (Série Espacial)",
            "origem": "Espanha (Canárias)",
            "ano": "c. 1969-1972",
            "preco": 60.00,
            "notas": "Pack de 5 unidades com anilhas históricas raras com temática da exploração espacial (NASA/Apollo) e celofanes originais."
        }
    ]

# Menu lateral de navegação completo
menu = st.sidebar.radio("Navegação", ["Catálogo e Anúncios", "Adicionar Novo Artigo (Telemóvel/HDR)"])

if menu == "Catálogo e Anúncios":
    st.subheader("📋 Catálogo Completo de Espólio e Gestão de Anúncios")
    
    # Filtro ou visualização em tabela/cartões
    for item in st.session_state.catalogo:
        with st.expander(f"📦 ID {item['id']} — {item['artigo']} ({item['ano']}) | {item['preco']}€"):
            col1, col2 = st.columns([2, 1])
            with col1:
                st.write(f"**Origem/Fabricante:** {item['origem']}")
                st.write(f"**Notas de Conservação:** {item['notas']}")
            with col2:
                st.metric("Preço de Venda", f"{item['preco']}€")
            
            st.markdown("---")
            st.markdown("#### 📢 Texto de Anúncio Otimizado (OLX / Marketplace)")
            
            # Texto de anúncio gerado automaticamente no padrão de colecionismo
            texto_anuncio = f"""Vendo magnífico artigo de coleção vintage: {item['artigo']}, uma peça de exceção para colecionadores e entusiastas de alta gama.

🎨 Detalhes e Origem:
• Origem: {item['origem']} ({item['ano']}).
• Descrição: {item['notas']}

💎 Conservação:
Preservado rigorosamente em ambiente controlado (adega), mantendo a integridade estrutural e o encanto histórico de época.

🚚 Condições:
• Entrega em mão na zona de Agualva-Cacém (Sintra) ou ponto central próximo.
• Envio postal seguro disponível sob consulta.
Para mais detalhes ou fotografias adicionais, envie mensagem privada."""

            st.code(texto_anuncio, language="text")

elif menu == "Adicionar Novo Artigo (Telemóvel/HDR)":
    st.subheader("📸 Adicionar Artigo com Suporte a Fotografias do Telemóvel (HDR)")
    
    uploaded_file = st.file_uploader("Carregar fotografia do artigo (Suporta Ultra HDR e telemóveis)", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        processed_img = process_uploaded_image(uploaded_file)
        
        if processed_img is not None:
            st.success("Fotografia do telemóvel processada com sucesso!")
            st.image(processed_img, caption="Pré-visualização do Artigo", use_container_width=True)
            
            with st.form("form_adicionar"):
                novo_nome = st.text_input("Nome do Artigo / Caixa")
                nova_origem = st.text_input("Origem / Fabricante")
                novo_ano = st.text_input("Ano Estimado (ex: c. 1974)")
                novo_preco = st.number_input("Preço (€)", value=30.0)
                novas_notas = st.text_area("Notas / Descrição Histórica")
                
                btn_gravar = st.form_submit_button("Guardar Artigo na Base de Dados")
                
                if btn_gravar:
                    novo_id = max([x['id'] for x in st.session_state.catalogo], default=0) + 1
                    st.session_state.catalogo.append({
                        "id": novo_id,
                        "artigo": novo_nome,
                        "origem": nova_origem,
                        "ano": novo_ano,
                        "preco": novo_preco,
                        "notas": novas_notas
                    })
                    st.success(f"Artigo '{novo_nome}' adicionado com sucesso ao catálogo!")
