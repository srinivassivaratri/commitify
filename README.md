# commitify

> AI-powered git commit message generator using Perplexity AI

## Progress

To mark a task as complete, replace `[ ]` with `[x]` and add strikethrough to the text.

- [x] ~~Initial project setup~~
- [x] ~~Add Perplexity AI integration~~
- [ ] Implement git diff parsing
  - [x] ~~Focus on specific changes with `--unified=0`~~
  - [x] ~~Remove surrounding context lines~~
- [ ] Improve commit message generation
  - [x] ~~Limit title to 50 characters~~
  - [x] ~~Use imperative mood~~
  - [ ] Focus on what/why vs how
- [x] ~~Simplify user interface~~
  - [x] ~~Remove multiple message options~~
  - [x] ~~Streamline user prompts~~
  - [x] ~~Add edit/cancel options~~

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
3. Change `[ ]` to `[x]`
4. Add strikethrough to the text by wrapping it in `~~`
   Example: `- [x] ~~Completed task~~`
5. Commit and push the changes

This will visually represent completed tasks with both a checked box and strikethrough text.
