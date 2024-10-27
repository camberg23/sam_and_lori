# def calculate_scores(responses):
#     # Reverse scoring for reverse-keyed items
#     reverse_keyed = {1: 26, 3: 8, 8: 3, 10: 20, 14: 19, 19: 14, 20: 10, 21: 6, 24: 9, 26: 11, 28: 13, 30: 15}
#     for i in reverse_keyed:
#         responses[i-1] = 6 - responses[reverse_keyed[i]-1]
    
#     # Adjust scores to start at 0
#     adjusted_responses = [score - 1 for score in responses]

#     # Calculate domain scores as a percentage
#     domain_scores = {
#         "Extraversion": sum([adjusted_responses[i-1] for i in [1, 6, 11, 16, 21, 26]]) / (6 * 4),
#         "Agreeableness": sum([adjusted_responses[i-1] for i in [2, 7, 12, 17, 22, 27]]) / (6 * 4),
#         "Conscientiousness": sum([adjusted_responses[i-1] for i in [3, 8, 13, 18, 23, 28]]) / (6 * 4),
#         "Negative Emotionality": sum([adjusted_responses[i-1] for i in [4, 9, 14, 19, 24, 29]]) / (6 * 4),
#         "Open-Mindedness": sum([adjusted_responses[i-1] for i in [5, 10, 15, 20, 25, 30]]) / (6 * 4)
#     }

#     # Calculate facet scores as a percentage
#     facet_scores = {
#         "Sociability": sum([adjusted_responses[i-1] for i in [1, 16]]) / (2 * 4),
#         "Assertiveness": sum([adjusted_responses[i-1] for i in [6, 21]]) / (2 * 4),
#         "Energy Level": sum([adjusted_responses[i-1] for i in [11, 26]]) / (2 * 4),
#         "Compassion": sum([adjusted_responses[i-1] for i in [2, 17]]) / (2 * 4),
#         "Respectfulness": sum([adjusted_responses[i-1] for i in [7, 22]]) / (2 * 4),
#         "Trust": sum([adjusted_responses[i-1] for i in [12, 27]]) / (2 * 4),
#         "Organization": sum([adjusted_responses[i-1] for i in [3, 18]]) / (2 * 4),
#         "Productiveness": sum([adjusted_responses[i-1] for i in [8, 23]]) / (2 * 4),
#         "Responsibility": sum([adjusted_responses[i-1] for i in [13, 28]]) / (2 * 4),
#         "Anxiety": sum([adjusted_responses[i-1] for i in [4, 19]]) / (2 * 4),
#         "Depression": sum([adjusted_responses[i-1] for i in [9, 24]]) / (2 * 4),
#         "Emotional Volatility": sum([adjusted_responses[i-1] for i in [14, 29]]) / (2 * 4),
#         "Aesthetic Sensitivity": sum([adjusted_responses[i-1] for i in [5, 20]]) / (2 * 4),
#         "Intellectual Curiosity": sum([adjusted_responses[i-1] for i in [10, 25]]) / (2 * 4),
#         "Creative Imagination": sum([adjusted_responses[i-1] for i in [15, 30]]) / (2 * 4)
#     }

#     # Round scores to three significant figures
#     domain_scores = {key: round(value * 100, 3) for key, value in domain_scores.items()}
#     facet_scores = {key: round(value * 100, 3) for key, value in facet_scores.items()}

#     return domain_scores, facet_scores


import copy

# Constants
MAX_RESPONSE = 5
MIN_RESPONSE = 1
REVERSE_KEYED = [1, 3, 8, 10, 14, 19, 20, 21, 24, 26, 28, 30]

def calculate_scores(responses):
    # Validate responses
    for idx, score in enumerate(responses, start=1):
        if score not in [1, 2, 3, 4, 5]:
            raise ValueError(f"Invalid response for question {idx}: {score}. Must be between {MIN_RESPONSE} and {MAX_RESPONSE}.")
    
    # Create a deep copy to avoid modifying the original responses
    processed_responses = copy.deepcopy(responses)
    
    # Reverse scoring: invert responses for reverse-keyed questions
    for i in REVERSE_KEYED:
        processed_responses[i-1] = (MAX_RESPONSE + 1) - processed_responses[i-1]
    
    # Adjust scores to start at 0
    adjusted_responses = [score - MIN_RESPONSE for score in processed_responses]
    
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
