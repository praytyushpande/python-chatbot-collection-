# Python Chatbot Collection 🤖

A collection of Python chatbots ranging from simple rule-based systems to more sophisticated conversational agents.

## 📋 Overview

This project contains multiple chatbot implementations:

1. **Simple Chatbot** (`simple_chatbot.py`) - Basic rule-based chatbot using pattern matching
2. **Enhanced Chatbot** (`enhanced_chatbot.py`) - Advanced chatbot with memory and conversation context
3. **NLP Chatbot** (`nlp_chatbot.py`) - Natural language processing chatbot (coming soon)

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- Terminal or command prompt

### Basic Setup
1. Clone or download this project to your local machine
2. Navigate to the project directory:
   ```bash
   cd python-chatbot
   ```

### Running the Simple Chatbot
```bash
python3 simple_chatbot.py
```

**Features:**
- Basic conversation patterns (greetings, questions, etc.)
- Random response selection
- Simple pattern matching
- Exit commands

### Running the Enhanced Chatbot
```bash
python3 enhanced_chatbot.py
```

**Features:**
- Conversation memory and context
- User name recognition and storage
- Session statistics
- Conversation history saving
- Context-aware responses
- Special commands (`stats`)

## 📦 Installation (For Advanced Features)

For the NLP version and additional features, install dependencies:

```bash
# Install optional dependencies
pip3 install -r requirements.txt

# For NLTK (if using NLP features)
python3 -c "import nltk; nltk.download('punkt'); nltk.download('vader_lexicon')"
```

## 💬 Usage Examples

### Simple Chatbot Interaction
```
🤖 ChatBot: Hello! I'm a simple chatbot. Type 'quit' or 'bye' to exit.
==================================================
👤 You: Hello there!
🤖 ChatBot: Hi there! What's on your mind?
👤 You: What's your name?
🤖 ChatBot: My name is ChatBot. What's yours?
👤 You: How are you?
🤖 ChatBot: I'm doing great, thank you for asking!
👤 You: bye
🤖 ChatBot: Goodbye! It was nice chatting with you!
```

### Enhanced Chatbot Interaction
```
🤖 Enhanced ChatBot: Hello! I'm an enhanced chatbot with memory.
   I can remember our conversation and get to know you better!
   Type 'quit', 'bye', or 'stats' for statistics, or just start chatting!
======================================================================
👤 You: Hi, I'm John
🤖 Enhanced ChatBot: Nice to meet you, John! I'll remember that.
👤 You: What's the weather like?
🤖 Enhanced ChatBot: I don't have access to real weather data, but I hope it's nice where you are! How's the weather on your end?
👤 You: stats
📊 Session Stats:
   Duration: 0:01:23
   Messages: 4
   Your name: John
👤 You: Do you remember what I said earlier?
🤖 Enhanced ChatBot: Yes, I remember we talked about that! You said: 'What's the weather like?'
```

## 🔧 Customization

### Adding New Responses
Edit the `responses` dictionary in either chatbot file:

```python
self.responses = {
    'new_category': [
        "Response 1",
        "Response 2",
        "Response 3"
    ]
}
```

### Adding New Patterns
Add regex patterns to detect new intents:

```python
self.patterns = {
    'new_pattern': re.compile(r'\b(keyword1|keyword2)\b', re.IGNORECASE)
}
```

## 📁 File Structure
```
python-chatbot/
├── simple_chatbot.py      # Basic rule-based chatbot
├── enhanced_chatbot.py    # Chatbot with memory and context
├── nlp_chatbot.py         # NLP-powered chatbot (coming soon)
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── conversation_*.json   # Saved conversation logs (generated)
```

## 🎯 Features Comparison

| Feature | Simple | Enhanced | NLP |
|---------|--------|----------|-----|
| Basic Conversation | ✅ | ✅ | ✅ |
| Pattern Matching | ✅ | ✅ | ✅ |
| Conversation Memory | ❌ | ✅ | ✅ |
| User Recognition | ❌ | ✅ | ✅ |
| Context Awareness | ❌ | ✅ | ✅ |
| Session Statistics | ❌ | ✅ | ✅ |
| Conversation Saving | ❌ | ✅ | ✅ |
| Sentiment Analysis | ❌ | ❌ | ✅ |
| Intent Recognition | ❌ | ❌ | ✅ |
| Entity Extraction | ❌ | ❌ | ✅ |

## 🛠️ Advanced Configuration

### Environment Variables
You can set these environment variables for customization:

```bash
export CHATBOT_NAME="YourBotName"
export CHATBOT_SAVE_CONVERSATIONS="true"
export CHATBOT_LOG_LEVEL="INFO"
```

### Conversation Storage
Enhanced chatbot saves conversations as JSON files:
- Location: `conversation_YYYYMMDD_HHMMSS.json`
- Format: Structured JSON with timestamps and metadata

## 🔍 Troubleshooting

### Common Issues

1. **Permission Error**: Make sure Python files are executable
   ```bash
   chmod +x simple_chatbot.py
   chmod +x enhanced_chatbot.py
   ```

2. **Module Not Found**: Ensure you're using Python 3.7+
   ```bash
   python3 --version
   ```

3. **Encoding Issues**: The chatbots use UTF-8 encoding for emoji support

## 📚 Learning Resources

To understand and extend these chatbots:

1. **Python Regex**: Learn about pattern matching with regular expressions
2. **JSON Handling**: Understanding data serialization for conversation storage
3. **Object-Oriented Programming**: Classes and methods in Python
4. **Natural Language Processing**: For advanced chatbot features

## 🎨 Future Enhancements

Planned features:
- [ ] Web interface using Flask
- [ ] Voice input/output capability
- [ ] Integration with external APIs
- [ ] Machine learning-based responses
- [ ] Multi-language support
- [ ] Plugin system for extensions

## 🤝 Contributing

Feel free to fork this project and submit improvements! Some ideas:
- Add new conversation patterns
- Improve response quality
- Add new features
- Fix bugs or optimize performance

## 📄 License

This project is open source and available under the MIT License.

---

**Happy Chatting!** 🎉

For questions or suggestions, feel free to reach out or create an issue in the repository.
