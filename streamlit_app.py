import streamlit as st
import os
import json
from datetime import datetime
import re
import random

# Set page configuration
st.set_page_config(
    page_title="LangChain Prompt Feedback Tool",
    page_icon="✨",
    layout="wide"
)

# App title and description
st.title("✨ Prompt Feedback Tool")
st.markdown("""
This tool helps you improve your prompts for LLMs by providing real-time feedback.
Type your prompt in the text area below and receive instant feedback on its quality.
""")

# Initialize session state for history
if 'history' not in st.session_state:
    st.session_state.history = []

# Handle LangChain imports with compatibility for different versions
try:
    # Try importing from langchain_community (newer versions)
    from langchain_community.chat_models import ChatOpenAI
    from langchain_community.llms import OpenAI
    has_langchain = True
except ImportError:
    try:
        # Try importing from langchain (older versions)
        from langchain.chat_models import ChatOpenAI
        from langchain.llms import OpenAI
        has_langchain = True
    except ImportError:
        has_langchain = False
        if st.sidebar.checkbox("Show LangChain Import Error", value=False):
            st.sidebar.error("""
            Failed to import LangChain modules. The app will use built-in heuristic evaluation only.
            
            If you want to use LLM-based evaluation, install:
            ```
            pip install langchain langchain_community openai
            ```
            """)

# Sidebar for configuration
st.sidebar.title("Configuration")

# API Key input - check for secrets first
api_key = None

# Try to get API key from secrets
try:
    if hasattr(st.secrets, "openai") and "api_key" in st.secrets.openai:
        api_key = st.secrets.openai.api_key
        st.sidebar.success("✅ Using API key from secrets")
    else:
        api_key = st.sidebar.text_input("OpenAI API Key", type="password", 
                                      help="Enter your OpenAI API key. It will not be stored.")
except:
    api_key = st.sidebar.text_input("OpenAI API Key", type="password", 
                                  help="Enter your OpenAI API key. It will not be stored.")

# Feedback criteria selection
st.sidebar.subheader("Feedback Criteria")
clarity = st.sidebar.checkbox("Clarity", value=True, help="Is the prompt clear and specific?")
context = st.sidebar.checkbox("Context", value=True, help="Does it provide necessary context?")
constraints = st.sidebar.checkbox("Constraints", value=True, help="Does it specify constraints?")
examples = st.sidebar.checkbox("Examples", value=True, help="Does it include examples if needed?")
format = st.sidebar.checkbox("Format", value=True, help="Does it specify desired output format?")

# LLM selection
use_llm = st.sidebar.checkbox("Use LLM for advanced feedback", value=has_langchain, 
                             help="Uses an LLM to provide more detailed feedback (requires API key)")

if not has_langchain and use_llm:
    st.sidebar.warning("LangChain is not available. Using heuristic evaluation only.")
    use_llm = False

# LLM model selection (only show if use_llm is checked)
llm_model = "gpt-3.5-turbo"
if use_llm:
    llm_model = st.sidebar.selectbox(
        "Select LLM Model",
        ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"],
        index=0,
        help="Select the OpenAI model to use for feedback"
    )

# Create feedback criteria
criteria = {
    "clarity": clarity,
    "context": context,
    "constraints": constraints,
    "examples": examples,
    "format": format
}

# Main content - two columns layout
col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("Your Prompt")
    prompt_input = st.text_area(
        "Enter your prompt:",
        height=200,
        placeholder="Type your prompt here. For example: Explain the concept of quantum computing to a high school student..."
    )

    # Process button
    process_button = st.button("Get Feedback")

# Standalone implementation of prompt evaluation
class PromptEvaluator:
    """A standalone implementation of prompt evaluation"""
    
    def __init__(self, criteria):
        self.criteria = criteria
    
    def evaluate_prompt(self, prompt):
        """Evaluate a prompt using heuristic methods"""
        result = {
            "score": 0,
            "strengths": [],
            "weaknesses": [],
            "suggestions": [],
            "improvedPrompt": ""
        }
        
        # Skip empty prompts
        if not prompt or len(prompt.strip()) < 5:
            result["score"] = 0
            result["weaknesses"].append("Prompt is too short or empty")
            result["suggestions"].append("Provide a more detailed prompt")
            return result
        
        # Calculate base score
        result["score"] = self._calculate_base_score(prompt)
        
        # Evaluate clarity
        if self.criteria.get("clarity", False):
            self._evaluate_clarity(prompt, result)
        
        # Evaluate context
        if self.criteria.get("context", False):
            self._evaluate_context(prompt, result)
        
        # Evaluate constraints
        if self.criteria.get("constraints", False):
            self._evaluate_constraints(prompt, result)
        
        # Evaluate examples
        if self.criteria.get("examples", False):
            self._evaluate_examples(prompt, result)
        
        # Evaluate format
        if self.criteria.get("format", False):
            self._evaluate_format(prompt, result)
        
        # Generate improved prompt
        result["improvedPrompt"] = self._generate_improved_prompt(prompt, result)
        
        # Ensure score is within bounds
        result["score"] = max(0, min(100, result["score"]))
        
        return result
    
    def _calculate_base_score(self, prompt):
        """Calculate a base score for the prompt"""
        # Start with a base score
        score = 50
        
        # Adjust based on length (too short or too long)
        prompt_length = len(prompt.split())
        if prompt_length < 10:
            score -= 10
        elif prompt_length > 10 and prompt_length <= 30:
            score += 10
        elif prompt_length > 30 and prompt_length <= 100:
            score += 15
        elif prompt_length > 100:
            score -= 5  # Too verbose
        
        # Check for question marks (indicates a clear question)
        if "?" in prompt:
            score += 5
        
        # Check for multiple sentences (indicates detail)
        sentences = len(re.split(r'[.!?]+', prompt))
        if sentences > 1:
            score += 5
        
        # Check for formatting elements
        if re.search(r'bullet|numbered|list|steps|points|format:|output:|return:', prompt, re.IGNORECASE):
            score += 5
        
        return score
    
    def _evaluate_clarity(self, prompt, result):
        """Evaluate the clarity of the prompt"""
        # Check for specific request
        if re.search(r'(explain|describe|what is|how to|why|when|where|who|which)', prompt, re.IGNORECASE):
            result["score"] += 5
            result["strengths"].append("Prompt contains a clear request")
        else:
            result["score"] -= 5
            result["weaknesses"].append("Prompt lacks a clear request")
            result["suggestions"].append("Start with a specific action word like 'explain', 'describe', or 'list'")
        
        # Check for ambiguous terms
        ambiguous_terms = ['thing', 'stuff', 'etc', 'and so on', 'something']
        for term in ambiguous_terms:
            if re.search(r'\b' + term + r'\b', prompt, re.IGNORECASE):
                result["score"] -= 5
                result["weaknesses"].append("Prompt contains ambiguous terms")
                result["suggestions"].append("Replace vague terms like 'thing', 'stuff', or 'etc' with specific descriptions")
                break
    
    def _evaluate_context(self, prompt, result):
        """Evaluate the context provided in the prompt"""
        # Check for context indicators
        context_indicators = [
            r'background', r'context', r'given that', r'assuming', r'in the context of',
            r'for a', r'as a', r'considering', r'taking into account'
        ]
        
        has_context = any(re.search(r'\b' + indicator + r'\b', prompt, re.IGNORECASE) for indicator in context_indicators)
        
        if has_context:
            result["score"] += 10
            result["strengths"].append("Prompt provides context for the request")
        else:
            result["score"] -= 5
            result["weaknesses"].append("Prompt lacks context")
            result["suggestions"].append("Add context about the target audience or situation")
    
    def _evaluate_constraints(self, prompt, result):
        """Evaluate the constraints specified in the prompt"""
        # Check for constraint indicators
        constraint_indicators = [
            r'limit', r'only', r'must', r'should', r'no more than', r'at least',
            r'maximum', r'minimum', r'between', r'not', r'exclude', r'don\'t'
        ]
        
        has_constraints = any(re.search(r'\b' + indicator + r'\b', prompt, re.IGNORECASE) for indicator in constraint_indicators)
        
        if has_constraints:
            result["score"] += 10
            result["strengths"].append("Prompt specifies constraints")
        else:
            result["weaknesses"].append("Prompt doesn't specify constraints")
            result["suggestions"].append("Add constraints like length, format, or specific requirements")
    
    def _evaluate_examples(self, prompt, result):
        """Evaluate if the prompt includes examples"""
        # Check for example indicators
        example_indicators = [
            r'example', r'such as', r'like', r'for instance', r'e\.g\.', 
            r'for example', r'sample', r'illustration'
        ]
        
        has_examples = any(re.search(r'\b' + indicator + r'\b', prompt, re.IGNORECASE) for indicator in example_indicators)
        
        if has_examples:
            result["score"] += 10
            result["strengths"].append("Prompt includes examples")
        else:
            # Only suggest examples for complex topics
            complex_topic_indicators = [
                r'complex', r'technical', r'advanced', r'difficult', r'complicated',
                r'explain', r'concept', r'theory', r'process', r'procedure'
            ]
            
            is_complex = any(re.search(r'\b' + indicator + r'\b', prompt, re.IGNORECASE) for indicator in complex_topic_indicators)
            
            if is_complex:
                result["weaknesses"].append("Prompt could benefit from examples")
                result["suggestions"].append("Include examples to clarify your request")
    
    def _evaluate_format(self, prompt, result):
        """Evaluate if the prompt specifies desired output format"""
        # Check for format indicators
        format_indicators = [
            r'format', r'structure', r'style', r'in the form of', r'as a', 
            r'bullet points', r'numbered list', r'table', r'diagram', r'step by step',
            r'summary', r'essay', r'report', r'analysis', r'review'
        ]
        
        has_format = any(re.search(r'\b' + indicator + r'\b', prompt, re.IGNORECASE) for indicator in format_indicators)
        
        if has_format:
            result["score"] += 10
            result["strengths"].append("Prompt specifies desired output format")
        else:
            result["weaknesses"].append("Prompt doesn't specify desired output format")
            result["suggestions"].append("Specify the desired format (e.g., bullet points, paragraph, step-by-step guide)")
    
    def _generate_improved_prompt(self, original_prompt, result):
        """Generate an improved version of the prompt based on the evaluation"""
        # If there are no weaknesses, return the original prompt
        if not result["weaknesses"]:
            return original_prompt
        
        # Start with the original prompt
        improved_prompt = original_prompt.strip()
        
        # Add missing elements based on weaknesses
        needs_clarity = "Prompt lacks a clear request" in result["weaknesses"]
        needs_context = "Prompt lacks context" in result["weaknesses"]
        needs_constraints = "Prompt doesn't specify constraints" in result["weaknesses"]
        needs_examples = "Prompt could benefit from examples" in result["weaknesses"]
        needs_format = "Prompt doesn't specify desired output format" in result["weaknesses"]
        
        # Simple improvements
        if needs_clarity and not improved_prompt.lower().startswith(("explain", "describe", "what", "how", "why", "when", "where", "who", "which")):
            action_verbs = ["Explain", "Describe", "Provide information about", "Analyze", "Summarize"]
            improved_prompt = f"{random.choice(action_verbs)} {improved_prompt}"
        
        additions = []
        
        if needs_context:
            additions.append("for a general audience")
        
        if needs_constraints:
            additions.append("in a concise manner")
        
        if needs_format:
            formats = ["in bullet points", "in a step-by-step guide", "in a structured paragraph", "with examples"]
            additions.append(random.choice(formats))
        
        # Add the improvements to the prompt
        if additions:
            improved_prompt += " " + " ".join(additions)
        
        # Add a period if missing
        if not improved_prompt.endswith((".", "!", "?")):
            improved_prompt += "."
        
        return improved_prompt

# Function to get feedback using OpenAI API directly
def get_llm_feedback(prompt, criteria, api_key, model="gpt-3.5-turbo"):
    """Get feedback using OpenAI API directly"""
    import openai
    import json
    
    openai.api_key = api_key
    
    # Create a prompt for the LLM
    system_prompt = """
    You are an expert prompt engineer. Evaluate the quality of the given prompt based on the specified criteria.
    Provide a score from 0-100, list strengths, weaknesses, and specific suggestions for improvement.
    Also provide an improved version of the prompt.
    
    Return your response in the following JSON format:
    {
        "score": <score>,
        "strengths": ["strength1", "strength2", ...],
        "weaknesses": ["weakness1", "weakness2", ...],
        "suggestions": ["suggestion1", "suggestion2", ...],
        "improvedPrompt": "<improved version of the prompt>"
    }
    """
    
    # Create a message about which criteria to evaluate
    criteria_message = "Evaluate the prompt based on these criteria: "
    criteria_list = []
    if criteria.get("clarity"):
        criteria_list.append("clarity (is it clear and specific)")
    if criteria.get("context"):
        criteria_list.append("context (does it provide necessary context)")
    if criteria.get("constraints"):
        criteria_list.append("constraints (does it specify limitations or requirements)")
    if criteria.get("examples"):
        criteria_list.append("examples (does it include examples if needed)")
    if criteria.get("format"):
        criteria_list.append("format (does it specify desired output format)")
    
    criteria_message += ", ".join(criteria_list)
    
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"{criteria_message}\n\nPrompt to evaluate: {prompt}"}
            ],
            temperature=0.7,
            max_tokens=800
        )
        
        # Extract the JSON response
        content = response.choices[0].message.content
        
        # Find JSON in the response
        json_match = re.search(r'```json\s*(.*?)\s*```|(\{.*\})', content, re.DOTALL)
        if json_match:
            json_str = json_match.group(1) or json_match.group(2)
            try:
                result = json.loads(json_str)
                return result
            except json.JSONDecodeError:
                pass
        
        # If we couldn't parse JSON, try to extract structured data
        result = {
            "score": 50,  # Default score
            "strengths": [],
            "weaknesses": [],
            "suggestions": [],
            "improvedPrompt": ""
        }
        
        # Try to find score
        score_match = re.search(r'score[:\s]+(\d+)', content, re.IGNORECASE)
        if score_match:
            result["score"] = int(score_match.group(1))
        
        # Try to find strengths
        strengths_section = re.search(r'strengths?:(.*?)(?:weaknesses?:|suggestions?:|improved)', content, re.IGNORECASE | re.DOTALL)
        if strengths_section:
            strengths = re.findall(r'[-*]\s*(.*?)(?:\n|$)', strengths_section.group(1))
            result["strengths"] = [s.strip() for s in strengths if s.strip()]
        
        # Try to find weaknesses
        weaknesses_section = re.search(r'weaknesses?:(.*?)(?:strengths?:|suggestions?:|improved)', content, re.IGNORECASE | re.DOTALL)
        if weaknesses_section:
            weaknesses = re.findall(r'[-*]\s*(.*?)(?:\n|$)', weaknesses_section.group(1))
            result["weaknesses"] = [w.strip() for w in weaknesses if w.strip()]
        
        # Try to find suggestions
        suggestions_section = re.search(r'suggestions?:(.*?)(?:strengths?:|weaknesses?:|improved)', content, re.IGNORECASE | re.DOTALL)
        if suggestions_section:
            suggestions = re.findall(r'[-*]\s*(.*?)(?:\n|$)', suggestions_section.group(1))
            result["suggestions"] = [s.strip() for s in suggestions if s.strip()]
        
        # Try to find improved prompt
        improved_section = re.search(r'improved.*?prompt:?(.*?)(?:$|strengths?:|weaknesses?:|suggestions?:)', content, re.IGNORECASE | re.DOTALL)
        if improved_section:
            result["improvedPrompt"] = improved_section.group(1).strip()
        
        return result
    except Exception as e:
        st.error(f"Error calling OpenAI API: {str(e)}")
        return {
            "score": 0,
            "strengths": [],
            "weaknesses": ["Failed to get LLM feedback"],
            "suggestions": ["Try again or use heuristic evaluation"],
            "improvedPrompt": ""
        }

# Function to get feedback (with caching)
@st.cache_data(ttl=300)
def get_feedback(prompt, criteria_json, use_llm_param, llm_model_param, api_key_param):
    """Get feedback for a prompt with caching"""
    # Convert criteria from JSON string back to dict
    criteria_dict = json.loads(criteria_json)
    
    # Create evaluator
    evaluator = PromptEvaluator(criteria_dict)
    
    # Get heuristic feedback
    heuristic_feedback = evaluator.evaluate_prompt(prompt)
    
    # If LLM feedback is requested and possible
    if use_llm_param and api_key_param and has_langchain:
        try:
            # Set API key
            os.environ["OPENAI_API_KEY"] = api_key_param
            
            # Try using LangChain if available
            chat_model = ChatOpenAI(model=llm_model_param, temperature=0.7)
            
            # Use the chat model to get feedback
            # This is a simplified version - in a real implementation, we'd use a proper chain
            llm_feedback = get_llm_feedback(prompt, criteria_dict, api_key_param, llm_model_param)
            
            # Combine heuristic and LLM feedback, preferring LLM
            return llm_feedback
        except Exception as e:
            st.error(f"Error using LangChain: {str(e)}")
            return heuristic_feedback
    elif use_llm_param and api_key_param:
        # Try direct OpenAI API call
        try:
            return get_llm_feedback(prompt, criteria_dict, api_key_param, llm_model_param)
        except Exception as e:
            st.error(f"Error using OpenAI API: {str(e)}")
            return heuristic_feedback
    else:
        # Use heuristic feedback only
        return heuristic_feedback

# Process the prompt if button is clicked
if process_button:
    if not prompt_input.strip():
        st.error("Please enter a prompt to receive feedback.")
    else:
        if use_llm and not api_key:
            st.error("Please enter your OpenAI API key to use LLM-based feedback.")
        else:
            with st.spinner("Analyzing your prompt..."):
                try:
                    # Convert criteria to JSON string for caching
                    criteria_json = json.dumps(criteria)
                    
                    # Get feedback with caching
                    feedback = get_feedback(
                        prompt_input, 
                        criteria_json, 
                        use_llm, 
                        llm_model if use_llm else None,
                        api_key
                    )
                    
                    # Save to history
                    history_item = {
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "original_prompt": prompt_input,
                        "score": feedback.get("score", 0),
                        "strengths": feedback.get("strengths", []),
                        "weaknesses": feedback.get("weaknesses", []),
                        "suggestions": feedback.get("suggestions", []),
                        "improved_prompt": feedback.get("improvedPrompt", "")
                    }
                    st.session_state.history.append(history_item)
                    
                    # Display feedback in the second column
                    with col2:
                        st.subheader("Prompt Feedback")
                        
                        # Score with color coding
                        score = feedback.get("score", 0)
                        score_color = "red" if score < 50 else "orange" if score < 75 else "green"
                        st.markdown(f"### Score: <span style='color:{score_color}'>{score}/100</span>", unsafe_allow_html=True)
                        
                        # Strengths
                        if strengths := feedback.get("strengths", []):
                            st.markdown("### Strengths:")
                            for strength in strengths:
                                st.markdown(f"- ✅ {strength}")
                        
                        # Weaknesses
                        if weaknesses := feedback.get("weaknesses", []):
                            st.markdown("### Areas for Improvement:")
                            for weakness in weaknesses:
                                st.markdown(f"- 🔍 {weakness}")
                        
                        # Suggestions
                        if suggestions := feedback.get("suggestions", []):
                            st.markdown("### Suggestions:")
                            for suggestion in suggestions:
                                st.markdown(f"- 💡 {suggestion}")
                        
                        # Improved prompt
                        if improved_prompt := feedback.get("improvedPrompt"):
                            st.markdown("### Improved Prompt:")
                            st.text_area("", value=improved_prompt, height=150, disabled=True, key="improved_prompt")
                            if st.button("Use This Improved Prompt"):
                                prompt_input = improved_prompt
                                st.experimental_rerun()
                
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
                    st.error("If you're using LLM-based feedback, please check your API key.")

# Display history in an expander
with st.expander("Prompt History"):
    if st.session_state.history:
        # Add a button to clear history
        if st.button("Clear History"):
            st.session_state.history = []
            st.experimental_rerun()
        
        # Display history items in reverse order (newest first)
        for i, item in enumerate(reversed(st.session_state.history)):
            with st.container():
                st.markdown(f"### Prompt {len(st.session_state.history) - i}")
                st.markdown(f"**Time**: {item['timestamp']}")
                st.markdown(f"**Score**: {item['score']}/100")
                st.markdown(f"**Original**: {item['original_prompt'][:100]}..." if len(item['original_prompt']) > 100 else f"**Original**: {item['original_prompt']}")
                
                # Expandable details
                with st.expander("View Details"):
                    st.markdown("**Original Prompt:**")
                    st.text_area("", value=item['original_prompt'], height=100, disabled=True, key=f"orig_{i}")
                    
                    if item['improved_prompt']:
                        st.markdown("**Improved Prompt:**")
                        st.text_area("", value=item['improved_prompt'], height=100, disabled=True, key=f"imp_{i}")
                        
                        # Button to use this prompt
                        if st.button("Use This Prompt", key=f"use_{i}"):
                            prompt_input = item['improved_prompt']
                            st.experimental_rerun()
                
                st.markdown("---")
    else:
        st.write("No history yet. Get feedback on prompts to build history.")

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit")