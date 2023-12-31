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
    "<h1 style='text-align: center;'>Availability</h1><br>", unsafe_allow_html=True
)

# loads dataframe from session state
df = st.session_state["dataframe"]

# group columns on name and date
gr = df.groupby(["pers_name", "date"]).sum().reset_index()
gr["max_basic"] = gr["date"].map(
    {
        r[0]: r[1]
        for r in df.groupby(["date", "pers_name"])
        .sum()
        .reset_index()
        .groupby("date")
        .agg({"total_basic": "max"})
        .reset_index()
        .to_dict("split")["data"]
    }
)
gr["availability"] = gr["net_working"] / gr["max_basic"] * 100
gr["over_time_pcnt"] = gr["over_time"] / gr["max_basic"] * 100
sec_av = gr.groupby("date").mean().reset_index()
gr["sec_av"] = gr["date"].map(
    {r[0]: r[1] for r in sec_av[["date", "availability"]].to_dict("split")["data"]}
)

month_range = sorted(df["date"].unique(), reverse=True)


def set_ss():
    st.session_state["ss_month_range"] = st.session_state["ms_month_range"]


if "ss_month_range" not in st.session_state:
    st.session_state["ss_month_range"] = []

with st.sidebar:
    with st.form("Exclude"):
        st.multiselect(
            "Months",
            month_range,
            default=st.session_state["ss_month_range"],
            key="ms_month_range",
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

pers_list = sorted(list(set(gr["pers_name"].to_list())))
width, height = 2, len(pers_list) // 2 + 1

v1, b1, v2 = st.columns([5, 1, 5])
for i, v in enumerate([v1, v2]):
    with v:
        try:
            for n in range(height):
                avg_all = gr[
                    gr["pers_name"].isin([pers_list[width * n + i]])
                    & gr["date"].isin(
                        set(month_range).difference(
                            set(st.session_state["ss_month_range"])
                        )
                    )
                ]["availability"].mean()
                over_avg_all = gr[
                    gr["pers_name"].isin([pers_list[width * n + i]])
                    & gr["date"].isin(
                        set(month_range).difference(
                            set(st.session_state["ss_month_range"])
                        )
                    )
                ]["over_time"].mean()

                st.vega_lite_chart(
                    gr[
                        gr["pers_name"].isin([pers_list[width * n + i]])
                        & ~gr["date"].isin(st.session_state["ss_month_range"])
                    ],
                    {
                        "transform": [
                            {"fold": ["availability", "sec_av", "over_time_pcnt"]}
                        ],
                        "width": "container",
                        "height": 400,
                        "title": {
                            "text": pers_list[width * n + i],
                            "offset": 15,
                            "fontSize": "15",
                        },
                        "mark": {
                            "type": "line",
                            "tooltip": {
                                "signal": "{'Availability (%)': round(datum.value), 'Month': datum.date}"
                            },
                        },
                        "encoding": {
                            "x": {
                                "field": "date",
                                "type": "nominal",
                                "axis": {"title": "Month", "grid": "true"},
                            },
                            "y": {
                                "field": "value",
                                "type": "quantitative",
                                "axis": {"title": "Availability (%)"},
                            },
                            "color": {"field": "key", "type": "nominal"},
                        },
                        "padding": {"top": 20, "bottom": 20, "left": 20, "right": 20},
                    },
                    use_container_width=True,
                )

                try:
                    st.markdown(
                        "<b>STATISTICS:</b><br>"
                        + "<br>".join(
                            [
                                f"AVG = <b>{int(avg_all)} %</b>",
                                f"AVG (OVERTIME)= <b>{int(over_avg_all)} h</b>",
                            ]
                        ),
                        unsafe_allow_html=True,
                    )
                except ValueError:
                    pass

        except IndexError:
            pass
