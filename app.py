import streamlit as st
import pandas as pd
import os

# Configuração da página
st.set_page_config(page_title="Base de Dados de Caixas de Charutos Vintage", page_icon="📦", layout="wide")

# Ficheiro local para guardar o inventário com fotos e estados
DATA_FILE = "inventario_charutos_vintage.csv"

# Dados iniciais baseados no catálogo oficial
dados_iniciais = [
    {"ID": 1, "Artigo": "Willem II 5 Half Corona", "Origem": "Holanda", "Ano": "c. 1982-1985", "Preço (€)": 25.0, "Selecionado para Venda": True, "Notas": "Pocket pack cartonado com janela em acetato. Selados.", "Foto": ""},
    {"ID": 2, "Artigo": "C.E. Kimling Sortido de Gala", "Origem": "Alemanha", "Ano": "1974", "Preço (€)": 110.0, "Selecionado para Venda": True, "Notas": "Mostruário de luxo com litografia equestre 'The Meet at Blagdon'.", "Foto": ""},
    {"ID": 3, "Artigo": "Toscani Extra-Vecchi (5 Unidades)", "Origem": "Itália", "Ano": "c. 1978-1983", "Preço (€)": 40.0, "Selecionado para Venda": True, "Notas": "Edição clássica de exportação, folha Kentucky fermentada.", "Foto": ""},
    {"ID": 4, "Artigo": "Don Julián N.º 5 Canárias", "Origem": "Espanha", "Ano": "c. 1988-1992", "Preço (€)": 50.0, "Selecionado para Venda": True, "Notas": "Caixa de madeira com 19 unidades em tubos de alumínio.", "Foto": ""},
    {"ID": 5, "Artigo": "Dutch Masters Panetelas", "Origem": "EUA", "Ano": "c. 1968-1974", "Preço (€)": 35.0, "Selecionado para Venda": True, "Notas": "Maço selado com carimbo militar 'TAX EXEMPT'.", "Foto": ""},
    {"ID": 6, "Artigo": "De Huifkar Exclusive 15 (Lote Militar)", "Origem": "Holanda", "Ano": "1974", "Preço (€)": 85.0, "Selecionado para Venda": True, "Notas": "Mostruário de 25 unidades com tampa de Oficial Couraceiro.", "Foto": ""},
    {"ID": 7, "Artigo": "Cerdan Perlas 10", "Origem": "República Dominicana", "Ano": "Meados anos 90", "Preço (€)": 65.0, "Selecionado para Venda": True, "Notas": "Puro dominicano, 10 unidades seladas com celofane.", "Foto": ""},
    {"ID": 8, "Artigo": "Stompkop Professional", "Origem": "Holanda", "Ano": "Anos 70", "Preço (€)": 60.0, "Selecionado para Venda": True, "Notas": "Lote de gala com 10 unidades e anilhas ilustradas históricas.", "Foto": ""},
    {"ID": 9, "Artigo": "Schneehasen Nº 301", "Origem": "Alemanha", "Ano": "c. 1968-1973", "Preço (€)": 55.0, "Selecionado para Venda": True, "Notas": "Edição rara 'Lebres da Neve' com janela e bases douradas.", "Foto": ""},
    {"ID": 10, "Artigo": "Medan 50 Wilde Cigarillos", "Origem": "Holanda", "Ano": "c. 1980-1983", "Preço (€)": 55.0, "Selecionado para Venda": True, "Notas": "Caixa de cedro maciça com 50 cigarrilhos Sumatra.", "Foto": ""},
    {"ID": 11, "Artigo": "Ritmeester Assortiment 7030", "Origem": "Holanda", "Ano": "c. 1976-1979", "Preço (€)": 125.0, "Selecionado para Venda": True, "Notas": "Luxuoso estojo de veludo vermelho com 30 unidades.", "Foto": ""}
]

# Função para carregar dados guardados ou criar iniciais
def carregar_dados():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        df_inicial = pd.DataFrame(dados_iniciais)
        df_inicial.to_csv(DATA_FILE, index=False)
        return df_inicial

df = carregar_dados()
if "Selecionado para Venda" not in df.columns:
    df["Selecionado para Venda"] = True
if "Foto" not in df.columns:
    df["Foto"] = ""

st.title("📦 Base de Dados de Caixas de Charutos Vintage")
st.write("Gerza o seu inventário visualmente, selecione artigos e consulte a tabela de vendas por separadores.")

# Organização por Separadores (Abas)
aba1, aba2, aba3 = st.tabs(["🖼️ Catálogo Visual (2 por linha)", "📊 Tabela de Vendas & Resumo", "➕ Adicionar Novo Artigo"])

with aba1:
    st.subheader("Inventário e Seleção Visual")
    st.info("Visualize as caixas em formato dividido (2 por linha), faça upload de fotografias e selecione o que deseja vender.")
    
    if df.empty:
        st.warning("Não existem artigos na base de dados.")
    else:
        # Percorrer os artigos de 2 em 2 para criar o layout dividido
        indices = list(df.index)
        for i in range(0, len(indices), 2):
            col_a, col_b = st.columns(2)
            
            # Primeiro artigo da linha
            idx_1 = indices[i]
            row_1 = df.loc[idx_1]
            
            with col_a:
                st.markdown(f"### {row_1['Artigo']}")
                if pd.notna(row_1['Foto']) and row_1['Foto'] != "" and os.path.exists(str(row_1['Foto'])):
                    st.image(row_1['Foto'], width=200)
                else:
                    st.markdown("🖼️ *Sem Fotografia*")
                
                # Upload de foto individual
                up_1 = st.file_uploader(f"Alterar foto (ID {row_1['ID']})", type=["jpg", "png", "jpeg"], key=f"up_{row_1['ID']}")
                if up_1 is not None:
                    os.makedirs("imagens_caixas", exist_ok=True)
                    caminho = os.path.join("imagens_caixas", f"artigo_{row_1['ID']}.jpg")
                    with open(caminho, "wb") as f:
                        f.write(up_1.getbuffer())
                    df.at[idx_1, 'Foto'] = caminho
                    df.to_csv(DATA_FILE, index=False)
                    st.rerun()
                
                # Campos editáveis rápidos
                novo_nome_1 = st.text_input("Nome", value=str(row_1['Artigo']), key=f"n_{row_1['ID']}")
                novo_preco_1 = st.number_input("Preço (€)", value=float(row_1['Preço (€)']), key=f"p_{row_1['ID']}", step=5.0)
                
                if novo_nome_1 != row_1['Artigo'] or novo_preco_1 != row_1['Preço (€)']:
                    df.at[idx_1, 'Artigo'] = novo_nome_1
                    df.at[idx_1, 'Preço (€)'] = novo_preco_1
                    df.to_csv(DATA_FILE, index=False)
                
                st.write(f"**Origem/Ano:** {row_1['Origem']} ({row_1['Ano']})")
                st.write(f"*Notas:* {row_1['Notas']}")
                
                sel_1 = st.checkbox("Selecionado para Venda", value=bool(row_1['Selecionado para Venda']), key=f"s_{row_1['ID']}")
                if sel_1 != row_1['Selecionado para Venda']:
                    df.at[idx_1, 'Selecionado para Venda'] = sel_1
                    df.to_csv(DATA_FILE, index=False)
                    st.rerun()
                
                # Botão de apagar artigo
                if st.button("🗑️ Eliminar Artigo", key=f"del_{row_1['ID']}"):
                    df = df.drop(idx_1)
                    df.to_csv(DATA_FILE, index=False)
                    st.success("Artigo eliminado!")
                    st.rerun()

            # Segundo artigo da linha (se existir)
            if i + 1 < len(indices):
                idx_2 = indices[i + 1]
                row_2 = df.loc[idx_2]
                
                with col_b:
                    st.markdown(f"### {row_2['Artigo']}")
                    if pd.notna(row_2['Foto']) and row_2['Foto'] != "" and os.path.exists(str(row_2['Foto'])):
                        st.image(row_2['Foto'], width=200)
                    else:
                        st.markdown("🖼️ *Sem Fotografia*")
                    
                    up_2 = st.file_uploader(f"Alterar foto (ID {row_2['ID']})", type=["jpg", "png", "jpeg"], key=f"up_{row_2['ID']}")
                    if up_2 is not None:
                        os.makedirs("imagens_caixas", exist_ok=True)
                        caminho = os.path.join("imagens_caixas", f"artigo_{row_2['ID']}.jpg")
                        with open(caminho, "wb") as f:
                            f.write(up_2.getbuffer())
                        df.at[idx_2, 'Foto'] = caminho
                        df.to_csv(DATA_FILE, index=False)
                        st.rerun()
                    
                    novo_nome_2 = st.text_input("Nome", value=str(row_2['Artigo']), key=f"n_{row_2['ID']}")
                    novo_preco_2 = st.number_input("Preço (€)", value=float(row_2['Preço (€)']), key=f"p_{row_2['ID']}", step=5.0)
                    
                    if novo_nome_2 != row_2['Artigo'] or novo_preco_2 != row_2['Preço (€)']:
                        df.at[idx_2, 'Artigo'] = novo_nome_2
                        df.at[idx_2, 'Preço (€)'] = novo_preco_2
                        df.to_csv(DATA_FILE, index=False)
                    
                    st.write(f"**Origem/Ano:** {row_2['Origem']} ({row_2['Ano']})")
                    st.write(f"*Notas:* {row_2['Notas']}")
                    
                    sel_2 = st.checkbox("Selecionado para Venda", value=bool(row_2['Selecionado para Venda']), key=f"s_{row_2['ID']}")
                    if sel_2 != row_2['Selecionado para Venda']:
                        df.at[idx_2, 'Selecionado para Venda'] = sel_2
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
        st.warning("Nenhum artigo selecionado para venda. Selecione artigos no primeiro separador.")
    else:
        total_valor = df_vendas["Preço (€)"].sum()
        st.success(f"**Total de artigos selecionados para venda:** {len(df_vendas)} | **Valor Total Combinado:** {total_valor}€")
        
        # Tabela resumo limpa
        st.dataframe(df_vendas[["Artigo", "Origem", "Ano", "Preço (€)"]], use_container_width=True)
        
        st.divider()
        st.subheader("Textos Prontos a Copiar para OLX e Marketplace (Seguros)")
        
        for index, row in df_vendas.iterrows():
            with st.expander(f"📢 Anúncio: {row['Artigo']} — {row['Preço (€)']}€"):
                titulo_seguro = f"Caixa Colecionável de Memorabilia e Arte - {row['Artigo']}"
                descricao_segura = f"""Magnífica caixa expositora de colecionismo de fabrico histórico ({row['Origem']}). 

• Detalhes do Artigo:
  - Referência: {row['Artigo']}
  - Período/Ano: {row['Ano']}
  - Descrição: {row['Notas']}
  - Estado de Conservação: Mantido em ambiente controlado.

• Preço: {row['Preço (€)']}€
• Condições: Entrega em mãos na zona de Sintra/Lisboa ou envio postal seguro sob consulta."""

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
        n_foto = st.file_uploader("Fotografia da Caixa", type=["jpg", "png", "jpeg"])
        
        submitted = st.form_submit_button("Guardar Novo Artigo")
        if submitted:
            nova_foto_path = ""
            if n_foto is not None:
                os.makedirs("imagens_caixas", exist_ok=True)
                nova_foto_path = os.path.join("imagens_caixas", f"artigo_novo_{len(df)+1}.jpg")
                with open(nova_foto_path, "wb") as f:
                    f.write(n_foto.getbuffer())
            
            novo_registo = pd.DataFrame([{
                "ID": int(df["ID"].max() + 1) if not df.empty else 1,
                "Artigo": n_artigo,
                "Origem": n_origem,
                "Ano": n_ano,
                "Preço (€)": n_preco,
                "Selecionado para Venda": True,
                "Notas": n_notas,
                "Foto": nova_foto_path
            }])
            df = pd.concat([df, novo_registo], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("Artigo adicionado com sucesso! Atualize a página.")