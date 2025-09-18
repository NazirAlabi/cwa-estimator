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
    if 'new_cwa_details' not in st.session_state:
        st.session_state.new_cwa_details=[0.0, 0, 0] 
    st.session_state.course_details = []

def calculate_cwa(previous_cwa: float, credits_finished: int, course_details_list: list):
    previous_sum_total=previous_cwa*float(credits_finished)
    sum_total_increment=0.0
    credits_complete_increment=0.0
    for course_details in course_details_list:
        sum_total_increment+=float(course_details.score*course_details.credits)
        credits_complete_increment+=float(course_details.credits)
    new_cwa=(previous_sum_total+sum_total_increment)/(credits_finished+credits_complete_increment)

    return [new_cwa, sum_total_increment, credits_complete_increment]

def total_credits(course_details):
    total=0
    if course_details:
        for course in course_details:
            total+=course.credits
    return total

def calculate_averages(course_details, value):
    weighted_average=0.0
    unweighted_average=0.0
    total=0.0
    if value is True:
        credits=0.0
        for course in course_details:
            total+=float(course.score*course.credits)
            credits+=float(course.credits)
        weighted_average=total/credits
        return weighted_average
    elif value is False:
        for course in course_details:
            total+=float(course.score)
        unweighted_average=total/float(len(course_details))
        return unweighted_average
    elif value is None:
        credits=0.0
        for course in course_details:
            total+=float(course.score*course.credits)
            credits+=float(course.credits)
        weighted_average=total/credits
        for course in course_details:
            total+=float(course.score)
        unweighted_average=total/float(len(course_details))
        return (weighted_average,unweighted_average)




