# Whispyr AI Interview Problem: Configurable Text Processing Pipeline

## Overview

This problem is designed to assess your problem-solving approach, code organization skills, and programming thinking. You should come to the interview with this question solved.

**Instructions:**
- You may use either Python or JavaScript/TypeScript
- You are allowed and encouraged to use Google, AI assistants, documentation, or any other resources you would normally use while programming
- Focus on demonstrating your problem-solving approach and code organization (there is no specific answer we are looking for)
- Organize your solution into multiple functions and files if you deem this as appropriate

---

## Problem: Configurable Text Processing Pipeline

### Background
You're building a text processing system that can apply multiple transformations to text data in a configurable sequence. The system should be extensible to support new processing steps.

### Requirements

**Core Functionality:**
1. Create a pipeline that can process text through multiple steps:
   - **Clean**: Remove extra whitespace
   - **Transform**: Convert to lowercase, remove punctuation
   - **Analyze**: Count words, characters, sentences
2. Make the pipeline configurable (choose which steps to apply)
3. Support processing single strings or lists of strings
4. Provide summary statistics about the processing results

**Sample Usage:**
```
# Configure pipeline
pipeline = TextPipeline(['clean', 'transform', 'analyze'])

# Process text
text = "  Hello, World!  \n  This is a TEST.  "
result = pipeline.process(text)

# Get statistics
stats = pipeline.get_statistics()
```

**Expected Organization:**
- Separate modules/classes for each processing step
- Pipeline orchestrator that manages the sequence
- Consider how to make adding new steps easy
- Think about data flow between steps

### What We're Looking For

**Problem-Solving Approach:**
- How you design the pipeline architecture
- Your approach to making the system extensible
- How you handle data flow between processing steps
- Code organization and separation of concerns
- Your thinking about configuration and flexibility
- How you structure the different processing modules

**Technical Thinking:**
- Modular design that supports easy extension
- Clean interfaces between components
- Efficient data processing and transformation
- Consideration of different input types and formats

