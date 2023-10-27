import streamlit as st
import distinctipy

st.set_page_config(layout="wide", page_title="Package Man-Hour")

hide_streamlit_logo = """
            <style>
            footer {visibility: hidden;}
            </style>
            """

st.markdown(hide_streamlit_logo, unsafe_allow_html=True)
st.markdown(
    "<h1 style='text-align: center;'>Monthly Breakdown - Projects</h1><br>",
    unsafe_allow_html=True,
)


df = st.session_state["dataframe"]

pers_list = sorted(list(set(df["pers_name"].to_list())))
cc_list = sorted(list(set(df["cost_center_id"].to_list())))

width, height = 2, len(pers_list) // 2 + 1

dc = distinctipy.get_colors(len(cc_list))
hex_code = [distinctipy.get_hex(c) for c in dc]

months = list(sorted(df["date"].unique(), reverse=True))
acts = list(sorted(df["activity_type"].unique()))
prjs = list(sorted(df["cost_center"].unique()))


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


v1, b1, v2 = st.columns([7, 1, 7])
for i, v in enumerate([v1, v2]):
    with v:
        try:
            for n in range(height):
                st.vega_lite_chart(
                    df[
                        df["pers_name"].isin([pers_list[width * n + i]])
                        & ~df["date"].isin(st.session_state["ss_month_range"])
                        & ~df["activity_type"].isin(st.session_state["ss_act_range"])
                        & ~df["cost_center"].isin(st.session_state["ss_prj_range"])
                    ]
                    .groupby(["date", "cost_center_id", "cost_center"])
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
                                "signal": "{'Total (h)': round(datum.total), 'Project': datum.cost_center}"
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
                                "field": "cost_center_id",
                                "type": "nominal",
                                "scale": {"domain": cc_list, "range": hex_code},
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

                st.vega_lite_chart(
                    df[
                        df["pers_name"].isin([pers_list[width * n + i]])
                        & ~df["date"].isin(st.session_state["ss_month_range"])
                        & ~df["activity_type"].isin(st.session_state["ss_act_range"])
                        & ~df["cost_center"].isin(st.session_state["ss_prj_range"])
                    ]
                    .groupby(["cost_center", "cost_center_id"])
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
                            "text": f"{pers_list[width * n + i]} - OVERALL BREAKDOWN",
                            "offset": 20,
                            "fontSize": "16",
                            "anchor": "start",
                        },
                        "mark": {
                            "type": "arc",
                            "innerRadius": 80,
                            "stroke": "#fff",
                            "tooltip": {
                                "signal": "{'Percent (%)': round(datum.percent), 'Project': datum.cost_center}"
                            },
                        },
                        "encoding": {
                            "theta": {"field": "percent", "type": "quantitative"},
                            "color": {
                                "field": "cost_center_id",
                                "type": "quantitative",
                                "type": "nominal",
                                "scale": {"domain": cc_list, "range": hex_code},
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
