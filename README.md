# Commitify

## Task
Create an AI-powered tool that generates meaningful git commit messages automatically.

## Spec
- Use Perplexity AI to generate commit messages
- Provide a command-line interface (CLI) for easy use
- Allow users to edit or cancel the generated message
- Support custom API key input

## Plan
1. Set up the project structure
2. Implement the core functionality:
   - Get git diff
   - Generate commit message using Perplexity AI
   - Handle user interaction
3. Create a CLI interface
4. Package the tool for easy installation

## Code

### Installation

1. Clone the repo:
   ```
   git clone https://github.com/your_username/commitify.git
   cd commitify
   ```

2. Install the package:
   ```
   pip install -e .
   ```

3. Set up your Perplexity API key:
   - Create a `.env` file in your home directory or project root
   - Add your API key: `PERPLEXITY_API_KEY=your_api_key_here`

### Usage

In your git repository, after staging your changes:

```
ai-commit
```

To provide the API key directly:

```
ai-commit --api-key your_api_key_here
```

### Development

To set up for development:

1. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

2. Install in editable mode:
   ```
   pip install -e .
   ```

3. Install dev dependencies:
   ```
   pip install -r requirements.txt
   ```

## License

This project is under the MIT License.
