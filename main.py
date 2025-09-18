import streamlit as st
import altair as alt
import pandas as pd
import time 
from classes import*
from func import*

# Set up Streamlit page configuration
st.set_page_config("🧮CWA Calculator", layout='wide')

# Display the main header
st.header("🧮CWA Calculator", divider="blue")

# Initialize session state and variables
initialize()

# Layout for user input: previous CWA, credits completed, number of courses
col1, col2, col3=st.columns([3,1,2])
with col1:
    # Slider for previous CWA input
    p_cwa=st.slider("#### Previous CWA", min_value=10.00, max_value=100.00, step=0.01, value=70.00, help="Enter your last reported cwa")
    st.caption("Enter your last reported cwa")
with col2:
    # Number input for credits completed
    credits_completed=st.number_input("#### Credits Completed: ", min_value=1, max_value=100, step=1, value=18)
    st.caption("Enter the credits completed at the time the last CWA was reported")
with col3:
    # Slider for number of courses taken
    course_no=st.slider("#### Number of courses", width=400, min_value=1, max_value=15, value=6, help="Enter the number of courses taken last semester")
    st.caption("Enter the number of courses taken last semester")    

# Store user inputs in session state
st.session_state.p_cwa=p_cwa
st.session_state.course_no=course_no
st.session_state.c_credits=credits_completed

st.divider()
# Calculate batch size for course input columns
if st.session_state.course_no%2==0:
    batch=st.session_state.course_no/2
elif st.session_state.course_no%2==1:
    batch=(st.session_state.course_no+1)/2

batch=int(batch)

# Input fields for each course (split into two columns)
courses_col1, courses_col2=st.columns([1,1])
with courses_col1:
    for courses in range(0,batch):
        # Input for course name, score estimate, and credits
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
        # Input for course name, score estimate, and credits (second column)
        course_name=st.text_input("Course name", width=200, key=f"{courses} name" ,help="The course name entered is purely for identification by the user and does not have to be the real course name")
        st.caption("Does not have to be the real course name")
        subcol1, subcol2=st.columns([2,1])
        with subcol1:
            score_estimate=st.slider("Estimate your score in the last exam", value=70, key=f"{courses} score")
        with subcol2:
            credits=st.number_input("Number of credit hours", min_value=1, max_value=7, step=1, key=f"{courses} credits")
        st.session_state.course_details.append(Course(course_name, score_estimate, credits))
        st.write("---")

# Button to trigger CWA calculation
if st.button("Calculate CWA", width=400):
    with st.spinner("Checking requirements..."):
        time.sleep(1)
        if not all_inputs_empty(st.session_state.course_details):
            confirm=st.success("Details accepted", width=400)
            with st.spinner("Calculating..."):
                time.sleep(1)
                # Calculate and store new CWA details in session state
                st.session_state.new_cwa_details=calculate_cwa(st.session_state.p_cwa, st.session_state.c_credits, st.session_state.course_details)
                confirm.empty()
        else:
            warn=st.error("Insufficient Details", width=400)
            time.sleep(2)
            warn.empty()

st.write("---")
# Display new CWA if calculated
if st.session_state.new_cwa_details[0]!=0:
    st.subheader(f"New CWA:  {st.session_state.new_cwa_details[0]:.2f}", )
    if not all_inputs_empty(st.session_state.course_details):
        with st.expander("Semester info", width=400):
            # Show semester averages and credits summary
            st.write(f"##### Semester Weighted Average: {calculate_averages(st.session_state.course_details, True):.2f}")
            st.write(f"##### Semester Unweighted Avrage: {calculate_averages(st.session_state.course_details, False):.2f}")
            st.caption(f"{total_credits(st.session_state.course_details)} credits accross {st.session_state.course_no} courses")

# Option to display graphs if course details are available
if not all_inputs_empty(st.session_state.course_details):
    if st.checkbox("Graph Information"):
            div1, div2= st.columns([1,1])
            with div1:
                # Prepare course names for display
                raw_names = [course.name.strip() if course.name else "" 
                            for course in st.session_state.course_details]

                # If all names are blank, auto-number them
                if all(name == "" for name in raw_names):
                    display_names = [f"Course {i+1}" for i in range(len(raw_names))]
                else:
                    display_names = raw_names   # keep them exactly as typed (blanks stay blank)
                    
                # Create DataFrame for course credits
                df = pd.DataFrame({
                "Course": display_names,
                "Credits": [course.credits for course in st.session_state.course_details]
                })
                st.write("##### 📊 Course Influence on CWA (by Credits)")

                # Bar chart for course credits
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

# Debugging code
# with st.expander("Debugging Info "):
#     courses={}
#     a=0
#     for course in st.session_state.course_details:
#         a+=1
#         courses[f'Course {a}']=[("Name", course.name), ("Score", course.score), ("Credits", course.credits)]
#     st.write(courses)