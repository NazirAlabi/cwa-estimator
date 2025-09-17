import streamlit as st
import time 
from classes import*
from func import*

st.set_page_config("🧮CWA Calculator", layout="wide")

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
        if len(st.session_state.course_details)!=st.session_state.course_no:
            st.error("Enter details for all courses first")
            st.stop()
        else:
            st.success("Details accepted")
    with st.spinner("Calculating..."):
        time.sleep(1)
        new_cwa=calculate_cwa(st.session_state.p_cwa, st.session_state.c_credits, st.session_state.course_details)
    st.subheader(f"New CWA:  {round(new_cwa, 2)}")







