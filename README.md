# Configurable Text Processing Pipeline

A flexible, extensible text processing system that can apply multiple transformations to text data in a configurable sequence.

## Features

- **Configurable Pipeline**: Choose which processing steps to apply
- **Extensible Architecture**: Easy to add new processing steps
- **Multiple Input Types**: Process single strings or lists of strings
- **Rich Statistics**: Detailed processing statistics and analysis
- **Beautiful CLI**: Command-line interface with rich formatting
- **Error Handling**: Configurable error handling strategies

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

### 2. Transform Step
- Converts to lowercase
- Removes punctuation
- Removes numbers (optional)
- Removes special characters (optional)

### 3. Analyze Step
- Counts words, characters, sentences, paragraphs
- Calculates average word length
- Provides reading level analysis

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
            'trim_edges': True
        },
        'transform': {
            'to_lowercase': True,
            'remove_punctuation': True,
            'remove_numbers': False
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
            "trim_edges": true
        },
        "transform": {
            "to_lowercase": true,
            "remove_punctuation": true,
            "remove_numbers": false
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

### Example 1: Basic Text Processing

```python
from pipeline import TextPipeline

pipeline = TextPipeline(['clean', 'transform', 'analyze'])
text = "  Hello, World!  \n  This is a TEST.  "
result = pipeline.process(text)

print(f"Original: {repr(text)}")
print(f"Processed: {repr(result.processed_text)}")
print(f"Word count: {result.analysis['word_count']}")
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

### Example 3: Custom Configuration

```python
config = {
    'steps': ['clean', 'analyze'],
    'error_handling': 'stop',
    'step_params': {
        'clean': {
            'remove_extra_spaces': True,
            'preserve_newlines': True
        }
    }
}

pipeline = TextPipeline(config)
```

## License

This project is licensed under the MIT License.
