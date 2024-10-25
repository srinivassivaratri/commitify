import os
from dotenv import load_dotenv
import requests
import sys
import subprocess
from colorama import init, Fore, Style
import json
import textwrap

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

    system_message = "You are a git commit message generator. Provide extremely concise and specific messages."
    user_message = f"""Generate {num_options} concise and specific git commit message{'s' if num_options > 1 else ''} for this diff:

Rules:
- Maximum 50 characters
- Use imperative mood
- No period at the end
- Only the message, no labels or numbering
- Be specific about the changes made
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
        content = response_data['choices'][0]['message']['content'].strip()
        
        messages = []
        for line in content.split('\n'):
            line = line.strip()
            if line and not line.startswith(('Here are', 'Subject:', 'Body:', 'Commit Message', '###')):
                clean_line = line.lstrip('0123456789.*- ')
                if len(clean_line) <= 50:  # Ensure message is not longer than 50 characters
                    messages.append(clean_line)
        
        return messages[:num_options]
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        print(f"{Fore.RED}Error parsing API response: {e}")
        return ["Failed to parse commit message"]

def main():
    diff = get_git_diff()
    
    if not diff.strip():
        print(f"{Fore.YELLOW}No changes to commit.")
        return

    print(f"\n{Fore.GREEN}{'=' * 50}")
    print(f"{Fore.GREEN}🤖 {Style.BRIGHT}Welcome to AICommit!{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{'=' * 50}\n")
    
    num_options = int(input(f"{Fore.CYAN}📊 How many commit message options do you want? {Fore.YELLOW}(default: 1) ") or 1)
    use_conventional = input(f"{Fore.CYAN}🏷️  Use Conventional Commits format? {Fore.YELLOW}(y/N) ").lower() == 'y'

    print(f"\n{Fore.CYAN}🧠 Generating your AI commit message(s)...")

    commit_messages = generate_commit_message(diff, num_options, use_conventional)
    
    print(f"\n{Fore.YELLOW}✨ Generated {len(commit_messages)} message(s)")

    if len(commit_messages) > 1:
        for i, message in enumerate(commit_messages, 1):
            print(f"\n{Fore.MAGENTA}{Style.BRIGHT}{message}")
        choice = int(input(f"\n{Fore.YELLOW}🔢 Which option would you like to use? {Fore.CYAN}(1-{len(commit_messages)}) ")) - 1
        commit_message = commit_messages[choice]
    else:
        commit_message = commit_messages[0]
        print(f"\n{Fore.MAGENTA}💡 {Style.BRIGHT}{commit_message}")

    response = input(f"\n{Fore.YELLOW}✅ Would you like to use this commit message? {Fore.CYAN}(Y / n) ").lower()
    
    if response in ['y', '']:
        try:
            subprocess.run(['git', 'commit', '-m', commit_message], check=True)
            commit_hash = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode().strip()
            print(f"\n{Fore.GREEN}{'=' * 50}")
            print(f"{Fore.GREEN}✔️  Commit successful!")
            print(f"{Fore.GREEN}📝 [main {commit_hash}] {Style.BRIGHT}{commit_message}")
            print(f"{Fore.GREEN}{'=' * 50}")
        except subprocess.CalledProcessError:
            print(f"\n{Fore.RED}❌ Commit failed. Check git command or permissions.")
    else:
        print(f"\n{Fore.YELLOW}🚫 Commit cancelled.")

if __name__ == "__main__":
    main()
