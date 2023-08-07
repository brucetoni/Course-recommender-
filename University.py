import streamlit as st
import pandas as pd


def University(courses):
    placeholder = '-Select an item-'
    col1, col2, col3 = st.columns([4, 6, 1])
    with col1:
        st.write('')
    with col2:
        st.image("Education.png", width=100)
    with col3:
        st.write('')
    st.title("Recommendation by University")

    discipline = set(courses["discipline"].tolist())
    discipline = st.selectbox("Choose your prefered discipline",
                              [placeholder] + list(discipline))

    # Using Weighted Rankings
    def university_ranker(discipline, DF=courses, inter=True):
        match_DF = DF.where(DF["discipline"] == discipline)
        match_DF.dropna(inplace=True)

        def get_weight():
            CC = []
            for index, row in match_DF.iterrows():
                # st.write(row['International_students'])
                CC.append(
                    (0.5 * row['UK_rank']) +
                    (0.25 * (float(row['International_students'][:-2]))) if inter == "Yes" else (0.25 * (100 - float(row['International_students'][:-2]))) +
                    (0.25 * (float(row['Student_satisfaction'][:-2])))

                )
            return CC

        match_DF["Cumulative Comparison"] = get_weight()
        match_DF.sort_values(by="Cumulative Comparison",
                             inplace=True, ascending=False)

        return match_DF.reset_index().head(3)
    _student = st.radio("Are you an International Student?", ["Yes", "No"])
    # if _student == "No":
    #     _region = st.selectbox("Select your Region", [
    #                            placeholder] + list(region))

    if st.button("Recommend"):
        if discipline == placeholder:
            st.error("Please select prefered!")
            return
        matched = university_ranker(discipline=discipline, inter=_student)
        for index, row in matched.iterrows():
            with st.container():
                st.subheader(row["University_name"])
                st.markdown(
                    f"""
                    <span style="display:block; font-size:15pt">Motto: <b>{row["Motto"]}</b></span>
                    <span style="display:block; font-size:15pt">Region: <b>{row["Region"]}</b></span>
                    <a href=https://{row["Website"]} target=_blank >Visit School Website</a>
                    <hr/>
                    """, unsafe_allow_html=True
                )
