import streamlit as st
import streamlit_card as sc
from model.brognoli_funnel import BrognoliFunnel
import pandas as pd
from components.metric import plot_metric
from components.funnel import funnel_chart
from components.bar import bar_chart

st.set_page_config(layout="wide")

bf = BrognoliFunnel()
bf.import_funnel()

st.title('Ações Tradicionais')
st.markdown('Resultados de disparos realizados por ações comuns')

# st.dataframe(bf.funnel)

top_left_column, top_right_column = st.columns((2, 1))
bottom_left_column, bottom_right_column = st.columns(2)

with top_left_column:
    column1, column2, column3, column4 = st.columns(4)

    with column1:
        plot_metric('Total de Envios', bf.sent_funnel.disparos.sum(),
                    show_graph=True, color_graph='rgba(255, 0, 0, 0.1)',
                    df=bf.sent_funnel,
                    x='data',
                    y='disparos')
    with column2:
        plot_metric('Total de Emails entregues', bf.delivered_funnel.disparos.sum(),
                    show_graph=True, color_graph='rgba(0, 255, 0, 0.3)',
                    df=bf.delivered_funnel,
                    x='data',
                    y='disparos')

    with column3:
        plot_metric('Total de Emails clicados', bf.opened_funnel.disparos.sum(),
                    show_graph=True, color_graph='rgba(0, 0, 255, 0.3)',
                    df=bf.opened_funnel,
                    x='data',
                    y='disparos')

    with column4:
        plot_metric('Total de Emails abertos', bf.clicked_funnel.disparos.sum(),
                    show_graph=True, color_graph='rgba(0, 122, 255, 0.3)',
                    df=bf.clicked_funnel,
                    x='data',
                    y='disparos')

with bottom_left_column:
    funnel_chart(bf.funnel, 'step', 'event', 'Funil de Interações', ['lightcoral'])

with bottom_right_column:
    bar_chart(bf.period, 'periodo', 'clicked', title='Período da interação')