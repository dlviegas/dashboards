import streamlit as st
import plotly.graph_objects as go
import plotly.express as px


def bar_chart(df, x, y, title):
    fig = go.Figure()

    fig.add_trace(go.Bar(
                    y=df[y],
                    x=df[x],
                    marker=dict(color='rgb(0, 255, 125, 0.5)'),
                ))

    fig.update_xaxes(visible=True, fixedrange=True)
    fig.update_yaxes(visible=False, fixedrange=True)
    fig.update_layout(
        # paper_bgcolor="lightgrey",
        showlegend=False,
        plot_bgcolor="white",
        height=500,
        title=go.layout.Title(text=title)
    )

    st.plotly_chart(fig, use_container_width=True)