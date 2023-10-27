import streamlit as st
import pandas as pd
import numpy as np
from pytimeparse.timeparse import timeparse
import distinctipy

st.set_page_config(layout="centered", page_title="Package Man-Hour")

hide_streamlit_logo = """
            <style>
            footer {visibility: hidden;}
            </style>
            """

st.markdown(hide_streamlit_logo, unsafe_allow_html=True)

# defines default columns names for database
DEFAULT_NAMES = [
    "Cost Center's Name",
    "Cost Center's Code",
    "Last Name",
    "First Name",
    "Prs Code",
    "Activity's Name",
    "Activity's Code",
    "Discipline",
    "Discipline Code",
    "Date",
    "Basic",
    "Over Time",
    "Mission",
    "Homework",
]

NEW_NAMES = [
    "cost_center",
    "cost_center_id",
    "last_name",
    "first_name",
    "pers_id",
    "activity_name",
    "activity_id",
    "discipline",
    "discipline_code",
    "date",
    "basic",
    "over_time",
    "mission",
    "homework",
]

# extracts package section personnel ids from a text file
PCKG_PERS_ID = [
    str(i) for i in sum(pd.read_csv("package_personnel_ids.txt").values.tolist(), [])
]

TIME_COLS = ["basic", "over_time", "mission", "homework"]

ACTIVITY_TYPES = {
    "EVD": "VDR",
    "clarification": "TCL",
    "data sheet": "DSH",
    "datasheet": "DSH",
    "requisition": "MRQ",
    "TBE": "TBE",
    "service": "ITC",
    "POR": "POR",
    "coordination": "CRD",
    "meeting": "MTG",
    "mission": "MSN",
    "contract": "CRW",
    "off": "OFF",
}


def clean_and_categorize(df: pd.DataFrame):
    # renames the columns
    df.rename(columns=dict(zip(DEFAULT_NAMES, NEW_NAMES)), inplace=True)
    df = df[df["pers_id"].isin(PCKG_PERS_ID)]
    df.drop("pers_id", axis=1, inplace=True)

    # converts time-format to number of hours
    df[TIME_COLS] = df[TIME_COLS].applymap(
        lambda t: timeparse(t, granularity="minutes") / 3600
    )
    df.drop(["discipline", "discipline_code"], axis=1, inplace=True)

    # adds thursday column to dataframe
    add_thursday_column(df)
    add_off_time_column(df)

    df["pers_name"] = (
        df["last_name"].str.split().str.get(0).str.title()
        + ", "
        + df["first_name"].str.title()
    )
    df.drop(["first_name", "last_name"], axis=1, inplace=True)

    # defines categories for different types of activies
    categorize_activity(df)

    df["month"] = df["date"].astype(str).str[4:6]
    df["year"] = df["date"].astype(str).str[0:4]
    df.drop("date", axis=1, inplace=True)
    df["date"] = df["year"] + " - " + df["month"]
    df["total_basic"] = df["basic"] + df["mission"]
    df["total"] = df["total_basic"] + df["over_time"]
    df["net_working"] = df["total_basic"] - df["off_time"] + df["over_time"]

    return df


def add_thursday_column(df):
    df.loc[df["basic"] == 0, "thursday"] = df["over_time"]
    df["thursday"].fillna(0, inplace=True)


def add_off_time_column(df):
    df.loc[df["cost_center_id"] == "OFF", "off_time"] = df["basic"]
    df["off_time"].fillna(0, inplace=True)


def categorize_activity(df):
    for activity, activity_type in ACTIVITY_TYPES.items():
        df.loc[
            df["activity_name"].str.contains(activity, case=False), "activity_type"
        ] = activity_type
    df["activity_type"].fillna("OTH", inplace=True)


def set_ss():
    st.session_state["ss_month_range"] = st.session_state["ms_month_range"]
    st.session_state["ss_act_range"] = st.session_state["ms_act_range"]
    st.session_state["ss_prj_range"] = st.session_state["ms_prj_range"]


if "ss_month_range" not in st.session_state:
    st.session_state["ss_month_range"] = []

if "ss_act_range" not in st.session_state:
    st.session_state["ss_act_range"] = []

if "ss_prj_range" not in st.session_state:
    st.session_state["ss_prj_range"] = []

if "dataframe" in st.session_state:
    df = st.session_state["dataframe"]

else:
    df = pd.read_csv("./db/demo_db.csv", dtype=str)
    df = clean_and_categorize(df)
    st.session_state["dataframe"] = df

try:
    months = list(sorted(df["date"].unique(), reverse=True))
    prjs = list(sorted(df["cost_center"].unique()))
    prj_ids = list(sorted(df["cost_center_id"].unique()))
    acts = [
        "DSH",
        "ITC",
        "MRQ",
        "TCL",
        "TBE",
        "POR",
        "VDR",
        "MTG",
        "CRD",
        "MSN",
        "OFF",
        "CRW",
        "OTH",
    ]
    act_hex = [
        "#ff3a15",
        "#d42200",
        "#951700",
        "#4e8ef1",
        "#115fd8",
        "#0b3d8a",
        "#29AB87",
        "#FFA52C",
        "#FF69B4",
        "#ffff1a",
        "#FFFFCC",
        "#A689E1",
        "#D3D3D3",
    ]

    dc = distinctipy.get_colors(len(prj_ids))
    hex_code = [distinctipy.get_hex(c) for c in dc]

    with st.sidebar:
        with st.form("Filter"):
            st.multiselect(
                "Months",
                months,
                default=st.session_state["ss_month_range"],
                key="ms_month_range",
            )
            st.multiselect(
                "Activities",
                acts,
                default=st.session_state["ss_act_range"],
                key="ms_act_range",
            )
            st.multiselect(
                "Projects",
                prjs,
                default=st.session_state["ss_prj_range"],
                key="ms_prj_range",
            )

            filtered = st.form_submit_button("Exclude", on_click=set_ss)

    st.vega_lite_chart(
        df[
            ~df["date"].isin(st.session_state["ss_month_range"])
            & ~df["cost_center"].isin(st.session_state["ss_prj_range"])
            & ~df["activity_type"].isin(st.session_state["ss_act_range"])
        ]
        .groupby(["activity_type"])
        .sum()
        .reset_index(),
        {
            "transform": [
                {
                    "joinaggregate": [
                        {"op": "sum", "field": "total", "as": "sumoftotal"}
                    ]
                },
                {"calculate": "datum.total/datum.sumoftotal * 100", "as": "percent"},
            ],
            "width": "container",
            "height": 400,
            "title": {
                "text": "OVERALL BREAKDOWN - ACTIVITIES",
                "offset": 30,
                "fontSize": "16",
                "anchor": "middle",
            },
            "mark": {
                "type": "arc",
                "innerRadius": 75,
                "stroke": "#fff",
                "tooltip": {
                    "signal": "{'Percent (%)': round(datum.percent), 'Activity': datum.activity_type}"
                },
            },
            "encoding": {
                "theta": {"field": "percent", "type": "quantitative"},
                "color": {
                    "field": "activity_type",
                    "type": "quantitative",
                    "type": "nominal",
                    "scale": {"domain": acts, "range": act_hex},
                },
            },
            "config": {
                "legend": {"orient": "right", "layout": {"right": {"anchor": "middle"}}}
            },
        },
        use_container_width=True,
    )

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.vega_lite_chart(
        df[
            ~df["date"].isin(st.session_state["ss_month_range"])
            & ~df["cost_center"].isin(st.session_state["ss_prj_range"])
            & ~df["activity_type"].isin(st.session_state["ss_act_range"])
        ]
        .groupby(["cost_center_id", "cost_center"])
        .sum()
        .reset_index(),
        {
            "transform": [
                {
                    "joinaggregate": [
                        {"op": "sum", "field": "total", "as": "sumoftotal"}
                    ]
                },
                {"calculate": "datum.total/datum.sumoftotal * 100", "as": "percent"},
            ],
            "width": "container",
            "height": 500,
            "title": {
                "text": "OVERALL BREAKDOWN - PROJECTS",
                "offset": 20,
                "fontSize": "16",
                "anchor": "middle",
            },
            "mark": {
                "type": "bar",
                "stroke": "#fff",
                "tooltip": {
                    "signal": "{'Percent (%)': round(datum.percent), 'Cost Center': datum.cost_center, 'Cost Center ID': datum.cost_center_id}"
                },
            },
            "encoding": {
                "x": {"field": "cost_center_id", "type": "nominal"},
                "y": {"field": "percent", "type": "quantitative"},
                "color": {
                    "field": "cost_center_id",
                    "type": "nominal",
                    "scale": {"domain": prj_ids, "range": hex_code},
                },
            },
            "config": {
                "legend": {
                    "orient": "right",
                    "layout": {"right": {"anchor": "middle"}},
                },
                "axisY": {"disable": "true"},
                "view": {"stroke": ""},
            },
        },
        use_container_width=True,
    )

except NameError:
    pass
