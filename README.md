# Prompt Feedback Tool

A Streamlit application that provides real-time feedback on prompts for large language models (LLMs). This tool helps users craft more effective prompts by analyzing various aspects of prompt quality and providing suggestions for improvement.

![Prompt Feedback Tool](https://i.imgur.com/YZy1Jb.png)

## Features

- ✅ Real-time prompt quality evaluation
- ✅ Detailed feedback on prompt strengths and weaknesses
- ✅ Suggestions for improvement
- ✅ Improved prompt generation
- ✅ History tracking of previous prompts
- ✅ Support for multiple OpenAI models

## Live Demo

Try the live demo: [Prompt Feedback Tool on Streamlit Cloud](https://prompt-feedback-tool.streamlit.app/)

## How It Works

The tool evaluates prompts based on five key criteria:

1. **Clarity**: Is the prompt clear and specific?
2. **Context**: Does it provide necessary context?
3. **Constraints**: Does it specify constraints?
4. **Examples**: Does it include examples if needed?
5. **Format**: Does it specify desired output format?

For each prompt, the app provides:
- An overall quality score
- Identified strengths
- Areas for improvement
- Specific suggestions
- An improved version of the prompt

## Usage

1. Enter your prompt in the text area
2. Select which criteria to evaluate
3. Choose between heuristic or LLM-based evaluation
4. Click "Get Feedback"
5. Review the feedback and suggestions
6. Use the improved prompt if desired

## Deployment Options

### Option 1: Run Locally

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the app:
   ```
   streamlit run streamlit_app.py
   ```

### Option 2: Deploy on Streamlit Cloud

1. Fork this repository
2. Sign up for [Streamlit Cloud](https://streamlit.io/cloud) using your GitHub account
3. Deploy this app from your forked repository
4. Add your OpenAI API key in the Streamlit Cloud secrets management (optional, for LLM-based feedback)

## Configuration

The app can be configured through the sidebar:

- **API Key**: Enter your OpenAI API key (or configure it in Streamlit Cloud secrets)
- **Feedback Criteria**: Select which aspects of prompts to evaluate
- **LLM Settings**: Choose whether to use LLM-based evaluation and which model to use
- **Debounce Time**: Adjust the responsiveness of the feedback

## Using LLM-Based Feedback

For more detailed feedback, you can enable LLM-based evaluation:

1. Get an [OpenAI API key](https://platform.openai.com/account/api-keys)
2. Enter the key in the sidebar or add it to Streamlit Cloud secrets
3. Check "Use LLM for advanced feedback"
4. Select your preferred model (GPT-3.5-turbo, GPT-4, etc.)

## Heuristic vs. LLM-Based Evaluation

- **Heuristic evaluation**: Uses rule-based algorithms to check basic prompt quality metrics. It's faster and doesn't require an API key.
- **LLM-based evaluation**: Uses an LLM to provide more detailed and contextual feedback. It's more comprehensive but requires an OpenAI API key.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.