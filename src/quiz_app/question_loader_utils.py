# this files load the quiz data for conducting the question

import random as rd
import pandas as pd
from quiz_app.utility_function.csv_validator import QuizFileValidator
from quiz_app.quiz_utils import Quiz

class QuizLoader(QuizFileValidator):

    def __init__(self, quiz_file, limit):
        '''
        inherit the QuizFileValidator proprty and creating the constructor
        '''
        super().__init__(quiz_file)
        self.limit = limit

    def load_quiz_data(self):
        '''
        loading the question if the file is valid
        return -> quiz Data (random question, with limit)
        return -> False (if did'nt pass the test)
        '''
        validate = super().validate_quiz_file()
        if super().found_duplicates_question(validate=validate):
            # shuffling the questions
            shuffled_data = self.dataframe.sample(frac=1, random_state=None).reset_index(drop=True)
            selected_random_question = shuffled_data.head(self.limit)

            # loading all the quiz data after selections
            question = selected_random_question['Question'].str.strip().to_list()
            options = (
            selected_random_question[['Option A', 'Option B', 'Option C', 'Option D']]
            .apply(lambda row: [str(x).strip() for x in row], axis=1)
            .tolist()
            )
            answer = selected_random_question['Correct Option'].astype(str).str.strip().to_list()
            _timer = selected_random_question['Timer'].astype(str).str.strip().to_list()
            explaination = selected_random_question['explaination'].astype(str).str.strip().to_list()
            print('Loaded Successfully')
            # returning the quiz data
            quiz = Quiz(question=question, options=options, answer=answer, time=_timer, explaination=explaination)
            quiz.conduct_quiz()
            quiz.display_quiz_reults()

        else:
            print('Unable to conduct the quiz due to teachnical issue')
            return False