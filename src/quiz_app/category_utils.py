import pandas as pd

class QuizNavigator:
    '''
    loading the category, subcategory and the quiz file path based on the user choice
    '''

    def __init__(self, csv_path):
        '''
        constructor for calling the csv and category
        '''
        self.data = pd.read_csv(csv_path)
        self.categories = self.data["Category"].unique().tolist()
    
    def load_category(self):
        '''
        loading the catgory 
        return -> category
        '''
        # display the welcome message
        print('=== Welcome to the quiz App ===')
        print('Choose the category:')

        # Displaying the available category
        for idx, category in enumerate(self.categories, start=1):
            print(f'{idx}. {category}')

        # user choice lock
        while True:
            try:
                prompt = input('Enter the number of Category: ').strip()
                choice = int(prompt)
                if 1 <= choice <= len(self.categories):
                    return self.categories[choice - 1]
                else:
                    print(f'Enter a number between 1 and {len(self.categories)}.')
            except ValueError:
                print('Please enter a valid number !!')
            except StopIteration:
                print('Loop is being infinite teachincal issue occured !')

    def load_subcategory(self, category):
        '''
        filter the subcategory based on the category
        return -> subcategory
        '''
        filtered_df = self.data[self.data['Category'] == category]

        # converting the sbcategories to list to get better access
        subcategories = filtered_df['Sub_Category'].unique().tolist()

        # printing the subcategories
        print(f'\nSubcategories in "{category}":')
        for idx, subcat in enumerate(subcategories, start=1):
            print(f'{idx}. {subcat}')

        # choice lock for the subcategories
        while True:
            try:
                choice = int(input('Enter the number of Subcategory: ').strip())
                if 1 <= choice <= len(subcategories):
                    return subcategories[choice - 1]
                else:
                    print(f'Enter a number between 1 and {len(subcategories)}.')
            except ValueError:
                print('Please enter a valid number.')

    def load_subcategory_filepath(self, subcategory):
        '''
        filter the quiz file path based on the subcategory
        return -> quiz file path
        '''
        filtered_df = self.data[self.data['Sub_Category'] == subcategory]
        quiz_file_path = filtered_df['Quiz_File_Path'].iloc[0]
        return quiz_file_path
    
    def category_subcategory_file_path(self):
        '''
        display category, subcategory and lock them
        return -> file_path
        '''
        category = self.load_category()
        sub_category = self.load_subcategory(category)
        file_path = self.load_subcategory_filepath(sub_category)
        return file_path
    
    def get_question_limit(self, file_path):

        '''
        fetch the question limit based on the question path
        return -> question_limit
        '''
        question_limit = self.data.loc[self.data['Quiz_File_Path'] == file_path, 'question_limit']
        return question_limit.iloc[0]
