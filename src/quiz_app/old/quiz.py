import time
import threading
import random
from collections import defaultdict

class Quiz:
    """Main quiz conductor class with timer functionality"""
    
    def __init__(self, questions, time_limit=30):
        """
        Initialize quiz with questions and time limit
        
        Args:
            questions (list): List of LoadQuestion objects
            time_limit (int): Time limit per question in seconds
        """
        self.questions = questions
        self.time_limit = max(10, min(60, time_limit))  # Clamp between 10-60 seconds
        self.score = 0
        self.total_questions = 0
        
    def get_categories_and_subcategories(self):
        """Get organized categories and subcategories"""
        categories_map = defaultdict(set)
        
        for question in self.questions:
            categories_map[question.category].add(question.subcategory)
        
        # Convert sets to sorted lists
        return {category: sorted(list(subcategories)) 
                for category, subcategories in categories_map.items()}
    
    def filter_questions(self, category, subcategory):
        """
        Filter questions by category and subcategory
        
        Args:
            category (str): Category to filter by
            subcategory (str): Subcategory to filter by
            
        Returns:
            list: Filtered questions
        """
        return [q for q in self.questions 
                if q.category == category and q.subcategory == subcategory]
    
    def select_option(self, prompt, options):
        """
        Display options and get user selection with validation
        
        Args:
            prompt (str): Prompt message
            options (list): List of options to choose from
            
        Returns:
            str: Selected option
        """
        while True:
            print(f'\n{prompt}')
            print('-' * len(prompt))
            
            for i, option in enumerate(options, 1):
                print(f'{i}. {option}')
            
            try:
                choice = input(f'\nSelect an option (1-{len(options)}): ').strip()
                
                if not choice:
                    print('Please enter a choice!')
                    continue
                
                choice_num = int(choice)
                if 1 <= choice_num <= len(options):
                    selected = options[choice_num - 1]
                    print(f'You selected: {selected}')
                    return selected
                else:
                    print(f'Please enter a number between 1 and {len(options)}!')
                    
            except ValueError:
                print('Please enter a valid number!')
            except KeyboardInterrupt:
                print('\nReturning to main menu...')
                raise
    
    def get_number_of_questions(self, max_questions):
        """
        Get number of questions to ask with validation
        
        Args:
            max_questions (int): Maximum available questions
            
        Returns:
            int: Number of questions to ask
        """
        while True:
            try:
                prompt = f'How many questions would you like to answer? (1-{max_questions}): '
                num_str = input(prompt).strip()
                
                if not num_str:
                    print('Please enter a number!')
                    continue
                
                num_questions = int(num_str)
                
                if 1 <= num_questions <= max_questions:
                    return num_questions
                else:
                    print(f'Please enter a number between 1 and {max_questions}!')
                    
            except ValueError:
                print('Please enter a valid number!')
            except KeyboardInterrupt:
                print('\nReturning to quiz setup...')
                raise
    
    def ask_question_with_timer(self, question, question_number, total_questions):
        """
        Ask a single question with timer functionality
        
        Args:
            question (LoadQuestion): Question to ask
            question_number (int): Current question number (1-based)
            total_questions (int): Total number of questions
            
        Returns:
            bool: True if answered correctly, False otherwise
        """
        print(f'\n{"="*60}')
        print(f'Question {question_number}/{total_questions}')
        print(f'Time limit: {self.time_limit} seconds')
        print(f'Category: {question.category} > {question.subcategory}')
        print("="*60)
        
        # Display question without passing index (it was causing duplicate numbering)
        print(f'\n{question.question}')
        print('-' * len(question.question))
        
        for i, option in enumerate(question.options):
            option_letter = chr(65 + i)  # A, B, C, D
            print(f'{option_letter}. {option}')
        print()  # Empty line for better readability
        
        # Get valid options for this question
        valid_options = question.get_valid_options()
        valid_options_str = ', '.join(valid_options)
        
        # Threading variables
        answer_received = threading.Event()
        user_answer = [None]  # Use list to allow modification in nested function
        
        def timer_function():
            """Timer that runs in separate thread"""
            time.sleep(self.time_limit)
            if not answer_received.is_set():
                print(f'\n⏰ Time\'s up! ({self.time_limit} seconds)')
                answer_received.set()
        
        # Start timer thread
        timer_thread = threading.Thread(target=timer_function, daemon=True)
        timer_thread.start()
        
        # Get user input
        print(f'Enter your answer ({valid_options_str}): ', end='', flush=True)
        
        start_time = time.time()
        
        # Simplified input handling for cross-platform compatibility
        try:
            user_input = input().strip().upper()
            if not answer_received.is_set():
                if user_input in valid_options:
                    user_answer[0] = user_input
                    answer_received.set()
                    elapsed_time = time.time() - start_time
                    print(f'Answer submitted in {elapsed_time:.1f} seconds')
                else:
                    print(f'Invalid option! Valid options are: {valid_options_str}')
                    answer_received.set()
        except KeyboardInterrupt:
            print('\nQuestion skipped by user.')
            answer_received.set()
        except EOFError:
            print('\nInput error occurred.')
            answer_received.set()
        
        # Wait for timer thread to complete
        timer_thread.join(timeout=0.1)
        
        # Process answer
        is_correct = False
        if user_answer[0]:
            is_correct = question.check_correct(user_answer[0])
            user_option_text = question.get_user_answer_text(user_answer[0])
            
            if is_correct:
                print(f'✅ Correct! You chose: {user_answer[0]}. {user_option_text}')
            else:
                correct_text = question.get_correct_option_text()
                print(f'❌ Incorrect! You chose: {user_answer[0]}. {user_option_text}')
                print(f'   Correct answer: {question.answer}. {correct_text}')
        else:
            correct_text = question.get_correct_option_text()
            print(f'⏰ No answer provided!')
            print(f'   Correct answer: {question.answer}. {correct_text}')
        
        return is_correct
    
    def display_final_results(self):
        """Display final quiz results with performance analysis"""
        print(f'\n{"="*60}')
        print('QUIZ COMPLETED!')
        print("="*60)
        
        percentage = (self.score / self.total_questions) * 100 if self.total_questions > 0 else 0
        
        print(f'Final Score: {self.score}/{self.total_questions} ({percentage:.1f}%)')
        
        # Performance feedback
        if percentage >= 90:
            print('🏆 Outstanding performance! Excellent work!')
        elif percentage >= 80:
            print('🎉 Great job! Very good performance!')
        elif percentage >= 70:
            print('👍 Good work! Room for improvement.')
        elif percentage >= 50:
            print('📚 Fair performance. Consider reviewing the material.')
        else:
            print('📖 Keep studying! Practice makes perfect.')
        
        print(f'\nThank you for taking the quiz!')
        print("="*60)
    
    def conduct(self):
        """Main method to conduct the quiz"""
        try:
            if not self.questions:
                print('❌ No questions available!')
                return
            
            print(f'\n🎯 Quiz Setup')
            print(f'Time limit per question: {self.time_limit} seconds')
            
            # Get categories and subcategories
            categories_map = self.get_categories_and_subcategories()
            
            if not categories_map:
                print('❌ No valid categories found!')
                return
            
            # Select category
            categories = sorted(list(categories_map.keys()))
            selected_category = self.select_option('Available Categories:', categories)
            
            # Select subcategory
            subcategories = categories_map[selected_category]
            selected_subcategory = self.select_option(
                f'Available Subcategories for {selected_category}:',
                subcategories
            )
            
            # Filter questions
            filtered_questions = self.filter_questions(selected_category, selected_subcategory)
            
            if not filtered_questions:
                print(f'❌ No questions found for {selected_category} > {selected_subcategory}')
                return
            
            print(f'\n📊 Found {len(filtered_questions)} questions in {selected_category} > {selected_subcategory}')
            
            # Get number of questions to ask
            num_to_ask = self.get_number_of_questions(len(filtered_questions))
            
            # Randomize questions
            random.shuffle(filtered_questions)
            selected_questions = filtered_questions[:num_to_ask]
            
            self.total_questions = len(selected_questions)
            self.score = 0
            
            print(f'\n🚀 Starting Quiz!')
            print(f'Questions: {self.total_questions}')
            print(f'Category: {selected_category} > {selected_subcategory}')
            print(f'Time per question: {self.time_limit} seconds')
            
            input('\nPress Enter to begin...')
            
            # Ask questions - Fixed the question numbering here
            for i, question in enumerate(selected_questions):
                if self.ask_question_with_timer(question, i + 1, self.total_questions):
                    self.score += 1
                
                # Brief pause between questions
                if i < len(selected_questions) - 1:
                    time.sleep(1)
            
            # Display results
            self.display_final_results()
            
        except KeyboardInterrupt:
            print('\n\n🛑 Quiz interrupted by user.')
            if self.total_questions > 0:
                print(f'Partial score: {self.score}/{self.total_questions}')
        except Exception as e:
            print(f'\n❌ An error occurred during the quiz: {e}')
            print('Please contact support if this issue persists.')
