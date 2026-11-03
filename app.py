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
        "ID": 1, "Artigo": "C.E. Kimling Sortido de Gala", "Origem": "Internacional", "Ano": "1974", 
        "Preço (€)": 110.0, "Selecionado para Venda": True, 
        "Notas": "Sortido de gala de prestígio com conteúdo preservado em adega climatizada.", "Fotos": "",
        "Anuncio": "Peça de Colecionismo Histórico - C.E. Kimling Sortido de Gala (1974)\n\nMagnífica peça de memorabilia e design industrial retro de época (1974), destinada a colecionadores e entusiastas de objectos gráficos e embalagens clássicas de prestígio.\n\n• Detalhes da Peça:\n  - Artigo: C.E. Kimling Sortido de Gala\n  - Apresentação: Estojo de colecionador original com elementos gráficos preservados.\n  - Estado de Conservação: Perfeito estado de preservação, mantido rigorosamente em ambiente próprio e controlado (adega climatizada).\n\n• Preço: 110.00 €\n• Condições: Entrega em mão em Agualva-Cacém ou envio postal seguro sob consulta.\n\nPara verdadeiros apreciadores de colecionismo histórico. Para mais informações, envie mensagem privada."
    },
    {
        "ID": 2, "Artigo": "Toscani Extra-Vecchi (5 Unidades)", "Origem": "Itália", "Ano": "c. 1978-1983", 
        "Preço (€)": 40.0, "Selecionado para Venda": True, 
        "Notas": "Edição clássica de exportação, folha Kentucky fermentada.", "Fotos": "",
        "Anuncio": "Peça de Colecionismo Histórico - Estojo Expositor Toscani Extra-Vecchi\n\nMagnífica peça de memorabilia e design industrial retro de fabrico italiano (c. 1978-1983), destinada a colecionadores e entusiastas de objectos de época e selos fiscais.\n\n• Detalhes da Peça:\n  - Artigo: Toscani Extra-Vecchi (5 Unidades)\n  - Apresentação: Edição clássica de exportação com selos fiscais originais de época.\n  - Estado de Conservação: Perfeito estado de preservação, mantido rigorosamente em ambiente próprio e controlado (adega climatizada).\n\n• Preço: 40.00 €\n• Condições: Entrega em mão em Agualva-Cacém ou envio postal seguro sob consulta.\n\nPara verdadeiros apreciadores de colecionismo histórico. Para mais informações, envie mensagem privada."
    },
    {
        "ID": 3, "Artigo": "Don Julián N.º 5 Canárias", "Origem": "Espanha", "Ano": "c. 1988-1992", 
        "Preço (€)": 50.0, "Selecionado para Venda": True, 
        "Notas": "Caixa de madeira com 19 unidades em tubos de alumínio.", "Fotos": "",
        "Anuncio": "Peça de Colecionismo Histórico - Caixa Expositora Don Julián Nº 5 (Espanha)\n\nMagnífica peça de memorabilia e design industrial retro de fabrico espanhol (Ilhas Canárias, c. 1988-1992), com 19 unidades em tubos de alumínio originais.\n\n• Detalhes da Peça:\n  - Artigo: Caixa Expositora Don Julián Nº 5\n  - Apresentação: Caixa de madeira nobre com tubos de alumínio decorativos e selagem original.\n  - Estado de Conservação: Perfeito estado de preservação, mantido rigorosamente em ambiente próprio e controlado (adega climatizada).\n\n• Preço: 50.00 €\n• Condições: Entrega em mão em Agualva-Cacém ou envio postal seguro sob consulta.\n\nPara verdadeiros apreciadores de colecionismo histórico. Para mais informações, envie mensagem privada."
    },
    {
        "ID": 4, "Artigo": "Dutch Masters Panetelas", "Origem": "EUA / Holanda", "Ano": "c. 1968-1974", 
        "Preço (€)": 35.0, "Selecionado para Venda": True, 
        "Notas": "Embalagem clássica vintage em perfeito estado de conservação.", "Fotos": "",
        "Anuncio": "Peça de Colecionismo Histórico - Embalagem Vintage Dutch Masters Panetelas\n\nMagnífica peça de memorabilia e design industrial retro internacional (c. 1968-1974), destinada a colecionadores e entusiastas de objectos gráficos e embalagens clássicas.\n\n• Detalhes da Peça:\n  - Artigo: Dutch Masters Panetelas\n  - Apresentação: Caixa expositora clássica com litografia retro intacta.\n  - Estado de Conservação: Perfeito estado de preservação, mantido rigorosamente em ambiente próprio e controlado (adega climatizada).\n\n• Preço: 35.00 €\n• Condições: Entrega em mão em Agualva-Cacém ou envio postal seguro sob consulta.\n\nPara verdadeiros apreciadores de colecionismo histórico. Para mais informações, envie mensagem privada."
    },
    {
        "ID": 5, "Artigo": "De Huifkar Exclusive 15 (Lote Militar)", "Origem": "Holanda", "Ano": "1974", 
        "Preço (€)": 85.0, "Selecionado para Venda": True, 
        "Notas": "Mostruário com tampa de Oficial Couraceiro e conteúdo original intacto.", "Fotos": "",
        "Anuncio": "Peça de Colecionismo Histórico - Estojo Expositor Militar (De Huifkar, 1974)\n\nExcecional mostruário de prestígio com litografia histórica de época (Oficial Couraceiro) e elementos originais intactos, destinado a colecionadores de memorabilia militar e industrial.\n\n• Detalhes da Peça:\n  - Artigo: De Huifkar Exclusive 15 (Lote Militar)\n  - Apresentação: Tampa decorativa com pintura de época e selagem original intacta.\n  - Estado de Conservação: Perfeito estado de preservação, mantido rigorosamente em ambiente próprio e controlado (adega climatizada).\n\n• Preço: 85.00 €\n• Condições: Entrega em mão em Agualva-Cacém ou envio postal seguro sob consulta.\n\nPara verdadeiros apreciadores de colecionismo histórico. Para mais informações, envie mensagem privada."
    },
    {
        "ID": 6, "Artigo": "Cerdan Perlas 10", "Origem": "Europa", "Ano": "Meados anos 90", 
        "Preço (€)": 65.0, "Selecionado para Venda": True, 
        "Notas": "Apresentação clássica de época em excelente estado.", "Fotos": "",
        "Anuncio": "Peça de Colecionismo Histórico - Estojo Expositor Cerdan Perlas 10\n\nMagnífica peça de memorabilia e design industrial clássico (meados anos 90), destinada a colecionadores e entusiastas de objectos gráficos de época.\n\n• Detalhes da Peça:\n  - Artigo: Cerdan Perlas 10\n  - Apresentação: Embalagem colecionável com design clássico e acabamentos de época.\n  - Estado de Conservação: Perfeito estado de preservação, mantido rigorosamente em ambiente próprio e controlado (adega climatizada).\n\n• Preço: 65.00 €\n• Condições: Entrega em mão em Agualva-Cacém ou envio postal seguro sob consulta.\n\nPara verdadeiros apreciadores de colecionismo histórico. Para mais informações, envie mensagem privada."
    },
    {
        "ID": 7, "Artigo": "Stompkop Professional", "Origem": "Europa", "Ano": "Anos 70", 
        "Preço (€)": 60.0, "Selecionado para Venda": True, 
        "Notas": "Edição profissional clássica dos anos 70.", "Fotos": "",
        "Anuncio": "Peça de Colecionismo Histórico - Estojo Expositor Stompkop Professional\n\nMagnífica peça de memorabilia e design industrial retro (anos 70), destinada a colecionadores e entusiastas de objectos gráficos e edições limitadas.\n\n• Detalhes da Peça:\n  - Artigo: Stompkop Professional\n  - Apresentação: Mostruário de época com tipografia e elementos gráficos originais.\n  - Estado de Conservação: Perfeito estado de preservação, mantido rigorosamente em ambiente próprio e controlado (adega climatizada).\n\n• Preço: 60.00 €\n• Condições: Entrega em mão em Agualva-Cacém ou envio postal seguro sob consulta.\n\nPara verdadeiros apreciadores de colecionismo histórico. Para mais informações, envie mensagem privada."
    },
    {
        "ID": 8, "Artigo": "Schneehasen Nº 301", "Origem": "Europa", "Ano": "c. 1968-1973", 
        "Preço (€)": 55.0, "Selecionado para Venda": True, 
        "Notas": "Edição vintage colecionável.", "Fotos": "",
        "Anuncio": "Peça de Colecionismo Histórico - Caixa Expositora Schneehasen Nº 301\n\nMagnífica peça de memorabilia e design industrial retro europeu (c. 1968-1973), destinada a colecionadores de objectos gráficos e embalagens clássicas.\n\n• Detalhes da Peça:\n  - Artigo: Schneehasen Nº 301\n  - Apresentação: Embalagem colecionável vintage com selagem de origem.\n  - Estado de Conservação: Perfeito estado de preservação, mantido rigorosamente em ambiente próprio e controlado (adega climatizada).\n\n• Preço: 55.00 €\n• Condições: Entrega em mão em Agualva-Cacém ou envio postal seguro sob consulta.\n\nPara verdadeiros apreciadores de colecionismo histórico. Para mais informações, envie mensagem privada."
    },
    {
        "ID": 9, "Artigo": "Medan 50 Wilde Cigarillos", "Origem": "Europa", "Ano": "c. 1980-1983", 
        "Preço (€)": 55.0, "Selecionado para Venda": True, 
        "Notas": "Caixa expositora com 50 unidades de época.", "Fotos": "",
        "Anuncio": "Peça de Colecionismo Histórico - Caixa Expositora Medan 50 Wilde Cigarillos\n\nMagnífica peça de memorabilia e design industrial retro de época (c. 1980-1983), contendo 50 unidades e destinada a colecionadores de embalagens clássicas.\n\n• Detalhes da Peça:\n  - Artigo: Medan 50 Wilde Cigarillos\n  - Apresentação: Mostruário completo com litografia original de época.\n  - Estado de Conservação: Perfeito estado de preservação, mantido rigorosamente em ambiente próprio e controlado (adega climatizada).\n\n• Preço: 55.00 €\n• Condições: Entrega em mão em Agualva-Cacém ou envio postal seguro sob consulta.\n\nPara verdadeiros apreciadores de colecionismo histórico. Para mais informações, envie mensagem privada."
    },
    {
        "ID": 10, "Artigo": "Ritmeester Assortiment 7030", "Origem": "Holanda", "Ano": "c. 1976-1979", 
        "Preço (€)": 125.0, "Selecionado para Venda": True, 
        "Notas": "Assortiment de prestígio holandês de grande valor para colecionadores.", "Fotos": "",
        "Anuncio": "Peça de Colecionismo Histórico - Mostruário Ritmeester Assortiment 7030\n\nExcecional mostruário de prestígio de fabrico holandês (c. 1976-1979), destinado a colecionadores de alta memorabilia e design industrial retro.\n\n• Detalhes da Peça:\n  - Artigo: Ritmeester Assortiment 7030\n  - Apresentação: Caixa expositora de grande formato com compartimentos e sortido original.\n  - Estado de Conservação: Perfeito estado de preservação, mantido rigorosamente em ambiente próprio e controlado (adega climatizada).\n\n• Preço: 125.00 €\n• Condições: Entrega em mão em Agualva-Cacém ou envio postal seguro sob consulta.\n\nPara verdadeiros apreciadores de colecionismo histórico. Para mais informações, envie mensagem privada."
    },
    {
        "ID": 11, "Artigo": "Fábrica Cañón Rayado", "Origem": "Venezuela", "Ano": "c. 1975-1982", 
        "Preço (€)": 65.0, "Selecionado para Venda": True, 
        "Notas": "Mostruário com aba expositora ilustrada e conteúdo selado completo.", "Fotos": "",
        "Anuncio": "Peça de Colecionismo Histórico - Estojo Expositor Cañón Rayado (Venezuela)\n\nMagnífica peça de memorabilia e design industrial retro de fabrico venezuelano (c. 1975-1982), com aba expositora ilustrada e destinada a colecionadores.\n\n• Detalhes da Peça:\n  - Artigo: Fábrica Cañón Rayado\n  - Apresentação: Mostruário com ilustrações gráficas exclusivas de época.\n  - Estado de Conservação: Perfeito estado de preservação, mantido rigorosamente em ambiente próprio e controlado (adega climatizada).\n\n• Preço: 65.00 €\n• Condições: Entrega em mão em Agualva-Cacém ou envio postal seguro sob consulta.\n\nPara verdadeiros apreciadores de colecionismo histórico. Para mais informações, envie mensagem privada."
    },
    {
        "ID": 12, "Artigo": "Tiparillo Mild Blend", "Origem": "EUA (New York)", "Ano": "c. 1970-1976", 
        "Preço (€)": 30.0, "Selecionado para Venda": True, 
        "Notas": "Pack de bolso vintage com 5 unidades, selado na película original de fábrica.", "Fotos": "",
        "Anuncio": "Peça de Colecionismo Histórico - Embalagem Vintage Tiparillo Mild Blend (EUA)\n\nMagnífica peça de memorabilia e design industrial retro norte-americano (c. 1970-1976), mantida na película celofane original de fábrica.\n\n• Detalhes da Peça:\n  - Artigo: Tiparillo Mild Blend (Pack de Bolso)\n  - Apresentação: Embalagem cartonada original selada de origem.\n  - Estado de Conservação: Perfeito estado de preservação, mantido rigorosamente em ambiente próprio e controlado (adega climatizada).\n\n• Preço: 30.00 €\n• Condições: Entrega em mão em Agualva-Cacém ou envio postal seguro sob consulta.\n\nPara verdadeiros apreciadores de colecionismo histórico. Para mais informações, envie mensagem privada."
    },
    {
        "ID": 13, "Artigo": "Ritmeester Pikeur", "Origem": "Holanda", "Ano": "c. 1978-1985", 
        "Preço (€)": 28.0, "Selecionado para Venda": True, 
        "Notas": "Pocket pack cartonado com janela em acetato e litografia clássica do cavaleiro.", "Fotos": "",
        "Anuncio": "Peça de Colecionismo Histórico - Estojo Expositor Ritmeester Pikeur (Holanda)\n\nMagnífica peça de memorabilia e design industrial retro de fabrico holandês (c. 1978-1985), com janela em acetato e litografia clássica.\n\n• Detalhes da Peça:\n  - Artigo: Ritmeester Pikeur\n  - Apresentação: Pocket pack cartonado com ilustrações temáticas originais.\n  - Estado de Conservação: Perfeito estado de preservação, mantido rigorosamente em ambiente próprio e controlado (adega climatizada).\n\n• Preço: 28.00 €\n• Condições: Entrega em mão em Agualva-Cacém ou envio postal seguro sob consulta.\n\nPara verdadeiros apreciadores de colecionismo histórico. Para mais informações, envie mensagem privada."
    },
    {
        "ID": 14, "Artigo": "Lorillard's L.T. Brown 120's", "Origem": "EUA", "Ano": "c. 1975-1982", 
        "Preço (€)": 32.0, "Selecionado para Venda": True, 
        "Notas": "Maço vintage preto e dourado com celofane original de fábrica intacto.", "Fotos": "",
        "Anuncio": "Peça de Colecionismo Histórico - Embalagem Vintage Lorillard's L.T. Brown 120's (EUA)\n\nMagnífica peça de memorabilia e design industrial retro norte-americano em tons preto e dourado (c. 1975-1982), com selagem integral em celofane.\n\n• Detalhes da Peça:\n  - Artigo: Lorillard's L.T. Brown 120's\n  - Apresentação: Maço rígido colecionável com monograma histórico original.\n  - Estado de Conservação: Perfeito estado de preservação, mantido rigorosamente em ambiente próprio e controlado (adega climatizada).\n\n• Preço: 32.00 €\n• Condições: Entrega em mão em Agualva-Cacém ou envio postal seguro sob consulta.\n\nPara verdadeiros apreciadores de colecionismo histórico. Para mais informações, envie mensagem privada."
    },
    {
        "ID": 15, "Artigo": "King Edward VII Imperial", "Origem": "EUA", "Ano": "c. 1970-1978", 
        "Preço (€)": 35.0, "Selecionado para Venda": True, 
        "Notas": "Estojo vintage com janela em acetato e retrato medalhão do Rei Eduardo VII.", "Fotos": "",
        "Anuncio": "Peça de Colecionismo Histórico - Estojo Expositor King Edward VII Imperial\n\nMagnífica peça de memorabilia e design industrial retro norte-americano (c. 1970-1978), apresentando o retrato medalhão clássico do Rei Eduardo VII.\n\n• Detalhes da Peça:\n  - Artigo: King Edward VII Imperial\n  - Apresentação: Embalagem de bolso com janela em acetato e anilhas originais.\n  - Estado de Conservação: Perfeito estado de preservação, mantido rigorosamente em ambiente próprio e controlado (adega climatizada).\n\n• Preço: 35.00 €\n• Condições: Entrega em mão em Agualva-Cacém ou envio postal seguro sob consulta.\n\nPara verdadeiros apreciadores de colecionismo histórico. Para mais informações, envie mensagem privada."
    },
    {
        "ID": 16, "Artigo": "Álvaro Especiales (Congresso Urologia Tenerife)", "Origem": "Espanha (Canárias)", "Ano": "1985", 
        "Preço (€)": 95.0, "Selecionado para Venda": True, 
        "Notas": "Caixa comemorativa com brasão em relevo e anilhas alusivas ao Congresso de Urologia de 1985.", "Fotos": "",
        "Anuncio": "Peça de Colecionismo Histórico - Caixa Expositora Álvaro Especiales (Tenerife 1985)\n\nExcecional peça de memorabilia e design comemorativo institucional (Congresso de Urologia, Tenerife, 1985), com brasão heráldico em relevo.\n\n• Detalhes da Peça:\n  - Artigo: Álvaro Especiales - Congresso Urologia Tenerife 1985\n  - Apresentação: Estojo comemorativo com anilhas personalizadas do evento.\n  - Estado de Conservação: Perfeito estado de preservação, mantido rigorosamente em ambiente próprio e controlado (adega climatizada).\n\n• Preço: 95.00 €\n• Condições: Entrega em mão em Agualva-Cacém ou envio postal seguro sob consulta.\n\nPara verdadeiros apreciadores de colecionismo histórico. Para mais informações, envie mensagem privada."
    },
    {
        "ID": 17, "Artigo": "Soberano (Gonzalez Byass, Jerez)", "Origem": "Espanha (Jerez)", "Ano": "c. 1978-1985", 
        "Preço (€)": 38.0, "Selecionado para Venda": True, 
        "Notas": "Estojo de bolso vintage associado à histórica casa González Byass com 5 unidades seladas.", "Fotos": "",
        "Anuncio": "Peça de Colecionismo Histórico - Estojo Expositor Soberano (Gonzalez Byass, Jerez)\n\nMagnífica peça de memorabilia e design industrial retro (c. 1978-1985), associada à histórica casa de Jerez González Byass.\n\n• Detalhes da Peça:\n  - Artigo: Soberano / González Byass\n  - Apresentação: Estojo de bolso cartonado com alusão à marca histórica de Jerez.\n  - Estado de Conservação: Perfeito estado de preservação, mantido rigorosamente em ambiente próprio e controlado (adega climatizada).\n\n• Preço: 38.00 €\n• Condições: Entrega em mão em Agualva-Cacém ou envio postal seguro sob consulta.\n\nPara verdadeiros apreciadores de colecionismo histórico. Para mais informações, envie mensagem privada."
    },
    {
        "ID": 18, "Artigo": "De Huifkar Exclusive (Assortment)", "Origem": "Holanda (Duizel)", "Ano": "c. 1978-1985", 
        "Preço (€)": 75.0, "Selecionado para Venda": True, 
        "Notas": "Caixa de prestígio mista com compartimentos Practicus, Pandora e Imperiales.", "Fotos": "",
        "Anuncio": "Peça de Colecionismo Histórico - Caixa Expositora De Huifkar Exclusive (Holanda)\n\nExcecional peça de memorabilia e design industrial retro de fabrico neerlandês (c. 1978-1985), com compartimentos múltiplos (Practicus, Pandora e Imperiales).\n\n• Detalhes da Peça:\n  - Artigo: De Huifkar Exclusive Assortment\n  - Apresentação: Estojo em madeira nobre com folheto decorativo original.\n  - Estado de Conservação: Perfeito estado de preservação, mantido rigorosamente em ambiente próprio e controlado (adega climatizada).\n\n• Preço: 75.00 €\n• Condições: Entrega em mão em Agualva-Cacém ou envio postal seguro sob consulta.\n\nPara verdadeiros apreciadores de colecionismo histórico. Para mais informações, envie mensagem privada."
    },
    {
        "ID": 19, "Artigo": "25 Cedros - Álvaro Especiales", "Origem": "Espanha (Ilhas Canárias)", "Ano": "c. 1978-1986", 
        "Preço (€)": 70.0, "Selecionado para Venda": True, 
        "Notas": "Caixa com 25 unidades, selos fiscais oficiais espanhóis e celofane de fábrica intacto.", "Fotos": "",
        "Anuncio": "Peça de Colecionismo Histórico - Caixa Lote 25 Cedros Álvaro Especiales (Espanha)\n\nMagnífica peça de memorabilia e design industrial retro de fabrico espanhol (Ilhas Canárias, c. 1978-1986), com selos fiscais oficiais de época intactos.\n\n• Detalhes da Peça:\n  - Artigo: 25 Cedros - Álvaro Especiales\n  - Apresentação: Caixa selada com selagem fiscal original de época.\n  - Estado de Conservação: Perfeito estado de preservação, mantido rigorosamente em ambiente próprio e controlado (adega climatizada).\n\n• Preço: 70.00 €\n• Condições: Entrega em mão em Agualva-Cacém ou envio postal seguro sob consulta.\n\nPara verdadeiros apreciadores de colecionismo histórico. Para mais informações, envie mensagem privada."
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
    df_iniciais = pd.DataFrame(dados_iniciais)
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        if "Foto" in df.columns and "Fotos" not in df.columns:
            df["Fotos"] = df["Foto"]
            df = df.drop(columns=["Foto"])
        
        # Sincroniza e adiciona automaticamente artigos novos que ainda não estejam no CSV local
        for _, row in df_iniciais.iterrows():
            if row["ID"] not in df["ID"].values and row["Artigo"] not in df["Artigo"].values:
                df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
    else:
        df = df_iniciais
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
                    
                    anuncio_padrao = f"Peça de Colecionismo Histórico - {row['Artigo']}\n\nMagnífica peça de memorabilia e design industrial retro ({row['Origem']}, {row['Ano']}), destinada a colecionadores e entusiastas de objectos de época.\n\n• Estado de Conservação: Perfeito estado de preservação, mantido rigorosamente em ambiente próprio e controlado (adega climatizada).\n• Preço: {row['Preço (€)']} €\n• Condições: Entrega em mão em Agualva-Cacém ou envio postal seguro sob consulta."
                    anuncio_atual = str(row['Anuncio']) if pd.notna(row['Anuncio']) and row['Anuncio'] != "" else anuncio_padrao
                    novo_anuncio = st.text_area("Texto do Anúncio Guardado (Seguro para Marketplace)", value=anuncio_atual, height=140)
                    
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
    st.info("Consulte e copie rapidamente os textos protegidos contra bloqueios no Marketplace e OLX.")
    
    if df.empty:
        st.info("Sem anúncios disponíveis.")
    else:
        for index, row in df.iterrows():
            with st.expander(f"📋 Anúncio: {row['Artigo']} ({row['Preço (€)']}€)"):
                texto_mostrar = row['Anuncio'] if pd.notna(row['Anuncio']) and row['Anuncio'] != "" else f"Peça de Colecionismo Histórico - {row['Artigo']}\nOrigem: {row['Origem']} ({row['Ano']})\nPreço: {row['Preço (€)']}€\nPerfeito estado de conservação em ambiente próprio. Entrega em Agualva-Cacém."
                st.text_area("Copiar Texto para Plataforma:", value=texto_mostrar, height=140, key=f"copia_txt_{row['ID']}")

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
    st.subheader("📄 Gerador de Catálogo PDF Profissional")
    df_venda = df[df["Selecionado para Venda"] == True]
    st.write(f"Artigos incluídos no catálogo atual para venda: **{len(df_venda)}**")
    
    if st.button("Gerar Catálogo PDF Oficial"):
        try:
            class PDF(FPDF):
                def header(self):
                    self.set_font("Arial", "B", 14)
                    self.cell(0, 8, "CATALOGO DE COLECAO PRIVADA", 0, 1, "C")
                    self.set_font("Arial", "I", 9)
                    self.cell(0, 5, "Localizacao Principal: Agualva-Cacem, Sintra, Portugal", 0, 1, "C")
                    self.set_font("Arial", "", 8)
                    self.set_text_color(100, 100, 100)
                    self.multi_cell(0, 4, "Nota: Inventario exclusivo de pecas de colecionismo historico e memorabilia. Conservacao rigorosa em adega climatizada.")
                    self.set_text_color(0, 0, 0)
                    self.ln(4)
                    self.set_draw_color(150, 150, 150)
                    self.line(10, self.get_y(), 200, self.get_y())
                    self.ln(6)

                def footer(self):
                    self.set_y(-15)
                    self.set_font("Arial", "I", 8)
                    self.cell(0, 10, f"Pagina {self.page_no()}", 0, 0, "C")

            pdf = PDF()
            pdf.add_page()
            pdf.set_font("Arial", "", 10)
            
            for index, (idx, row) in enumerate(df_venda.iterrows(), start=1):
                if pdf.get_y() > 210:
                    pdf.add_page()
                
                pdf.set_font("Arial", "B", 11)
                pdf.cell(150, 6, f"{index}. {row['Artigo']}", 0, 0)
                pdf.set_font("Arial", "B", 11)
                pdf.set_text_color(180, 0, 0)
                pdf.cell(30, 6, f"{row['Preço (€)']} EUR", 0, 1, "R")
                pdf.set_text_color(0, 0, 0)
                
                pdf.set_font("Arial", "I", 9)
                pdf.cell(0, 5, f"Origem: {row['Origem']} | Ano: {row['Ano']}", 0, 1)
                pdf.ln(3)
                
                y_conteudo = pdf.get_y()
                fotos = [f.strip() for f in str(row['Fotos']).split(";") if f.strip() != ""]
                
                texto_detalhes = f"Detalhes / Conservacao: {row['Notas']}"
                
                if fotos and os.path.exists(fotos[0]):
                    try:
                        pdf.image(fotos[0], x=10, y=y_conteudo, h=28)
                        pdf.set_xy(58, y_conteudo)
                        pdf.set_font("Arial", "", 9)
                        pdf.multi_cell(142, 5, texto_detalhes)
                        
                        y_fim_texto = pdf.get_y()
                        y_baixo = max(y_fim_texto, y_conteudo + 28)
                        pdf.set_y(y_baixo + 6)
                    except:
                        pdf.set_font("Arial", "", 9)
                        pdf.multi_cell(0, 5, texto_detalhes)
                        pdf.ln(4)
                else:
                    pdf.set_font("Arial", "", 9)
                    pdf.multi_cell(0, 5, texto_detalhes)
                    pdf.ln(4)
                
                pdf.set_draw_color(220, 220, 220)
                pdf.line(10, pdf.get_y(), 200, pdf.get_y())
                pdf.ln(6)
            
            st.session_state['pdf_bytes'] = bytes(pdf.output())
            st.success("Catálogo PDF profissional gerado com sucesso!")
        except Exception as e:
            st.error(f"Erro ao gerar PDF: {e}")

    if 'pdf_bytes' in st.session_state:
        st.download_button(
            label="Descarregar Catálogo PDF Profissional",
            data=st.session_state['pdf_bytes'],
            file_name="catalogo_colecao_privada.pdf",
            mime="application/pdf",
            key="download_pdf_btn"
        )
