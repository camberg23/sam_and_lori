import streamlit as st
from messages import *
from functions import *

from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate 
from langchain.chains import LLMChain

st.title("Sam & Lori Intake Form")

# Initialize session state variables if they don't exist
if 'page' not in st.session_state:
    st.session_state.page = 1

if 'responses' not in st.session_state:
    st.session_state.responses = [None]*30

if 'personal_info' not in st.session_state:
    st.session_state.personal_info = {"first_name": "", "last_name": "", "email": ""}

if 'if_not_money' not in st.session_state:
    st.session_state.if_not_money = ""

if 'get_paid_for' not in st.session_state:
    st.session_state.get_paid_for = ""

if 'world_need' not in st.session_state:
    st.session_state.world_need = ""

if 'want_from_job' not in st.session_state:
    st.session_state.want_from_job = ""


# Progress bar
total_pages = 5
progress_bar_value = (min(st.session_state.page, total_pages)) / total_pages
st.progress(progress_bar_value)

# Navigation functions
def go_next():
    st.session_state.page += 1
    st.rerun()

def go_back():
    if st.session_state.page > 1:
        st.session_state.page -= 1
        st.rerun()

def get_insights():
    chat_model = ChatOpenAI(openai_api_key=st.secrets['API_KEY'], model_name='gpt-4-1106-preview', temperature=0.2)
    chat_chain = LLMChain(prompt=PromptTemplate.from_template(get_insights_prompt), llm=chat_model)
    generated_output = chat_chain.run(
                                    personal_info=st.session_state.personal_info,
                                    domain_scores=st.session_state.domain_scores,
                                    facet_scores=st.session_state.facet_scores,
                                    selected_values=st.session_state.selected_values,
                                    if_no_money=st.session_state.if_not_money,
                                    get_paid_for=st.session_state.get_paid_for,
                                    word_need=st.session_state.world_need,
                                    want_from_job=st.session_state.want_from_job,
                                    soft_skills=st.session_state.soft_skills,
                                    hard_skills=st.session_state.hard_skills,
                                    salary_low=st.session_state.salary_low,
                                    salary_high=st.session_state.salary_high,
                                    preferred_geography=st.session_state.preferred_geography,
                                    current_location=st.session_state.current_location,
                                    willing_to_move=st.session_state.willing_to_move,
                                    dream_job=st.session_state.dream_job,
                                    do_more=st.session_state.do_more)
    return generated_output

def get_recommendations():
    chat_model = ChatOpenAI(openai_api_key=st.secrets['API_KEY'], model_name='gpt-4-1106-preview', temperature=0.2)
    chat_chain = LLMChain(prompt=PromptTemplate.from_template(get_recommendations_prompt), llm=chat_model)
    recs = chat_chain.run(insights=st.session_state.insights)
    return recs

# Page 1: Basic Information
if st.session_state.page == 1:
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    
    # Replace these with your SendGrid username and password
    sendgrid_username = 'apikey'
    sendgrid_password = st.secrets['SENDGRID']
    
    # Sender and recipient
    from_email = 'cam.h.berg@gmail.com'  # Replace with your sender email
    to_email = 'cam.h.berg@gmail.com'  # Replace with the recipient email
    
    # Email subject and body
    subject = 'Hello from SendGrid'
    body = 'This is a test email sent via SendGrid SMTP relay.'
    
    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = from_email
    message['To'] = to_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))
    
    # Create SMTP session for sending the mail
    try:
        server = smtplib.SMTP('smtp.sendgrid.net', 465)  # Use 465 for SSL
        server.starttls()  # Secure the connection
        server.login(sendgrid_username, sendgrid_password)
        text = message.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        st.write("Email sent successfully!")
    except Exception as e:
        st.write(f"Failed to send email: {e}")
        
    st.subheader("Basic Information")
    st.write("Please fill in your basic information below:")  # Placeholder for more specific instructions

    # Placeholder for error messages
    error_placeholder = st.empty()

    # Organize first name and last name inputs into two columns on the same row
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.personal_info['first_name'] = st.text_input("First Name", value=st.session_state.personal_info['first_name'], key="first_name")
    with col2:
        st.session_state.personal_info['last_name'] = st.text_input("Last Name", value=st.session_state.personal_info['last_name'], key="last_name")

    st.session_state.personal_info['email'] = st.text_input("Email", value=st.session_state.personal_info['email'], key="email")

    # Right-justify the "Next" button using columns
    col1, col2 = st.columns([6,1])
    with col2:
        next_pressed = st.button("Next")

    # Show error messages in the placeholder outside of columns
    if next_pressed:
        if not st.session_state.personal_info['first_name'] or not st.session_state.personal_info['last_name']:
            error_placeholder.error("Please enter both your first and last name.")
        elif "@" not in st.session_state.personal_info['email'] or "." not in st.session_state.personal_info['email']:  # Simple check, consider more comprehensive validation
            error_placeholder.error("Please enter a valid email address.")
        else:
            go_next()


# Page 2: Personality Test
elif st.session_state.page == 2:
    st.write("To begin, please indicate the extent to which you agree with the following descriptions. The more accurately you answer, the better the quality of this tool's output!")
    st.subheader("I am someone who...")
    col1, col2 = st.columns(2)
    for i, question in enumerate(questions, start=1):
        with col1 if i <= len(questions)/2 else col2:
            st.session_state.responses[i-1] = st.selectbox(f"{i}. {question}", options=list(response_options.keys()), index=None, format_func=lambda x: response_options[x], key=f"Q{i}")

    error_placeholder = st.empty()
    col1, col2, col3 = st.columns([1,5,1])
    with col1:
        if st.button("Go Back", key=f'back_{st.session_state.page}'):
            go_back()
    with col3:
        if st.button("Next", key=f'next_{st.session_state.page}'):
            if None not in st.session_state.responses:
                st.session_state.domain_scores, st.session_state.facet_scores = calculate_scores(st.session_state.responses)
                go_next()
            else:
                with error_placeholder:
                    st.error("Please answer all questions.")
    

# Page 3: Open-Ended 1
elif st.session_state.page == 3:
    st.subheader("About Yourself")
    
    # Placeholder for error messages
    error_placeholder = st.empty()
    
    values_options = [
        "Innovation", "Leadership", "Community", "Lifelong Learning", "Responsibility",
        "Critical Thinking", "Wealth", "Excellence", "Diversity", "Teamwork", "Cooperation",
        "Gratitude", "Justice", "Work-Life Balance", "Intellectual Curiosity", "Accountability",
        "Flexibility", "Reliability", "Financial Responsibility", "Security", "Compassion",
        "Respect", "Trust", "Courage", "Efficiency", "Growth", "Transparency", "Strategic Thinking",
        "Equality", "Perseverance", "Independence", "Ethical Awareness", "Adaptability", "Humility",
        "Optimism", "Time Management", "Conflict Resolution", "Contribution to Society", "Inclusivity",
        "Integrity", "Mindfulness", "Creativity"
    ]
    
    # Multiselect for values
    if 'selected_values' not in st.session_state:
        st.session_state.selected_values = []

    st.session_state.selected_values = st.multiselect("What do you value most? (Choose up to seven values)", options=values_options, default=None, key="values_multiselect", max_selections=7)
    
    # Open-ended questions
    st.session_state.if_not_money = st.text_area("If money were no object, how would you spend your day-to-day life?", value=st.session_state.if_not_money, max_chars=1500)
    st.session_state.get_paid_for = st.text_area("What can you get paid for?", value=st.session_state.get_paid_for, max_chars=1500)
    st.session_state.world_need = st.text_area("What does the world need?", value=st.session_state.world_need, max_chars=1500)  # Assuming a new session_state variable
    st.session_state.want_from_job = st.text_area("What do you want from a job?", value=st.session_state.want_from_job, max_chars=1500)  # Assuming a new session_state variable

    col1, col2, col3 = st.columns([1,5,1])
    with col1:
        if st.button("Go Back", key=f'back_{st.session_state.page}'):
            go_back()

    # Validation and navigation
    if col3.button("Next", key=f'next_{st.session_state.page}'):
        # Check multiselect and open-ended responses
        if not st.session_state.selected_values:
            error_placeholder.error("Please select at least one thing you most value.")
        elif not st.session_state.if_not_money.strip():
            error_placeholder.error("Please fill in how you would spend your day-to-day life if money were no object.")
        elif not st.session_state.get_paid_for.strip():
            error_placeholder.error("Please fill in what you can get paid for.")
        elif not st.session_state.world_need.strip():
            error_placeholder.error("Please fill in what you think the world needs.")
        elif not st.session_state.want_from_job.strip():
            error_placeholder.error("Please fill in what you want from a job.")
        else:
            go_next()



# Page 4: Open-Ended 2
elif st.session_state.page == 4:
    # Initialize lists in session state if not present
    if 'hard_skills' not in st.session_state:
        st.session_state.hard_skills = [{'skill': '', 'example': ''}]
    if 'soft_skills' not in st.session_state:
        st.session_state.soft_skills = [{'skill': '', 'example': ''}]

    # Soft Skills Section
    st.subheader("Soft skills")
    soft_error_placeholder = st.empty()
    with st.expander("See examples of soft skills"):
        st.write(soft_skills)  # Fill in with more detailed examples as needed
    for i, skill in enumerate(st.session_state.soft_skills):
        col1, col2 = st.columns([1,3])
        with col1:
            st.session_state.soft_skills[i]['skill'] = st.text_input(f"Soft Skill Name {i+1}", value=skill['skill'], key=f"soft_skill_{i}")
        with col2:
            st.session_state.soft_skills[i]['example'] = st.text_input(f"Concrete examples of Soft Skill {i+1}", value=skill['example'], key=f"soft_example_{i}")
    if st.button("Add another soft skill"):
        st.session_state.soft_skills.append({'skill': '', 'example': ''})
        st.rerun()

    # Hard Skills Section
    st.subheader("Hard skills")
    hard_error_placeholder = st.empty()
    with st.expander("See examples of hard skills"):
        st.write(hard_skills)  # Fill in with more detailed examples as needed
    for i, skill in enumerate(st.session_state.hard_skills):
        col1, col2 = st.columns([1,3])
        with col1:
            st.session_state.hard_skills[i]['skill'] = st.text_input(f"Hard Skill Name {i+1}", value=skill['skill'], key=f"hard_skill_{i}")
        with col2:
            st.session_state.hard_skills[i]['example'] = st.text_input(f"Concrete examples of Hard Skill {i+1}", value=skill['example'], key=f"hard_example_{i}")
    if st.button("Add another hard skill"):
        st.session_state.hard_skills.append({'skill': '', 'example': ''})
        st.rerun()

    # Navigation buttons
    col1, col2, col3 = st.columns([1,5,1])
    with col1:
        if st.button("Go Back", key='back_page_4'):
            go_back()
    with col3:
        if st.button("Next", key='next_page_4'):
            # Validation for at least one hard skill and one soft skill
            valid_submission = True
            if not any(skill['skill'] for skill in st.session_state.soft_skills):
                soft_error_placeholder.error("Please input at least one soft skill.")
                valid_submission = False
            if not any(skill['skill'] for skill in st.session_state.hard_skills):
                hard_error_placeholder.error("Please input at least one hard skill.")
                valid_submission = False
            
            if valid_submission:
                go_next()

elif st.session_state.page == 5:
    st.subheader("Final Details")

    # Placeholder for error messages
    error_placeholder = st.empty()

    # Salary Range
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.salary_low = st.number_input("Salary range - Low end ($)", min_value=0, value=st.session_state.get('salary_low', 0), format="%d")
    with col2:
        st.session_state.salary_high = st.number_input("Salary range - High end ($)", min_value=0, value=st.session_state.get('salary_high', 0), format="%d")

    # Preferred Geography
    geography_options = ["Urban", "Suburban", "Rural", "Remote work", "West Coast", "East Coast", "Abroad"]
    st.session_state.preferred_geography = st.multiselect("Preferred Geography", options=geography_options)

    # Current Location
    st.session_state.current_location = st.text_input("Where are you located currently?", value=st.session_state.get('current_location', ''))

    # Willingness to Move
    move_options = ["Yes", "No", "Maybe"]
    st.session_state.willing_to_move = st.radio("Would you consider moving for a new job?", options=move_options, index=0)

    # Open-ended Questions
    st.session_state.dream_job = st.text_area("What's your dream job?", value=st.session_state.get('dream_job', ''), max_chars=1500)
    st.session_state.do_more = st.text_area("What would you like to do more of that you don't get to do in your current job?", value=st.session_state.get('do_more', ''), max_chars=1500)

    spinner_placeholder = st.empty()
    # Navigation buttons
    col1, col2, col3 = st.columns([1,5,1])
    with col1:
        if st.button("Go Back", key='back_page_5'):
            go_back()
    
    with col3:
        if st.button("**Finish**", key='next_page_5'):
            # Validation checks
            if st.session_state.salary_low >= st.session_state.salary_high:
                error_placeholder.error("Please ensure the low end of the salary range is less than the high end.")
            elif not st.session_state.preferred_geography:
                error_placeholder.error("Please select a preferred geography.")
            elif not st.session_state.current_location.strip():
                error_placeholder.error("Please enter your current location.")
            elif not st.session_state.dream_job.strip() or not st.session_state.do_more.strip():
                error_placeholder.error("Please fill in both open-ended questions.")
            else:
                with spinner_placeholder:
                    with st.spinner('Processing your responses, this will take approximately one minute. Please sit tight...'):
                        st.session_state.insights = get_insights()
                        st.session_state.recommendations = get_recommendations()
                        go_next()

elif st.session_state.page == 6:
    st.balloons()
    with st.expander("**Comprehensive synthesis from responses**"):
        st.write(st.session_state.insights)
    with st.expander("**Concrete job search recommendations**"):
        st.write(st.session_state.recommendations)
