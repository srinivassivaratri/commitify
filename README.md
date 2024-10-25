# commitify

> AI-powered git commit message generator using Perplexity AI

## Progress

- [ ] Initial project setup
- [ ] Add Perplexity AI integration
- [ ] Implement git diff parsing
  - [ ] Focus on specific changes with `--unified=0`
  - [ ] Remove surrounding context lines
- [ ] Improve commit message generation
  - [ ] Limit title to 50 characters
  - [ ] Use imperative mood
  - [ ] Focus on what/why vs how
- [ ] Simplify user interface
  - [ ] Remove multiple message options
  - [ ] Streamline user prompts
  - [ ] Add edit/cancel options

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

☑️ Concise, focused commit messages
☑️ Git best practices enforced
☑️ Interactive editing
☑️ Specific change analysis
