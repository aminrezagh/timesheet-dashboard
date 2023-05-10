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

st.markdown("<h1 style='text-align: center;'>Project Activities</h1><br>", unsafe_allow_html=True)

def set_ss():

    st.session_state["ss_month_range"] = st.session_state["ms_month_range"]


# loads dataframe from session state
if "dataframe" in st.session_state:
    df = st.session_state["dataframe"]

    months = list(sorted(df["date"].unique(), reverse=True))
    acts = ["DSH", "ITC", "MRQ", "TCL", "TBE", "POR", "VDR", "MTG", "CRD", "MSN", "OFF", "CRW", "OTH"]
    act_hex = ["#ff3a15", "#d42200", "#951700", "#4e8ef1", "#115fd8", "#0b3d8a", "#29AB87", "#FFA52C", "#FF69B4", "#ffff1a", "#FFFFCC", "#A689E1", "#D3D3D3"]
    prjs = list(sorted(df["cost_center"].unique()))
    prj_ids = list(sorted(df["cost_center_id"].unique()))

    dom = acts # Color domain
    rng = act_hex # Color range

    if "ss_month_range" not in st.session_state:
        st.session_state["ss_month_range"] = []

    
    with st.sidebar:
        with st.form("Exclude"):

            st.multiselect("Months", months, default=st.session_state["ss_month_range"], key="ms_month_range")

            filtered = st.form_submit_button("Exclude", on_click=set_ss)

    width, height = 3, len(prjs) // 3 + 1

    v1, b1, v2, b2, v3 = st.columns([7, 1, 7, 1, 7])
    for i, v in enumerate([v1, v2, v3]):
        with v:
            try:
                for n in range(height):

                    st.vega_lite_chart(df[~df["date"].isin(st.session_state["ss_month_range"])].groupby(["cost_center_id", 
                     "cost_center", "activity_type"]).agg(percent=("total", "sum")).groupby(level=0).apply(
                     lambda x: 100 * x / float(x.sum())).reset_index().query('cost_center_id == @prj_ids[@width * @n + @i]'), {
                        "width": "container",
                        "height": 350,
                        "title": {"text": prj_ids[width * n + i], "offset": 20, "fontSize": "16", "anchor": "middle"},
                        "mark": {"type": "bar", "stroke": "#fff",
                                "tooltip": {"signal": "{'Percent (%)': round(datum.percent), 'Project': datum.cost_center}"}},
                        "encoding": {
                            "x": {"field": "activity_type", "type": "nominal", "sort": "-y", "axis": {"title": "", "grid": "true"}},
                            "y": {"field": "percent", "type": "quantitative", "axis": {"title": "%"}},
                            "color": {"value": "#318CE7"}
                     }
                     }, use_container_width=True)
                    
            except IndexError:
                pass


else:
    st.error("Please upload the database", icon="❌")