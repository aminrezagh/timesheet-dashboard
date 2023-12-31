import streamlit as st
import pandas as pd
from pytimeparse.timeparse import timeparse
import distinctipy

st.set_page_config(page_icon="📊", layout="wide", page_title="Package Man-Hour")

PAGE_STYLE = """
            <style>
            footer {visibility: hidden;}
            #MainMenu {visibility: hidden;}
            .stDeployButton {visibility: hidden;}
            .main {
                background-image: url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAAAXNSR0IArs4c6QAABKpJREFUeF7tnduygyAMRWv7/5/c9gzO0GFy0FyBRNPXKsa92IQgttv3+/0+8uNGgS2BuGGxB5JAfPFIIM54JJAE4k0BZ/FkDkkgzhRwFk46JIE4U8BZOJdwSFls2LbNmbSycMIDKTDq6s/z+ZSp4Ois0EAKiM/n85OzuCQ6lLBAqjPg2mh0KCGBQGfAEScylHBAjpxxFSihgGDOuAKUMECozogOJQQQrjMiQ3EPROqMqFDcAynCah1S4USYfYUAUgQtBaDFfgzvUFwCqcLD9ak7OMUdkHZtqgCBUK7uFFdAeg4oa1N3coobIGdrU3dyigsglNxwF6csB0KtM6pLrp5TlgKhOAMWeFd3yjIgVGf0Ku4r55QlQCTOuItTpgOROoO6NhW9TpkKxMIZ+5Z95Nn5rOuM2BsxDUjdjKBdj8JgVJGiOmUKkJHi1CGwt9skolOGAxnpjFbwq9QpQ4GMdMZR29HrlGFARs6mMNC9PIOdQ03Q1BxGbe/f7HHES58jb57adk+4CDnF3CErnUGpVahAsR4+yimmQEberLTtaE4xAzJrNoX13N73vUQvBUxxoSTG30YMixwy+ua07R8NLx5zitohI51huQXo9Xp1O64WtvUWIxWQGTdj1YuPgFhCt0j0YiAzYFiKdQbE074vEZBZMGYCsbyWxilsICPrjN4gP2PIaq9r1dl6MzvK7IsNxCJgbg/SXpN7PYtOcLTYiUFhAbEKlPti5mwgVjmF2xH2h2+cOmSFMNoHThJR6jUtOiA2mRAvLmpzh0YYTcKVjuXajlDP516f7BANEC0MSdKVjuHWEwvuvbOAtC/pY8nJuoJth5F2h3wvDq4IlHuRDtfcWMhApAFxLUsRpz2mwultnuO2hR0v0cAdkBlCYUJafI+58ugaw4BYzDgshInWRgJxRmwoEKltnWk0NRxuDiUndavqdaoaDi42rDDUFGcOdFkSAne4Yi+dpEvoXKWFKWvIqi7JXIKDkbhD5JB0yTgYYiAJ5RiK1Bm1RfaQBZctJOtbeB+LeYQWhsohVTLNKnBM2f9HLU3gvftXOQS65W7JvoDYe3XnN1mknc0MCIRTZ2TSwLye10IYEeMQICMCvUubCcQZ6QSSQJwp4CycaQ7hzMDafVvwPLini1oHwZkQFo/lzInDfBoQ6vNoWFzBV58hkPf7Tbpf+FyCGg/3eQYpmJODEgiioGXRR4G1BAhniYHqEK5wrUOwV9448VJEPzsmgTwe+5/A1IKvXRJq8xP3yZ8UzDIgUIB6A2fC9HpqzSFYEobtYg4p8VCOkQp/dN4SIGc3AXsrdcg6HQY6P+dEEZtyTAIBf/xFmWX1nEURm3LMJYCcDS+aIauuvPZEyiELqNL2Ns6shTpkWc+y4HOeyyd16ltUq4BIO5B2CFuS1DkzIi4QLLnX76Hg7ZAGl1U4jg4JBBOtBUYFggkBRYVLJxBIOw2nuhmLgfL9Eod4BAJjqoBmwtgnJZyXPimEj44pPZ366c20zgpHSbuUeI6KV+r1JMdNAyIJ7o7nJBBn1BNIAnGmgLNw0iEJxJkCzsJJhyQQZwo4CycdkkCcKeAsnHRIAnGmgLNw/gAOvtkgXy6PIAAAAABJRU5ErkJggg==');
                background-size: 100px;
            }
            </style>
            """

st.markdown(PAGE_STYLE, unsafe_allow_html=True)

# defines default columns names for database<br
default_names = [
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

new_names = [
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
pckg_pers_id = [
    str(i) for i in sum(pd.read_csv("package_personnel_ids.txt").values.tolist(), [])
]


def clean_and_categorize(df: pd.DataFrame):
    # renames the columns
    df.rename(columns=dict(zip(default_names, new_names)), inplace=True)
    df = df[df["pers_id"].isin(pckg_pers_id)]
    df.drop("pers_id", axis=1, inplace=True)

    # converts time-format to number of hours
    time_cols = ["basic", "over_time", "mission", "homework"]
    df[time_cols] = df[time_cols].applymap(
        lambda t: timeparse(t, granularity="minutes") / 3600
    )
    df.drop(["discipline", "discipline_code"], axis=1, inplace=True)

    # adds thursday column to dataframe
    df.loc[df["basic"] == 0, "thursday"] = df["over_time"]
    df["thursday"].fillna(0, inplace=True)
    df.loc[df["cost_center_id"] == "OFF", "off_time"] = df["basic"]
    df["off_time"].fillna(0, inplace=True)
    df["pers_name"] = (
        df["last_name"].str.split().str.get(0).str.title()
        + ", "
        + df["first_name"].str.title()
    )
    df.drop(["first_name", "last_name"], axis=1, inplace=True)

    # defines categories for different types of activies
    df.loc[df["activity_id"].str.contains("EVD", case=True), "activity_type"] = "VDR"
    df.loc[
        df["activity_name"].str.contains("clarification", case=False), "activity_type"
    ] = "TCL"
    df.loc[
        df["activity_name"].str.contains("data sheet", case=False), "activity_type"
    ] = "DSH"
    df.loc[
        df["activity_name"].str.contains("datasheet", case=False), "activity_type"
    ] = "DSH"
    df.loc[
        df["activity_name"].str.contains("requisition", case=False), "activity_type"
    ] = "MRQ"
    df.loc[df["activity_name"].str.contains("TBE", case=True), "activity_type"] = "TBE"
    df.loc[
        df["activity_name"].str.contains("service", case=False), "activity_type"
    ] = "ITC"
    df.loc[df["activity_name"].str.contains("POR", case=True), "activity_type"] = "POR"
    df.loc[
        df["activity_name"].str.contains("coordination", case=False), "activity_type"
    ] = "CRD"
    df.loc[
        df["activity_name"].str.contains("meeting", case=False), "activity_type"
    ] = "MTG"
    df.loc[
        df["activity_name"].str.contains("mission", case=False), "activity_type"
    ] = "MSN"
    df.loc[
        df["activity_name"].str.contains("contract", case=False), "activity_type"
    ] = "CRW"
    df.loc[
        df["cost_center_id"].str.contains("off", case=False), "activity_type"
    ] = "OFF"
    df["activity_type"].fillna("OTH", inplace=True)
    df["month"] = df["date"].astype(str).str[4:6]
    df["year"] = df["date"].astype(str).str[0:4]
    df.drop("date", axis=1, inplace=True)
    df["date"] = df["year"] + " - " + df["month"]
    df["total_basic"] = df["basic"] + df["mission"]
    df["total"] = df["total_basic"] + df["over_time"]
    df["net_working"] = df["total_basic"] - df["off_time"] + df["over_time"]

    return df


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
    if "dc" not in st.session_state:
        st.session_state["dc"] = distinctipy.get_colors(len(prj_ids))
        st.session_state["hex_code"] = [
            distinctipy.get_hex(c) for c in st.session_state["dc"]
        ]

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

        st.markdown(
            f""" <h4 style='font-family: "Segoe UI"; font-weight: normal'>
                        ⚠️
                        <br>
                        <br>
                        THIS DASHBOARD IS INTENDED SOLELY FOR <b>PREVIEW PURPOSES</b>, AND THE DATA PRESENTED HEREIN SHOULD NOT BE REGARDED AS FACTUAL.
                        </h4>
                    """,
            unsafe_allow_html=True,
        )

    v1, v2, v3 = st.columns([1, 2, 1])
    with v2:
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
                    {
                        "calculate": "datum.total/datum.sumoftotal * 100",
                        "as": "percent",
                    },
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
                        "type": "nominal",
                        "scale": {"domain": acts, "range": act_hex},
                        "legend": {
                            "orient": "right",
                            "title": "Activity Types",  # Add a title for the legend, if desired
                        },
                    },
                },
                "padding": {"top": 20, "bottom": 20, "left": 20, "right": 20},
            },
            use_container_width=True,
        )

    st.markdown("<br><br>", unsafe_allow_html=True)

    v1, v2, v3 = st.columns([1, 7, 1])
    with v2:
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
                    {
                        "calculate": "datum.total/datum.sumoftotal * 100",
                        "as": "percent",
                    },
                ],
                "width": "container",
                "height": 550,
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
                        "scale": {
                            "domain": prj_ids,
                            "range": st.session_state["hex_code"],
                        },
                    },
                },
                "padding": {"top": 20, "bottom": 20, "left": 20, "right": 20},
                "config": {
                    "legend": {
                        "orient": "right",
                        "layout": {"right": {"anchor": "middle"}},
                        "labelFontSize": 12,
                        "columns": 2,
                    },
                    "axisY": {"disable": "true"},
                    "view": {"stroke": ""},
                },
            },
            use_container_width=True,
        )

except NameError:
    pass
