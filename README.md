# commitify

> AI-powered git commit message generator using Perplexity AI

## Progress

- [x] Initial project setup
- [x] Add Perplexity AI integration
- [x] Implement git diff parsing
  - [x] Focus on specific changes with `--unified=0`
  - [x] Remove surrounding context lines
- [x] Improve commit message generation
  - [x] Limit title to 50 characters
  - [x] Use imperative mood
  - [x] Focus on what/why vs how
- [x] Simplify user interface
  - [x] Remove multiple message options
  - [x] Streamline user prompts
  - [x] Add edit/cancel options

## Setup

1. Clone repo
2. Create `.env` file:
   ```
   PERPLEXITY_API_KEY=your_api_key_here
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

```bash
# Stage changes
git add <files>

# Generate commit message
python ai_commit.py
```

## Features

- Concise, focused commit messages
- Git best practices enforced
- Interactive editing
- Specific change analysis

