import streamlit as st
import random
import copy

# Define the questionnaire
questions = [
    "Tends to be quiet.",                              # Q1 [Reverse]
    "Is compassionate, has a soft heart.",            # Q2
    "Tends to be disorganized.",                      # Q3 [Reverse]
    "Worries a lot.",                                  # Q4
    "Is fascinated by art, music, or literature.",     # Q5
    "Is dominant, acts as a leader.",                 # Q6
    "Is sometimes rude to others.",                    # Q7 [Reverse]
    "Has difficulty getting started on tasks.",        # Q8 [Reverse]
    "Tends to feel down, blue.",                       # Q9
    "Has little interest in abstract ideas.",          # Q10 [Reverse]
    "Is full of energy.",                              # Q11
    "Assumes the best about people.",                  # Q12
    "Is reliable, can always be counted on.",          # Q13 [Reverse]
    "Is emotionally stable, not easily upset.",        # Q14 [Reverse]
    "Is original, comes up with new ideas.",            # Q15
    "Is outgoing, sociable.",                          # Q16
    "Can be cold and uncaring.",                       # Q17 [Reverse]
    "Keeps things neat and tidy.",                     # Q18 [Reverse]
    "Is relaxed, handles stress well.",                # Q19 [Reverse]
    "Has few artistic interests.",                     # Q20 [Reverse]
    "Prefers to have others take charge.",             # Q21 [Reverse]
    "Is respectful, treats others with respect.",       # Q22
    "Is persistent, works until the task is finished.",# Q23 [Reverse]
    "Feels secure, comfortable with self.",            # Q24 [Reverse]
    "Is complex, a deep thinker.",                      # Q25
    "Is less active than other people.",               # Q26 [Reverse]
    "Tends to find fault with others.",                # Q27 [Reverse]
    "Can be somewhat careless.",                       # Q28 [Reverse]
    "Is temperamental, gets emotional easily.",        # Q29 [Reverse]
    "Has little creativity."                           # Q30 [Reverse]
]

# Response options
response_options = {
    1: "Strongly Disagree",
    2: "Disagree",
    3: "Neutral",
    4: "Agree",
    5: "Strongly Agree"
}

# Initialize session state
if 'responses' not in st.session_state:
    st.session_state.responses = [None] * len(questions)

if 'page' not in st.session_state:
    st.session_state.page = 2  # Starting at page 2 for this example

# Shuffle questions once per session
if 'shuffled_questions' not in st.session_state:
    st.session_state.shuffled_questions = questions.copy()
    random.shuffle(st.session_state.shuffled_questions)

# Define navigation functions (placeholders)
def go_back():
    st.session_state.page -= 1

def go_next():
    st.session_state.page += 1

# Revised calculate_scores function
REVERSE_KEYED = [1, 3, 7, 8, 10, 14, 17, 19, 20, 21, 24, 26, 27, 28, 30]

def calculate_scores(responses):
    # Validate responses
    for idx, score in enumerate(responses, start=1):
        if score not in [1, 2, 3, 4, 5]:
            raise ValueError(f"Invalid response for question {idx}: {score}. Must be between 1 and 5.")
    
    # Create a deep copy to avoid modifying the original responses
    processed_responses = copy.deepcopy(responses)
    
    # Reverse scoring: invert responses for reverse-keyed questions
    for i in REVERSE_KEYED:
        processed_responses[i-1] = (5 + 1) - processed_responses[i-1]
    
    # Adjust scores to start at 0
    adjusted_responses = [score - 1 for score in processed_responses]
    
    # Define domain and facet mappings
    domain_mapping = {
        "Extraversion": [1, 6, 11, 16, 21, 26],
        "Agreeableness": [2, 7, 12, 17, 22, 27],
        "Conscientiousness": [3, 8, 13, 18, 23, 28],
        "Negative Emotionality": [4, 9, 14, 19, 24, 29],
        "Open-Mindedness": [5, 10, 15, 20, 25, 30]
    }
    
    facet_mapping = {
        "Sociability": [1, 16],
        "Assertiveness": [6, 21],
        "Energy Level": [11, 26],
        "Compassion": [2, 17],
        "Respectfulness": [7, 22],
        "Trust": [12, 27],
        "Organization": [3, 18],
        "Productiveness": [8, 23],
        "Responsibility": [13, 28],
        "Anxiety": [4, 19],
        "Depression": [9, 24],
        "Emotional Volatility": [14, 29],
        "Aesthetic Sensitivity": [5, 20],
        "Intellectual Curiosity": [10, 25],
        "Creative Imagination": [15, 30]
    }
    
    # Calculate domain scores as a percentage
    domain_scores = {}
    for domain, qs in domain_mapping.items():
        domain_sum = sum([adjusted_responses[i-1] for i in qs])
        domain_scores[domain] = round((domain_sum / (len(qs) * 4)) * 100, 3)  # 4 = MAX_RESPONSE - MIN_RESPONSE
    
    # Calculate facet scores as a percentage
    facet_scores = {}
    for facet, qs in facet_mapping.items():
        facet_sum = sum([adjusted_responses[i-1] for i in qs])
        facet_scores[facet] = round((facet_sum / (len(qs) * 4)) * 100, 3)
    
    return domain_scores, facet_scores

# Page 2: Personality Test (Single Column Layout)
elif st.session_state.page == 2:
    st.write("To begin, please indicate the extent to which you agree with the following descriptions. The more accurately you answer, the better the quality of this tool's output!")
    st.subheader("I am someone who...")
    
    # Display all questions in a single column
    for i, question in enumerate(questions, start=1):
        st.session_state.responses[i-1] = st.selectbox(
            f"{i}. {question}",
            options=list(response_options.keys()),
            index=None,
            format_func=lambda x: response_options[x],
            key=f"Q{i}"
        )
    
    error_placeholder = st.empty()
    
    # Navigation buttons
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
