import streamlit as st

st.set_page_config(layout="wide", page_title="Package Man-Hour")

hide_streamlit_logo = """
            <style>
            footer {visibility: hidden;}
            </style>
            """

st.markdown(hide_streamlit_logo, unsafe_allow_html=True)

st.markdown(
    '<h1 style="text-align: center;">Monthly Breakdown - Activities</h1><br>',
    unsafe_allow_html=True,
)


def set_ss():
    st.session_state["ss_month_range"] = st.session_state["ms_month_range"]
    st.session_state["ss_act_range"] = st.session_state["ms_act_range"]
    st.session_state["ss_prj_range"] = st.session_state["ms_prj_range"]


# loads dataframe from session state
df = st.session_state["dataframe"]

# defines options for multiselect widget
pers_list = sorted(list(df["pers_name"].unique()))
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
months = list(sorted(df["date"].unique(), reverse=True))
prjs = list(sorted(df["cost_center"].unique()))

dom = acts
rng = act_hex

if "ss_month_range" not in st.session_state:
    st.session_state["ss_month_range"] = []

if "ss_act_range" not in st.session_state:
    st.session_state["ss_act_range"] = []

if "ss_prj_range" not in st.session_state:
    st.session_state["ss_prj_range"] = []

with st.sidebar:
    with st.form("Exclude"):
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

width, height = 2, len(pers_list) // 2 + 1
v1, b1, v2 = st.columns([7, 1, 7])

for i, v in enumerate([v1, v2]):
    with v:
        try:
            for n in range(height):
                # chart-01
                st.vega_lite_chart(
                    df[
                        df["pers_name"].isin([pers_list[width * n + i]])
                        & ~df["date"].isin(st.session_state["ss_month_range"])
                        & ~df["cost_center"].isin(st.session_state["ss_prj_range"])
                        & ~df["activity_type"].isin(st.session_state["ss_act_range"])
                    ]
                    .groupby(["date", "activity_type"])
                    .sum()
                    .reset_index(),
                    {
                        "width": "container",
                        "height": {"step": 25},
                        "title": {
                            "text": pers_list[width * n + i],
                            "offset": 15,
                            "fontSize": "16",
                            "anchor": "start",
                        },
                        "mark": {
                            "type": "bar",
                            "stroke": "#fff",
                            "tooltip": {
                                "signal": "{'Total (h)': round(datum.total), 'Activity': datum.activity_type, 'Month': datum.date}"
                            },
                        },
                        "encoding": {
                            "x": {
                                "field": "total",
                                "type": "quantitative",
                                "axis": {"title": "Total (h)"},
                            },
                            "y": {
                                "field": "date",
                                "type": "nominal",
                                "axis": {"title": "Month", "grid": "true"},
                            },
                            "color": {
                                "field": "activity_type",
                                "type": "nominal",
                                "scale": {"domain": dom, "range": rng},
                            },
                        },
                        "config": {
                            "legend": {
                                "orient": "right",
                                "layout": {"right": {"anchor": "middle"}},
                            }
                        },
                    },
                    use_container_width=True,
                )

                # chart-02
                st.vega_lite_chart(
                    df[
                        df["pers_name"].isin([pers_list[width * n + i]])
                        & ~df["date"].isin(st.session_state["ss_month_range"])
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
                        "height": 350,
                        "title": {
                            "text": f"{pers_list[width * n + i]} - OVERALL BREAKDOWN",
                            "offset": 20,
                            "fontSize": "16",
                            "anchor": "start",
                        },
                        "mark": {
                            "type": "arc",
                            "innerRadius": 70,
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
                                "scale": {"domain": dom, "range": rng},
                            },
                        },
                        "config": {
                            "legend": {
                                "orient": "right",
                                "layout": {"right": {"anchor": "middle"}},
                            }
                        },
                    },
                    use_container_width=True,
                )

        except IndexError:
            pass
