# commitify

> AI-powered git commit message generator using Perplexity AI

## Project Journey

1. [x] Project Initialization
   - [x] Create a new directory for the project
   - [x] Initialize a Git repository
   - [x] Set up a virtual environment

2. [x] Environment Setup
   - [x] Create a `.env` file for API key storage
   - [x] Install required packages
   - [x] Create `requirements.txt` file

3. [x] Core Functionality Implementation
   - [x] Implement git diff parsing
     - [x] Use `git diff --cached --unified=0` for specific changes
   - [x] Integrate Perplexity AI API
   - [x] Develop commit message generation logic

4. [x] User Interface Development
   - [x] Create a command-line interface
   - [x] Implement colorized output using colorama
   - [x] Add options to use, edit, or cancel generated messages

5. [x] Code Refinement
   - [x] Optimize commit message generation
   - [x] Improve error handling
   - [x] Enhance code readability and structure

6. [x] Testing and Iteration
   - [x] Test with various git diffs
   - [x] Refine commit message quality based on results

7. [x] Documentation
   - [x] Write comprehensive README.md
   - [x] Document setup process
   - [x] Explain usage instructions

8. [ ] Final Touches
   - [ ] Perform final code review
   - [ ] Ensure all features are working as expected
   - [ ] Prepare for public release

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/commitify.git
   cd commitify
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root and add your Perplexity AI API key:
   ```
   PERPLEXITY_API_KEY=your_api_key_here
   ```

## Usage

1. Stage your changes:
   ```bash
   git add .
   ```

2. Run commitify:
   ```bash
   python ai_commit.py
   ```

3. Choose an option:
   - Generate a commit message
   - Generate a project narrative
   - Exit

4. For commit messages:
   - Review the generated message
   - Use it as is, edit it, or cancel and write your own

5. For project narratives:
   - Specify the number of recent commits to include
   - Review the generated narrative

The project narrative feature creates a story from your recent commits, providing insights into your project's evolution. This can be particularly useful for onboarding new team members or conducting project retrospectives.

## Features

- Generates concise, focused commit messages
- Enforces git best practices
- Provides interactive editing
- Performs specific change analysis
- Generates project narratives from commit history

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
