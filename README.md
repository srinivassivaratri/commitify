# commitify

> AI-powered git commit message generator using Perplexity AI

## Progress

To mark a task as complete, replace `[ ]` with `[x]`.

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

## Updating Progress

To update the progress:

1. Edit this README.md file
2. Find the task you want to mark as complete
3. Change `[ ]` to `[x]` for that task
4. Commit and push the changes

This will visually update the checkbox in the GitHub interface.
