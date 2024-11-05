# 🤖 Commitify

A CLI tool that generates meaningful git commit messages using Perplexity AI's powerful language models.

## Why?

Writing good commit messages is hard. They need to be concise yet descriptive, follow conventions, and provide context. Most developers end up with vague messages like "fix bug" or "update code" that make git history useless.

Commitify solves this by automatically analyzing your staged changes and generating high-quality commit messages that:
- Follow conventional commits format
- Include both summary and detailed description
- Provide context about why changes were made
- Maintain consistent style across your repository

## 🚀 Quick Start

1. Install Commitify:
```bash
pip install git+https://github.com/srinivassivaratri/commitify.git
```

2. Add your Perplexity API key to `~/.env`:
```bash
PERPLEXITY_API_KEY=your_api_key_here
```

3. Stage your changes and run:
```bash
ai-commit
```

## 📖 Usage

### Basic Usage
After staging changes with `git add`, simply run:
```bash
ai-commit
```

### Provide API Key via CLI
```bash
ai-commit --api-key your_api_key_here
```

### Interactive Options
After generating a message, you can:
- `U`: Use the message as-is
- `E`: Edit the message before committing
- `C`: Cancel without committing

The generated messages follow conventional commits format:
```
type(scope): description

Detailed explanation of why this change was made
Additional context and impact
```

## 🤝 Contributing

### Setup Development Environment

1. Clone the repo:
```bash
git clone https://github.com/srinivassivaratri/commitify.git
cd commitify
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -e .
pip install -r requirements.txt
```

### Run Tests
```bash
python -m unittest discover tests
```

### Submit Changes
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Open a pull request

## 📄 License

This project is licensed under the MIT License.
