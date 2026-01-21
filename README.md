# DiamondCLI 💎 - Autonomous Refactoring Agent

![Python](https://img.shields.io/badge/Python-3.11%2B-blue?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Gemini API](https://img.shields.io/badge/AI-Gemini%202.0%20Flash-orange?style=for-the-badge&logo=google-gemini)

## 📖 Description

**DiamondCLI** is a powerful, Python-based autonomous agent designed to orchestrate large-scale code refactoring. Powered by **Google's Gemini 2.0 Flash**, it scans your repositories, detects legacy patterns, and intelligently upgrades code to the "Diamond Standard".

## ✨ Key Features

- **Self-Healing Code**: Automatically detects and fixes issues.
- **Strict Typing Enforcement**: Adds type hints to Python and TypeScript files.
- **Automated Pull Requests**: Commits changes and opens PRs on GitHub autonomously.
- **Multi-Repo Batch Processing**: Seamlessly handles multiple repositories in a single run.
- **JSDoc & Docstrings**: Ensures comprehensive documentation for every function and class.

## 🚀 Usage

### Prerequisites

- Python 3.11+
- Git
- GitHub CLI (`gh`) authenticated

### Installation

1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your environment variables:
   Create a `.env` file and add your Gemini API key:
   ```env
   GEMINI_API_KEY=your_api_key_here
   ```

### Running the Agent

Execute the manager script to start the autonomous refactoring process:

```bash
python main.py
```

The agent will:

1. Scan for repositories in the parent directory.
2. Create a new branch `diamond-auto`.
3. Refactor code files (`.py`, `.ts`, `.tsx`).
4. Commit changes and open a Pull Request.

---

_Built with ❤️ by the Autonomous Agent Team._
