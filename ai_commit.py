import os
from dotenv import load_dotenv
import requests
import sys
import subprocess

# Load the API key from .env file
load_dotenv()
PERPLEXITY_API_KEY = os.getenv('PERPLEXITY_API_KEY')

if not PERPLEXITY_API_KEY:
    raise ValueError("No Perplexity API key found. Please set it in your .env file.")

def get_git_diff(max_tokens=100000):  # Set a reasonable token estimate for diff content
    try:
        result = subprocess.run(['git', 'diff', '--cached'], capture_output=True, text=True, check=True)
        # Here we'll estimate tokens crudely by counting characters since exact token count can be complex
        if len(result.stdout) > max_tokens:
            # If the diff is too long, provide a summary or first few lines
            lines = result.stdout.splitlines()
            return '\n'.join(lines[:50]) + '\n\n... (diff truncated for API limits) ...'
        return result.stdout
    except subprocess.CalledProcessError:
        print("Error: No staged changes or git command failed.")
        sys.exit(1)

def generate_commit_message(diff):
    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        'Authorization': f'Bearer {PERPLEXITY_API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        "model": "llama-3.1-sonar-small-128k-online",
        "messages": [
            {"role": "system", "content": "You are an assistant that generates concise git commit messages based on code diffs. If the diff is large, only consider the first part for brevity."},
            {"role": "user", "content": f"Generate a commit message for this diff:\n\n{diff}\n(Note: Diff might be truncated)"}
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code != 200:
        print(f"Failed to generate message. Status code: {response.status_code}")
        print(response.text)
        return "Failed to generate commit message due to API error."
    
    return response.json()['choices'][0]['message']['content'].strip()

def main():
    diff = get_git_diff()
    
    if not diff.strip():
        print("No changes to commit.")
        return

    commit_message = generate_commit_message(diff)
    
    print(f"Generated commit message:\n{commit_message}")

    response = input("\nUse this commit message? (Y/n/edit) ").lower()
    
    if response == 'n':
        commit_message = input("Enter your commit message: ")
    elif response == 'edit':
        commit_message += " " + input("Edit or add to the message: ")
    
    if response in ['y', '']:
        try:
            subprocess.run(['git', 'commit', '-m', commit_message], check=True)
            print("Commit successful.")
        except subprocess.CalledProcessError:
            print("Commit failed. Check the git command or permissions.")
    else:
        print("Commit cancelled.")

if __name__ == "__main__":
    main()
