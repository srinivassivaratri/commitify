import os
from dotenv import load_dotenv
import requests
import sys
import subprocess
from colorama import init, Fore, Style
import json

# Initialize colorama
init(autoreset=True)

# Load the API key from .env file
load_dotenv()
PERPLEXITY_API_KEY = os.getenv('PERPLEXITY_API_KEY')

if not PERPLEXITY_API_KEY:
    raise ValueError("No Perplexity API key found. Please set it in your .env file.")

def get_git_diff():
    try:
        result = subprocess.run(['git', 'diff', '--cached'], capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError:
        print(f"{Fore.RED}Error: No staged changes or the git command failed.")
        sys.exit(1)

def generate_commit_message(diff, num_options=1, use_conventional=False):
    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        'Authorization': f'Bearer {PERPLEXITY_API_KEY}',
        'Content-Type': 'application/json'
    }

    system_message = "You are a git commit message generator. Provide extremely concise messages."
    user_message = f"""Generate {num_options} concise git commit message{'s' if num_options > 1 else ''} for this diff:

Rules:
- Maximum 50 characters
- Use imperative mood
- No period at the end
- Only the message, no labels or numbering
{'- Use Conventional Commits format' if use_conventional else ''}

Diff:
{diff}
"""

    data = {
        "model": "llama-3.1-sonar-small-128k-online",
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}Error making API request: {e}")
        return ["Failed to generate commit message"]

    try:
        response_data = response.json()
        print(f"{Fore.YELLOW}API Response: {json.dumps(response_data, indent=2)}")
        content = response_data['choices'][0]['message']['content'].strip()
        messages = [msg.strip() for msg in content.split('\n') if msg.strip() and not msg.strip().startswith(('Subject:', 'Body:', 'Commit Message', '###'))]
        return messages[:num_options]
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        print(f"{Fore.RED}Error parsing API response: {e}")
        print(f"{Fore.YELLOW}Raw response: {response.text}")
        return ["Failed to parse commit message"]

def main():
    diff = get_git_diff()
    
    if not diff.strip():
        print(f"{Fore.YELLOW}No changes to commit.")
        return

    print(f"{Fore.GREEN}Welcome to AICommit!")
    
    num_options = int(input(f"{Fore.CYAN}How many commit message options do you want? (default: 1) ") or 1)
    use_conventional = input(f"{Fore.CYAN}Use Conventional Commits format? (y/N) ").lower() == 'y'

    print(f"{Fore.CYAN}Generating your AI commit message(s)...")

    commit_messages = generate_commit_message(diff, num_options, use_conventional)
    
    print(f"{Fore.YELLOW}Generated {len(commit_messages)} message(s)")

    if len(commit_messages) > 1:
        for i, message in enumerate(commit_messages, 1):
            print(f"\n{Fore.MAGENTA}{i}. {Style.BRIGHT}{message}")
        choice = int(input(f"\n{Fore.YELLOW}Which option would you like to use? (1-{len(commit_messages)}) ")) - 1
        commit_message = commit_messages[choice]
    else:
        commit_message = commit_messages[0]
        print(f"\n{Fore.MAGENTA}{Style.BRIGHT}{commit_message}")

    response = input(f"\n{Fore.YELLOW}Would you like to use this commit message? (Y / n) ").lower()
    
    if response in ['y', '']:
        try:
            subprocess.run(['git', 'commit', '-m', commit_message], check=True)
            commit_hash = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode().strip()
            print(f"{Fore.GREEN}[main {commit_hash}] {Style.BRIGHT}{commit_message}")
        except subprocess.CalledProcessError:
            print(f"{Fore.RED}Commit failed. Check git command or permissions.")
    else:
        print(f"{Fore.YELLOW}Commit cancelled.")

if __name__ == "__main__":
    main()
