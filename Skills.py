import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Create job URL
ori_url = "https://www.google.com/search?q={}+jobs+in+uk&rlz=1C1ONGR_en-GBGB1062GB1062&oq={}+jobs+in+uk&gs_lcrp=EgZjaHJvbWUyBggAEEUYOTIICAEQABgWGB4yCAgCEAAYFhgeMggIAxAAGBYYHjIICAQQABgWGB4yBggFEEUYPDIGCAYQRRg8MgYIBxBFGDyoAgCwAgA&sourceid=chrome&ie=UTF-8&ibp=htl;jobs&sa=X&sqi=2&ved=2ahUKEwir8f2c0aSAAxU4QvEDHU01AnQQutcGKAF6BAhLEAY&sxsrf=AB5stBidec_30QqsLco7ZO3GOZZdA5pg6A:1690108614907#htivrt=jobs&htidocid=AvLudwfLAVYAAAAAAAAAAA%3D%3D&fpstate=tldetail"


def Skills(courses):
    # Image icon
    col1, col2, col3 = st.columns([4, 6, 1])
    with col1:
        st.write('')
    with col2:
        st.image("Education.png", width=100)
    with col3:
        st.write('')

    # Explode the list of skills
    exploded_data = courses["skills"].apply(lambda x: x.split(",")).explode()
    SKILLS = set(map(lambda x: x.replace(
        ".", "").title().strip(), exploded_data.tolist()))
    SKILLS.discard('')

    # Set title text and decription
    st.title("Recommendation by skills")
    st.markdown(
        """<hr>
            <style>hr{border: 1.5px solid #FFA07A; margin-top: -.8rem }</style>
        """,
        unsafe_allow_html=True
    )
    st.write('### Discover courses by your interests and skills')

    # Get all minimun reuired qqualifcations from the dataset
    qual = courses["Required Quailification"].apply(
        lambda x: x.split(", ")).explode()
    EXPERIENCE = set(
        map(lambda x: x.title(), qual.tolist()))
    placeholder = '-Select an item-'

    qualification = st.selectbox(
        'Select your previous area of study', [placeholder] + sorted(list(EXPERIENCE)))

    # Populate the DEGREE list with obtainable classes of degree and sort in decending order
    DEGREE = reversed(["First Class", "Second Class Upper",
                       "Second Class Lower", "Third Class", "Pass"])

    # Populate the classess of degree in a slider bar
    degree_class = st.select_slider("Select your degree class", DEGREE)

    # Collect all the available skills in a multiselect input
    user_skills = st.multiselect('Select your interests',
                                 sorted(SKILLS, key=lambda x: x.lower()))

    course_map = courses[['Course Title', 'skills']]

    tfidf_vectorizer = TfidfVectorizer()

    tfidf_matrix = tfidf_vectorizer.fit_transform(
        course_map['skills'].apply(lambda x: x.replace(",", " ")))

    # A function to computer cosine similarities
    def get_course_recommendation(student_profile, courses, top_n=3):
        student_profile_vector = tfidf_vectorizer.transform([student_profile])
        cosine_similarities = cosine_similarity(
            student_profile_vector, tfidf_matrix)
        global course_indices
        course_indices = cosine_similarities.argsort()[0][-top_n:][::-1]
        recommend_course = [courses[i] for i in course_indices]
        return recommend_course

    # A function to check if user meets requirements for the Course.
    def qualification_check(student_qual, course_qual):
        QUAL_BY_DEGREE = student_qual["degree"].lower() not in [
            "third class", "pass"]
        QUAL_BY_STUDY = student_qual["study"].lower() in map(
            lambda x: x.lower(), course_qual.split(", "))

        return [QUAL_BY_DEGREE, QUAL_BY_STUDY]

    if st.button("Recommend"):
        if qualification == placeholder:
            st.error('Please select previous qualification')
            return
        elif not user_skills:
            st.error('Please select your skills')
            return
        user_skills = ','.join(user_skills)
        top_recommendations = get_course_recommendation(
            user_skills, course_map['Course Title'],)

        # Creating a DataFrame from the recommendations, course links, Job Roles and Qualification
        TR = pd.DataFrame(
            {"Course Names": top_recommendations,
             "Course Links": courses["url"][course_indices].tolist(),
             "Job Roles": courses["job roles"][course_indices].tolist(),
             "Qualified": map(lambda x: qualification_check({"degree": degree_class, "study": qualification}, courses["Required Quailification"][x]), course_indices)},
            index=[1, 2, 3])
        reason = ""

        # Rendering the collected data on the page
        for i in range(1, 4):

            if TR["Qualified"][i][0]:
                reason = "Your previous course of study did not meet the course requirements!"
            elif TR["Qualified"][i][1]:
                reason = "Your degree class is below course requirment!"
            elif not any(TR["Qualified"][i]):
                reason = "You did not meet the minimum requirements for this course"

            with st.container():
                st.subheader(top_recommendations[i-1])
                st.markdown(
                    f"""
                    <a href={TR["Course Links"][i]}>Get course information</a>
                    """, unsafe_allow_html=True
                )
                DF_JB = TR["Job Roles"][i].split(',')
                all_anchor_tags = "Jobe Roles: "
                for x in DF_JB:
                    final_url = ori_url.format(
                        '+'.join(x.split()), '+'.join(x.split()))
                    anchor_tag = f'<a href="{final_url}" target ="_black">{x}</a>' + " "
                    all_anchor_tags += anchor_tag
                st.markdown(
                    all_anchor_tags, unsafe_allow_html=True
                )

                st.error(
                    f"""Unfortunately, you do not meet the minimum reuirements this course. \n
                    Reason: {reason}""") if not all(TR["Qualified"][i]) else ""
                st.markdown("<br/> <hr/>", unsafe_allow_html=True)
