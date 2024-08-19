from collections import Counter

def score(dice):
    # Define the points for three of a kind and single dice
    points_for_three = {
        1: 1000,
        2: 200,
        3: 300,
        4: 400,
        5: 500,
        6: 600
    }
    
    points_for_single = {
        1: 100,
        5: 50
    }
    
    # Count occurrences of each dice value
    counts = Counter(dice)

    print(counts, "<<<<< COUNTER(DICE)")
    
    # Calculate the score
    total_score = 0
    
    # Calculate points for three of a kind
    for num, count in counts.items():
        if count >= 3:
            total_score += points_for_three[num]
            count -= 3
        
        # Calculate points for remaining single dice
        if num in points_for_single:
            total_score += count * points_for_single[num]
    
    return total_score


print(score([5, 1, 3, 4, 1]))  # Output: 250


