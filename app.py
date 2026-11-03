import streamlit as st
import pandas as pd
import os
from PIL import Image, ImageOps

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

def carregar_dados():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        # Compatibilidade se vinha do formato antigo "Foto"
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

st.title("📦 Base de Dados de Caixas de Charutos Vintage")
st.write("Gestão de inventário visual (até 4 fotos por artigo), seleção e anúncios.")

aba1, aba2, aba3 = st.tabs(["🖼️ Catálogo Visual (2 por linha)", "📊 Tabela de Vendas & Resumo", "➕ Adicionar Novo Artigo"])

with aba1:
    st.subheader("Inventário e Seleção Visual")
    
    if df.empty:
        st.warning("Não existem artigos na base de dados.")
    else:
        indices = list(df.index)
        for i in range(0, len(indices), 2):
            col_a, col_b = st.columns(2)
            
            # Artigo A
            idx_1 = indices[i]
            row_1 = df.loc[idx_1]
            with col_a:
                st.markdown(f"### {row_1['Artigo']}")
                
                # Mostrar fotografias existentes (separadas por ponto e vírgula)
                fotos_1 = [f.strip() for f in str(row_1['Fotos']).split(";") if f.strip() != ""]
                if fotos_1:
                    cols_fotos = st.columns(min(len(fotos_1), 4))
                    for f_idx, f_path in enumerate(fotos_1):
                        if os.path.exists(f_path):
                            with cols_fotos[f_idx]:
                                st.image(f_path, width=100)
                else:
                    st.markdown("🖼️ *Sem Fotografias*")
                
                # Upload múltiplo (até 4 fotos)
                ups_1 = st.file_uploader(f"Carregar fotos (Máx 4) - ID {row_1['ID']}", type=["jpg", "png", "jpeg"], accept_multiple_files=True, key=f"up_{row_1['ID']}")
                if ups_1:
                    if len(ups_1) > 4:
                        st.warning("Pode selecionar no máximo 4 fotografias.")
                    else:
                        os.makedirs("imagens_caixas", exist_ok=True)
                        novos_caminhos = []
                        for f_pos, up_file in enumerate(ups_1):
                            processed_img = process_uploaded_image(up_file)
                            if processed_img:
                                caminho = os.path.join("imagens_caixas", f"artigo_{row_1['ID']}_f{f_pos+1}.jpg")
                                processed_img.save(caminho, "JPEG")
                                novos_caminhos.append(caminho)
                        df.at[idx_1, 'Fotos'] = ";".join(novos_caminhos)
                        df.to_csv(DATA_FILE, index=False)
                        st.success("Fotografias atualizadas com sucesso!")
                        st.rerun()
                
                novo_nome_1 = st.text_input("Nome", value=str(row_1['Artigo']), key=f"n_{row_1['ID']}")
                novo_preco_1 = st.number_input("Preço (€)", value=float(row_1['Preço (€)']), key=f"p_{row_1['ID']}", step=5.0)
                
                if novo_nome_1 != row_1['Artigo'] or novo_preco_1 != row_1['Preço (€)']:
                    df.at[idx_1, 'Artigo'] = str(novo_nome_1)
                    df.at[idx_1, 'Preço (€)'] = float(novo_preco_1)
                    df.to_csv(DATA_FILE, index=False)
                
                st.write(f"**Origem/Ano:** {row_1['Origem']} ({row_1['Ano']})")
                st.write(f"*Notas:* {row_1['Notas']}")
                
                sel_1 = st.checkbox("Selecionado para Venda", value=bool(row_1['Selecionado para Venda']), key=f"s_{row_1['ID']}")
                if sel_1 != row_1['Selecionado para Venda']:
                    df.at[idx_1, 'Selecionado para Venda'] = bool(sel_1)
                    df.to_csv(DATA_FILE, index=False)
                    st.rerun()
                
                if st.button("🗑️ Eliminar Artigo", key=f"del_{row_1['ID']}"):
                    df = df.drop(idx_1)
                    df.to_csv(DATA_FILE, index=False)
                    st.success("Artigo eliminado!")
                    st.rerun()

            # Artigo B
            if i + 1 < len(indices):
                idx_2 = indices[i + 1]
                row_2 = df.loc[idx_2]
                with col_b:
                    st.markdown(f"### {row_2['Artigo']}")
                    
                    fotos_2 = [f.strip() for f in str(row_2['Fotos']).split(";") if f.strip() != ""]
                    if fotos_2:
                        cols_fotos2 = st.columns(min(len(fotos_2), 4))
                        for f_idx, f_path in enumerate(fotos_2):
                            if os.path.exists(f_path):
                                with cols_fotos2[f_idx]:
                                    st.image(f_path, width=100)
                    else:
                        st.markdown("🖼️ *Sem Fotografias*")
                    
                    ups_2 = st.file_uploader(f"Carregar fotos (Máx 4) - ID {row_2['ID']}", type=["jpg", "png", "jpeg"], accept_multiple_files=True, key=f"up_{row_2['ID']}")
                    if ups_2:
                        if len(ups_2) > 4:
                            st.warning("Pode selecionar no máximo 4 fotografias.")
                        else:
                            os.makedirs("imagens_caixas", exist_ok=True)
                            novos_caminhos2 = []
                            for f_pos, up_file in enumerate(ups_2):
                                processed_img = process_uploaded_image(up_file)
                                if processed_img:
                                    caminho = os.path.join("imagens_caixas", f"artigo_{row_2['ID']}_f{f_pos+1}.jpg")
                                    processed_img.save(caminho, "JPEG")
                                    novos_caminhos2.append(caminho)
                            df.at[idx_2, 'Fotos'] = ";".join(novos_caminhos2)
                            df.to_csv(DATA_FILE, index=False)
                            st.success("Fotografias atualizadas com sucesso!")
                            st.rerun()
                    
                    novo_nome_2 = st.text_input("Nome", value=str(row_2['Artigo']), key=f"n_{row_2['ID']}")
                    novo_preco_2 = st.number_input("Preço (€)", value=float(row_2['Preço (€)']), key=f"p_{row_2['ID']}", step=5.0)
                    
                    if novo_nome_2 != row_2['Artigo'] or novo_preco_2 != row_2['Preço (€)']:
                        df.at[idx_2, 'Artigo'] = str(novo_nome_2)
                        df.at[idx_2, 'Preço (€)'] = float(novo_preco_2)
                        df.to_csv(DATA_FILE, index=False)
                    
                    st.write(f"**Origem/Ano:** {row_2['Origem']} ({row_2['Ano']})")
                    st.write(f"*Notas:* {row_2['Notas']}")
                    
                    sel_2 = st.checkbox("Selecionado para Venda", value=bool(row_2['Selecionado para Venda']), key=f"s_{row_2['ID']}")
                    if sel_2 != row_2['Selecionado para Venda']:
                        df.at[idx_2, 'Selecionado para Venda'] = bool(sel_2)
                        df.to_csv(DATA_FILE, index=False)
                        st.rerun()
                    
                    if st.button("🗑️ Eliminar Artigo", key=f"del_{row_2['ID']}"):
                        df = df.drop(idx_2)
                        df.to_csv(DATA_FILE, index=False)
                        st.success("Artigo eliminado!")
                        st.rerun()
            
            st.divider()

with aba2:
    st.subheader("📊 Resumo da Tabela de Vendas & Anúncios Seguros")
    df_vendas = df[df["Selecionado para Venda"] == True]
    
    if df_vendas.empty:
        st.warning("Nenhum artigo selecionado para venda.")
    else:
        total_valor = df_vendas["Preço (€)"].sum()
        st.success(f"**Total selecionado:** {len(df_vendas)} artigos | **Valor Total:** {total_valor}€")
        st.dataframe(df_vendas[["Artigo", "Origem", "Ano", "Preço (€)"]], use_container_width=True)
        
        st.divider()
        for index, row in df_vendas.iterrows():
            with st.expander(f"📢 Anúncio: {row['Artigo']} — {row['Preço (€)']}€"):
                titulo_seguro = f"Caixa Colecionável de Memorabilia e Arte - {row['Artigo']}"
                descricao_segura = f"""Magnífica caixa expositora de colecionismo de fabrico histórico ({row['Origem']}). 

- Detalhes do Artigo:
  - Referência: {row['Artigo']}
  - Período/Ano: {row['Ano']}
  - Descrição: {row['Notas']}
  - Estado de Conservação: Mantido em ambiente controlado.

- Preço: {row['Preço (€)']}€
- Condições: Entrega em mãos na zona de Sintra/Lisboa ou envio postal seguro sob consulta."""

                st.text_area("Título Otimizado:", value=titulo_seguro, key=f"t_{row['ID']}")
                st.text_area("Descrição Otimizada:", value=descricao_segura, height=120, key=f"d_{row['ID']}")

with aba3:
    st.subheader("➕ Adicionar Novo Artigo à Base de Dados")
    with st.form("form_novo", clear_on_submit=True):
        n_artigo = st.text_input("Nome / Marca do Artigo")
        n_origem = st.text_input("Origem (Ex: Holanda, Alemanha)")
        n_ano = st.text_input("Ano Estimado (Ex: c. 1975)")
        n_preco = st.number_input("Preço (€)", value=50.0)
        n_notas = st.text_area("Notas / Descrição do Estado")
        n_fotos = st.file_uploader("Fotografias da Caixa (Até 4)", type=["jpg", "png", "jpeg"], accept_multiple_files=True)
        
        submitted = st.form_submit_button("Guardar Novo Artigo")
        if submitted:
            novos_caminhos_novo = []
            if n_fotos:
                if len(n_fotos) > 4:
                    st.warning("Pode carregar no máximo 4 fotografias.")
                else:
                    os.makedirs("imagens_caixas", exist_ok=True)
                    novo_id_temp = int(df["ID"].max() + 1) if not df.empty else 1
                    for f_pos, up_file in enumerate(n_fotos):
                        processed_img = process_uploaded_image(up_file)
                        if processed_img:
                            caminho = os.path.join("imagens_caixas", f"artigo_novo_{novo_id_temp}_f{f_pos+1}.jpg")
                            processed_img.save(caminho, "JPEG")
                            novos_caminhos_novo.append(caminho)
            
            novo_registo = pd.DataFrame([{
                "ID": int(df["ID"].max() + 1) if not df.empty else 1,
                "Artigo": str(n_artigo),
                "Origem": str(n_origem),
                "Ano": str(n_ano),
                "Preço (€)": float(n_preco),
                "Selecionado para Venda": True,
                "Notas": str(n_notas),
                "Fotos": ";".join(novos_caminhos_novo)
            }])
            df = pd.concat([df, novo_registo], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("Artigo adicionado com sucesso!")
            st.rerun()
