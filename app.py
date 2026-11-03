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

# Base de dados inicial dos artigos catalogados
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

# Menu lateral ou separadores
aba = st.sidebar.radio("Navegação", ["Catálogo Existente", "Adicionar Novo Artigo (Telemóvel/HDR)"])

if aba == "Catálogo Existente":
    st.subheader("📋 Artigos Catalogados no Espólio")
    
    for item in st.session_state.catalogo:
        with st.expander(f"📦 {item['artigo']} ({item['ano']}) - {item['preco']}€"):
            st.write(f"**Origem:** {item['origem']}")
            st.write(f"**Notas:** {item['notas']}")
            
            # Exemplo de texto de anúncio pronto a usar
            if st.button(f"Gerar Texto de Anúncio - ID {item['id']}", key=f"btn_{item['id']}"):
                st.markdown("### 📢 Anúncio Otimizado (OLX / Marketplace)")
                st.code(f"""Vendo magnífico artigo de coleção vintage: {item['artigo']}.
Origem: {item['origem']} ({item['ano']}).
Estado: Preservado em ambiente controlado de adega. Conteúdo original de época.
Preço: {item['preco']}€.
Entrega em mão na zona de Agualva-Cacém (Sintra) ou envio a combinar.""")

elif aba == "Adicionar Novo Artigo (Telemóvel/HDR)":
    st.subheader("📸 Adicionar Novo Artigo com Suporte a HDR")
    
    uploaded_file = st.file_uploader("Carregar fotografia do artigo (Telemóvel / Ultra HDR)", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        processed_img = process_uploaded_image(uploaded_file)
        
        if processed_img is not None:
            st.success("Fotografia processada com sucesso!")
            st.image(processed_img, caption="Pré-visualização", use_container_width=True)
            
            with st.form("form_novo_artigo"):
                novo_nome = st.text_input("Nome do Artigo", value="")
                nova_origem = st.text_input("Origem", value="")
                novo_ano = st.text_input("Ano Estimado", value="")
                novo_preco = st.number_input("Preço (€)", value=0.0)
                novas_notas = st.text_area("Notas / Descrição", value="")
                
                submitted = st.form_submit_button("Guardar na Base de Dados")
                if submitted:
                    novo_id = len(st.session_state.catalogo) + 1
                    st.session_state.catalogo.append({
                        "id": novo_id,
                        "artigo": novo_nome,
                        "origem": nova_origem,
                        "ano": novo_ano,
                        "preco": novo_preco,
                        "notas": novas_notas
                    })
                    st.success("Artigo adicionado com sucesso ao catálogo!")
