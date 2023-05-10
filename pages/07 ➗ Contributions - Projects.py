import streamlit as st
import pandas as pd
import numpy as np
from pytimeparse.timeparse import timeparse
import distinctipy
from colour import Color

st.set_page_config(layout="wide", page_title="Package Man-Hour")

hide_streamlit_logo = """
            <style>
            footer {visibility: hidden;}
            </style>
            """

st.markdown(hide_streamlit_logo, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>Contributions - Projects</h1><br>", unsafe_allow_html=True)

def set_ss():

    st.session_state["ss_month_range"] = st.session_state["ms_month_range"]
    st.session_state["ss_act_range"] = st.session_state["ms_act_range"]

# loads dataframe from session state
if "dataframe" in st.session_state:
    df = st.session_state["dataframe"]

    months = list(sorted(df["date"].unique(), reverse=True))
    acts = ["DSH", "ITC", "MRQ", "TCL", "TBE", "POR", "VDR", "MTG", "CRD", "MSN", "OFF", "CRW", "OTH"]
    prj_ids = list(sorted(df["cost_center_id"].unique()))
    pers_list = list(sorted(df["pers_name"].unique()))
    dc = distinctipy.get_colors(len(pers_list))
    hex_code = [distinctipy.get_hex(c) for c in dc]

    if "ss_month_range" not in st.session_state:
        st.session_state["ss_month_range"] = []

    if "ss_act_range" not in st.session_state:
        st.session_state["ss_act_range"] = []

    
    with st.sidebar:
        with st.form("Exclude"):

            st.multiselect("Months", months, default=st.session_state["ss_month_range"], key="ms_month_range")
            st.multiselect("Activities", acts, default=st.session_state["ss_act_range"], key="ms_act_range")

            filtered = st.form_submit_button("Exclude", on_click=set_ss)

    width, height = 3, len(prj_ids) // 3 + 1

    v1, b1, v2, b2, v3 = st.columns([7, 1, 7, 1, 7])
    for i, v in enumerate([v1, v2, v3]):
        with v:
            try:
                for n in range(height):

                    st.vega_lite_chart(df[df["cost_center_id"].isin([prj_ids[width * n + i]]) &
                     ~df["date"].isin(st.session_state["ss_month_range"]) & 
                     ~df["activity_type"].isin(st.session_state["ss_act_range"])].groupby(["cost_center", "pers_name"]).sum().reset_index(), {
                        "transform": [{"joinaggregate": [{"op": "sum", "field": "total", "as": "sumoftotal"}]},
                                    {"calculate": "datum.total/datum.sumoftotal * 100", "as": "percent"}],
                        "width": "container",
                        "height": 350,
                        "title": {"text": prj_ids[width * n + i], "offset": 20, "fontSize": "14", "anchor": "start"},
                        "mark": {"type": "bar", "stroke": "#fff",
                                "tooltip": {"signal": "{'Percent (%)': round(datum.percent), 'Employee': datum.pers_name, 'Project': datum.cost_center}"}},
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