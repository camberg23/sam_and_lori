import streamlit as st

# Define the questionnaire
questions = [
    "Tends to be quiet.",
    "Is compassionate, has a soft heart.",
    "Tends to be disorganized.",
    "Worries a lot.",
    "Is fascinated by art, music, or literature.",
    "Is dominant, acts as a leader.",
    "Is sometimes rude to others.",
    "Has difficulty getting started on tasks.",
    "Tends to feel down, blue.",
    "Has little interest in abstract ideas.",
    "Is full of energy.",
    "Assumes the best about people.",
    "Is reliable, can always be counted on.",
    "Is emotionally stable, not easily upset.",
    "Is original, comes up with new ideas.",
    "Is outgoing, sociable.",
    "Can be cold and uncaring.",
    "Keeps things neat and tidy.",
    "Is relaxed, handles stress well.",
    "Has few artistic interests.",
    "Prefers to have others take charge.",
    "Is respectful, treats others with respect.",
    "Is persistent, works until the task is finished.",
    "Feels secure, comfortable with self.",
    "Is complex, a deep thinker.",
    "Is less active than other people.",
    "Tends to find fault with others.",
    "Can be somewhat careless.",
    "Is temperamental, gets emotional easily.",
    "Has little creativity."
]

# Define response options
response_options = {1: "Disagree strongly", 2: "Disagree a little", 3: "Neutral; no opinion", 4: "Agree a little", 5: "Agree strongly"}

soft_skills = """
1. **Communication:** Ability to convey information clearly and effectively in both written and verbal forms.
2. **Leadership:** Capacity to inspire, motivate, and guide others towards achieving goals.
3. **Teamwork:** Ability to work effectively within a group, respecting and valuing contributions from all members.
4. **Problem-Solving:** Capacity to identify issues, analyze problems, and come up with effective solutions.
5. **Adaptability:** Ability to adjust to new conditions and handle unforeseen challenges.
6. **Emotional Intelligence:** Understanding and managing your emotions, as well as recognizing and influencing the emotions of others.
7. **Creativity:** Capacity to think outside the box and generate innovative ideas.
8. **Time Management:** Skills in managing one's time effectively to complete tasks and meet deadlines.
9. **Conflict Resolution:** Ability to address disagreements and mediate between conflicting parties to achieve a resolution.
10. **Critical Thinking:** Capacity to analyze facts, logic, and reasoning to form a judgment or conclusion.
11. **Work Ethic:** Commitment to professionalism, responsibility, and reliability in completing job duties.
12. **Attention to Detail:** Ability to perform tasks with thoroughness and accuracy.
13. **Resilience:** Capacity to recover quickly from difficulties and setbacks.
14. **Interpersonal Skills:** Ability to establish and maintain positive relationships with colleagues and clients.
15. **Customer Service:** Skills in understanding and meeting the needs of customers, including patience, empathy, and communication.
"""

hard_skills = """
1. **Technical Proficiency:** Knowledge of specific software, tools, or programming languages (e.g., proficiency in Python, Excel, Adobe Creative Suite).
2. **Data Analysis:** Ability to collect, process, and analyze data to inform decisions (e.g., using SQL, R, or data visualization tools).
3. **Project Management:** Skills in organizing, planning, and executing projects from inception to completion, often using tools like Asana, Trello, or Microsoft Project.
4. **Digital Marketing:** Knowledge of SEO, SEM, content marketing, social media marketing, and email marketing practices.
5. **Foreign Languages:** Ability to speak, read, or write in additional languages.
6. **Financial Literacy:** Understanding of financial reports, budgeting, and financial forecasting.
7. **Legal Compliance:** Knowledge of relevant laws and regulations in a specific industry.
8. **Technical Writing:** Ability to produce clear and concise manuals, reports, and documentation.
9. **Cybersecurity:** Skills in protecting systems, networks, and programs from digital attacks.
10. **Engineering and Technical Design:** Proficiency in CAD software, engineering principles, or architectural design.
11. **Healthcare Skills:** Clinical competencies, diagnostic skills, patient care, and understanding of medical protocols.
12. **Sales and Negotiation:** Skills in persuasion, negotiation, and closing deals.
13. **Supply Chain Management:** Knowledge of procurement, logistics, inventory management, and supply chain coordination.
14. **Teaching and Curriculum Design:** Ability to educate others, develop educational materials, and assess learning outcomes.
15. **Graphic Design:** Skills in visual communication, using software like Adobe Illustrator or Photoshop.
"""

get_insights_prompt = """
Your job is to generate a comprehensive report and synthesis of a large collection of information that a user inputted into a platform designed by recruiters who like to use holistic and concrete information to match people with the perfect jobs.

Your job is NOT to recommend a job or anything like this, but rather to simply synthesize and organize all of the information that the user input. Be sure to add analysis at the end given the provided information (again, not about finding them a job yet, just about analyzing them as a person/job applicant)

Personal information:
{personal_info}

Results of Big Five test, domain scores:
{domain_scores} 

Results of Big Five test, facet scores:
{facet_scores} 
Most important values to user (from very large list, they selected these):
{selected_values}

The user's input on how they would spend their day-to-day life if money were no object:
{if_no_money}

What the user believes they can get paid for:
{get_paid_for}

The user's input on what they think the world needs:
{word_need}

What the user wants from a job:
{want_from_job}

Soft skills (dict of user input where key is name of the skills and value is concrete examples of that skill in action):
{soft_skills}

Hard skills (same format as above):
{hard_skills}

Desired salary range:
{salary_low}-{salary_high}

Preferred geography (multiselect from City, Country, West Coast, East Coast, Abroad):
{preferred_geography}

User's current location:
{current_location}

User's willingness to move (Yes, No, Maybe):
{willing_to_move}

User's response to what their dream job is:
{dream_job}

User's response to what they'd like to do more of that they don't get to do in their current job:
{do_more}

GIVEN THIS INFORMATION, please output a few key levels of analysis:
1. Personality analysis: first, explain what each individual score means (succinctly) and then systematize this into a comprehensive personality profile that is LIGHTLY tailored to/framed by the fact that this tool is related to finding a perfect job. Be sure to include both the Big Five Traits and the Facets information wherever appropriate or relevant. (Describe each trait and then pull in specific facet scores to provide a fuller picture.)
2. Open-ended response analysis: next, go through all of the bigger picture and open-ended responses the user gave above and attempt to again systematize them and then synthesize and offer insights 'on top of' what they wrote. This should help tie all of their most important writing into a cohesive piece. If they wrote a little, you can write a little here. If they wrote a lot, you MUST also write a lot to match their dedication and level of detail they put into this.
3. Detail-oriented analysis: finally, go through all of the more fine-grained details offered by the user (eg, salary, location, soft/hard skills, etc) and systematize and synthesize these as well and offer any insights related to these. Please be sure to make some comments related to leadership potential/skills (or lack thereof) in this piece as well.

You should NOT offer job-related advice in this output, just insightful analysis and synthesis of what the user has shared.

Please output your comprehensive synthesis and analysis in HTML for clean formatting! Just immediately give the HTML, don't do anything like ```HTML...``` or something.
"""

get_recommendations_prompt = """
You will be given a comprehensive synthesis of a user's information related to finding the perfect job using holistic and concrete information gathered from them.

Here are the raw responses given by the user:
{raw_data}

Here are some insights that was generated from the user's raw responses:
{insights}

Given the user's responses and these insights, your job is to provide concrete recommendations for jobs/job types in the creative world that might suit the user.

These recommendations will be given to two professional recruiters as a basis for their consultation and continued work with the user. 

Be sure to provide specific information wherever appropriate and to make sure you explain why your suggestions align with the insights about the user provided. Do not give any links.

Format your outputs in HTML! Just immediately give the HTML, don't do anything like ```HTML...``` or something.

YOUR OUTPUTS:
"""
