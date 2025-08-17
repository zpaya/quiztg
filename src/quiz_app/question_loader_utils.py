import pandas as pd
# from quiz_app.category_utils import QuizNavigator
from quiz_app.utility_function.csv_validator import QuizFileValidator

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
        return -> quiz Data
        return -> False (if did'nt pass the test)
        '''
        validate = super().validate_quiz_file()
        if super().found_duplicates_question(validate=validate):
            # loading all the quiz data
            question = super().dataframe['Question'].str.strip().to_list()
            options = (
            super().dataframe[['Option A', 'Option B', 'Option C', 'Option D']]
            .apply(lambda row: [str(x).strip() for x in row], axis=1)
            .tolist()
            )
            answer = super().dataframe['Correct Option'].str.strip().to_list()
            _timer = super().dataframe['Timer'].strip().str.to_list()
            explaination = super().dataframe['explaination'].str.strip().to_list()

            return question, options, answer, _timer, explaination

        else:
            print('Unable to conduct the quiz due to teachnical issue')
            return False