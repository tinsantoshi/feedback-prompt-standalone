# Contributing to Prompt Feedback Tool

Thank you for your interest in contributing to the Prompt Feedback Tool! This document provides guidelines for contributions.

## Ways to Contribute

There are several ways you can contribute to this project:

1. **Report bugs**: If you find a bug, please create an issue with a detailed description
2. **Suggest features**: Have an idea for a new feature? Open an issue to discuss it
3. **Improve documentation**: Help improve or translate documentation
4. **Submit code changes**: Fix bugs or add features by submitting pull requests
5. **Share feedback**: Use the tool and let us know how it can be improved

## Development Setup

1. Fork the repository
2. Clone your fork:
   ```
   git clone https://github.com/YOUR_USERNAME/feedback_prompt_1.git
   cd feedback_prompt_1
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the app locally:
   ```
   streamlit run streamlit_app.py
   ```

## Pull Request Process

1. Create a new branch for your feature or bugfix:
   ```
   git checkout -b feature/your-feature-name
   ```
   or
   ```
   git checkout -b fix/your-bugfix-name
   ```

2. Make your changes and test them thoroughly

3. Update documentation if necessary

4. Commit your changes with clear, descriptive commit messages:
   ```
   git commit -m "Add feature: description of your feature"
   ```

5. Push to your fork:
   ```
   git push origin feature/your-feature-name
   ```

6. Submit a pull request to the main repository

## Code Style Guidelines

- Follow PEP 8 style guidelines for Python code
- Use descriptive variable and function names
- Add comments for complex logic
- Write docstrings for functions and classes
- Keep functions focused on a single responsibility

## Improving the Prompt Evaluator

If you want to improve the prompt evaluation logic:

1. The core evaluation logic is in the `PromptEvaluator` class
2. Each criterion has its own evaluation method (e.g., `_evaluate_clarity`)
3. Consider adding new criteria or improving existing ones
4. Make sure to test your changes with various prompts
5. Document any new parameters or behavior

## Adding New Features

Some ideas for new features:

- Support for additional LLM providers
- More detailed analysis of specific prompt types
- Domain-specific prompt templates
- Export/import functionality for prompts
- User accounts and saved preferences
- Batch processing of multiple prompts

## Testing

Before submitting a pull request:

1. Test your changes with various prompts
2. Ensure the app works with and without an API key
3. Check that the UI is responsive on different screen sizes
4. Verify that history functionality works correctly

## Questions?

If you have any questions about contributing, please open an issue for discussion.

Thank you for helping improve the Prompt Feedback Tool!