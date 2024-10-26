# Commitify

AI-powered git commit message generator using Perplexity AI

## Task

Create a tool that automatically generates meaningful and standardized git commit messages based on the staged changes in a git repository.

## Spec

- Use Perplexity AI API for generating commit messages
- Follow Conventional Commits format
- Provide interactive editing of generated messages
- Handle common error scenarios
- Ensure easy setup and usage

## Plan

1. Set up project structure and environment
2. Implement git diff retrieval
3. Integrate Perplexity AI API for message generation
4. Develop user interaction for message review and editing
5. Implement error handling and edge cases
6. Create documentation and usage instructions

## Code

### Setup

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

4. Create a `.env` file in the project root:
   ```
   PERPLEXITY_API_KEY=your_api_key_here
   ```

### Usage

1. Stage your changes:
   ```bash
   git add .
   ```

2. Run Commitify:
   ```bash
   python ai_commit.py
   ```

3. Review the generated commit message:
   - Use it as is
   - Edit it
   - Cancel and write your own

### How It Works

1. Retrieve git diff of staged changes
2. Send diff to Perplexity AI API with instructions
3. Receive generated commit message
4. Allow user to review, edit, or use the message

### Configuration

Set the following in your `.env` file:
- `PERPLEXITY_API_KEY`: Your Perplexity AI API key

### Error Handling

Commitify handles:
- No staged changes
- API connection failures
- Invalid API responses

## Contributing

Contributions are welcome. Please submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
