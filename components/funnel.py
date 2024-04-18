import streamlit as st
import plotly.graph_objects as go
import plotly.express as px


def funnel_chart(df, x, y, title, color_graph):

    fig = px.funnel(df,
                    y=x,
                    x=y,
                    title=title,
                    labels={'xaxis':['Disparos', 'Recebidos', 'Abertos', 'Clicados']})

    fig.update_xaxes(visible=False, fixedrange=True)
    fig.update_yaxes(visible=True, fixedrange=True)
    fig.update_layout(
        # paper_bgcolor="lightgrey",
        showlegend=False,
        plot_bgcolor="white",
        height=500,
    )

    st.plotly_chart(fig, use_container_width=True)