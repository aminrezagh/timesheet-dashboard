from cgitb import grey
import streamlit as st
import pandas as pd
import numpy as np
from pytimeparse.timeparse import timeparse
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(layout="wide", page_title="Package Man-Hour")

hide_streamlit_logo = """
            <style>
            footer {visibility: hidden;}
            </style>
            """

st.markdown(hide_streamlit_logo, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>Availability</h1><br>", unsafe_allow_html=True)

#loads dataframe from session state
if "dataframe" in st.session_state:
    df = st.session_state["dataframe"]

    # group columns on name and date 
    gr = df.groupby(["pers_name", "date"]).sum().reset_index()
    gr["max_basic"] = gr["date"].map({r[0]: r[1] for r in 
    df.groupby(["date", "pers_name"]).sum().reset_index().groupby("date").agg({"total_basic": "max"}).reset_index().to_dict("split")["data"]})
    gr["availability"] = gr["net_working"] / gr["max_basic"] * 100
    gr["over_time_pcnt"] = gr["over_time"] / gr["max_basic"] * 100
    sec_av = gr.groupby("date").mean().reset_index()
    gr["sec_av"] = gr["date"].map({r[0]: r[1] for r in sec_av[["date", "availability"]].to_dict("split")["data"]})

    month_range = sorted(df["date"].unique(), reverse=True)

    def set_ss():
        st.session_state["ss_month_range"] = st.session_state["ms_month_range"]

    if "ss_month_range" not in st.session_state:
        st.session_state["ss_month_range"] = []

    with st.sidebar:
        with st.form("Exclude"):

            st.multiselect("Months", month_range, default=st.session_state["ss_month_range"], key="ms_month_range")

            filtered = st.form_submit_button("Exclude", on_click=set_ss)

    pers_list = sorted(list(set(gr["pers_name"].to_list())))
    width, height = 2, len(pers_list) // 2 + 1
    
    v1, b1, v2= st.columns([5, 1, 5])
    for i, v in enumerate([v1, v2]):
        with v:
            try:
                for n in range(height):

                    avg_all = gr[gr["pers_name"].isin([pers_list[width * n + i]]) & gr["date"].isin(
                        set(month_range).difference(set(st.session_state["ss_month_range"])))]["availability"].mean()
                    over_avg_all = gr[gr["pers_name"].isin([pers_list[width * n + i]]) & gr["date"].isin(
                        set(month_range).difference(set(st.session_state["ss_month_range"])))]["over_time"].mean()

                    st.vega_lite_chart(gr[gr["pers_name"].isin([pers_list[width * n + i]]) & ~gr["date"].isin(st.session_state["ss_month_range"])], {
                        "transform": [{"fold": ["availability", "sec_av", "over_time_pcnt"]}],
                        "width": "container",
                        "height": 400,
                        "title": {"text": pers_list[width * n + i], "offset": 15, "fontSize": "15"},
                        "mark": {"type": "line",
                                "tooltip": {"signal": "{'Availability (%)': round(datum.value), 'Month': datum.date}"}},
                        "encoding": {
                            "x": {"field": "date", "type": "nominal", "axis": {"title": "Month", "grid": "true"}},
                            "y": {"field": "value", "type": "quantitative", "axis": {"title": "Availability (%)"}},
                            "color": {"field": "key", "type": "nominal"}}
                        }, use_container_width=True)

                    try:
                        st.markdown("<b>STATISTICS:</b><br>" + 
                                    "<br>".join([f"AVG = <b>{int(avg_all)} %</b>",
                                                f"AVG (OVERTIME)= <b>{int(over_avg_all)} h</b>"]), unsafe_allow_html=True)
                    except ValueError:
                        pass

            except IndexError:
                pass

else:
    st.error("Please upload the database", icon="❌")