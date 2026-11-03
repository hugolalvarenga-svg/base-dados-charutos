import streamlit as st
import pandas as pd
import os
import base64
from PIL import Image, ImageOps
from fpdf import FPDF

# Configuração da página
st.set_page_config(page_title="Base de Dados de Colecionismo Vintage", page_icon="📦", layout="wide")

DATA_FILE = "inventario_charutos_vintage.csv"

dados_iniciais = [
    {
        "ID": 1, "Artigo": "Willem II 5 Half Corona", "Origem": "Holanda", "Ano": "c. 1982-1985", 
        "Preço (€)": 25.0, "Selecionado para Venda": True, 
        "Notas": "Pocket pack cartonado com janela em acetato. Selados.", "Fotos": "",
        "Anuncio": "Peça de Colecionismo Histórico - Estojo Expositor Vintage (Willem II)\n\nMagnífica peça de memorabilia e design industrial retro de fabrico holandês (c. 1982-1985), destinada a colecionadores e entusiastas de objectos de época.\n\n• Estado de Conservação: Perfeito estado de preservação, mantido rigorosamente em ambiente próprio e controlado (adega climatizada).\n• Preço: 25.00 €\n• Condições: Entrega em mão em Agualva-Cacém ou envio postal seguro sob consulta."
    },
    {
        "ID": 2, "Artigo": "De Huifkar Exclusive 15 (Lote Militar)", "Origem": "Holanda", "Ano": "1974", 
        "Preço (€)": 85.0, "Selecionado para Venda": True, 
        "Notas": "Mostruário com tampa de Oficial Couraceiro e conteúdo original intacto.", "Fotos": "",
        "Anuncio": "Peça de Colecionismo Histórico - Estojo Expositor Militar (De Huifkar, 1974)\n\nExcecional mostruário de prestígio com litografia histórica de época e elementos originais intactos.\n\n• Estado de Conservação: Perfeito estado de preservação, mantido rigorosamente em ambiente próprio e controlado (adega climatizada).\n• Preço: 85.00 €\n• Condições: Entrega em mão em Agualva-Cacém ou envio postal seguro sob consulta."
    },
    {
        "ID": 3, "Artigo": "Toscani Extra-Vecchi (5 Unidades)", "Origem": "Itália", "Ano": "c. 1978-1983", 
        "Preço (€)": 40.0, "Selecionado para Venda": True, 
        "Notas": "Edição clássica de exportação, folha Kentucky fermentada.", "Fotos": "",
        "Anuncio": "Peça de Colecionismo Histórico - Estojo Expositor Toscani Extra-Vecchi\n\nMagnífica peça de memorabilia e design industrial retro de fabrico italiano (c. 1978-1983) com selos fiscais originais.\n\n• Estado de Conservação: Perfeito estado de preservação, mantido rigorosamente em ambiente próprio e controlado (adega climatizada).\n• Preço: 40.00 €\n• Condições: Entrega em mão em Agualva-Cacém ou envio postal seguro sob consulta."
    },
    {
        "ID": 4, "Artigo": "Don Julián N.º 5 Canárias", "Origem": "Espanha", "Ano": "c. 1988-1992", 
        "Preço (€)": 50.0, "Selecionado para Venda": True, 
        "Notas": "Caixa de madeira com 19 unidades em tubos de alumínio.", "Fotos": "",
        "Anuncio": "Peça de Colecionismo Histórico - Caixa Expositora Don Julián Nº 5 (Espanha)\n\nMagnífica peça de memorabilia e design industrial retro de fabrico espanhol (Ilhas Canárias, c. 1988-1992), com 19 unidades em tubos de alumínio originais.\n\n• Estado de Conservação: Perfeito estado de preservação, mantido rigorosamente em ambiente próprio e controlado (adega climatizada).\n• Preço: 50.00 €\n• Condições: Entrega em mão em Agualva-Cacém ou envio postal seguro sob consulta."
    }
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
    
    colunas_obrigatorias = {
        "ID": int, "Artigo": str, "Origem": str, "Ano": str, 
        "Preço (€)": float, "Selecionado para Venda": bool, 
        "Notas": str, "Fotos": str, "Anuncio": str
    }
    for col, tipo in colunas_obrigatorias.items():
        if col not in df.columns:
            df[col] = "" if tipo == str else (0.0 if tipo == float else (True if tipo == bool else 1))
        df[col] = df[col].astype(tipo)
    return df

df = carregar_dados()

st.title("📦 Inventário de Colecionismo Vintage")
st.markdown("Gestão de espólio, fotografias seguras, anúncios guardados e catálogo PDF profissional.")

aba1, aba2, aba3, aba4 = st.tabs(["🖼️ Catálogo & Edição", "📢 Anúncios Guardados", "➕ Novo Artigo", "📄 Catálogo PDF"])

with aba1:
    st.subheader("Catálogo Visual e Gestão de Artigos")
    if df.empty:
        st.info("Sem artigos na base de dados.")
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
                    
                    anuncio_padrao = f"Peça de Colecionismo Histórico - Estojo Expositor Vintage ({row['Artigo']})\n\nMagnífica peça de memorabilia e design industrial retro de época ({row['Origem']}, {row['Ano']}), destinada a colecionadores e entusiastas.\n\n• Estado de Conservação: Perfeito estado de preservação, mantido rigorosamente em ambiente próprio e controlado (adega climatizada).\n• Preço: {row['Preço (€)']} €\n• Condições: Entrega em mão em Agualva-Cacém ou envio postal seguro sob consulta."
                    anuncio_atual = str(row['Anuncio']) if pd.notna(row['Anuncio']) and row['Anuncio'] != "" else anuncio_padrao
                    novo_anuncio = st.text_area("Texto do Anúncio Guardado (Seguro contra Bots)", value=anuncio_atual, height=140)
                    
                    novas_fotos = st.file_uploader("Alterar / Adicionar Fotos (Máx 4)", type=["jpg", "png", "jpeg"], accept_multiple_files=True, key=f"uf_{row['ID']}")
                    
                    if st.form_submit_button("Guardar Alterações e Anúncio"):
                        if novas_fotos:
                            caminhos = guardar_fotos(novas_fotos, row['ID'])
                            df.at[index, 'Fotos'] = caminhos
                        df.at[index, 'Artigo'] = str(novo_artigo)
                        df.at[index, 'Origem'] = str(nova_origem)
                        df.at[index, 'Ano'] = str(novo_ano)
                        df.at[index, 'Preço (€)'] = float(novo_preco)
                        df.at[index, 'Selecionado para Venda'] = bool(novo_sel)
                        df.at[index, 'Notas'] = str(novas_notas)
                        df.at[index, 'Anuncio'] = str(novo_anuncio)
                        df.to_csv(DATA_FILE, index=False)
                        st.success("Alterações e anúncio guardados com sucesso!")
                        st.rerun()

                if st.button("🗑️ Eliminar Artigo", key=f"del_{row['ID']}"):
                    df = df.drop(index)
                    df.to_csv(DATA_FILE, index=False)
                    st.success("Artigo eliminado!")
                    st.rerun()

with aba2:
    st.subheader("📢 Central de Anúncios Guardados (Prontos a Publicar)")
    st.info("Consulte e copie rapidamente os textos protegidos contra bloqueios para colocar no OLX ou Marketplace.")
    
    if df.empty:
        st.info("Sem anúncios disponíveis.")
    else:
        for index, row in df.iterrows():
            with st.expander(f"📋 Anúncio: {row['Artigo']} ({row['Preço (€)']}€)"):
                texto_mostrar = row['Anuncio'] if pd.notna(row['Anuncio']) and row['Anuncio'] != "" else f"Peça de Colecionismo Histórico - {row['Artigo']}\nOrigem: {row['Origem']} ({row['Ano']})\nPreço: {row['Preço (€)']}€\nPerfeito estado de conservação em ambiente próprio. Entrega em Agualva-Cacém."
                st.text_input("Copiar Texto para Plataforma:", value=texto_mostrar, key=f"copia_{row['ID']}")

with aba3:
    st.subheader("➕ Adicionar Novo Artigo")
    with st.form("form_novo_artigo", clear_on_submit=True):
        n_artigo = st.text_input("Título / Nome do Artigo")
        c1, c2 = st.columns(2)
        with c1:
            n_origem = st.text_input("Origem (Ex: Holanda)")
            n_ano = st.text_input("Ano (Ex: c. 1974)")
        with c2:
            n_preco = st.number_input("Preço (€)", value=50.0, step=5.0)
        
        n_notas = st.text_area("Notas / Descrição")
        anuncio_novo_padrao = "Peça de Colecionismo Histórico - Estojo Expositor Vintage\n\nMagnífica peça de memorabilia e design industrial retro, destinada a colecionadores.\n\n• Estado de Conservação: Perfeito estado de preservação, mantido rigorosamente em ambiente próprio e controlado (adega climatizada).\n• Condições: Entrega em mão em Agualva-Cacém ou envio postal seguro sob consulta."
        n_anuncio = st.text_area("Texto do Anúncio Seguro", value=anuncio_novo_padrao, height=140)
        n_fotos = st.file_uploader("Fotografias (Até 4)", type=["jpg", "png", "jpeg"], accept_multiple_files=True)
        
        submitted = st.form_submit_button("Criar Artigo")
        if submitted:
            novo_id = int(df["ID"].max() + 1) if not df.empty else 1
            caminhos_novos = ""
            if n_fotos:
                caminhos_novos = guardar_fotos(n_fotos, novo_id)
            
            novo_registo = pd.DataFrame([{
                "ID": novo_id, "Artigo": str(n_artigo), "Origem": str(n_origem),
                "Ano": str(n_ano), "Preço (€)": float(n_preco), "Selecionado para Venda": True,
                "Notas": str(n_notas), "Fotos": str(caminhos_novos), "Anuncio": str(n_anuncio)
            }])
            df = pd.concat([df, novo_registo], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("Artigo e anúncio criados com sucesso!")
            st.rerun()

with aba4:
    st.subheader("📄 Gerador de Catálogo PDF Profissional para Venda")
    df_venda = df[df["Selecionado para Venda"] == True]
    st.write(f"Artigos incluídos no catálogo atual para venda: **{len(df_venda)}**")
    
    if st.button("Criar Catálogo PDF com Fotografias"):
        try:
            class PDF(FPDF):
                def header(self):
                    self.set_font("Arial", "B", 16)
                    self.cell(0, 10, "CATALOGO DE COLECONISMO VINTAGE", 0, 1, "C")
                    self.set_font("Arial", "I", 10)
                    self.cell(0, 6, "Pecas Exclusivas - Conservacao Rigorosa em Adega Climatizada (Agualva-Cacem)", 0, 1, "C")
                    self.ln(5)
                def footer(self):
                    self.set_y(-15)
                    self.set_font("Arial", "I", 8)
                    self.cell(0, 10, f"Pagina {self.page_no()}", 0, 0, "C")

            pdf = PDF()
            pdf.add_page()
            pdf.set_font("Arial", "", 10)
            
            for idx, row in df_venda.iterrows():
                # Obter a primeira fotografia de cada artigo
                fotos = [f.strip() for f in str(row['Fotos']).split(";") if f.strip() != ""]
                primeira_foto = fotos[0] if fotos and os.path.exists(fotos[0]) else None
                
                # Registar posição inicial do bloco do artigo
                y_inicio = pdf.get_y()
                if y_inicio > 240: # Se estiver perto do fim da página, cria nova página
                    pdf.add_page()
                    y_inicio = pdf.get_y()
                
                # Inserir fotografia à esquerda (largura 30mm) se existir
                if primeira_foto:
                    try:
                        pdf.image(primeira_foto, x=10, y=y_inicio, w=30)
                    except:
                        pass
                
                # Definir texto descritivo à direita da foto (posição X = 45)
                pdf.set_x(45)
                pdf.set_font("Arial", "B", 12)
                pdf.cell(0, 7, f"{row['Artigo']} ({row['Ano']})", 0, 1)
                
                pdf.set_x(45)
                pdf.set_font("Arial", "B", 10)
                pdf.set_text_color(180, 0, 0) # Destacar o preço em tom forte
                pdf.cell(0, 6, f"Preco: {row['Preço (€)']} EUR | Origem: {row['Origem']}", 0, 1)
                
                pdf.set_text_color(0, 0, 0) # Repor cor normal
                pdf.set_x(45)
                pdf.set_font("Arial", "", 9)
                pdf.multi_cell(0, 5, f"Detalhes: {row['Notas']}")
                
                pdf.ln(8) # Espaço elegante entre artigos
                pdf.set_draw_color(200, 200, 200)
                pdf.line(10, pdf.get_y(), 200, pdf.get_y()) # Linha divisória subtil
                pdf.ln(5)
            
            st.session_state['pdf_bytes'] = bytes(pdf.output())
            st.success("Catálogo PDF profissional gerado com sucesso!")
        except Exception as e:
            st.error(f"Erro ao gerar PDF: {e}")

    if 'pdf_bytes' in st.session_state:
        st.download_button(
            label="Descarregar Catálogo PDF para Venda",
            data=st.session_state['pdf_bytes'],
            file_name="catalogo_venda_colecionismo.pdf",
            mime="application/pdf",
            key="download_pdf_btn"
        )
