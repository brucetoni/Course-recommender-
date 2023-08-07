import streamlit as st
import pandas as pd
from Budget import Budget
from Skills import Skills
from University import University

st.set_page_config(
    page_title="PG Course Recommender System",
    initial_sidebar_state="expanded"
)


# Load the universities dataset
@st.cache_data
def load_data():
    # Load the course_skills dataset
    course_skills_ds = pd.read_csv(
        r".\datasets\mydataset2.csv")
    university_ds = pd.read_csv(
        r".\datasets\uk_universities.csv")

    return [course_skills_ds, university_ds]


[course_skills_ds, university_ds] = load_data()
# Define the Home componet


def Home():
    col1, col2, col3 = st.columns([4, 1, 2])
    with col1:
        st.markdown("""
        <span style='color:#191970; font-size: 45pt; font-weigth: bolder margin-bottom:1rem'>Welcome back!</span>
        """, unsafe_allow_html=True)
    with col2:
        st.write('')
    with col3:
        st.image("Education.png", width=100)
    st.markdown("""
    <hr>
    <p style="font-size: 15pt">Our aim is to help you select the right course for you. So we have gathered the best courses from the UK and ranked them.</p>
    <b style="font-size: 15pt">We provide recommendations by:</b>

    <ul>
        <li style="font-size: 15pt">Skills</li>
        <li style="font-size: 15pt">Universities</li>
        <li style="font-size: 15pt">Funding</li>
    </ul>
    """, unsafe_allow_html=True)

    st.image("university.jpg", use_column_width=True)
    st.markdown(
        "<div style='text-align:center; padding:1rem'>Copyright @2023 <br/> All Rights Reserved</div>", unsafe_allow_html=True
    )
    html_temp = """
    <style>
        button {border-radius: 5px; background-color: darkblue; border:none; display:flex; width:100%}
        # MainMenu {display: none;}
        footer {display: none;}
        .css-uf99v8 {background-color: #FFFFFF; background-image: linear-gradient(180deg, #FFFFFF 0%, #d7e7ed 50%, #799cd8 100%);}
        .css-18ni7ap {background-image: linear-gradient(to top, #30cfd0 0%, #330867 100%);}
        .css-6qob1r{background-image: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);}
        hr{border: 1.5px solid #FFA07A; margin-top: -.8rem }
    </style> """
    st.markdown(html_temp, unsafe_allow_html=True)


def main():
    st.sidebar.image("pg.png",  width=100)
    st.sidebar.title("Get Started")
    st.sidebar.caption("Choose an option to continue")
    options = ["Home", "Recommend by Skills",
               "Recommend by University", "Recommend by Funding"]
    choice = st.sidebar.radio("Go to", options)

    if choice == "Home":
        Home()
    elif choice == "Recommend by Skills":
        Skills(course_skills_ds)
    elif choice == "Recommend by University":
        University(university_ds)
    elif choice == "Recommend by Funding":
        Budget(university_ds)


if __name__ == "__main__":
    main()
