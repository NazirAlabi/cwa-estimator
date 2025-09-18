import streamlit as st

# Initialize
def initialize():
    if 'p_cwa' not in st.session_state:
        st.session_state.p_cwa=0
    if 'c_credits' not in st.session_state:
        st.session_state.c_credits=0
    if 'course_no' not in st.session_state:
        st.session_state.course_no=0
    if 'course_details' not in st.session_state:
        st.session_state.course_details=[]
    if 'new_cwa' not in st.session_state:
        st.session_state.new_cwa= 0
    st.session_state.course_details = []

def calculate_cwa(previous_cwa: float, credits_finished: int, course_details_list: list):
    previous_sum_total=previous_cwa*float(credits_finished)
    sum_total_increment=0.0
    credits_complete_increment=0.0
    for course_details in course_details_list:
        sum_total_increment+=float(course_details.score*course_details.credits)
        credits_complete_increment+=float(course_details.credits)
    new_cwa=(previous_sum_total+sum_total_increment)/(credits_finished+credits_complete_increment)

    return (new_cwa, sum_total_increment, credits_complete_increment)

def all_inputs_filled():
    # check top-level inputs
    if "p_cwa" not in st.session_state or "c_credits" not in st.session_state or "course_no" not in st.session_state:
        return False

    if st.session_state.p_cwa is None or st.session_state.c_credits is None:
        return False

    # check course details
    if not st.session_state.course_details:
        return False

    for course in st.session_state.course_details:
        if not course.credits is None or course.score is None:
            return False 
    return True
