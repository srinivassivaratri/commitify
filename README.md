# Commitify

## Task
Create an AI-powered tool that generates meaningful git commit messages automatically using Perplexity AI.

## Spec
- Generate commit messages based on staged git changes
- Provide a command-line interface (CLI) for easy use
- Allow users to edit or cancel the generated message
- Support custom API key input
- Compatible with Python 3.7 and above

## Plan
1. Set up the project structure
2. Implement core functionality:
   - Fetch git diff for staged changes
   - Generate commit message using Perplexity AI
   - Handle user interaction (use/edit/cancel)
3. Create a CLI interface with argparse
4. Package the tool for easy installation and global use

## Code

### Installation

1. Install the package globally:
   ```
   pip install git+https://github.com/srinivassivaratri/commitify.git
   ```

2. Set up your Perplexity API key:
   - Create a `.env` file in your home directory
   - Add your API key: `PERPLEXITY_API_KEY=your_api_key_here`

### Usage

In any git repository, after staging your changes:

```
ai-commit
```

To provide the API key directly:

```
ai-commit --api-key your_api_key_here
```

Follow the prompts to use, edit, or cancel the generated commit message.

### Development

To set up for development:

1. Clone the repository:
   ```
   git clone https://github.com/srinivassivaratri/commitify.git
   cd commitify
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install in editable mode:
   ```
   pip install -e .
   ```

4. Install development dependencies:
   ```
   pip install -r requirements.txt
   ```

## License

This project is under the MIT License.
