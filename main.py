import streamlit as st
import altair as alt
import pandas as pd
import time 
from classes import*
from func import*

st.set_page_config("🧮CWA Calculator", layout='wide')

st.header("🧮CWA Calculator", divider="blue")

initialize()

col1, col2, col3=st.columns([3,1,2])
with col1:
    p_cwa=st.slider("#### Previous CWA", min_value=10.00, max_value=100.00, step=0.01, value=70.00, help="Enter your last reported cwa")
    st.caption("Enter your last reported cwa")
with col2:
    credits_completed=st.number_input("#### Credits Completed: ", min_value=1, max_value=100, step=1, value=18)
    st.caption("Enter the credits completed at the time the last CWA was reported")
with col3:
    course_no=st.slider("#### Number of courses", width=400, min_value=1, max_value=15, value=6, help="Enter the number of courses taken last semester")
    st.caption("Enter the number of courses taken last semester")    

st.session_state.p_cwa=p_cwa
st.session_state.course_no=course_no
st.session_state.c_credits=credits_completed

st.divider()
if st.session_state.course_no%2==0:
    batch=st.session_state.course_no/2
elif st.session_state.course_no%2==1:
    batch=(st.session_state.course_no+1)/2

batch=int(batch)

courses_col1, courses_col2=st.columns([1,1])
with courses_col1:
    for courses in range(0,batch):
        course_name=st.text_input("Course name", width=200, key=f"{courses} name" ,help="The course name entered is purely for identification by the user and does not have to be the real course name")
        st.caption("Does not have to be the real course name")
        subcol1, subcol2=st.columns([2,1])
        with subcol1:
            score_estimate=st.slider("Estimate your score in the last exam", value=70, key=f"{courses} score")
        with subcol2:
            credits=st.number_input("Number of credit hours", min_value=1, max_value=7, step=1, key=f"{courses} credits")
        st.session_state.course_details.append(Course(course_name, score_estimate, credits))
        st.write("---")

with courses_col2:
    for courses in range(batch, st.session_state.course_no):
        course_name=st.text_input("Course name", width=200, key=f"{courses} name" ,help="The course name entered is purely for identification by the user and does not have to be the real course name")
        st.caption("Does not have to be the real course name")
        subcol1, subcol2=st.columns([2,1])
        with subcol1:
            score_estimate=st.slider("Estimate your score in the last exam", value=70, key=f"{courses} score")
        with subcol2:
            credits=st.number_input("Number of credit hours", min_value=1, max_value=7, step=1, key=f"{courses} credits")
        st.session_state.course_details.append(Course(course_name, score_estimate, credits))
        st.write("---")

if st.button("Calculate CWA", width=400):
    with st.spinner("Checking requirements..."):
        time.sleep(1)
        confirm=st.success("Details accepted", width=400)
    with st.spinner("Calculating..."):
        time.sleep(1)
        st.session_state.new_cwa_details=calculate_cwa(st.session_state.p_cwa, st.session_state.c_credits, st.session_state.course_details)
        confirm.empty()

st.write("---")
if st.session_state.new_cwa_details[0]!=0:
    st.subheader(f"New CWA:  {st.session_state.new_cwa_details[0]:.2f}")
    with st.expander("Semester info", width=400):
        st.write(f"##### Semester Weighted Average: {calculate_averages(st.session_state.course_details, True):.2f}")
        st.write(f"##### Semester Unweighted Avrage: {calculate_averages(st.session_state.course_details, False):.2f}")
        st.caption(f"{total_credits(st.session_state.course_details)} credits accross {st.session_state.course_no} courses")


if st.checkbox("Graph Information"):
        div1, div2= st.columns([1,1])
        with div1:
            # Raw names, stripping whitespace
            raw_names = [course.name.strip() if course.name else "" 
                        for course in st.session_state.course_details]

            # If ALL names are blank -> auto-number all
            if all(name == "" for name in raw_names):
                display_names = [f"Course {i+1}" for i in range(len(raw_names))]
            else:
                display_names = raw_names   # keep them exactly as typed (blanks stay blank)
                
            df = pd.DataFrame({
            "Course": display_names,
            "Credits": [course.credits for course in st.session_state.course_details]
            })
            st.write("##### 📊 Course Influence on CWA (by Credits)")

            chart = (
                alt.Chart(df)
                .mark_bar()
                .encode(
                    x=alt.X("Course:N", sort='-y', title="Course"),
                    y=alt.Y("Credits:Q", title="Credit Hours"),
                    color=alt.Color("Credits:Q", scale=alt.Scale(scheme="blues")),
                    tooltip=["Course", "Credits"]
                )
                .properties(height=400)
            )

            st.altair_chart(chart, use_container_width=True)

        with div2:
            previous_total = st.session_state.p_cwa*float(st.session_state.c_credits)   # total credits before this semester
            current_addition = 0
            for course in st.session_state.course_details:
                current_addition+=float(course.score*course.credits) # credits from current exams/semester
            df_compare = pd.DataFrame({
                "Category": ["All other semesters", "Last Semester"],
                "Credits": [previous_total, current_addition]
            })

            st.write("##### 📈 Influence of Last Semester Grades Relative To All Previous Ones")

            chart_compare = (
                alt.Chart(df_compare)
                .mark_bar()
                .encode(
                    x=alt.X("Category:N", title=""),
                    y=alt.Y("Credits:Q", title="Credits"),
                    color=alt.Color("Category:N", scale=alt.Scale(scheme="set2")),
                    tooltip=["Category", "Credits"]
                )
                .properties(height=400)
            )

            st.altair_chart(chart_compare, use_container_width=True)














