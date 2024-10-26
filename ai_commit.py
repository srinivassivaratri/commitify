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
   - No signatures or timestamps"""

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
        
        # Remove the "feat(utility): " part from the title
        lines = commit_message.split('\n')
        title = lines[0]
        if ':' in title:
            title = title.split(':', 1)[1].strip()
        
        # Reconstruct the commit message
        commit_message = f"{title}\n\n" + '\n'.join(lines[2:])
        
        return commit_message
    except Exception as e:
        print(f"{Fore.RED}Error generating commit message: {e}")
        return "Update code"

def get_commit_history(num_commits=10):
    try:
        result = subprocess.run(['git', 'log', f'-{num_commits}', '--pretty=format:%H|%s|%ad', '--date=short'], capture_output=True, text=True, check=True)
        commits = result.stdout.strip().split('\n')
        return [commit.split('|') for commit in commits]
    except subprocess.CalledProcessError:
        print(f"{Fore.RED}Error: Failed to retrieve git commit history.")
        return []

def generate_project_narrative(commits):
    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        'Authorization': f'Bearer {PERPLEXITY_API_KEY}',
        'Content-Type': 'application/json'
    }

    system_message = """You are an AI assistant specialized in creating project narratives from git commit histories. Your task is to weave the commits into a coherent story or timeline of the project's evolution. Follow these guidelines:

1. Create a narrative that highlights key developments, features, and milestones.
2. Group related commits together thematically.
3. Provide insights into the project's progress and direction.
4. Use a professional yet engaging tone.
5. Keep the narrative concise but informative.
6. Highlight any significant changes or pivotal moments in the project's history."""

    commit_history = "\n".join([f"{hash[:7]} - {date} - {message}" for hash, message, date in commits])
    user_message = f"Based on this git commit history, generate a project narrative:\n\n{commit_history}"

    data = {
        "model": "llama-3.1-sonar-small-128k-online",
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.7,
        "max_tokens": 1000
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        response_data = response.json()
        narrative = response_data['choices'][0]['message']['content'].strip()
        return narrative
    except Exception as e:
        print(f"{Fore.RED}Error generating project narrative: {e}")
        return "Failed to generate project narrative."

def main():
    print(f"\n{Fore.YELLOW + Style.BRIGHT}AICommit")
    
    while True:
        print(f"\n{Fore.YELLOW + Style.BRIGHT}Choose an option:")
        print(f"{Fore.YELLOW}1. Generate commit message")
        print(f"{Fore.YELLOW}2. Generate project narrative")
        print(f"{Fore.YELLOW}3. Exit")
        
        choice = input(f"\n{Fore.YELLOW + Style.BRIGHT}Enter your choice (1/2/3): ").strip()
        
        if choice == '1':
            diff = get_git_diff()
            if not diff.strip():
                print(f"{Fore.YELLOW + Style.BRIGHT}No changes to commit.")
                continue

            print(f"{Fore.YELLOW + Style.BRIGHT}Generating commit message...")
            commit_message = generate_commit_message(diff)
            
            # Split the commit message into title and description
            lines = commit_message.split('\n')
            title = lines[0].strip()
            description = '\n'.join(line.strip() for line in lines[2:] if line.strip())

            print(f"\n{Fore.YELLOW + Style.BRIGHT}Generated Message:")
            print(f"{Fore.YELLOW + Style.BRIGHT}{title}")
            if description:
                print(f"\n{Fore.YELLOW + Style.BRIGHT}{description}")
            
            response = input(f"\n{Fore.YELLOW + Style.BRIGHT}(U)se / (E)dit / (C)ancel: ").lower()
            if response == 'c':
                print(f"{Fore.YELLOW + Style.BRIGHT}Commit cancelled.")
                continue
            elif response == 'e':
                while True:
                    title = input(f"{Fore.YELLOW + Style.BRIGHT}Edit title (max 50 chars): ")[:50]
                    if any(title.startswith(prefix) for prefix in ['feat', 'fix', 'docs', 'style', 'refactor', 'test', 'chore', 'perf']):
                        break
                    else:
                        print(f"{Fore.RED}Title must start with one of: feat|fix|docs|style|refactor|test|chore|perf")
                
                print(f"{Fore.YELLOW + Style.BRIGHT}Edit description (max 72 chars per line, press Enter twice to finish):")
                lines = []
                while True:
                    line = input(f"{Fore.YELLOW + Style.BRIGHT}")[:72]
                    if line:
                        lines.append(line)
                    else:
                        break
                description = '\n'.join(lines)
                commit_message = f"{title}\n\n{description}"

            try:
                subprocess.run(['git', 'commit', '-m', commit_message], check=True)
                commit_hash = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode().strip()
                print(f"\n{Fore.YELLOW + Style.BRIGHT}Commit successful!")
                print(f"{Fore.YELLOW + Style.BRIGHT}[{commit_hash}] {title}")
                if description:
                    print(f"\n{Fore.YELLOW + Style.BRIGHT}{description}")
            except subprocess.CalledProcessError:
                print(f"\n{Fore.RED + Style.BRIGHT}Commit failed. Check git command or permissions.")
        
        elif choice == '2':
            num_commits = int(input(f"{Fore.YELLOW + Style.BRIGHT}Enter the number of commits to include in the narrative: "))
            commits = get_commit_history(num_commits)
            if not commits:
                continue

            print(f"{Fore.YELLOW + Style.BRIGHT}Generating project narrative...")
            narrative = generate_project_narrative(commits)
            
            print(f"\n{Fore.YELLOW + Style.BRIGHT}Project Narrative:")
            print(f"{Fore.WHITE}{narrative}")
            
            input(f"\n{Fore.YELLOW + Style.BRIGHT}Press Enter to continue...")
        
        elif choice == '3':
            print(f"{Fore.YELLOW + Style.BRIGHT}Exiting AICommit. Goodbye!")
            break
        
        else:
            print(f"{Fore.RED}Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
