import streamlit as st
import plotly.graph_objects as go

st.set_page_config(
    page_title="Getaround Project",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed"
  )

with st.columns([2,3,2])[1]:
    st.markdown("<h1 style='text-align: center; color: #a404c4;'>Late Returns</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: black;'>Scope of a pervasive issue and possible solutions</h3>", unsafe_allow_html=True)

    with st.spinner("Preparing the data. This may take a couple of minutes."):
        from get_formatted_data import get_affected_rentals_df, get_optimal_buffer_df, get_plot_width


with st.columns([1,3,1])[1]:
    st.markdown("### How Common Late Checkouts are and How Many People are Affected")

    affected_rentals_df = get_affected_rentals_df()

    st.markdown("How much later than exactly on time should a checkout be to qualify as a \"late checkout\"?")
    user_input_delay = st.number_input("In minutes", step=1, width=100)
    if user_input_delay < 0:
        st.markdown("If the user checks out early, then nobody is negatively affected!")
    else:
        max_delay = len(affected_rentals_df) - 1
        user_input_delay_index = int(user_input_delay) if user_input_delay <= max_delay else max_delay

        later_returns = affected_rentals_df.loc[user_input_delay_index, "percentage_of_even_later_returns"]
        potentially_affected = affected_rentals_df.loc[user_input_delay_index, "percentage_of_potentially_affected_rentals"]
        cancelled_bc_late = affected_rentals_df.loc[user_input_delay_index, "percentage_rentals_cancelled_bc_late"]
        user_input_delay_text = f"{user_input_delay} minute" if user_input_delay == 1 else f"{user_input_delay} minutes"

        st.markdown(f"Answer:\n{later_returns:.1f}% of non-cancelled rentals were returned later than {user_input_delay_text}, "
                    f"which was {potentially_affected:.1f}% likely to affect another user.\n"
                    f"{cancelled_bc_late:.1f}% of rentals that followed a "
                    f"{"timely checkout" if user_input_delay == 0 else f"checkout {user_input_delay_text} late or less late"} were cancelled.")


    st.markdown("### Visualise the Best Time Buffer Between Rentals")

    col_1, col_2 = st.columns([2, 1])
    optimal_buffer_df = get_optimal_buffer_df()

    with col_2:
        custom_income_on = st.toggle("Calculate income loss based on my own income", key="custom_income_on")
        if custom_income_on:
            income_per_minute = st.number_input("Please enter an hourly income", value=1.0, step=0.01, width=100) / 60
        else:
            income_per_minute = 1
        st.markdown("In order to avoid friction due to users being late at checkout, we would like to impose a time buffer between each rental. "
                    "The data show the sweet spot between a low percentage of rentals that would have been hindered by a buffer that is too long, "
                    "and the percentage of late returns rendered unproblematic thanks to a buffer that is long enough, is very close to 90 minutes; "
                    "Hence the default value being set to 90 minutes. Feel free to play around with the slider to see whether a different value would suit you better.")
        max_buffer_value = len(optimal_buffer_df) - 1
        user_buffer_value = st.slider("Please select a buffer time value to check.",
                                    min_value=0,
                                    max_value=max_buffer_value,
                                    value=90,
                                    key="buffer_time_slider")
        
        helped_late_returns = optimal_buffer_df.loc[user_buffer_value, "percentage_helped_late_returns"]
        hindered_rentals = optimal_buffer_df.loc[user_buffer_value, "percentage_hindered_rentals"]
        if custom_income_on:
            income_loss_series = optimal_buffer_df["buffer_value"] * income_per_minute
            user_income_loss = income_loss_series[user_buffer_value]
            income_loss_text = f"The estimated income loss amounts to {user_income_loss:.2f}"
        else:
            income_loss_series = optimal_buffer_df["dummy_income_loss"]
            dummy_income_loss = income_loss_series[user_buffer_value]
            income_loss_text = f"The estimated income loss amounts to {dummy_income_loss:.2f}, assuming that the income loss " \
                               f"associated with the latest checkout in the data ({max_buffer_value} minutes) is 100. " \
                                "Input an hourly income above for a more accurate estimate."

    with col_1:
        fig = go.Figure()

        percentage_helped_late_returns = optimal_buffer_df["percentage_helped_late_returns"].to_list()
        income_loss = income_loss_series.to_list()
        percentage_hindered_rentals = optimal_buffer_df["percentage_hindered_rentals"].to_list()

        base_plot_width = get_plot_width()
        real_plot_width = base_plot_width if base_plot_width > user_buffer_value else user_buffer_value + 100
        buffer_value = optimal_buffer_df.loc[0:real_plot_width, "buffer_value"].to_list()

        fig.add_trace(go.Scatter(
            x=buffer_value, y=percentage_helped_late_returns,
            mode="lines",
            name="Percentage helped late returns",
            line={"color": "blue", "width": 2},
            line_shape="spline"
        ))

        fig.add_trace(go.Scatter(
            x=buffer_value, y=income_loss,
            mode="lines",
            name="Income loss",
            line={"color": "red", "width": 2}
        ))

        fig.add_trace(go.Scatter(
            x=buffer_value, y=percentage_hindered_rentals,
            mode="lines",
            name="Percentage hindered rentals",
            line={"color": "green", "width": 2},
            line_shape="spline"
        ))

        fig.add_vline(
            x=user_buffer_value,
            line=dict(color="black", dash="dot"),
            annotation_text="Your choice of buffer" if user_buffer_value != 90 else "Default buffer",
            annotation_position="top",
            annotation_font_size=10,
            annotation_font_color="black",
        )
        
        fig.update_layout(
            title="Finding the optimal buffer time before a new rental",
            xaxis_title="Buffer in minutes",
            yaxis_title="",
            legend={"title": "Labels"},
            template="plotly_white"
        )

        st.plotly_chart(fig)

        st.markdown(f"""
                    With a buffer of {user_buffer_value} {"minute" if user_buffer_value == 1 else "minutes"}:
                    - {helped_late_returns:.1f}% of late returns are no longer an issue;
                    - {hindered_rentals:.1f}% of bookings that followed another booking in the data could not have gone through;
                    - {income_loss_text}
                    """)
        