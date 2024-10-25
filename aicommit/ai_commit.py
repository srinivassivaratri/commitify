#!/usr/bin/env python3
import os
from dotenv import load_dotenv
import requests
import sys
import subprocess
from colorama import init, Fore, Style
import json
import textwrap
import argparse

# Initialize colorama with autoreset
init(autoreset=True)

# Load the API key from .env file
load_dotenv()
PERPLEXITY_API_KEY = os.getenv('PERPLEXITY_API_KEY')

def get_git_diff():
    try:
        # Get only the specific changes, not the full diff
        result = subprocess.run(['git', 'diff', '--cached', '--unified=0'], capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError:
        print(f"{Fore.RED}Error: No staged changes or the git command failed.")
        sys.exit(1)

def generate_commit_message(diff):
    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        'Authorization': f'Bearer {PERPLEXITY_API_KEY}',
        'Content-Type': 'application/json'
    }

    system_message = """You are an AI assistant specialized in generating git commit messages. Your task is to create concise, specific, and meaningful commit messages based on the provided git diff. Follow these rules strictly:

1. Output Format:
   - Provide ONLY the commit message
   - First line is the title
   - Leave one blank line after the title
   - Following lines are the description
   - Do not include any labels, markdown, or meta-text

2. Title Requirements:
   - Maximum 50 characters
   - Use conventional commits format: type(scope): description
   - Start with one of: feat|fix|docs|style|refactor|test|chore|perf
   - Use imperative mood (Add, not Added)
   - No period at the end
   - Example: "feat(auth): add password reset endpoint"

3. Description Requirements:
   - Maximum 72 characters per line
   - Use complete sentences with proper punctuation
   - Explain WHY the change was made, not what was done
   - Include relevant context and reasoning
   - Mention related issue numbers if applicable
   - Example:
     "Implements password reset functionality to improve user experience.
      Users were frequently requesting this feature through support.
      Closes #123."

4. Content Guidelines:
   - Be specific about what changed
   - Avoid vague terms like "update", "fix", "change"
   - Focus on the business impact or user benefit
   - Mention affected components or modules
   - Note any breaking changes with "BREAKING CHANGE:" prefix

5. What to Exclude:
   - No markdown syntax or formatting
   - No bullet points or lists
   - No technical implementation details
   - No redundant information
   - No meta-text like "Commit Message:" or "Description:"
   - No signatures or timestamps

Example of correct output:
Implement email verification flow

Add email verification step during registration to reduce spam accounts.
This change improves platform security and ensures valid user contact info.
Required by new compliance requirements.
BREAKING CHANGE: requires email verification for all new signups."""

    user_message = f"Based on this git diff, generate a specific commit message:\n\n{diff}"

    data = {
        "model": "llama-3.1-sonar-small-128k-online",
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.7,
        "max_tokens": 300
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        response_data = response.json()
        commit_message = response_data['choices'][0]['message']['content'].strip()
        return commit_message
    except Exception as e:
        print(f"{Fore.RED}Error generating commit message: {e}")
        return "Update code"

def main():
    parser = argparse.ArgumentParser(description="Generate AI-powered commit messages for your git repository.")
    parser.add_argument("--api-key", help="Perplexity API key (overrides .env file)")
    args = parser.parse_args()

    global PERPLEXITY_API_KEY
    if args.api_key:
        PERPLEXITY_API_KEY = args.api_key
    
    if not PERPLEXITY_API_KEY:
        print(f"{Fore.RED}Error: No Perplexity API key found. Please set it in your .env file or use the --api-key option.")
        sys.exit(1)

    print(f"\n{Fore.YELLOW + Style.BRIGHT}AICommit")
    
    diff = get_git_diff()
    if not diff.strip():
        print(f"{Fore.YELLOW + Style.BRIGHT}No changes to commit.")
        return

    print(f"{Fore.YELLOW + Style.BRIGHT}Generating commit message...")
    commit_message = generate_commit_message(diff)
    
    print(f"\n{Fore.YELLOW + Style.BRIGHT}Generated Message:")
    print(f"{Fore.YELLOW + Style.BRIGHT}{commit_message}")
    
    response = input(f"\n{Fore.YELLOW + Style.BRIGHT}(U)se / (E)dit / (C)ancel: ").lower()
    if response == 'c':
        print(f"{Fore.YELLOW + Style.BRIGHT}Commit cancelled.")
        return
    elif response == 'e':
        print(f"{Fore.YELLOW + Style.BRIGHT}Edit commit message (press Enter twice to finish):")
        lines = []
        while True:
            line = input(f"{Fore.YELLOW + Style.BRIGHT}")
            if line:
                lines.append(line)
            else:
                if not lines:  # If the user hasn't entered anything yet, continue
                    continue
                break
        commit_message = '\n'.join(lines)

    try:
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        commit_hash = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode().strip()
        print(f"\n{Fore.YELLOW + Style.BRIGHT}Commit successful!")
        print(f"{Fore.YELLOW + Style.BRIGHT}[{commit_hash}] {commit_message.split('\n')[0]}")
        if len(commit_message.split('\n')) > 1:
            print(f"\n{Fore.YELLOW + Style.BRIGHT}{'\n'.join(commit_message.split('\n')[1:])}")
    except subprocess.CalledProcessError:
        print(f"\n{Fore.RED + Style.BRIGHT}Commit failed. Check git command or permissions.")

if __name__ == "__main__":
    main()
