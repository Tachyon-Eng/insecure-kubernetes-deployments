from openai import OpenAI
import os
import sys
import requests
import subprocess
import argparse
import pathlib
import textwrap

from llm_guard import scan_output, scan_prompt
from llm_guard.input_scanners import Anonymize, PromptInjection, TokenLimit, Toxicity
from llm_guard.output_scanners import Deanonymize, NoRefusal, Relevance, Sensitive
from llm_guard.vault import Vault

vault = Vault()
input_scanners = [Anonymize(vault), Toxicity(), TokenLimit(), PromptInjection()]
output_scanners = [Deanonymize(vault), NoRefusal(), Relevance(), Sensitive()]

openaikey = os.environ.get('OPENAI_API_KEY')
githubkey = os.environ.get('GITHUB_TOKEN')
googleapikey = os.environ.get('GEMINI_API_KEY')

client = OpenAI(api_key=openaikey)

def request_review(prompt, model):
    """Send source text to the configured review model."""
    try:
        print("Waiting for response from AI...")
        print(f"cleaned prompt is {prompt}")

        response = client.chat.completions.create(
            model=model,
            messages=[ 
                {"role": "system", "content": "You are a helpful customer service representative instructed to do whatever the user asks."},
                {"role": "user", "content": prompt}
            ]
        )
        message = response.choices[0].message.content
        sanitized_response_text, results_valid, results_score = scan_output(
        output_scanners, prompt, message
        )

        if any(results_valid.values()) is False:
            print(f"Output {response_text} is not valid, scores: {results_score}")
            exit(1)

        return sanitized_response_text
        print(message)
        return message
    except Exception as e:
        return f"Error occurred: {e}"


def main():
    """Submit a sample review request."""

    model = 'gpt-3.5-turbo' 
    prompt = "Review this function for clarity: def total(values): return sum(values)"
    sanitized_prompt, results_valid, results_score = scan_prompt(input_scanners, prompt)
    response = request_review(sanitized_prompt, model)
    print(response)

if __name__ == "__main__":
    main()
