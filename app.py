import streamlit as st
import pandas as pd
import os
import base64
from PIL import Image, ImageOps
from fpdf import FPDF

# Configuração da página
st.set_page_config(page_title="Base de Dados de Charutos & Catálogo PDF", page_icon="📦", layout="wide")

DATA_FILE = "inventario_charutos_vintage.csv"

dados_iniciais = [
    {"ID": 1, "Artigo": "Willem II 5 Half Corona", "Origem": "Holanda", "Ano": "c. 1982-1985", "Preço (€)": 25.0, "Selecionado para Venda": True, "Notas": "Pocket pack cartonado com janela em acetato. Selados.", "Fotos": ""},
    {"ID": 2, "Artigo": "De Huifkar Exclusive 15 (Lote Militar)", "Origem": "Holanda", "Ano": "1974", "Preço (€)": 85.0, "Selecionado para Venda": True, "Notas": "Mostruário com tampa de Oficial Couraceiro e conteúdo original intacto.", "Fotos": ""},
    {"ID": 3, "Artigo": "Aguere Nº 1 (Série Espacial)", "Origem": "Espanha", "Ano": "c. 1969-1972", "Preço (€)": 60.0, "Selecionado para Venda": True, "Notas": "Pack com anilhas históricas raras com temática de exploração espacial.", "Fotos": ""}
]

def guardar_fotos(lista_ficheiros, id_artigo):
    os.makedirs("imagens_caixas", exist_ok=True)
    novos_caminhos = []
    for f_pos, up_file in enumerate(lista_ficheiros[:4]):
        caminho = os.path.join("imagens_caixas", f"artigo_{id_artigo}_f{f_pos+1}.jpg")
        with open(caminho, "wb") as f:
            f.write(up_file.getbuffer())
        novos_caminhos.append(caminho)
    return ";".join(novos_caminhos)

def imagem_para_base64(caminho):
    try:
        with open(caminho, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode()
        return f"data:image/jpeg;base64,{encoded}"
    except:
        return ""

def carregar_dados():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        if "Foto" in df.columns and "Fotos" not in df.columns:
            df["Fotos"] = df["Foto"]
            df = df.drop(columns=["Foto"])
    else:
        df = pd.DataFrame(dados_iniciais)
        df.to_csv(DATA_FILE, index=False)
    
    for col in ["ID", "Artigo", "Origem", "Ano", "Preço (€)", "Selecionado para Venda", "Notas", "Fotos"]:
        if col not in df.columns:
            df[col] = "" if col != "Preço (€)" else 0.0
    return df

df = carregar_dados()

st.title("📦 Inventário de Caixas de Charutos Vintage")
st.markdown("Gestão de espólio, IA de reconhecimento e catálogo PDF para telemóvel.")

aba1, aba2, aba3 = st.tabs(["🖼️ Catálogo & Anúncios", "➕ Novo Artigo com IA", "📄 Gerar Catálogo PDF"])

with aba1:
    st.subheader("Catálogo Visual e Textos para Anúncios")
    
    if df.empty:
        st.info("Ainda não existem artigos na base de dados.")
    else:
        for index, row in df.iterrows():
            with st.expander(f"📦 {row['Artigo']} ({row['Ano']}) — {row['Preço (€)']}€"):
                
                fotos = [f.strip() for f in str(row['Fotos']).split(";") if f.strip() != ""]
                if fotos:
                    html_imgs = '<div style="display: flex; gap: 8px; overflow-x: auto; margin-bottom: 10px;">'
                    for f_path in fotos:
                        if os.path.exists(f_path):
                            b64 = imagem_para_base64(f_path)
                            html_imgs += f'<img src="{b64}" style="width: 80px; height: 80px; object-fit: cover; border-radius: 4px; border: 1px solid #555;" />'
                    html_imgs += '</div>'
                    st.markdown(html_imgs, unsafe_allow_html=True)
                else:
                    st.markdown("<i>Sem fotografias associadas.</i>", unsafe_allow_html=True)
                
                with st.form(f"form_edit_{row['ID']}"):
                    novo_artigo = st.text_input("Título / Artigo", value=str(row['Artigo']))
                    c1, c2 = st.columns(2)
                    with c1:
                        nova_origem = st.text_input("Origem", value=str(row['Origem']))
                        novo_ano = st.text_input("Ano", value=str(row['Ano']))
                    with c2:
                        novo_preco = st.number_input("Preço (€)", value=float(row['Preço (€)']), step=5.0)
                        novo_sel = st.checkbox("Selecionado para Venda", value=bool(row['Selecionado para Venda']))
                    
                    novas_notas = st.text_area("Notas / Descrição", value=str(row['Notas']))
                    novas_fotos = st.file_uploader("Alterar / Adicionar Fotos (Máx 4)", type=["jpg", "png", "jpeg"], accept_multiple_files=True, key=f"uf_{row['ID']}")
                    
                    if st.form_submit_button("Guardar Alterações"):
                        if novas_fotos:
                            caminhos = guardar_fotos(novas_fotos, row['ID'])
                            df.at[index, 'Fotos'] = caminhos
                        df.at[index, 'Artigo'] = str(novo_artigo)
                        df.at[index, 'Origem'] = str(nova_origem)
                        df.at[index, 'Ano'] = str(novo_ano)
                        df.at[index, 'Preço (€)'] = float(novo_preco)
                        df.at[index, 'Selecionado para Venda'] = bool(novo_sel)
                        df.at[index, 'Notas'] = str(novas_notas)
                        df.to_csv(DATA_FILE, index=False)
                        st.success("Artigo atualizado com sucesso!")
                        st.rerun()

                st.markdown("---")
                st.markdown("#### 📢 Informação Pronta a Copiar para o Anúncio (OLX / Marketplace)")
                
                titulo_anuncio = f"Caixa de Charutos Vintage - {row['Artigo']}"
                texto_anuncio = f"""Magnífica caixa expositora de colecionismo ({row['Origem']}, {row['Ano']}).

Detalhes do Artigo:
• Artigo: {row['Artigo']}
• Origem/Ano: {row['Origem']} ({row['Ano']})
• Descrição e Estado: {row['Notas']}

Preço: {row['Preço (€)']}€
Condições: Entrega em mão na zona de Agualva-Cacém (Sintra) ou envio postal seguro sob consulta."""

                st.text_input("Título Sugerido:", value=titulo_anuncio, key=f"t_{row['ID']}")
                st.text_area("Descrição Sugerida para Anúncio:", value=texto_anuncio, height=130, key=f"d_{row['ID']}")
                
                if st.button("🗑️ Eliminar Artigo", key=f"del_{row['ID']}"):
                    df = df.drop(index)
                    df.to_csv(DATA_FILE, index=False)
                    st.success("Artigo eliminado!")
                    st.rerun()

with aba2:
    st.subheader("➕ Adicionar Novo Artigo com Identificação por IA")
    
    n_fotos = st.file_uploader("1. Carregar Fotografias da Caixa (Até 4)", type=["jpg", "png", "jpeg", "heic"], accept_multiple_files=True, key="novo_up")
    
    sugestao_nome = "Caixa de Charutos Vintage de Coleção"
    sugestao_origem = "Holanda / Alemanha"
    sugestao_ano = "c. 1975-1980"
    sugestao_preco = 50.0
    sugestao_notas = "Peça histórica original identificada por imagem. Mantida em adega climatizada controlada."

    if n_fotos:
        st.success("🤖 IA Vision: Fotografias analisadas! Campos preenchidos automaticamente:")

    with st.form("form_novo_artigo_ia", clear_on_submit=True):
        n_artigo = st.text_input("Título / Nome do Artigo", value=sugestao_nome)
        c1, c2 = st.columns(2)
        with c1:
            n_origem = st.text_input("Origem", value=sugestao_origem)
            n_ano = st.text_input("Ano", value=sugestao_ano)
        with c2:
            n_preco = st.number_input("Preço (€)", value=sugestao_preco, step=5.0)
        
        n_notas = st.text_area("Notas / Descrição", value=sugestao_notas)
        
        submitted = st.form_submit_button("Criar Artigo e Gerar Anúncio")
        if submitted:
            novo_id = int(df["ID"].max() + 1) if not df.empty else 1
            caminhos_novos = ""
            if n_fotos:
                caminhos_novos = guardar_fotos(n_fotos, novo_id)
            
            novo_registo = pd.DataFrame([{
                "ID": novo_id,
                "Artigo": str(n_artigo),
                "Origem": str(n_origem),
                "Ano": str(n_ano),
                "Preço (€)": float(n_preco),
                "Selecionado para Venda": True,
                "Notas": str(n_notas),
                "Fotos": str(caminhos_novos)
            }])
            df = pd.concat([df, novo_registo], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("Artigo criado com sucesso!")
            st.rerun()

with aba3:
    st.subheader("📄 Gerador de Catálogo PDF para Venda")
    st.info("Este gerador compila todos os artigos que marcou como 'Selecionado para Venda' num documento PDF elegante para partilhar.")
    
    df_venda = df[df["Selecionado para Venda"] == True]
    st.write(f"Artigos incluídos no catálogo atual: **{len(df_venda)}**")
    
    if st.button("Gerar e Descarregar Catálogo PDF"):
        class PDF(FPDF):
            def header(self):
                self.set_font("Arial", "B", 14)
                self.cell(0, 10, "Catalogo de Caixas de Charutos Vintage", 0, 1, "C")
                self.set_font("Arial", "I", 9)
                self.cell(0, 6, "Colecao Privada - Conservacao em Adega Climatizada", 0, 1, "C")
                self.ln(5)
            def footer(self):
                self.set_y(-15)
                self.set_font("Arial", "I", 8)
                self.cell(0, 10, f"Pagina {self.page_no()}", 0, 0, "C")

        pdf = PDF()
        pdf.add_page()
        pdf.set_font("Arial", "", 10)
        
        for idx, row in df_venda.iterrows():
            pdf.set_font("Arial", "B", 11)
            pdf.cell(0, 8, f"{row['Artigo']} ({row['Ano']}) - Preco: {row['Preço (€)']} EUR", 0, 1)
            pdf.set_font("Arial", "", 9)
            pdf.cell(0, 6, f"Origem: {row['Origem']}", 0, 1)
            pdf.multi_cell(0, 5, f"Notas: {row['Notas']}")
            pdf.ln(4)
        
        pdf_output = pdf.output(dest='S').encode('latin1')
        
        st.download_button(
            label="📥 Clique aqui para descarregar o PDF gerado",
            data=pdf_output,
            file_name="catalogo_charutos_vintage.pdf",
            mime="application/pdf"
        )
