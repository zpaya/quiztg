from quiz_app.category_utils import QuizNavigator 

def main_executer():
    '''
    caller for all the module
    execute the quiz game
    '''
    # loading file path
    csv_path = r"D:\python\project\quiztg\resources\data\category_subcategory.csv"
    # creating the object for the QuizNavigator
    quiz_nav = QuizNavigator(csv_path)
    # loading the category, subcategory and quiz_file_path
    quiz_file_path = quiz_nav.category_subcategory_file_path()
    # fetching the limit
    question_limit = quiz_nav.get_question_limit(quiz_file_path)
    print(f'available question limit : {question_limit}')
    
if __name__ == '__main__':
    main_executer()
