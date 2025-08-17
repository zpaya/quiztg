# make the answer to the crrect formate
def _normalize_answer(answer=None):

    if answer is None:
        return None
    
    answer = answer.strip().upper()
    
    # If it's already a letter, return as is
    if len(answer) == 1 and answer in 'ABCD':
        return answer
    
    # If it's a number, convert to letter
    if answer.isdigit():
        num = int(answer)
        if 1 <= num <= 4:
            return chr(64 + num)  # Convert 1->A, 2->B, 3->C, 4->D
    
    # dictionary for the common user inputs
    answer_mapping = {
        'FIRST': 'A', 
        '1ST': 'A',
        'ONE': 'A',
        'SECOND': 'B',
        '2ND': 'B',
        'TWO': 'B',
        'THIRD': 'C',
        '3RD': 'C',
        'THREE': 'C',
        'FOURTH': 'D', 
        '4TH': 'D', 
        'FOUR': 'D'
    }
    
    if answer in answer_mapping:
        return answer_mapping[answer]
    
    # If we can't normalize it, return the original for error handling
    return answer