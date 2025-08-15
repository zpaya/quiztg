from quiz_app.category_utils import QuizNavigator 
from quiz_app.question_utils import Quiz

def main_executer():
    '''
    caller for all the module
    execute the quiz game
    '''
    # loading the ctaegory, subcategory, quiz file path, limit and noramlize the quiz path
    csv_path = r"D:\python\project\quiztg\resources\data\category_subcategory.csv"
    quiz_nav = QuizNavigator(csv_path)
    quiz_path, limit = quiz_nav.category_subcategory_file_path()
    noramlize_path = quiz_nav.get_quiz_file_path(quiz_path)

    # Quiz Class
    quiz = Quiz(noramlize_path, limit)
    
    
if __name__ == '__main__':
    main_executer()
