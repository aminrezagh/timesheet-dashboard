import streamlit as st
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

st.markdown(
    "<h1 style='text-align: center;'>Contributions - Projects</h1><br>",
    unsafe_allow_html=True,
)


def set_ss():
    st.session_state["ss_month_range"] = st.session_state["ms_month_range"]
    st.session_state["ss_act_range"] = st.session_state["ms_act_range"]


# loads dataframe from session state
df = st.session_state["dataframe"]

months = list(sorted(df["date"].unique(), reverse=True))
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
width, height = 3, len(prj_ids) // 3 + 1

v1, b1, v2, b2, v3 = st.columns([7, 1, 7, 1, 7])
for i, v in enumerate([v1, v2, v3]):
    with v:
        try:
            for n in range(height):
                st.vega_lite_chart(
                    df[
                        df["cost_center_id"].isin([prj_ids[width * n + i]])
                        & ~df["date"].isin(st.session_state["ss_month_range"])
                        & ~df["activity_type"].isin(st.session_state["ss_act_range"])
                    ]
                    .groupby(["cost_center", "pers_name"])
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
                            "text": prj_ids[width * n + i],
                            "offset": 20,
                            "fontSize": "14",
                            "anchor": "start",
                        },
                        "mark": {
                            "type": "bar",
                            "stroke": "#fff",
                            "tooltip": {
                                "signal": "{'Percent (%)': round(datum.percent), 'Employee': datum.pers_name, 'Project': datum.cost_center}"
                            },
                        },
                        "encoding": {
                            "x": {
                                "field": "pers_name",
                                "type": "nominal",
                                "sort": "-y",
                                "axis": {"title": "", "grid": "true"},
                            },
                            "y": {
                                "field": "percent",
                                "type": "quantitative",
                                "axis": {"title": "%"},
                            },
                            "color": {"value": "#00A693"},
                        },
                        "padding": {"top": 10, "bottom": 10, "left": 10, "right": 10},
                    },
                    use_container_width=True,
                )

        except IndexError:
            pass
