# Commitify

AI-powered git commit message generator using Perplexity AI.

## Installation

1. Clone the repository:
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

## Usage

After installation, you can use the `ai-commit` command directly in your git repository:

```
ai-commit
```

You can also provide the API key directly:

```
ai-commit --api-key your_api_key_here
```

Alternatively, you can run the script as a module:

```
python -m aicommit
```

Follow the prompts to generate, edit, or use the AI-generated commit message.

## Development

To set up the development environment:

1. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

2. Install the package in editable mode:
   ```
   pip install -e .
   ```

3. Install development dependencies:
   ```
   pip install -r requirements.txt
   ```

## License

This project is licensed under the MIT License.
