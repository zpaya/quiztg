# this file conducts the Quiz
import pandas as pd
import time 
from quiz_app.utility_function.answer_mapping import _normalize_answer
from quiz_app.utility_function.score_percentage import percentage_calculator
from inputimeout import inputimeout, TimeoutOccurred

class Quiz:
    '''
    quiz class for conducting the quiz
    '''
    def __init__(self, question, options, answer, time, explaination):
        self.question = question
        self.options = options
        self.answer = answer
        self.time = time
        self.explaination = explaination # excluded as per our talk
        self.score = 0 # initializing the score to 0

    def conduct_quiz(self):
        '''
        conduct the Quiz 
        '''
        print('=== Beigning the Quiz ===\n')
        # looping the question
        for idx, questions in enumerate(self.question):
        
            print(f'\nQuestion {idx + 1}. {questions}')
            # nesting for printing the options
            for alpha, options in enumerate(self.options[idx]):
                print(f'    {chr(65 + alpha)}. {options}')
            
            # lock user answer 
            try:
                user_input = inputimeout(prompt='Enter Answer (A/B/C/D) : ', timeout=int(self.time[idx]))
                user_ans = _normalize_answer(user_input)
                if user_ans == self.answer[idx]:
                    self.score += 1
                    print('correct ! Nice Job') 
                else:
                    print('\nWrong Answer\n')
                    print(f'Correct Answer is : {self.answer[idx]}') # printing the correct answer
                    time.sleep(2)
                 
            except TimeoutOccurred:
                print('Time Out')
                print(f'Correct Answer is : {self.answer[idx]}') # printing the correct answer
                user_ans = None
                time.sleep(2) # pausing for 2 second for reading the explaination
    
    def display_quiz_reults(self):
        print('\n======== Quiz Completed ========')
        score = percentage_calculator(score=self.score, total_question=len(self.question))
        print(f'Your total correct are {self.score} out of {len(self.question)}')



            






