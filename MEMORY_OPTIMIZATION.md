# Memory Optimization Features

## Overview

The quiz application now includes several memory optimization features to handle large CSV files efficiently:

## Key Features

### 1. Dynamic File Discovery
- Automatically discovers all CSV files in the `data/` directory
- No need to hardcode file paths in the code
- Simply add new CSV files to the `data/` directory and they'll be available

### 2. Lazy Loading
- Questions are only loaded when a specific quiz is selected
- File statistics are shown before loading to give users information about file size
- No pre-loading of all CSV files into memory

### 3. Intelligent Caching
- Questions are cached after first load to avoid re-parsing the same file
- Cache can be manually cleared to free memory
- Cache information is available for monitoring

### 4. Memory-Efficient File Statistics
- File statistics (size, question count) are calculated without loading all questions
- Uses efficient row counting instead of full file parsing

## Usage

### Adding New Quiz Files
1. Create a new CSV file in the `data/` directory
2. Follow the standard format: `category,subcategory,question,option1,option2,option3,option4,answer`
3. The application will automatically detect and list it as an option

### Memory Management
- The application will show file statistics before loading
- After completing a quiz, you can choose to clear the cache
- Cache clearing frees memory but means files will be re-parsed if selected again

### Example CSV Format
```csv
category,subcategory,question,option1,option2,option3,option4,answer
Programming,Basic,What is Python?,A programming language,A database,A web browser,A game,a
```

## Benefits

1. **Scalability**: Can handle hundreds of CSV files without memory issues
2. **Flexibility**: Easy to add new quiz subjects without code changes
3. **Performance**: Caching prevents repeated file parsing
4. **User Control**: Users can manage memory usage through cache clearing
5. **Information**: File statistics help users understand what they're loading

## Technical Details

- Uses `pathlib.Path` for robust file path handling
- Implements class-level caching in `QuizLoader`
- Provides file statistics without full file loading
- Graceful error handling for missing or corrupted files 