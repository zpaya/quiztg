# load the questions and the answer and conduct the quiz
import pandas as pd

class QuizFileValidator:

    def __init__(self, quiz_file):
        '''
        Creating the constructor for the Quiz class
        :param quiz_file: The path to the CSV file containing the quiz data
        '''
        self.dataframe = pd.read_csv(quiz_file)

    def validate_quiz_file(self):
        '''
        validate the quiz csv file
        return -> True for correct formate and
        return -> False for the incorrect formate
        '''
        # initialize the defaul valid to true
        validate = False 
        # default row in the quiz 
        default_quiz_rows = ['ID', 'Question', 'Option A', 'Option B', 'Option C', 'Option D', 'Correct Option', 'Timer', 'explaination']
        # quiz file rows
        quiz_file_columns = []

        # loop for fetching the columns
        for cols in self.dataframe.columns:
            quiz_file_columns.append(cols)

        # condition for validate
        if quiz_file_columns == default_quiz_rows:
            validate = True
            return validate
        else:
            print(f'Invalide file columns \nexpected -> {default_quiz_rows} got {quiz_file_columns}')
            return validate
    
    def found_duplicates_question(self, validate):
        '''
        find the duplicates question
        return -> duplicate question
        '''
        verified = False
        # if the file is valid formate of the quiz_file_columns
        if validate:
            # counting how many time the question ocurred
            counts = self.dataframe['Question'].value_counts()
            # appending the question if count greater then 1 
            duplicate_question = counts[counts > 1]

            # condition flag to alow the quiz to being conducted

            if not duplicate_question.empty:
                return validate
            else:
                validate = True
                return validate
