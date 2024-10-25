import os
from dotenv import load_dotenv
import requests
import sys
import subprocess
from colorama import init, Fore, Back, Style
import json
import textwrap

# Initialize colorama with autoreset
init(autoreset=True)

# Load the API key from .env file
load_dotenv()
PERPLEXITY_API_KEY = os.getenv('PERPLEXITY_API_KEY')

if not PERPLEXITY_API_KEY:
    raise ValueError("No Perplexity API key found. Please set it in your .env file.")

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

    system_message = """You are an AI assistant specialized in generating git commit messages. Your task is to create a concise, specific, and meaningful commit message based on the provided git diff. Follow these rules:
    - Provide a commit title and a description
    - For the title:
        - Use imperative mood (e.g., "Add feature" not "Added feature")
        - Capitalize the first word
        - No period at the end
        - Aim for 50 characters or less
        - Focus on WHAT changed
    - For the description:
        - Explain WHY the change was made
        - Provide context or reasoning behind the change
        - Keep it concise but informative
        - Use complete sentences
    - Separate the title and description with a blank line
    - Do not use any formatting symbols like *, #, or other markdown syntax
    - Do not include any prefixes like "Commit Message", "Title:", or "Description:"
    - Provide ONLY the commit message (title and description), no other text or explanations"""

    user_message = f"Based on this git diff, generate a specific commit message with title and description:\n\n{diff}"

    data = {
        "model": "llama-3.1-sonar-small-128k-online",
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.7,
        "max_tokens": 200
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
    diff = get_git_diff()
    
    if not diff.strip():
        print(f"{Fore.YELLOW}No changes to commit.")
        return

    print(f"\n{Fore.YELLOW}AICommit")
    
    print(f"{Fore.YELLOW}Generating commit message...")

    commit_message = generate_commit_message(diff)
    
    # Clean up the commit message
    lines = commit_message.split('\n')
    title = next((line.strip('*#- ') for line in lines if line.strip()), '')
    description = '\n'.join(line.strip('*#- ') for line in lines[1:] if line.strip())

    print(f"\n{Fore.YELLOW}{title}")
    if description:
        print(f"\n{Fore.YELLOW}{description}")
    
    response = input(f"\n{Fore.YELLOW}(U)se / (E)dit / (C)ancel: ").lower()
    if response == 'c':
        print(f"{Fore.YELLOW}Commit cancelled.")
        return
    elif response == 'e':
        title = input(f"{Fore.YELLOW}Edit title: ")
        print(f"{Fore.YELLOW}Edit description (press Enter twice to finish):")
        lines = []
        while True:
            line = input(f"{Fore.YELLOW}")
            if line:
                lines.append(line)
            else:
                break
        description = '\n'.join(lines)
        commit_message = f"{title}\n\n{description}"

    try:
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        commit_hash = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode().strip()
        print(f"\n{Fore.YELLOW}Commit successful!")
        print(f"{Fore.YELLOW}[{commit_hash}] {title}")
        if description:
            print(f"\n{Fore.YELLOW}{description}")
    except subprocess.CalledProcessError:
        print(f"\n{Fore.RED}Commit failed. Check git command or permissions.")

if __name__ == "__main__":
    main()
