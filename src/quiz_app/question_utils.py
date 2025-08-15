# load the questions and the answer and conduct the quiz
import pandas as pd
import random as rd
from quiz_app.category_utils import QuizNavigator

class Quiz:

    def __init__(self, quiz_file, question_limit):

        self.dataframe = pd.read_csv(quiz_file)
        self.limit = question_limit

    def read_csv(self):
        question = []
        option = []
