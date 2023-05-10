import streamlit as st
import pandas as pd
import numpy as np
from pytimeparse.timeparse import timeparse

st.set_page_config(layout="wide", page_title="Package Man-Hour")

hide_streamlit_logo = """
            <style>
            footer {visibility: hidden;}
            </style>
            """

st.markdown(hide_streamlit_logo, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>Contributions - Activities</h1><br>", unsafe_allow_html=True)

def set_ss():

    st.session_state["ss_month_range"] = st.session_state["ms_month_range"]
    st.session_state["ss_prj_range"] = st.session_state["ms_prj_range"]

# loads dataframe from session state
if "dataframe" in st.session_state:
    df = st.session_state["dataframe"]

    months = list(sorted(df["date"].unique(), reverse=True))
    acts = ["DSH", "ITC", "MRQ", "TCL", "TBE", "POR", "VDR", "MTG", "CRD", "MSN", "OFF", "CRW", "OTH"]
    act_hex = ["#ff3a15", "#d42200", "#951700", "#4e8ef1", "#115fd8", "#0b3d8a", "#29AB87", "#FFA52C", "#FF69B4", "#ffff1a", "#FFFFCC", "#A689E1", "#D3D3D3"]
    prjs = list(sorted(df["cost_center"].unique()))

    dom = acts
    rng = act_hex

    if "ss_month_range" not in st.session_state:
        st.session_state["ss_month_range"] = []

    if "ss_prj_range" not in st.session_state:
        st.session_state["ss_prj_range"] = []

    
    with st.sidebar:
        with st.form("Exclude"):

            st.multiselect("Months", months, default=st.session_state["ss_month_range"], key="ms_month_range")
            st.multiselect("Projects", prjs, default=st.session_state["ss_prj_range"], key="ms_prj_range")

            filtered = st.form_submit_button("Exclude", on_click=set_ss)

    width, height = 3, len(acts) // 3 + 1

    v1, b1, v2, b2, v3 = st.columns([7, 1, 7, 1, 7])
    for i, v in enumerate([v1, v2, v3]):
        with v:
            try:
                for n in range(height):

                    st.vega_lite_chart(df[df["activity_type"].isin([acts[width * n + i]]) &
                     ~df["date"].isin(st.session_state["ss_month_range"]) & 
                     ~df["cost_center"].isin(st.session_state["ss_prj_range"])].groupby("pers_name").sum().reset_index(), {
                        "transform": [{"joinaggregate": [{"op": "sum", "field": "total", "as": "sumoftotal"}]},
                                    {"calculate": "datum.total/datum.sumoftotal * 100", "as": "percent"}],
                        "width": "container",
                        "height": 350,
                        "title": {"text": acts[width * n + i], "offset": 20, "fontSize": "16", "anchor": "middle"},
                        "mark": {"type": "bar", "stroke": "#fff",
                                "tooltip": {"signal": "{'Percent (%)': round(datum.percent), 'Employee': datum.pers_name}"}},
                        "encoding": {
                            "x": {"field": "pers_name", "type": "nominal", "sort": "-y", "axis": {"title": "", "grid": "true"}},
                            "y": {"field": "percent", "type": "quantitative", "axis": {"title": "%"}},
                            "color": {"value": "#00A693"}
                     }
                     }, use_container_width=True)
                    
            except IndexError:
                pass


else:
    st.error("Please upload the database", icon="❌")