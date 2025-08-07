import csv
import os
from question import LoadQuestion

class QuizLoader:
    """Utility class for loading quiz questions from CSV files with memory optimization"""
    
    # Class-level cache to avoid reloading the same file
    _cache = {}
    
    @staticmethod
    def load_questions(file_path):
        """
        Load questions from a CSV file with caching for memory efficiency
        
        Expected CSV format:
        Category, Subcategory, Question, Option1, Option2, Option3, Option4, Answer
        
        Args:
            file_path (str): Path to the CSV file
            
        Returns:
            list: List of LoadQuestion objects
        """
        # Check cache first
        if file_path in QuizLoader._cache:
            print(f"📋 Loading from cache: {file_path}")
            return QuizLoader._cache[file_path]
        
        questions = []
        skipped_rows = 0
        
        try:
            # Validate file existence and readability
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
            
            if not os.access(file_path, os.R_OK):
                raise PermissionError(f"Cannot read file: {file_path}")
            
            print(f"📂 Loading questions from: {file_path}")
            
            with open(file_path, mode='r', newline='', encoding='utf-8') as file:
                # Use csv.reader for better column handling
                reader = csv.reader(file)
                
                # Skip header row
                try:
                    header = next(reader)
                    print(f"📋 CSV Header: {header}")
                except StopIteration:
                    raise ValueError("CSV file is empty")
                
                # Validate header format
                expected_min_columns = 8  # Category, Subcategory, Question, 4 options, Answer
                if len(header) < expected_min_columns:
                    print(f"⚠️  Warning: Expected at least {expected_min_columns} columns, found {len(header)}")
                
                row_number = 1  # Start from 1 since we skipped header
                
                for row in reader:
                    row_number += 1
                    
                    try:
                        # Skip empty rows
                        if not any(cell.strip() for cell in row):
                            continue
                        
                        # Validate row has minimum required columns
                        if len(row) < expected_min_columns:
                            print(f"⚠️  Row {row_number}: Insufficient columns ({len(row)}/{expected_min_columns}). Skipping.")
                            skipped_rows += 1
                            continue
                        
                        # Extract data with validation
                        category = row[0].strip()
                        subcategory = row[1].strip()
                        question_text = row[2].strip()
                        options = [row[i].strip() for i in range(3, 7)]  # Options 1-4
                        answer = row[7].strip()
                        
                        # Debug: Print problematic row data
                        if not answer or len(answer) > 10:  # Suspicious answer format
                            print(f"🔍 Row {row_number} Debug - Answer: '{answer}' (length: {len(answer)})")
                            print(f"   Full row: {row[:8]}")  # Show first 8 columns
                        
                        # Validate essential fields
                        if not category:
                            print(f"⚠️  Row {row_number}: Empty category. Skipping.")
                            skipped_rows += 1
                            continue
                        
                        if not subcategory:
                            print(f"⚠️  Row {row_number}: Empty subcategory. Skipping.")
                            skipped_rows += 1
                            continue
                        
                        if not question_text:
                            print(f"⚠️  Row {row_number}: Empty question text. Skipping.")
                            skipped_rows += 1
                            continue
                        
                        if not answer:
                            print(f"⚠️  Row {row_number}: Empty answer. Skipping.")
                            skipped_rows += 1
                            continue
                        
                        # Filter out empty options
                        valid_options = [opt for opt in options if opt]
                        
                        if len(valid_options) < 2:
                            print(f"⚠️  Row {row_number}: Insufficient options ({len(valid_options)}). Skipping.")
                            print(f"   Options found: {valid_options}")
                            skipped_rows += 1
                            continue
                        
                        # Create question object
                        question = LoadQuestion(
                            category=category,
                            subcategory=subcategory,
                            question=question_text,
                            options=valid_options,
                            answer=answer
                        )
                        
                        questions.append(question)
                        
                    except ValueError as ve:
                        print(f"⚠️  Row {row_number}: Data validation error - {ve}")
                        print(f"   Raw answer: '{row[7] if len(row) > 7 else 'N/A'}'")
                        skipped_rows += 1
                        continue
                    
                    except Exception as e:
                        print(f"⚠️  Row {row_number}: Unexpected error - {e}")
                        print(f"   Row data: {row[:8] if len(row) >= 8 else row}")
                        skipped_rows += 1
                        continue
        
        except FileNotFoundError as e:
            print(f"❌ File Error: {e}")
            print(f"Please ensure the file exists at: {file_path}")
            return []
        
        except PermissionError as e:
            print(f"❌ Permission Error: {e}")
            print(f"Please check file permissions for: {file_path}")
            return []
        
        except csv.Error as e:
            print(f"❌ CSV Format Error: {e}")
            print(f"Please check the CSV file format at: {file_path}")
            return []
        
        except UnicodeDecodeError as e:
            print(f"❌ Encoding Error: {e}")
            print(f"Please ensure the file is saved in UTF-8 encoding: {file_path}")
            return []
        
        except Exception as e:
            print(f"❌ Unexpected Error: {e}")
            print(f"Please contact support if this issue persists.")
            return []
        
        # Summary report
        total_processed = len(questions) + skipped_rows
        print(f"\n📊 Loading Summary:")
        print(f"   Total rows processed: {total_processed}")
        print(f"   Questions loaded: {len(questions)}")
        print(f"   Rows skipped: {skipped_rows}")
        
        if questions:
            print(f"   Categories found: {len(set(q.category for q in questions))}")
            print(f"   Subcategories found: {len(set(q.subcategory for q in questions))}")
            
            # Show sample of loaded questions
            print(f"\n📝 Sample Questions Loaded:")
            for i, q in enumerate(questions[:3]):  # Show first 3 questions
                print(f"   {i+1}. {q.category}/{q.subcategory}: {q.question[:50]}...")
                print(f"      Answer: {q.answer}")
        
        # Cache the results for future use
        QuizLoader._cache[file_path] = questions
        
        return questions
    
    @staticmethod
    def clear_cache():
        """Clear the question cache to free memory"""
        QuizLoader._cache.clear()
        # print("🗑️  Question cache cleared")
    
    @staticmethod
    def get_cache_info():
        """Get information about cached files"""
        return {
            'cached_files': list(QuizLoader._cache.keys()),
            'total_cached_questions': sum(len(questions) for questions in QuizLoader._cache.values())
        }
    
    @staticmethod
    def validate_csv_format(file_path):
        """
        Validate CSV file format without loading all questions
        
        Args:
            file_path (str): Path to CSV file
            
        Returns:
            tuple: (is_valid, error_message)
        """
        try:
            if not os.path.exists(file_path):
                return False, f"File not found: {file_path}"
            
            with open(file_path, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                
                # Check header
                try:
                    header = next(reader)
                    if len(header) < 8:
                        return False, f"Header has insufficient columns ({len(header)}/8 minimum)"
                except StopIteration:
                    return False, "File is empty"
                
                # Check first few data rows
                sample_size = min(5, sum(1 for _ in reader))  # Reset reader
                file.seek(0)
                reader = csv.reader(file)
                next(reader)  # Skip header again
                
                valid_rows = 0
                for i, row in enumerate(reader):
                    if i >= sample_size:
                        break
                    
                    if len(row) >= 8 and any(cell.strip() for cell in row):
                        valid_rows += 1
                
                if valid_rows == 0:
                    return False, "No valid data rows found"
                
                return True, "CSV format appears valid"
        
        except Exception as e:
            return False, f"Validation error: {e}"
    
    @staticmethod
    def get_file_stats(file_path):
        """
        Get statistics about a CSV file without loading all questions into memory
        
        Args:
            file_path (str): Path to the CSV file
            
        Returns:
            dict: File statistics
        """
        try:
            if not os.path.exists(file_path):
                return None
            
            with open(file_path, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                
                # Skip header
                try:
                    header = next(reader)
                except StopIteration:
                    return None
                
                # Count rows efficiently
                row_count = sum(1 for row in reader if any(cell.strip() for cell in row))
                
                return {
                    'file_path': file_path,
                    'total_questions': row_count,
                    'header': header,
                    'file_size_mb': os.path.getsize(file_path) / (1024 * 1024)
                }
                
        except Exception as e:
            print(f"❌ Error getting file stats: {e}")
            return None
        """
        Get basic statistics about the CSV file
        
        Args:
            file_path (str): Path to CSV file
            
        Returns:
            dict: Statistics about the file
        """
        stats = {
            'total_rows': 0,
            'categories': set(),
            'subcategories': set(),
            'file_size': 0
        }
        
        try:
            stats['file_size'] = os.path.getsize(file_path)
            
            with open(file_path, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                
                for row in reader:
                    stats['total_rows'] += 1
                    if len(row) >= 2:
                        if row[0].strip():
                            stats['categories'].add(row[0].strip())
                        if row[1].strip():
                            stats['subcategories'].add(row[1].strip())
        
        except Exception:
            pass  # Return empty stats on error
        
        # Convert sets to counts
        stats['categories'] = len(stats['categories'])
        stats['subcategories'] = len(stats['subcategories'])
        
        return stats
