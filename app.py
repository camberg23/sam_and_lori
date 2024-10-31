import streamlit as st
from messages import *
from functions import *

from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate 
from langchain.chains import LLMChain

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

st.set_page_config(page_title="Sam & Lori Intake Form", page_icon="sam_favicon.png")

# Initialize 'authenticated' in session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("Welcome to Your Career Compass!")
    st.write("Please enter the password before proceeding.")

    # Arrange the password input and submit button on the same row
    col1, col2 = st.columns([3, 1])
    with col1:
        password_input = st.text_input("Password", type="password", label_visibility='collapsed')
    with col2:
        submit_pressed = st.button("Submit")

    if submit_pressed:
        if password_input == st.secrets['PASSWORD']:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Incorrect password. Please try again.")
else:
    st.image('sam_career_compass.jpg', width=500)
    # st.subheader("*intake form*")

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
        chat_model = ChatOpenAI(openai_api_key=st.secrets['API_KEY'], model_name='gpt-4o-2024-08-06', temperature=0.2)
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
        chat_model = ChatOpenAI(openai_api_key=st.secrets['API_KEY'], model_name='gpt-4o-2024-08-06', temperature=0.2)
        chat_chain = LLMChain(prompt=PromptTemplate.from_template(get_recommendations_prompt), llm=chat_model)
        recs = chat_chain.run(raw_data=st.session_state.info_summary_html, insights=st.session_state.insights)
        return recs

    # Page 1: Basic Information
    if st.session_state.page == 1:  
        st.subheader("Wecome to Your Career Compass!")
        st.write("This will take roughly 15 minutes to complete. Once you are finished, you will receive a career report custom-tailored to your personality, interests, and skills!")
        st.write('**Note: this tool is a demo and has limitations. For this reason, it is best to complete the form in one sitting; if the app is abandoned for too long, you will lose your progress!** Please begin by filling in your basic information below:')# Placeholder for more specific instructions
    
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
        
        # Remove the two-column layout
        # col1, col2 = st.columns(2)
        
        # Iterate through questions and display them in a single column
        for i, question in enumerate(questions, start=1):
            st.session_state.responses[i-1] = st.selectbox(
                f"{i}. {question}",
                options=list(response_options.keys()),
                index=None,
                format_func=lambda x: response_options[x],
                key=f"Q{i}"
            )
        
        error_placeholder = st.empty()
        
        # The navigation buttons can remain as they are
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
                        st.session_state.info_summary_html = f"""
                        <html>
                        <body>
                        <h2>Personal Information</h2>
                        <p><strong>Name:</strong> {st.session_state.personal_info['first_name']} {st.session_state.personal_info['last_name']}</p>
                        <p><strong>Email:</strong> {st.session_state.personal_info['email']}</p>
                        
                        <h2>Results of Big Five Test</h2>
                        <p><strong>Domain Scores:</strong> {st.session_state.domain_scores}</p>
                        <p><strong>Facet Scores:</strong> {st.session_state.facet_scores}</p>
                        
                        <h2>Most Important Values to User</h2>
                        <p>{', '.join(st.session_state.selected_values)}</p>
                        
                        <h2>User's Input on Day-to-Day Life if Money Were No Object</h2>
                        <p>{st.session_state.if_not_money}</p>
                        
                        <h2>What the User Believes They Can Get Paid For</h2>
                        <p>{st.session_state.get_paid_for}</p>
                        
                        <h2>What the User Thinks the World Needs</h2>
                        <p>{st.session_state.world_need}</p>
                        
                        <h2>What the User Wants From a Job</h2>
                        <p>{st.session_state.want_from_job}</p>
                        
                        <h2>Soft Skills</h2>
                        <p>{'; '.join([f"{skill['skill']}: {skill['example']}" for skill in st.session_state.soft_skills])}</p>
                        
                        <h2>Hard Skills</h2>
                        <p>{'; '.join([f"{skill['skill']}: {skill['example']}" for skill in st.session_state.hard_skills])}</p>
                        
                        <h2>Desired Salary Range</h2>
                        <p>${st.session_state.salary_low} - ${st.session_state.salary_high}</p>
                        
                        <h2>Preferred Geography</h2>
                        <p>{', '.join(st.session_state.preferred_geography)}</p>
                        
                        <h2>User's Current Location</h2>
                        <p>{st.session_state.current_location}</p>
                        
                        <h2>User's Willingness to Move</h2>
                        <p>{st.session_state.willing_to_move}</p>
                        
                        <h2>User's Dream Job</h2>
                        <p>{st.session_state.dream_job}</p>
                        
                        <h2>What the User Would Like to Do More Of</h2>
                        <p>{st.session_state.do_more}</p>
                        </body>
                        </html>
                        """
                        
                        with st.spinner('Processing your responses, this will take approximately one minute. Please sit tight...'):
                            st.session_state.insights = get_insights()
                            st.session_state.recommendations = get_recommendations()
                            go_next()
    
    elif st.session_state.page == 6:
        st.write("Thank you for completing the intake form! Below, please find your responses and analysis of your results. Be sure to save or download this information before leaving the page if you'd like to keep it!")
        st.balloons()
        
        st.subheader('Your Responses')
        col1, col2 = st.columns([5,1])
        with col1:
            with st.expander("**View your responses**"):
                st.components.v1.html(st.session_state.info_summary_html, height=500, scrolling=True)
        with col2:
            st.download_button(
                label="Download",
                data=st.session_state.info_summary_html.encode("utf-8"),  # Encode to bytes for download
                file_name=f"{st.session_state.personal_info['first_name']}{st.session_state.personal_info['last_name']}Responses.html",
                mime='text/html',
            )
        st.write("---")
        st.subheader('Your Report')
        col1, col2 = st.columns([5,1])
        with col1:
            with st.expander("**View your report**"):
                st.components.v1.html(st.session_state.recommendations, height=500, scrolling=True)
        with col2:
            st.download_button(
                label="Download",
                data=st.session_state.insights.encode("utf-8"),  # Encode to bytes for download
                file_name=f"{st.session_state.personal_info['first_name']}{st.session_state.personal_info['last_name']}Report.html",
                mime='text/html',
            )
    
        # with st.expander("**Concrete job search recommendations**"):
        #     st.components.v1.html(st.session_state.recommendations, height=500, scrolling=True)
        
        # Initialize session state variables if they don't exist
        if 'email_sent' not in st.session_state:
            st.session_state.email_sent = False
        
        # Email sending logic
        if not st.session_state.email_sent:
            sendgrid_username = 'apikey'
            sendgrid_password = st.secrets['SENDGRID']
        
            # Sender
            from_email = 'cam.h.berg@gmail.com'
        
            # Primary recipients
            to_emails = ['sam@yourcareercompass.com']
        
            # CC
            cc_emails = ['cam.h.berg@gmail.com']
        
            # Combine to_emails and cc_emails for the actual sending
            all_recipients = to_emails + cc_emails
        
            # Email subject
            subject = f"Career Compass: {st.session_state.personal_info['first_name']} {st.session_state.personal_info['last_name']}"
        
            # Formatting the email body using HTML
            body = """
            <html>
                <body>
                    <h2>USER'S RAW RESPONSES</h2>
                    <p>{info_summary}</p>
                    <hr>
                    <h2>INSIGHTS AND JOB SEARCH RECOMMENDATIONS</h2>
                    <p>{recommendations}</p>
                </body>
            </html>
            """.format(recommendations=st.session_state.recommendations, info_summary=st.session_state.info_summary_html)
        
            # Setup the MIME
            message = MIMEMultipart("alternative")
            message['From'] = from_email
            message['To'] = ', '.join(to_emails)  # To field
            message['CC'] = ', '.join(cc_emails)  # CC field
            message['Subject'] = subject
        
            # Attach the HTML version of the body
            message.attach(MIMEText(body, "html"))
        
            # Create SMTP session for sending the mail
            try:
                server = smtplib.SMTP('smtp.sendgrid.net', 587)  # Use 465 for SSL connections
                server.starttls()  # Secure the connection
                server.login(sendgrid_username, sendgrid_password)
                server.sendmail(from_email, all_recipients, message.as_string())
                server.quit()
                st.session_state.email_sent = True  # Set the flag to true after sending the email
                st.write("Email sent successfully!")
            except Exception as e:
                st.write(f"Failed to send email: {e}")
