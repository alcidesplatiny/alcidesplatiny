from streamlit import exception
import streamlit as st
import pandas as pd
import plotly.express as px


try:
    # Configurações iniciais
    st.set_page_config(page_title="Panorama de Imóveis - Alcides Platiny", layout="wide")

        
    # Cabeçalho
    st.header(":red[Dashboard - Panorama de Imóveis para Aluguel no Brasil]", divider="red")
   

    # Importação e tratamento inicial dos dados
    dados = pd.read_csv("houses_to_rent_v2.csv")

    # Converter dados da Dataframe
    dados_imoveis = dados.rename(columns = {"city": "Cidade", "area": "Área do imóvel", "rooms": "Qtd Quartos", "bathroom": "Qtd Banheiros", "parking spaces": "Qtd Garagens", "floor": "Andar do Imóvel", "animal": "Permite Animais", "furniture": "Mobiliado", "hoa (R$)": "Taxa de Condomínio", "rent amount (R$)": "Valor do Aluguel (R$)", "property tax (R$)": "Valor do IPTU (R$)", "fire insurance (R$)": "Seguro contra Incêndio (R$)", "total (R$)": "Total (R$)" })

    # Tconverter colunas "animal" e "furniture":
    dados_imoveis["Permite Animais"] = dados_imoveis["Permite Animais"].replace({"acept": "Sim", "not acept": "Não"})

    dados_imoveis["Mobiliado"] = dados_imoveis["Mobiliado"].replace({"furnished": "Sim", "not furnished": "Não"})

    # Faixas de valores de aluguel para segmentação dos dados no dashboard
    # Função para categorizar as faixas de preço do aluguel
    def categoria_aluguel(valor):
        if valor < 1000:
            return "até R$ 1000"
        elif 1000 <= valor <2000:
            return "Entre R$ 1000 e R$ 1999"
        elif 2000 <= valor <3000:
            return "Entre R$ 2000 e R$ 2999"
        elif 3000 <= valor <4000:
            return "Entre R$ 3000 e R$ 3999"
        elif 4000 <= valor <5000:
            return "Entre R$ 4000 e R$ 4999"
        elif 5000 <= valor:
            return "Acima de R$ 5000"
        

    # Função à coluna de valor do aluguel
    dados_imoveis["Faixas de Preço"] = dados_imoveis["Valor do Aluguel (R$)"].apply(categoria_aluguel)

    # Barra lateral para filtragem
    with st.sidebar:

        # Cabeçalho e informações do aluno
        st.subheader(":red[Discente: Aalcides Platiny Alves Batista]")
        st.subheader(":red[Matrícula: 20242003282]", divider="red")

        st.write("Selecione as opções abaixo para visualizar:")

        cidade = st.multiselect("Cidade", options=dados_imoveis["Cidade"].unique(), default=dados_imoveis["Cidade"].unique())
        mobiliado = st.selectbox("Imóvel Mobiliado?", options=dados_imoveis["Mobiliado"].unique())
        aceita_animais = st.selectbox("Aceita Animais?", options=dados_imoveis["Permite Animais"].unique())
        faixa_preço = st.selectbox("Escolha a faixa de preços de aluguel", options = ["até R$ 1000", "Entre R$ 1000 e R$ 1999", "Entre R$ 2000 e R$ 2999", "Entre R$ 3000 e R$ 3999", "Entre R$ 4000 e R$ 4999", "Acima de R$ 5000"])
        quartos = st.selectbox("Número de Quartos", options=sorted(dados_imoveis["Qtd Quartos"].unique()))
        banheiros = st.selectbox("Número de Banheiros", options = sorted(dados_imoveis["Qtd Banheiros"].unique()))

    # Filtrar os dados com base nas seleções
    dados_filtro = dados_imoveis[
        (dados_imoveis["Cidade"].isin(cidade)) &
        (dados_imoveis["Mobiliado"] == (mobiliado)) &
        (dados_imoveis["Permite Animais"] == (aceita_animais)) &
        (dados_imoveis["Faixas de Preço"] == (faixa_preço)) &
        (dados_imoveis["Qtd Quartos"] == (quartos)) &
        (dados_imoveis["Qtd Banheiros"] == (banheiros))
    ]

    # Dividindo a tela

    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)

    # Segmentando o dataset para os gráficos

    # Quantidade de imóveis por municipio
    imoveis_qtd = dados_imoveis.groupby("Cidade")["Cidade"].count() # dados estáticos, sem relação com os elementos de seleção
    imoveis_cidade = imoveis_qtd.sort_values(ascending=False) # dados estáticos, sem relação com os elementos de seleção

    imoveis_qtd_fil = dados_filtro.groupby("Cidade")["Cidade"].count() # dados filtrados pelos elementos de seleção
    imoveis_cidade_fil = imoveis_qtd_fil.sort_values(ascending=False) # dados filtrados pelos elementos de seleção


    fig_qtd = px.bar(imoveis_cidade, x = imoveis_cidade.index, y = imoveis_cidade.values, color="Cidade", text_auto=True, title= "Total de Imóveis Disponíveis por Múnicipio")
    
    # Remove linhas dos eixos
    fig_qtd.update_layout(
        xaxis=dict(showgrid=False),  # Remove linha do eixo X
        yaxis=dict(showgrid=False)   # Remove linha do eixo Y
    )

    # Remove linhas de grade
    fig_qtd.update_layout(
    yaxis=dict(showticklabels=False)   # Remove linha do eixo Y
    )

    # Nome dos eixos
    fig_qtd.update_layout(
        xaxis_title='Múnicipios',
        yaxis_title=None
    )

    # Filtro de seleção para a quantidade de imóveis por Múnicipio
    fig_qtd_fil = px.bar(imoveis_cidade_fil, x = imoveis_cidade_fil.index, y = imoveis_cidade_fil.values, color="Cidade", text_auto=True, title= "Total de Imóveis Disponíveis por Múnicipios (Filtrado)")
    
    # Remove linhas dos eixos
    fig_qtd_fil.update_layout(
        xaxis=dict(showgrid=False),  # Remove linha do eixo X
        yaxis=dict(showgrid=False)   # Remove linha do eixo Y
    )
    # Removendo as linhas de grade
    fig_qtd_fil.update_layout(
        yaxis=dict(showticklabels=False)   # Remover a linha do eixo Y
    )

    # Nome dos eixos
    fig_qtd_fil.update_layout(
        xaxis_title='Múnicipios',
        yaxis_title=None
    )

    # Plotagem dos gráficos
    col1.plotly_chart(fig_qtd)
    col3.plotly_chart(fig_qtd_fil)

    # Valor médio do aluguel por Múnicipio
    aluguel_cid = dados_imoveis.groupby("Cidade")["Valor do Aluguel (R$)"].mean() # dados estáticos, sem relação com os elementos de seleção
    aluguel_medio = aluguel_cid.sort_values(ascending=False) # dados estáticos, sem relação com os elementos de seleção

    aluguel_cid_fil = dados_filtro.groupby("Cidade")["Valor do Aluguel (R$)"].mean() # dados filtrados pelos elementos de seleção
    aluguel_medio_fil = aluguel_cid_fil.sort_values(ascending=False) # dados filtrados pelos elementos de seleção


    fig_alu = px.bar(aluguel_medio, x = aluguel_medio.index, y = aluguel_medio.values, color="Valor do Aluguel (R$)", text_auto=True, title= "Valor médio do aluguel por Múnicipio - em R$")
    
    # Removendo as linhas dos eixos
    fig_alu.update_layout(
        xaxis=dict(showgrid=False),  # Remover a linha do eixo X
        yaxis=dict(showgrid=False)   # Remover a linha do eixo Y
    )
    # Removendo as linhas de grade
    fig_alu.update_layout(
    
        yaxis=dict(showticklabels=False)   # Remover a linha do eixo Y
    )

    # Nome dos eixos
    fig_alu.update_layout(
        xaxis_title='Múnicipios',
        yaxis_title=None
    )

    # Gráfico de seleção para o valor médio do aluguel por municipio
    fig_alu_fil = px.bar(aluguel_medio_fil, x = aluguel_medio_fil.index, y = aluguel_medio_fil.values, color="Valor do Aluguel (R$)", text_auto=True, title= "Valor médio do aluguel por Múnicipio - em R$ (Filtrado)")
    
    # Remove as linhas dos eixos
    fig_alu_fil.update_layout(
        xaxis=dict(showgrid=False),  # Remove linha do eixo X
        yaxis=dict(showgrid=False)   # Remove linha do eixo Y
    )
    # Remove linhas de grade
    fig_alu_fil.update_layout(
        yaxis=dict(showticklabels=False)   # Remove linha do eixo Y
    )

    # Nomeando os eixos
    fig_alu_fil.update_layout(
        xaxis_title='Municipios',
        yaxis_title=None
    )

    # Plotagem dos gráficos
    col2.plotly_chart(fig_alu)
    col4.plotly_chart(fig_alu_fil)

    # Exibe tabela
    st.subheader(":red[Resultado Filtrado]", divider="red")
    
    st.dataframe(dados_filtro.style.highlight_max(axis=0, color="#5f6362"))


except:
    st.error(
        'A seleção não retornou dados.',)