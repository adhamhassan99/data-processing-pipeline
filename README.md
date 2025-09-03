# Configurable Text Processing Pipeline

A flexible, extensible text processing system that can apply multiple transformations to text data in a configurable sequence.

## Features

- **Configurable Pipeline**: Choose which processing steps to apply
- **Extensible Architecture**: Easy to add new processing steps
- **Multiple Input Types**: Process single strings or lists of strings
- **Rich Statistics**: Detailed processing statistics and analysis
- **Beautiful CLI**: Command-line interface with rich formatting
- **Error Handling**: Configurable error handling strategies
- **Advanced NLP**: spaCy-powered text processing with sophisticated tokenization
- **Smart Text Processing**: Punctuation removal, stop word filtering, and lemmatization
- **Intelligent Tokenization**: Context-aware tokenization for better text analysis

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd data-processing-pipeline
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install spaCy language model:
```bash
python -m spacy download en_core_web_sm
```

**Note**: The pipeline requires spaCy and its English language model for advanced NLP features. If spaCy models are not available, the pipeline will fall back to basic regex-based processing.

## Quick Start

### Basic Usage

```python
from pipeline import TextPipeline

# Create pipeline with default steps
pipeline = TextPipeline(['clean', 'transform', 'analyze'])

# Process text
text = "  Hello, World!  \n  This is a TEST.  "
result = pipeline.process(text)

print(f"Processed: {result.processed_text}")
print(f"Analysis: {result.analysis}")
```

### Command Line Usage

```bash
# Basic processing
python main.py "  Hello, World!  "

# Interactive mode
python main.py --interactive

# Custom steps
python main.py "Text to process" --steps "clean,transform"

# With configuration file
python main.py "Text to process" --config config.json
```

## Available Processing Steps

### 1. Clean Step
- Removes extra whitespace
- Trims edges
- Optionally preserves newlines
- **spaCy-powered features**:
  - Intelligent punctuation removal
  - Stop word filtering
  - Context-aware lowercase conversion

### 2. Transform Step
- Converts to lowercase
- Removes punctuation
- Removes numbers (optional)
- Removes special characters (optional)
- **spaCy-powered features**:
  - Advanced lemmatization (stemming)
  - Smart number detection (including written numbers)
  - Sophisticated character classification

### 3. Analyze Step
- Counts words, characters, sentences, paragraphs
- Calculates average word length
- Provides reading level analysis
- **Enhanced with spaCy**:
  - Intelligent tokenization for accurate word counting
  - Context-aware text analysis

## Configuration

### Programmatic Configuration

```python
from pipeline import TextPipeline, PipelineConfig

config = PipelineConfig(
    steps=['clean', 'transform', 'analyze'],
    error_handling='continue',
    step_params={
        'clean': {
            'remove_extra_spaces': True,
            'preserve_newlines': False,
            'trim_edges': True,
            'lowercase': True,
            'remove_punctuation': True,
            'remove_stopwords': True
        },
        'transform': {
            'to_lowercase': True,
            'remove_punctuation': True,
            'remove_numbers': True,
            'remove_special_chars': True,
            'apply_stemming': True
        }
    }
)

pipeline = TextPipeline(config)
```

### JSON Configuration

```json
{
    "steps": ["clean", "transform", "analyze"],
    "error_handling": "continue",
    "step_params": {
        "clean": {
            "remove_extra_spaces": true,
            "preserve_newlines": false,
            "trim_edges": true,
            "lowercase": true,
            "remove_punctuation": true,
            "remove_stopwords": true
        },
        "transform": {
            "to_lowercase": true,
            "remove_punctuation": true,
            "remove_numbers": true,
            "remove_special_chars": true,
            "apply_stemming": true
        }
    }
}
```

## CLI Options

- `--config, -c`: Path to JSON configuration file
- `--steps, -s`: Comma-separated list of steps to apply
- `--error-handling, -e`: Error handling strategy (continue/stop)
- `--interactive, -i`: Run in interactive mode
- `--verbose, -v`: Verbose output

## Architecture

The pipeline follows a modular, extensible architecture:

```
pipeline/
├── core/
│   ├── pipeline.py          # Main pipeline orchestrator
│   ├── base_step.py         # Base step class
│   ├── step_registry.py     # Step registration system
│   └── statistics.py        # Statistics collection
├── steps/
│   ├── clean_step.py        # Text cleaning step
│   ├── transform_step.py    # Text transformation step
│   └── analyze_step.py      # Text analysis step
├── models/
│   ├── config.py            # Configuration models
│   └── data.py              # Data models
└── exceptions.py            # Custom exceptions
```

## Extending the Pipeline

### Adding a New Step

1. Create a new step class inheriting from `BaseStep`:

```python
from pipeline.core.base_step import BaseStep

class CustomStep(BaseStep):
    def validate_params(self):
        # Validate step parameters
        pass
    
    def process(self, text: str) -> str:
        # Process the text
        return processed_text
```

2. Register the step in the registry:

```python
from pipeline.core.step_registry import StepRegistry

registry = StepRegistry()
registry.register_step('custom', CustomStep)
```

## Error Handling

The pipeline supports two error handling strategies:

- **continue**: Skip failed steps and continue processing
- **stop**: Stop processing on first error

## Examples

### Example 1: Basic Text Processing with spaCy

```python
from pipeline import TextPipeline

pipeline = TextPipeline(['clean', 'transform', 'analyze'])
text = "  Hello, World!  \n  This is a TEST.  "
result = pipeline.process(text)

print(f"Original: {repr(text)}")
print(f"Processed: {repr(result.processed_text)}")
print(f"Tokenized: {result.tokenized_text}")
print(f"Word count: {result.analysis['word_count']}")
```

**Output:**
```
Original: '  Hello, World!  \n  This is a TEST.  '
Processed: 'hello world test'
Tokenized: ['hello', ',', 'world', 'test']
Word count: 3
```

### Example 2: Batch Processing

```python
texts = [
    "  First text  ",
    "  Second text  ",
    "  Third text  "
]

results = pipeline.process(texts)
for i, result in enumerate(results):
    print(f"Text {i+1}: {result.processed_text}")
```

### Example 3: Custom Configuration with spaCy Features

```python
config = {
    'steps': ['clean', 'transform', 'analyze'],
    'error_handling': 'stop',
    'step_params': {
        'clean': {
            'remove_extra_spaces': True,
            'preserve_newlines': True,
            'lowercase': False,  # Keep original case
            'remove_punctuation': True,
            'remove_stopwords': False  # Keep stop words
        },
        'transform': {
            'remove_numbers': True,
            'remove_special_chars': False,  # Keep special characters
            'apply_stemming': True  # Apply lemmatization
        }
    }
}

pipeline = TextPipeline(config)
```

### Example 4: Advanced spaCy Features

```python
# Demonstrate spaCy's intelligent processing
pipeline = TextPipeline(['clean', 'transform', 'analyze'])

# Test with complex text
text = "The running dogs are better than the walking cats. They've been running for 3 hours!"
result = pipeline.process(text)

print(f"Original: {text}")
print(f"Processed: {result.processed_text}")
print(f"Tokenized: {result.tokenized_text}")
```

**Output:**
```
Original: The running dogs are better than the walking cats. They've been running for 3 hours!
Processed: run dog be good walk cat run hour
Tokenized: ['run', 'dog', 'be', 'good', 'walk', 'cat', 'run', 'hour']
```

### Example 5: Command Line Usage

```bash
# Basic processing
python main.py "Hello, World! This is a test."

# Interactive mode
python main.py --interactive

# Custom steps only
python main.py "Text to process" --steps "clean,analyze"

# With custom error handling
python main.py "Text to process" --error-handling stop

# Using configuration file
python main.py "Text to process" --config config.json

# Verbose output
python main.py "Text to process" --verbose
```

### Example 6: Text Preprocessing for Machine Learning

```python
from pipeline import TextPipeline

# Configure pipeline for ML preprocessing
ml_config = {
    'steps': ['clean', 'transform'],
    'step_params': {
        'clean': {
            'remove_extra_spaces': True,
            'trim_edges': True,
            'lowercase': True,
            'remove_punctuation': True,
            'remove_stopwords': True
        },
        'transform': {
            'remove_numbers': True,
            'remove_special_chars': True,
            'apply_stemming': True
        }
    }
}

pipeline = TextPipeline(ml_config)

# Process training data
documents = [
    "The quick brown fox jumps over the lazy dog.",
    "Machine learning is revolutionizing technology!",
    "Natural language processing helps computers understand text."
]

processed_docs = pipeline.process(documents)
for doc in processed_docs:
    print(f"Processed: {doc.processed_text}")
    print(f"Tokens: {doc.tokenized_text}")
    print("---")
```

### Example 7: Content Analysis Pipeline

```python
from pipeline import TextPipeline

# Configure for content analysis
analysis_config = {
    'steps': ['clean', 'analyze'],
    'step_params': {
        'clean': {
            'remove_extra_spaces': True,
            'trim_edges': True,
            'preserve_newlines': True,  # Keep paragraph structure
            'lowercase': False,  # Keep original case for analysis
            'remove_punctuation': False,  # Keep punctuation for sentence analysis
            'remove_stopwords': False  # Keep all words for analysis
        }
    }
}

pipeline = TextPipeline(analysis_config)

# Analyze article content
article = """
Artificial Intelligence (AI) is transforming industries worldwide. 
Companies are investing billions in AI research and development.

The future looks promising for AI applications in healthcare, 
finance, and education sectors.
"""

result = pipeline.process(article)
print(f"Word Count: {result.analysis['word_count']}")
print(f"Sentence Count: {result.analysis['sentence_count']}")
print(f"Paragraph Count: {result.analysis['paragraph_count']}")
print(f"Average Word Length: {result.analysis['average_word_length']:.2f}")
print(f"Reading Level: {result.analysis['reading_level']['difficulty']}")
```

### Example 8: Social Media Text Processing

```python
from pipeline import TextPipeline

# Configure for social media text
social_config = {
    'steps': ['clean', 'transform', 'analyze'],
    'step_params': {
        'clean': {
            'remove_extra_spaces': True,
            'trim_edges': True,
            'lowercase': True,
            'remove_punctuation': True,
            'remove_stopwords': True
        },
        'transform': {
            'remove_numbers': False,  # Keep numbers (mentions, dates)
            'remove_special_chars': False,  # Keep hashtags, mentions
            'apply_stemming': True
        }
    }
}

pipeline = TextPipeline(social_config)

# Process social media posts
posts = [
    "Just had the BEST coffee ever! ☕ #coffee #morning #delicious",
    "Working on my new project. Can't wait to share it! 🚀",
    "Meeting with the team at 3 PM today. Excited! 💼"
]

for post in pipeline.process(posts):
    print(f"Original: {post.processed_text}")
    print(f"Analysis: {post.analysis['word_count']} words, {post.analysis['reading_level']['difficulty']} reading level")
    print("---")
```

### Example 9: Error Handling and Recovery

```python
from pipeline import TextPipeline

# Configure with error handling
error_config = {
    'steps': ['clean', 'transform', 'analyze'],
    'error_handling': 'continue',  # Continue processing even if a step fails
    'step_params': {
        'clean': {
            'remove_extra_spaces': True,
            'trim_edges': True,
            'lowercase': True,
            'remove_punctuation': True,
            'remove_stopwords': True
        }
    }
}

pipeline = TextPipeline(error_config)

# Process text that might cause issues
problematic_text = "This text has some issues but should still process."

try:
    result = pipeline.process(problematic_text)
    print(f"Processed successfully: {result.processed_text}")
    if result.errors:
        print(f"Errors encountered: {result.errors}")
    print(f"Steps applied: {result.steps_applied}")
    print(f"Steps skipped: {result.steps_skipped}")
except Exception as e:
    print(f"Pipeline failed: {e}")
```

### Example 10: Performance Monitoring

```python
from pipeline import TextPipeline
import time

pipeline = TextPipeline(['clean', 'transform', 'analyze'])

# Process multiple texts and monitor performance
texts = [
    "Short text",
    "This is a medium length text with some content to process.",
    "This is a much longer text that contains multiple sentences and paragraphs. It has more complex structure and will take longer to process through all the pipeline steps including cleaning, transformation, and analysis."
] * 10  # Process 30 texts total

start_time = time.time()
results = pipeline.process(texts)
end_time = time.time()

print(f"Processed {len(results)} texts in {end_time - start_time:.2f} seconds")
print(f"Average time per text: {(end_time - start_time) / len(results):.4f} seconds")

# Get pipeline statistics
stats = pipeline.get_statistics()
print(f"Pipeline statistics: {stats}")
```

## Common Use Cases

### 1. **Data Preprocessing for NLP Models**
- Clean and normalize text data before training machine learning models
- Remove noise, standardize format, and prepare features
- Use lemmatization for better model performance

### 2. **Content Analysis and SEO**
- Analyze readability and content quality
- Extract key metrics for content optimization
- Process large volumes of text for insights

### 3. **Social Media Monitoring**
- Process tweets, posts, and comments
- Extract sentiment and topic information
- Clean and normalize user-generated content

### 4. **Document Processing**
- Clean and standardize documents
- Extract structured information
- Prepare text for search and indexing

### 5. **Research and Academic Use**
- Preprocess research papers and articles
- Analyze text complexity and readability
- Extract linguistic features for analysis

## Best Practices

### Configuration Tips
- **For ML preprocessing**: Enable all cleaning and transformation features
- **For content analysis**: Keep original formatting and case
- **For social media**: Preserve hashtags and mentions
- **For documents**: Maintain paragraph structure

### Performance Optimization
- Use batch processing for multiple texts
- Choose appropriate spaCy model size for your needs
- Monitor memory usage with large datasets
- Consider caching results for repeated processing

### Error Handling
- Use `continue` error handling for robust processing
- Monitor error logs for problematic inputs
- Implement validation for input text quality
- Test with edge cases and malformed input

## spaCy Integration

This pipeline leverages spaCy's advanced natural language processing capabilities for sophisticated text processing:

### Features
- **Intelligent Tokenization**: Context-aware tokenization that handles contractions, punctuation, and special cases
- **Advanced Lemmatization**: More sophisticated than traditional stemming, handling irregular forms (e.g., "better" → "good")
- **Smart Stop Word Detection**: Accurate identification of stop words across different contexts
- **Sophisticated Punctuation Handling**: Proper handling of punctuation in various contexts
- **Number Recognition**: Detects both numeric and written numbers (e.g., "twenty", "3rd")

### Model Requirements
- **Primary Model**: `en_core_web_sm` (small English model, ~12MB)
- **Fallback Model**: `en_core_web_lg` (large English model, ~560MB)
- **Graceful Degradation**: Falls back to regex-based processing if spaCy models are unavailable

### Installation
```bash
# Install the small English model (recommended)
python -m spacy download en_core_web_sm

# Or install the large model for better accuracy
python -m spacy download en_core_web_lg
```

### Performance Notes
- spaCy models are loaded once during pipeline initialization
- Processing is optimized for batch operations
- Memory usage scales with model size and text volume

## License

This project is licensed under the MIT License.
