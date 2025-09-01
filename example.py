#!/usr/bin/env python3
"""Example usage of the text processing pipeline."""

from pipeline import TextPipeline, PipelineConfig


def main():
    """Example usage of the text processing pipeline."""

    print("=== Example 1: Basic Usage ===")
    pipeline = TextPipeline(['clean', 'transform'])

    text = "  Hello, World!  \n  This is a TEST.  "
    result = pipeline.process(text)

    print(f"Original text: {repr(text)}")
    print(f"Processed text: {repr(result.processed_text)}")
    print(f"Analysis: {result.analysis}")
    print(f"Steps applied: {result.steps_applied}")
    print(f"Processing time: {result.processing_time:.4f}s")
    print()

    print("=== Example 2: Custom Configuration ===")
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

    pipeline2 = TextPipeline(config)
    result2 = pipeline2.process("  Multiple\n\n  Lines  ")

    print(f"Original: {repr('  Multiple\n\n  Lines  ')}")
    print(f"Processed: {repr(result2.processed_text)}")
    print(f"Paragraph count: {result2.analysis.get('paragraph_count', 'N/A')}")
    print()

    print("=== Example 3: Batch Processing ===")
    texts = [
        "  First text  ",
        "  Second text  ",
        "  Third text  "
    ]

    results = pipeline.process(texts)
    for i, result in enumerate(results):
        print(f"Text {i+1}: {repr(result.processed_text)}")

    print()
    print("=== Example 4: Error Handling ===")
    try:
        # This will fail because 'invalid_step' doesn't exist
        pipeline3 = TextPipeline(['clean', 'invalid_step', 'analyze'])
    except Exception as e:
        print(f"Configuration error (expected): {e}")

    print()
    print("=== Example 5: Statistics ===")
    stats = pipeline.get_statistics()
    print(f"Total steps executed: {stats['step_count']}")
    print(f"Success rate: {stats['success_rate']:.2%}")
    print(f"Total execution time: {stats['total_execution_time']:.4f}s")


if __name__ == '__main__':
    main()
