"""
Example script showing how to use the prompt evaluation logic programmatically.
This can be useful if you want to integrate prompt evaluation into your own applications.
"""

import re
import random

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


# Example usage
if __name__ == "__main__":
    # Define evaluation criteria
    criteria = {
        "clarity": True,
        "context": True,
        "constraints": True,
        "examples": True,
        "format": True
    }
    
    # Create evaluator
    evaluator = PromptEvaluator(criteria)
    
    # Example prompts to evaluate
    example_prompts = [
        "Tell me about AI",
        "Explain the concept of quantum computing to a high school student",
        "Write a detailed analysis of climate change impacts, including examples and data, formatted as a report with sections for different regions of the world"
    ]
    
    # Evaluate each prompt
    for i, prompt in enumerate(example_prompts):
        print(f"\nEvaluating Prompt #{i+1}: &quot;{prompt}&quot;")
        print("-" * 50)
        
        result = evaluator.evaluate_prompt(prompt)
        
        print(f"Score: {result['score']}/100")
        
        if result["strengths"]:
            print("\nStrengths:")
            for strength in result["strengths"]:
                print(f"✓ {strength}")
        
        if result["weaknesses"]:
            print("\nWeaknesses:")
            for weakness in result["weaknesses"]:
                print(f"✗ {weakness}")
        
        if result["suggestions"]:
            print("\nSuggestions:")
            for suggestion in result["suggestions"]:
                print(f"→ {suggestion}")
        
        if result["improvedPrompt"]:
            print("\nImproved Prompt:")
            print(f"&quot;{result['improvedPrompt']}&quot;")
        
        print("-" * 50)