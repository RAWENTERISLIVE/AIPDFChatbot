# Contributing to AI PDF Chatbot

Thank you for your interest in contributing to the AI PDF Chatbot! 🎉

## 🚀 How to Contribute

### 🐛 Reporting Bugs
- Use the GitHub Issues tab
- Include your operating system and version
- Provide steps to reproduce the issue
- Include relevant log files from the `logs/` directory

### 💡 Suggesting Features
- Open an issue with the "enhancement" label
- Describe your use case clearly
- Explain how the feature would benefit users

### 🔧 Code Contributions
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Test thoroughly using `./validate-release.sh`
5. Commit with clear messages
6. Push to your fork
7. Open a Pull Request

## 🛠️ Development Setup

### Prerequisites
- Python 3.8+
- macOS (Linux support coming soon)
- Gemini API key

### Setup
```bash
git clone https://github.com/RAWENTERISLIVE/AIPDFChatbot.git
cd AIPDFChatbot
echo "GEMINI_API_KEY=your_key" > server/.env
./setup-autostart.sh
```

### Testing
```bash
./validate-release.sh  # Validate installation
./status.sh           # Check service status
```

## 📋 Code Standards

### Python Code
- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Include docstrings for functions
- Test your changes thoroughly

### Shell Scripts
- Use bash for compatibility
- Include error handling
- Provide user-friendly output with colors
- Test on macOS

### Documentation
- Update README.md for user-facing changes
- Update relevant .md files
- Include examples where helpful

## 🎯 Priority Areas

We're especially interested in contributions for:
- **Cross-platform support** (Linux, Windows)
- **Performance optimizations**
- **UI/UX improvements**
- **Documentation enhancements**
- **Testing and validation**

## 📞 Questions?

Feel free to open an issue for any questions about contributing!

**Thank you for helping make AI PDF Chatbot better!** 🙏
