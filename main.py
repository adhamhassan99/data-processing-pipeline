#!/usr/bin/env python3
"""Main entry point for the text processing pipeline."""

import click
import json
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from pipeline import TextPipeline, PipelineConfig

console = Console()


@click.command()
@click.argument('text', required=False)
@click.option('--config', '-c', help='Configuration file path (JSON)')
@click.option('--steps', '-s', help='Comma-separated list of steps to apply')
@click.option('--error-handling', '-e', type=click.Choice(['continue', 'stop']), default='continue', help='Error handling strategy')
@click.option('--interactive', '-i', is_flag=True, help='Interactive mode')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def main(text, config, steps, error_handling, interactive, verbose):
    """Text Processing Pipeline - Process text through configurable steps."""

    try:
        # Load configuration
        pipeline_config = _load_config(config, steps, error_handling)

        # Create pipeline
        pipeline = TextPipeline(pipeline_config)

        if interactive:
            _run_interactive(pipeline)
        else:
            if not text:
                console.print(
                    "[red]Error: Text input required unless using interactive mode[/red]")
                return

            _process_text(pipeline, text, verbose)

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        if verbose:
            console.print_exception()


def _load_config(config_file, steps, error_handling):
    """Load pipeline configuration."""
    if config_file:
        with open(config_file, 'r') as f:
            config_data = json.load(f)
    else:
        config_data = {}

    # Override with command line options
    if steps:
        config_data['steps'] = [s.strip() for s in steps.split(',')]
    if error_handling:
        config_data['error_handling'] = error_handling

    return PipelineConfig(**config_data)


def _run_interactive(pipeline):
    """Run the pipeline in interactive mode."""
    console.print(
        Panel.fit("Text Processing Pipeline - Interactive Mode", style="blue"))

    while True:
        try:
            text = console.input(
                "\n[green]Enter text to process (or 'quit' to exit):[/green] ")

            if text.lower() in ['quit', 'exit', 'q']:
                break

            if text.strip():
                _process_text(pipeline, text, verbose=True)
            else:
                console.print("[yellow]Please enter some text.[/yellow]")

        except KeyboardInterrupt:
            console.print("\n[yellow]Exiting...[/yellow]")
            break
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")


def _process_text(pipeline, text, verbose=False):
    """Process text through the pipeline and display results."""
    console.print(
        f"\n[blue]Processing text:[/blue] {text[:100]}{'...' if len(text) > 100 else ''}")

    # Process the text
    result = pipeline.process(text)

    # Display results
    _display_results(result, verbose)


def _display_results(result, verbose=False):
    """Display processing results in a formatted way."""
    # Create results table
    table = Table(title="Processing Results", show_header=True,
                  header_style="bold magenta")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")

    # Add basic results
    table.add_row("Processed Text", result.processed_text[:100] + (
        '...' if len(result.processed_text) > 100 else ''))
    table.add_row("Tokenized Text", ", ".join(result.tokenized_text))
    table.add_row("Steps Applied", ", ".join(result.steps_applied))
    table.add_row("Steps Skipped", ", ".join(result.steps_skipped)
                  if result.steps_skipped else "None")
    table.add_row("Processing Time", f"{result.processing_time:.4f}s")

    # Add analysis results
    for key, value in result.analysis.items():
        table.add_row(key.replace('_', ' ').title(), str(value))

    console.print(table)
    # Display errors if any
    if result.errors:
        console.print("\n[red]Errors encountered:[/red]")
        for error in result.errors:
            console.print(f"  • {error}")

    # Display full text if verbose
    if verbose:
        console.print(
            f"\n[blue]Full processed text:[/blue]\n{result.processed_text}")


if __name__ == '__main__':
    main()
