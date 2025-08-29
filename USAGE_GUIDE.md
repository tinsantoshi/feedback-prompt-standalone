# How to Use the Prompt Feedback Tool Effectively

This guide provides tips and best practices for getting the most out of the Prompt Feedback Tool.

## Getting Started

1. **Enter your prompt** in the text area on the left side of the screen
2. **Select evaluation criteria** in the sidebar:
   - Clarity: Is the prompt clear and specific?
   - Context: Does it provide necessary context?
   - Constraints: Does it specify constraints?
   - Examples: Does it include examples if needed?
   - Format: Does it specify desired output format?
3. **Choose evaluation method**:
   - Heuristic evaluation: Fast, rule-based analysis (no API key needed)
   - LLM-based evaluation: More detailed feedback (requires OpenAI API key)
4. **Click "Get Feedback"** to analyze your prompt
5. **Review the feedback** on the right side of the screen
6. **Use the improved prompt** if provided

## Understanding the Feedback

### Score

The score (0-100) represents the overall quality of your prompt based on the selected criteria:
- **0-49**: Needs significant improvement
- **50-74**: Good but could be better
- **75-100**: Excellent prompt

### Strengths

These are aspects of your prompt that are well-crafted. Try to maintain these strengths when revising your prompt.

### Areas for Improvement

These highlight specific weaknesses in your prompt that could be addressed to make it more effective.

### Suggestions

Concrete recommendations for improving your prompt. These are actionable steps you can take to address the identified weaknesses.

### Improved Prompt

An AI-generated improved version of your prompt that addresses the identified weaknesses. You can use this as a starting point for your revised prompt.

## Tips for Writing Effective Prompts

### 1. Be Clear and Specific

- Start with action verbs like "explain," "describe," or "analyze"
- Clearly state what you want the AI to do
- Avoid vague terms like "thing," "stuff," or "etc."

Example:
- ❌ "Tell me about AI"
- ✅ "Explain the key concepts of artificial intelligence and its current applications in healthcare"

### 2. Provide Context

- Specify the target audience or situation
- Include relevant background information
- Mention your level of familiarity with the topic

Example:
- ❌ "Explain quantum computing"
- ✅ "Explain quantum computing to a high school student with basic physics knowledge"

### 3. Specify Constraints

- Set limits on length, scope, or complexity
- Mention any specific requirements or exclusions
- Indicate time periods or geographical focus if relevant

Example:
- ❌ "Write about climate change"
- ✅ "Write a 500-word summary of climate change impacts, focusing only on coastal regions in the past decade"

### 4. Include Examples

- Provide examples to clarify your request
- Show sample formats or styles you prefer
- Reference specific cases or scenarios

Example:
- ❌ "Give me programming tips"
- ✅ "Give me programming tips for improving Python code readability, such as using descriptive variable names like 'customer_name' instead of 'cn'"

### 5. Specify Format

- Indicate how you want the information structured
- Mention if you want bullet points, paragraphs, tables, etc.
- Specify any sections or headings you want included

Example:
- ❌ "Explain the benefits of exercise"
- ✅ "Explain the benefits of exercise in a numbered list, with each point containing a benefit and a brief explanation"

## Advanced Usage

### Using History

The app keeps track of your prompt history. You can:
- View previous prompts and their scores
- See detailed feedback for each prompt
- Reuse improved prompts from your history

### Combining with Other Tools

For best results, use this tool as part of your prompt engineering workflow:
1. Draft your initial prompt
2. Get feedback using this tool
3. Revise based on suggestions
4. Test the improved prompt with your target LLM
5. Iterate as needed

## Examples of Before and After

### Example 1: Vague Request

**Before:**
```
Tell me about space exploration.
```

**After:**
```
Explain the major milestones in space exploration from 1950 to present day, highlighting key missions and their scientific contributions. Include examples of both manned and unmanned missions. Present the information in chronological order with separate sections for each decade.
```

### Example 2: Missing Context

**Before:**
```
How do I fix a bug in my code?
```

**After:**
```
As a junior Python developer working on a web application, I'm encountering a bug where my database connection closes unexpectedly during long operations. Explain step-by-step debugging approaches I should take to identify the root cause, with examples of common solutions for database connection issues in Python web applications.
```

### Example 3: Lack of Format Specification

**Before:**
```
Explain machine learning algorithms.
```

**After:**
```
Explain the top 5 machine learning algorithms used in data science for a technical audience with basic statistics knowledge. For each algorithm, provide: 1) a brief description, 2) typical use cases, 3) advantages, and 4) limitations. Format this as a structured guide with clear headings and bullet points for easy reference.
```

## Conclusion

By following these guidelines and using the feedback from this tool, you can craft more effective prompts that yield better results from large language models. Remember that prompt engineering is an iterative process - continue refining your prompts based on the feedback and results you receive.