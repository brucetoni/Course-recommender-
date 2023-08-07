import streamlit as st
import pandas as pd


def Budget(courses):
    placeholder = '-Select an item-'

    col1, col2, col3 = st.columns([4, 6, 1])
    with col1:
        st.write('')
    with col2:
        st.image("Education.png", width=100)
    with col3:
        st.write('')

    # Using Set Intersection technique
    def budget_ranker(discipline, TB, LB, DF=courses):
        # Selecting the rows where the discipline is equal to our selected discipline.
        match_DF = DF.where(DF["discipline"] == discipline)
        # Removing the rows with empty values (NaN)
        match_DF.dropna(inplace=True)

        # Filtering the DataFrame to get the rows where the Post Graduate Fees is Less than or equal to the tuition budget
        filtered_df_1 = match_DF[match_DF['PG_average_fees_(in_pounds)'] <= TB]
        # Filtering the DataFrame to get the rows where the Estimated Living Costs Per Year is less than or equal to the living budget
        filtered_df_2 = match_DF[
            match_DF['Estimated_cost_of_living_per_year_(in_pounds)'] <= LB]
        # Finding the Set Intersection between the two filtered DataFrames to recommend the best possible option for the user.
        return pd.merge(filtered_df_1, filtered_df_2, on="University_name", how="inner").head(3)

    st.markdown("## Recommendation by Funding")

    tuition = courses["PG_average_fees_(in_pounds)"]
    living_cost = courses["Estimated_cost_of_living_per_year_(in_pounds)"]

    discipline = set(courses["discipline"].tolist())
    discipline = st.selectbox("Choose your prefered discipline",
                              [placeholder] + list(discipline))

    tuition_budget = st.slider(label="Your budget for Tuition Fees (£)",
                               min_value=int(tuition.min()), max_value=int(tuition.max()))

    living_budget = st.slider(label="Your budget for Living Costs (£)",
                              min_value=int(living_cost.min()), max_value=int(living_cost.max()))

    if st.button("Recommend"):
        if discipline == placeholder:
            st.error("Please select prefered!")
            return
        matched = budget_ranker(discipline=discipline,
                                LB=living_budget, TB=tuition_budget)
        if matched.empty:
            st.error("Sorry, we could not recommend a university for you within the specified budget and discipline.\n Please consider making some adjustments")
        else:
            for index, row in matched.iterrows():
                with st.container():
                    st.subheader(row["University_name"])
                    st.markdown(
                        f"""
                        <span style="display:block; font-size:15pt">Tuition Fees: <b>£{row["PG_average_fees_(in_pounds)_x"]}</b></span>
                        <span style="display:block; font-size:15pt">Cost of Living Per Year: <b>£{row["Estimated_cost_of_living_per_year_(in_pounds)_x"]}</b></span>
                        <a href=https://{row["Website_x"]} target=_blank >Visit School Website</a>
                        <hr/>
                        """, unsafe_allow_html=True
                    )
