# importando as bilbiotecas do projeto  
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import streamlit as st
   
   
# lendo o arquivo xlsx da fonte http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_06
exportacao_vinho = pd.read_excel('https://raw.githubusercontent.com/lucianesantos/Tech_Challenge_Fase_1/main/ExpVinhoFull.xlsx')
exportacao_vinho.head(5)

#título
st.title("Tech Challenge 1 - Vinícola Brasil")
st.subheader('By Luciane dos Santos Reis')

#layout
tab0, tab1 = st.tabs(['   ', ' '])


with tab0:
    st.write('')


#Iniciando as manipulações no arquivo
#Definindo a coluna País como Indice do dataframe, para que ela não desapareça na manipulação das colunas que vou fazer
exportacao_vinho= exportacao_vinho.set_index("País")
#Filtro dos ultimos 15 anos pelo código do índice - O escopo do trabalho são os últimos 15 anos
exportacao_vinho_15 = exportacao_vinho.iloc[-124:,-30:]
#Renomeando as colunas para ter uma descrição mais amigável de valores em dólares e quantidade em litros juntos.
exportacao_vinho_15.columns=[
'2008_qtd','2008_valor',
'2009_qtd','2009_valor',
'2010_qtd','2010_valor',
'2011_qtd','2011_valor',
'2012_qtd','2012_valor',
'2013_qtd','2013_valor',
'2014_qtd','2014_valor',
'2015_qtd','2015_valor',
'2016_qtd','2016_valor',
'2017_qtd','2017_valor',
'2018_qtd','2018_valor',
'2019_qtd','2019_valor',
'2020_qtd','2020_valor',
'2021_qtd','2021_valor',
'2022_qtd','2022_valor']

#Dataframe valor em dolares
#Separando valor em dólares da quantidade em litros exportada para utilizar nos gráficos - Para manter os valores, apaguei a quantidade.
exportacao_vinho_valores = exportacao_vinho_15.drop(columns=['2008_qtd','2009_qtd','2010_qtd','2011_qtd','2012_qtd','2013_qtd','2014_qtd','2015_qtd','2016_qtd','2017_qtd','2018_qtd','2019_qtd','2020_qtd','2021_qtd','2022_qtd'])
exportacao_vinho_valores.head(5)
#Mantive apenas os anos para agrupar por ano no futuro
exportacao_vinho_valores.columns=['2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018','2019','2020','2021','2022']

#Dataframe quantidade em litros
#Separando valor em dólares de quantidade em litros exportada para utilizar nos gráficos - Para manter as quantidades em litros apaguei o valor em dólares
exportacao_vinho_qtd = exportacao_vinho_15.drop(columns=['2008_valor','2009_valor','2010_valor','2011_valor','2012_valor','2013_valor','2014_valor','2015_valor','2016_valor','2017_valor','2018_valor','2019_valor','2020_valor','2021_valor','2022_valor'])
exportacao_vinho_qtd.head(5)
#Novamente, mantive apenas os anos para agrupar por ano no futuro
exportacao_vinho_qtd.columns=['2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018','2019','2020','2021','2022']

##Valores em dólares - melt
#Com o comando melt, vou transformar essas diversas colunas em apenas 3 - PRIMEIRO PARA VALORES
exportacao_vinho_valores = exportacao_vinho_valores.reset_index().melt(id_vars=['País'], value_vars=exportacao_vinho_valores.columns)

#Renomeando as colunas alteradas pelo comando melt
exportacao_vinho_valores.columns=['pais','ano','valor']
exportacao_vinho_valores['ano'] = pd.to_numeric(exportacao_vinho_valores['ano'])

##quantidade em litros - melt
#tratando os dados com o melt para ter apens 3 colunas
exportacao_vinho_qtd = exportacao_vinho_qtd.reset_index().melt(id_vars=['País'], value_vars=exportacao_vinho_qtd.columns)
#definindo as colunas
exportacao_vinho_qtd.columns = ['pais', 'ano', 'valor']



with tab0:
    st.markdown('<h1 style="text-align: center;">Análise econômica</h1>', unsafe_allow_html=True)

    #graficos
    #Evolução da Exportação em dólares ano a ano sem países- Grafico
exportacao_vinho_valores_ano_a_ano = exportacao_vinho_valores.groupby('ano')['valor'].sum()
exportacao_vinho_valores_ano_a_ano = exportacao_vinho_valores_ano_a_ano.reset_index()
#st.line_chart(data=exportacao_vinho_valores_ano_a_ano, x='ano', y='valor', marker='o', ax=axis)

st.markdown("---")
st.markdown('<p style="text-align: center;font-size:23px;"> De 2008 à 2015, nota-se grandes oscilações nas exportações, com momentos de forte crescimento e quedas, entretanto, a partir de 2015, é percebido uma tendência mais consistente, com menos oscilações e crescimento (738% de crescimento de 2021 vs 2015)​.Esse crescimento pode ser observado e correlacionado ao aumento do número de países que passaram a importar nosso vinho a partir de 2015, como pode ser visto no gráfico 2.</p>', unsafe_allow_html=True)
st.markdown("---")
fig, axis = plt.subplots(figsize=(15, 6))
cores = ['firebrick','maroon', 'brown','indianred','#8B0000','#800000','#DC143C', '#5C4033','#8C001A']
grafico_vl = exportacao_vinho_valores_ano_a_ano.plot( grid='gray',y='valor', x='ano', marker='o', kind='line', color=cores, title='Exportação em dólares Ano a Ano', fontsize=16)
fig1 = grafico_vl.get_figure()
fig1.set_size_inches(12, 6)  # Ajuste os valores conforme necessário
grafico_vl.set_title('Exportação em dólares Ano a Ano\n', fontsize=20)
plt.xticks(rotation=45)
plt.xlabel('')
st.pyplot(fig1)



#grafico4
#Quantidade de países Exportados por ano
#agrupando por ano e somando os valores por ano
exportacao_vinho_qtd.groupby('ano')['valor'].sum()
#filtrando apenas paises que tiveram exportação
filtro = exportacao_vinho_qtd[exportacao_vinho_qtd['valor'] > 0]
#contando os paises por ano
contagem_paises = filtro.groupby('ano')['pais'].count()
contagem_paises = contagem_paises.reset_index()

#ax = sns.barplot(data=contagem_paises, x='ano', y='pais', palette=cores)

st.markdown("---")
st.markdown('<p style="text-align: center;font-size:23px;"> A quantidade de países que realizamos exportações aumentou significativamente de 41 países em 2008 para 75 países em 2022 (195%), sendo que o crescimento desde 2015 é de 247%.</p>', unsafe_allow_html=True)
st.markdown("---")
cores = ['firebrick','maroon', 'brown','indianred','#8B0000','#800000','#DC143C', '#5C4033','#8C001A']
grafico_v4 = contagem_paises.plot(y='pais', x='ano', kind='bar', color=cores, title='Quantidade de Países Exportados por Ano', fontsize=16)
fig4 = grafico_v4.get_figure()
fig4.set_size_inches(12, 6)  
grafico_v4.set_title('Quantidade de Países Exportados por Ano\n', fontsize=20)
plt.xticks(rotation=45)
plt.xlabel('')
plt.ylim(0,90)
st.pyplot(fig4)






#Media de litros exportados - quantidade em litros 
filtro_total_litros = exportacao_vinho_qtd
filtro_total_litros = exportacao_vinho_qtd.groupby('ano')['valor'].sum()
filtro_total_litros = filtro_total_litros.reset_index()
#Dividindo litro por quantidadde de paises
media_litros=filtro_total_litros
media_litros['valor'] = filtro_total_litros['valor'].div(contagem_paises['pais'])
#ax = sns.barplot(data=media_litros, x='ano', y='valor', palette=cores)


st.markdown("---")
st.markdown('<p style="text-align: center;font-size:23px;">Após fortes oscilações até 2014, a partir de 2015 a quantidade média  de litros exportado por país mantém uma tendência de crescimento (272% de 2021 vs 2015).</p>', unsafe_allow_html=True)
st.markdown("---")

cores = ['firebrick','maroon', 'brown','indianred','#8B0000','#800000','#DC143C', '#5C4033','#8C001A']
grafico_v5 = media_litros.plot(y='valor', x='ano', kind='bar', color=cores, title='Media - Litros por países', fontsize=16)
fig5 = grafico_v5.get_figure()
fig5.set_size_inches(12, 6)  
plt.xticks(rotation=45)
grafico_v5.set_title('Media - Litros por países\n', fontsize=20)
plt.xlabel('')
plt.ylim(0,800000)
st.pyplot(fig5)


#Media litros por valor
soma_valores_exportacao_ano = exportacao_vinho_valores.groupby('ano')['valor'].sum()
soma_valores_exportacao_ano = soma_valores_exportacao_ano.reset_index()
soma_quantidade_exportacao = exportacao_vinho_qtd.groupby('ano')['valor'].sum()
soma_quantidade_exportacao = soma_quantidade_exportacao.reset_index()
media_litros_por_valor = soma_valores_exportacao_ano
media_litros_por_valor['valor'] = soma_valores_exportacao_ano['valor'].div(soma_quantidade_exportacao['valor'])
media_litros_por_valor = media_litros_por_valor.reset_index()
media_litros_por_valor['ano'] = pd.to_numeric(media_litros_por_valor['ano'])

#sns.barplot(media_litros_por_valor, x ='ano' , y='valor', palette=cores)


st.markdown("---")
st.markdown('<p style="text-align: center;font-size:23px;">O crescimento do valor médio por litro acompanha o crescimento da taxa de câmbio de 2,60 em 2015 para 5,58 em 2021, que fez com que o valor unitário em dólares reduzisse de US$2.3 para US$1.2 no mesmo período.</p>', unsafe_allow_html=True)
st.markdown("---")

cores = ['firebrick','maroon', 'brown','indianred','#8B0000','#800000','#DC143C', '#5C4033','#8C001A']
grafico_v6 = media_litros_por_valor.plot(y='valor', x='ano', kind='bar', color=cores, title='Media - Litros por Valor Exportado', fontsize=16)
fig6 = grafico_v6.get_figure()
fig6.set_size_inches(12, 6)  
grafico_v6.set_title('Media - Litros por Valor Exportado\n', fontsize=20)
plt.xticks(rotation=45)
plt.xlabel('')
plt.ylim(0.0,3.5)
st.pyplot(fig6)



#grafico 2
# TOP 10 PAÍSES EXPORTAÇÃO em dólares
##Agrupando por País e somando o valor - grafico

top_10_maior_valor_pais  = exportacao_vinho_valores.groupby('pais')['valor'].sum()  #substitui exportacao_vinho_maior_valor por exportacao_vinho_valores
top_10_maior_valor_pais  = top_10_maior_valor_pais.reset_index()
top_10_maior_valor_pais = top_10_maior_valor_pais.sort_values(by=['valor'], ascending= False)
top_10_maior_valor_pais = top_10_maior_valor_pais.head(10)
top_10_maior_valor_pais = top_10_maior_valor_pais.reset_index()
#axis = sns.catplot(data=top_10_maior_valor_pais,  x='pais', y='valor', kind='bar', errorbar=None, zorder=2, aspect=1.8)
st.markdown("---")
st.markdown('<p style="text-align: center;font-size:23px;">TOP 10 Países com maior exportação em litros de Vinho de Mesa representam 87% dos litros de Vinho exportados.</p>', unsafe_allow_html=True)
st.markdown("---")

cores = ['firebrick','maroon', 'brown','indianred','#8B0000','#800000','#DC143C', '#5C4033','#8C001A']
grafico_v2 = top_10_maior_valor_pais.plot(y='valor', x='pais', kind='bar', color=cores, title='Top 10 Países - Exportação de Vinho em Dólares', fontsize=16)
fig2 = grafico_v2.get_figure()
grafico_v2.set_title('Top 10 Países - Exportação de Vinho em Dólares\n', fontsize=20)
fig2.set_size_inches(12, 6)  
plt.xticks(rotation=45)
plt.xlabel('')
st.pyplot(fig2)


#Top 10 paises - exportaçaõ em litros
dados_exportacao_qtd_soma  = exportacao_vinho_qtd.groupby('pais')['valor'].sum() # aqui eu sumarizei em todos os anos para saber qual é o pais com a maior quantidade de exportação
dados_exportacao_qtd_soma  = dados_exportacao_qtd_soma.reset_index()
dados_exportacao_qtd_soma.rename(columns={exportacao_vinho_qtd.columns[-1] : 'Total'}, inplace=True)
dados_exportacao_qtd_total = dados_exportacao_qtd_soma.sort_values(by='Total', ascending=False)
#axis = sns.catplot(data=dados_exportacao_qtd_total.head(10),  x='pais', y='Total', kind='bar', errorbar=None, zorder=2, aspect=1.8) # aqui eu plotei os valores sumarizados

st.markdown("---")
st.markdown('<p style="text-align: center;font-size:23px;">TOP 10 Países com maior Exportação em dólares de Vinho de Mesa representam 94% do valor das exportações (US$).</p>', unsafe_allow_html=True)
st.markdown("---")


cores = ['firebrick','maroon', 'brown','indianred','#8B0000','#800000','#DC143C', '#5C4033','#8C001A']

grafico_v3 = dados_exportacao_qtd_total.head(10).plot(y='Total', x='pais', kind='bar', color=cores, title='Top 10 Países com Exportação de Vinho em Litros',fontsize=16)
fig3 = grafico_v3.get_figure()
fig3.set_size_inches(12, 6)  

grafico_v3.set_title('Top 10 Países com Exportação de Vinho em Litros\n', fontsize=20)
plt.xticks(rotation=45)
plt.xlabel('')

st.pyplot(fig3)


st.markdown("---")
st.markdown('<p style="text-align: center;font-size:26px;"><strong>Conclusão</strong></p>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center;font-size:23px;">Pensando que vinhos Brasileiros são vendidos para apenas 74 países, há a oportunidade de buscar vender vinho para mais países. ​"</p>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center;font-size:23px;">Ao mesmo tempo, a média de litro por países também tem aumentado, sendo que a manutenção dessa tendência também é uma oportunidade para aumentar as exportações em quantidade e litros.</p>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center;font-size:23px;">Se o câmbio se mantiver estável, esse aumento na quantidade vendida também vai impactar no resultado financeiro em dólares.</p>', unsafe_allow_html=True)


st.markdown("---")

