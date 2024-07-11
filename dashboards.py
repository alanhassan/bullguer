import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout='wide')

# Adiciona o título da página centralizado
st.markdown("<h1 style='text-align: center;'>🍔Bullguer Dash - Oficial🍔</h1>", unsafe_allow_html=True)

# Estilo personalizado para o fundo
st.markdown(
    """
    <style>
    body {
        background-color: #e1e1d5;
    }
    .stApp {
        background-color: #e1e1d5;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Carregar o dataframe
df = pd.read_excel('df.xlsx')

# Convert 'Data' column to datetime
df['Data'] = pd.to_datetime(df['Data'])

# Extract only the date part
df['Data'] = df['Data'].dt.date

df = df.sort_values('Data')

df['mes'] = df['Data'].apply(lambda x: f"{x.year}-{str(x.month).zfill(2)}")

# Adiciona o título do painel de filtros
st.sidebar.title("Filtros")

# Adiciona "Todos" como a primeira opção nas listas de filtros
categorias = ['Todos'] + df['Categoria'].unique().tolist()
integrantes = ['Todos'] + df['Integrante'].unique().tolist()
unidades = ['Todos'] + df['Unidade'].unique().tolist()

categoria = st.sidebar.selectbox("Categoria", categorias)
integrante = st.sidebar.selectbox("Integrante", integrantes)
unidade = st.sidebar.selectbox("Unidade", unidades)

# Filtra o dataframe com base na categoria, integrante e unidade selecionados, se "Todos" não estiver selecionado
df_filtered = df.copy()

if categoria != 'Todos':
    df_filtered = df_filtered[df_filtered['Categoria'] == categoria]

if integrante != 'Todos':
    df_filtered = df_filtered[df_filtered['Integrante'] == integrante]

if unidade != 'Todos':
    df_filtered = df_filtered[df_filtered['Unidade'] == unidade]

df_filtered = df_filtered.reset_index(drop=True)

# Função para definir a cor das barras
def color_bars(values):
    colors = []
    for value in values:
        if value == max(values):
            colors.append('#53c654')  # Maior valor em verde
        elif value == min(values):
            colors.append('#940e0a')    # Menor valor em vermelho
        else:
            colors.append('#767bb2')   # Outros valores em azul
    return colors

# Criar containers para os gráficos
container1 = st.container()
container2 = st.container()
container3 = st.container()

# Primeiro container com o primeiro gráfico
with container1:
    unidade_total = df_filtered.groupby(['Unidade'])[['Nota']].mean().reset_index()
    fig_nota_unidade = px.bar(unidade_total, y="Nota", x="Unidade", title="Unidade", height=500)
    fig_nota_unidade.update_traces(marker_color=color_bars(unidade_total['Nota']), texttemplate='%{y:.2f}', textposition='outside') 
    fig_nota_unidade.update_layout(title_x=0.5, plot_bgcolor='#f0f0f0', paper_bgcolor='#f0f0f0')
    fig_nota_unidade.update_yaxes(title_text=None)
    st.plotly_chart(fig_nota_unidade, use_container_width=True)

# Segundo container com o segundo gráfico
with container2:
    categoria_total = df_filtered.groupby(['Categoria'])[['Nota']].mean().reset_index()
    fig_nota_categoria = px.bar(categoria_total, y="Nota", x="Categoria", title="Categoria", height=500)
    fig_nota_categoria.update_traces(marker_color=color_bars(categoria_total['Nota']), texttemplate='%{y:.2f}', textposition='outside') 
    fig_nota_categoria.update_layout(title_x=0.5, plot_bgcolor='#f0f0f0', paper_bgcolor='#f0f0f0')
    fig_nota_categoria.update_yaxes(title_text=None)
    st.plotly_chart(fig_nota_categoria, use_container_width=True)

# Terceiro container com o terceiro gráfico
with container3:
    integrante_total = df_filtered.groupby(['Integrante'])[['Nota']].mean().reset_index()
    fig_nota_integrante = px.bar(integrante_total, y="Nota", x="Integrante", title="Integrante", height=500)
    fig_nota_integrante.update_traces(marker_color=color_bars(integrante_total['Nota']), texttemplate='%{y:.2f}', textposition='outside') 
    fig_nota_integrante.update_layout(title_x=0.5, plot_bgcolor='#f0f0f0', paper_bgcolor='#f0f0f0')
    fig_nota_integrante.update_yaxes(title_text=None)
    st.plotly_chart(fig_nota_integrante, use_container_width=True)