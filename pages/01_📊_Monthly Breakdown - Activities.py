import streamlit as st

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
                        "padding": {"top": 20, "bottom": 20, "left": 20, "right": 20},
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
                        "padding": {"top": 20, "bottom": 20, "left": 20, "right": 20},
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
