import streamlit as st
import pandas as pd
import os
import base64

# Configuração da página
st.set_page_config(page_title="Base de Dados de Caixas de Charutos Vintage", page_icon="📦", layout="wide")

DATA_FILE = "inventario_charutos_vintage.csv"

dados_iniciais = [
    {"ID": 1, "Artigo": "Willem II 5 Half Corona", "Origem": "Holanda", "Ano": "c. 1982-1985", "Preço (€)": 25.0, "Selecionado para Venda": True, "Notas": "Pocket pack cartonado com janela em acetato. Selados.", "Fotos": ""},
    {"ID": 2, "Artigo": "C.E. Kimling Sortido de Gala", "Origem": "Alemanha", "Ano": "1974", "Preço (€)": 110.0, "Selecionado para Venda": True, "Notas": "Mostruário de luxo com litografia equestre 'The Meet at Blagdon'.", "Fotos": ""},
    {"ID": 3, "Artigo": "Toscani Extra-Vecchi (5 Unidades)", "Origem": "Itália", "Ano": "c. 1978-1983", "Preço (€)": 40.0, "Selecionado para Venda": True, "Notas": "Edição clássica de exportação, folha Kentucky fermentada.", "Fotos": ""},
    {"ID": 4, "Artigo": "Don Julián N.º 5 Canárias", "Origem": "Espanha", "Ano": "c. 1988-1992", "Preço (€)": 50.0, "Selecionado para Venda": True, "Notas": "Caixa de madeira com 19 unidades em tubos de alumínio.", "Fotos": ""},
    {"ID": 5, "Artigo": "Dutch Masters Panetelas", "Origem": "EUA", "Ano": "c. 1968-1974", "Preço (€)": 35.0, "Selecionado para Venda": True, "Notas": "Maço selado com carimbo militar 'TAX EXEMPT'.", "Fotos": ""},
    {"ID": 6, "Artigo": "De Huifkar Exclusive 15 (Lote Militar)", "Origem": "Holanda", "Ano": "1974", "Preço (€)": 85.0, "Selecionado para Venda": True, "Notas": "Mostruário de 25 unidades com tampa de Oficial Couraceiro.", "Fotos": ""},
    {"ID": 7, "Artigo": "Cerdan Perlas 10", "Origem": "República Dominicana", "Ano": "Meados anos 90", "Preço (€)": 65.0, "Selecionado para Venda": True, "Notas": "Puro dominicano, 10 unidades seladas com celofane.", "Fotos": ""},
    {"ID": 8, "Artigo": "Stompkop Professional", "Origem": "Holanda", "Ano": "Anos 70", "Preço (€)": 60.0, "Selecionado para Venda": True, "Notas": "Lote de gala com 10 unidades e anilhas ilustradas históricas.", "Fotos": ""},
    {"ID": 9, "Artigo": "Schneehasen Nº 301", "Origem": "Alemanha", "Ano": "c. 1968-1973", "Preço (€)": 55.0, "Selecionado para Venda": True, "Notas": "Edição rara 'Lebres da Neve' com janela e bases douradas.", "Fotos": ""},
    {"ID": 10, "Artigo": "Medan 50 Wilde Cigarillos", "Origem": "Holanda", "Ano": "c. 1980-1983", "Preço (€)": 55.0, "Selecionado para Venda": True, "Notas": "Caixa de cedro maciça com 50 cigarrilhos Sumatra.", "Fotos": ""},
    {"ID": 11, "Artigo": "Ritmeester Assortiment 7030", "Origem": "Holanda", "Ano": "c. 1976-1979", "Preço (€)": 125.0, "Selecionado para Venda": True, "Notas": "Luxuoso estojo de veludo vermelho com 30 unidades.", "Fotos": ""}
]

# Gravação direta por bytes (Garante que qualquer foto do telemóvel, HDR ou JPG, é guardada de imediato)
def guardar_fotos_direto(lista_ficheiros, id_artigo):
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
    
    df["ID"] = df["ID"].astype(int)
    df["Artigo"] = df["Artigo"].astype(str)
    df["Origem"] = df["Origem"].astype(str)
    df["Ano"] = df["Ano"].astype(str)
    df["Preço (€)"] = df["Preço (€)"].astype(float)
    df["Selecionado para Venda"] = df["Selecionado para Venda"].astype(bool)
    df["Notas"] = df["Notas"].astype(str)
    if "Fotos" not in df.columns:
        df["Fotos"] = ""
    else:
        df["Fotos"] = df["Fotos"].astype(str)
    return df

df = carregar_dados()

st.title("📦 Base de Dados de Charutos")
st.markdown("<small>Gestão compacta otimizada para telemóvel</small>", unsafe_allow_html=True)

aba1, aba2, aba3 = st.tabs(["🖼️ Catálogo", "📊 Vendas & Anúncios", "➕ Novo Artigo"])

with aba1:
    st.subheader("Inventário Compacto")
    
    if df.empty:
        st.warning("Sem artigos.")
    else:
        indices = list(df.index)
        for i in range(0, len(indices), 2):
            col_a, col_b = st.columns(2)
            
            # --- ARTIGO A ---
            idx_1 = indices[i]
            row_1 = df.loc[idx_1]
            with col_a:
                st.markdown(f"**{row_1['Artigo']}**")
                
                fotos_1 = [f.strip() for f in str(row_1['Fotos']).split(";") if f.strip() != ""]
                if fotos_1:
                    html_imgs = '<div style="display: flex; gap: 5px; overflow-x: auto; margin-bottom: 6px;">'
                    for f_path in fotos_1:
                        if os.path.exists(f_path):
                            b64 = imagem_para_base64(f_path)
                            html_imgs += f'<img src="{b64}" style="width: 55px; height: 55px; object-fit: cover; border-radius: 4px; border: 1px solid #444;" />'
                    html_imgs += '</div>'
                    st.markdown(html_imgs, unsafe_allow_html=True)
                else:
                    st.markdown("<small><i>Sem fotos</i></small>", unsafe_allow_html=True)
                
                c_up, c_nom, c_pre = st.columns([1.2, 1.3, 1])
                with c_up:
                    ups_1 = st.file_uploader(f"Fotos ID {row_1['ID']}", type=["jpg", "png", "jpeg", "heic"], accept_multiple_files=True, key=f"up_{row_1['ID']}")
                with c_nom:
                    novo_nome_1 = st.text_input("Nome", value=str(row_1['Artigo']), key=f"n_{row_1['ID']}")
                with c_pre:
                    novo_preco_1 = st.number_input("Preço (€)", value=float(row_1['Preço (€)']), key=f"p_{row_1['ID']}", step=5.0)
                
                if ups_1:
                    novos_caminhos = guardar_fotos_direto(ups_1, row_1['ID'])
                    df.at[idx_1, 'Fotos'] = novos_caminhos
                    df.to_csv(DATA_FILE, index=False)
                    st.success("Fotos guardadas com sucesso!")
                    st.rerun()
                
                if novo_nome_1 != row_1['Artigo'] or novo_preco_1 != row_1['Preço (€)']:
                    df.at[idx_1, 'Artigo'] = str(novo_nome_1)
                    df.at[idx_1, 'Preço (€)'] = float(novo_preco_1)
                    df.to_csv(DATA_FILE, index=False)
                
                st.markdown(f"<small><b>Origem:</b> {row_1['Origem']} ({row_1['Ano']})<br><b>Notas:</b> {row_1['Notas']}</small>", unsafe_allow_html=True)
                
                c_chk, c_del = st.columns([1, 1])
                with c_chk:
                    sel_1 = st.checkbox("Vender", value=bool(row_1['Selecionado para Venda']), key=f"s_{row_1['ID']}")
                    if sel_1 != row_1['Selecionado para Venda']:
                        df.at[idx_1, 'Selecionado para Venda'] = bool(sel_1)
                        df.to_csv(DATA_FILE, index=False)
                        st.rerun()
                with c_del:
                    if st.button("🗑️ Apagar", key=f"del_{row_1['ID']}"):
                        df = df.drop(idx_1)
                        df.to_csv(DATA_FILE, index=False)
                        st.rerun()

            # --- ARTIGO B ---
            if i + 1 < len(indices):
                idx_2 = indices[i + 1]
                row_2 = df.loc[idx_2]
                with col_b:
                    st.markdown(f"**{row_2['Artigo']}**")
                    
                    fotos_2 = [f.strip() for f in str(row_2['Fotos']).split(";") if f.strip() != ""]
                    if fotos_2:
                        html_imgs2 = '<div style="display: flex; gap: 5px; overflow-x: auto; margin-bottom: 6px;">'
                        for f_path in fotos_2:
                            if os.path.exists(f_path):
                                b64 = imagem_para_base64(f_path)
                                html_imgs2 += f'<img src="{b64}" style="width: 55px; height: 55px; object-fit: cover; border-radius: 4px; border: 1px solid #444;" />'
                        html_imgs2 += '</div>'
                        st.markdown(html_imgs2, unsafe_allow_html=True)
                    else:
                        st.markdown("<small><i>Sem fotos</i></small>", unsafe_allow_html=True)
                    
                    c_up2, c_nom2, c_pre2 = st.columns([1.2, 1.3, 1])
                    with c_up2:
                        ups_2 = st.file_uploader(f"Fotos ID {row_2['ID']}", type=["jpg", "png", "jpeg", "heic"], accept_multiple_files=True, key=f"up_{row_2['ID']}")
                    with c_nom2:
                        novo_nome_2 = st.text_input("Nome", value=str(row_2['Artigo']), key=f"n_{row_2['ID']}")
                    with c_pre2:
                        novo_preco_2 = st.number_input("Preço (€)", value=float(row_2['Preço (€)']), key=f"p_{row_2['ID']}", step=5.0)
                    
                    if ups_2:
                        novos_caminhos2 = guardar_fotos_direto(ups_2, row_2['ID'])
                        df.at[idx_2, 'Fotos'] = novos_caminhos2
                        df.to_csv(DATA_FILE, index=False)
                        st.success("Fotos guardadas com sucesso!")
                        st.rerun()
                    
                    if novo_nome_2 != row_2['Artigo'] or novo_preco_2 != row_2['Preço (€)']:
                        df.at[idx_2, 'Artigo'] = str(novo_nome_2)
                        df.at[idx_2, 'Preço (€)'] = float(novo_preco_2)
                        df.to_csv(DATA_FILE, index=False)
                    
                    st.markdown(f"<small><b>Origem:</b> {row_2['Origem']} ({row_2['Ano']})<br><b>Notas:</b> {row_2['Notas']}</small>", unsafe_allow_html=True)
                    
                    c_chk2, c_del2 = st.columns([1, 1])
                    with c_chk2:
                        sel_2 = st.checkbox("Vender", value=bool(row_2['Selecionado para Venda']), key=f"s_{row_2['ID']}")
                        if sel_2 != row_2['Selecionado para Venda']:
                            df.at[idx_2, 'Selecionado para Venda'] = bool(sel_2)
                            df.to_csv(DATA_FILE, index=False)
                            st.rerun()
                    with c_del2:
                        if st.button("🗑️ Apagar", key=f"del_{row_2['ID']}"):
                            df = df.drop(idx_2)
                            df.to_csv(DATA_FILE, index=False)
                            st.rerun()
            
            st.divider()

with aba2:
    st.subheader("📊 Vendas & Anúncios")
    df_vendas = df[df["Selecionado para Venda"] == True]
    
    if df_vendas.empty:
        st.warning("Nenhum artigo selecionado.")
    else:
        st.success(f"Total: {len(df_vendas)} artigos | Valor: {df_vendas['Preço (€)'].sum()}€")
        st.dataframe(df_vendas[["Artigo", "Origem", "Preço (€)"]], use_container_width=True)
        
        for index, row in df_vendas.iterrows():
            with st.expander(f"📢 {row['Artigo']} — {row['Preço (€)']}€"):
                t = f"Caixa Colecionável de Memorabilia e Arte - {row['Artigo']}"
                d = f"Magnífica caixa de colecionismo ({row['Origem']}, {row['Ano']}). {row['Notas']}\nPreço: {row['Preço (€)']}€."
                st.text_input("Título:", value=t, key=f"t_{row['ID']}")
                st.text_area("Descrição:", value=d, key=f"d_{row['ID']}")

with aba3:
    st.subheader("➕ Adicionar Artigo")
    with st.form("form_novo", clear_on_submit=True):
        n_artigo = st.text_input("Nome")
        n_origem = st.text_input("Origem")
        n_ano = st.text_input("Ano")
        n_preco = st.number_input("Preço (€)", value=50.0)
        n_notas = st.text_area("Notas")
        n_fotos = st.file_uploader("Fotos (Max 4)", type=["jpg", "png", "jpeg", "heic"], accept_multiple_files=True)
        
        if st.form_submit_button("Guardar"):
            novo_id_temp = int(df["ID"].max() + 1) if not df.empty else 1
            novos_caminhos_novo = ""
            if n_fotos:
                novos_caminhos_novo = guardar_fotos_direto(n_fotos, f"novo_{novo_id_temp}")
            
            novo_registo = pd.DataFrame([{
                "ID": novo_id_temp,
                "Artigo": str(n_artigo),
                "Origem": str(n_origem),
                "Ano": str(n_ano),
                "Preço (€)": float(n_preco),
                "Selecionado para Venda": True,
                "Notas": str(n_notas),
                "Fotos": str(novos_caminhos_novo)
            }])
            df = pd.concat([df, novo_registo], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("Adicionado!")
            st.rerun()
