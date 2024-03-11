def calculate_scores(responses):
    # Reverse scoring for reverse-keyed items
    reverse_keyed = {1: 26, 3: 8, 8: 3, 10: 20, 14: 19, 19: 14, 20: 10, 21: 6, 24: 9, 26: 11, 28: 13, 30: 15}
    for i in reverse_keyed:
        responses[i-1] = 6 - responses[reverse_keyed[i]-1]
    
    # Calculate domain scores as a percentage
    domain_scores = {
        "Extraversion": sum([responses[i-1] for i in [1, 6, 11, 16, 21, 26]]) / (5 * 6),
        "Agreeableness": sum([responses[i-1] for i in [2, 7, 12, 17, 22, 27]]) / (5 * 6),
        "Conscientiousness": sum([responses[i-1] for i in [3, 8, 13, 18, 23, 28]]) / (5 * 6),
        "Negative Emotionality": sum([responses[i-1] for i in [4, 9, 14, 19, 24, 29]]) / (5 * 6),
        "Open-Mindedness": sum([responses[i-1] for i in [5, 10, 15, 20, 25, 30]]) / (5 * 6)
    }

    # Calculate facet scores as a percentage
    facet_scores = {
        "Sociability": sum([responses[i-1] for i in [1, 16]]) / (5 * 2),
        "Assertiveness": sum([responses[i-1] for i in [6, 21]]) / (5 * 2),
        "Energy Level": sum([responses[i-1] for i in [11, 26]]) / (5 * 2),
        "Compassion": sum([responses[i-1] for i in [2, 17]]) / (5 * 2),
        "Respectfulness": sum([responses[i-1] for i in [7, 22]]) / (5 * 2),
        "Trust": sum([responses[i-1] for i in [12, 27]]) / (5 * 2),
        "Organization": sum([responses[i-1] for i in [3, 18]]) / (5 * 2),
        "Productiveness": sum([responses[i-1] for i in [8, 23]]) / (5 * 2),
        "Responsibility": sum([responses[i-1] for i in [13, 28]]) / (5 * 2),
        "Anxiety": sum([responses[i-1] for i in [4, 19]]) / (5 * 2),
        "Depression": sum([responses[i-1] for i in [9, 24]]) / (5 * 2),
        "Emotional Volatility": sum([responses[i-1] for i in [14, 29]]) / (5 * 2),
        "Aesthetic Sensitivity": sum([responses[i-1] for i in [5, 20]]) / (5 * 2),
        "Intellectual Curiosity": sum([responses[i-1] for i in [10, 25]]) / (5 * 2),
        "Creative Imagination": sum([responses[i-1] for i in [15, 30]]) / (5 * 2)
    }

    # Round scores to three significant figures and convert to percentage
    domain_scores = {key: round(value, 3) for key, value in domain_scores.items()}
    facet_scores = {key: round(value, 3) for key, value in facet_scores.items()}

    return domain_scores, facet_scores