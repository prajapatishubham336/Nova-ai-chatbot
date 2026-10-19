# Nova-ai-chatbot
Nova AI is an intelligent conversational chatbot built with Python, Streamlit, and Groq API, featuring real-time streaming responses, multiple conversations, and a modern chat interface.

# ✦ Nova AI — Intelligent AI Chatbot

**Nova AI** is a modern, interactive AI chatbot built using **Python, Streamlit, and the Groq API**. It provides a clean conversational interface where users can ask questions, explore ideas, write code, and receive AI-generated responses in real time.

Designed with a minimal interface and a multi-conversation workflow, Nova AI makes interacting with large language models simple, responsive, and accessible.

---

## 🚀 Features

- **AI-Powered Conversations:** Generate helpful, context-aware responses using a language model through the Groq API.
- **Real-Time Streaming:** Display AI responses progressively as they are generated.
- **Multiple Conversations:** Create and switch between separate chat sessions.
- **Conversation Management:** Delete individual conversations or clear the current chat.
- **Automatic Chat Titles:** Generate conversation titles from the user's first message.
- **Conversation Context:** Include previous messages from the active conversation when generating responses.
- **Interactive Chat Interface:** Use Streamlit's native chat messages and chat input components.
- **Suggested Prompts:** Start conversations quickly with built-in example questions.
- **Custom UI Design:** Enjoy a polished interface with custom CSS, sidebar navigation, and responsive styling.
- **Secure API Configuration:** Load the Groq API key from environment variables rather than displaying it in the application interface.
- **Error Handling:** Handle authentication errors, API failures, rate limits, and missing configuration.
- **Markdown Support:** Display formatted AI responses, including code snippets and structured explanations.

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Streamlit | Web application and interactive chat UI |
| Groq API | Access to language model inference |
| OpenAI-compatible Chat Completions API | Generate AI responses through Groq |
| python-dotenv | Load environment variables from a `.env` file |
| UUID | Generate unique conversation identifiers |
| datetime | Record conversation creation timestamps |
| Custom CSS | Style the interface |

---

## 🏗️ How It Works

1. The user opens the Nova AI application.
2. Streamlit initializes the session state and creates a new conversation if needed.
3. The user enters a message or selects a suggested prompt.
4. The application stores the message in the active conversation.
5. The conversation history and system instructions are sent to the configured language model through the Groq API.
6. The model generates a response, which is streamed to the interface.
7. The assistant's response is added to the conversation history.
8. The user can continue the conversation, create another chat, switch between conversations, or clear and delete chats.

### Architecture

```text
User
 |
 v
Streamlit Chat Interface
 |
 v
Session State & Conversation History
 |
 v
System Prompt + Conversation Messages
 |
 v
Groq API Client
 |
 v
Language Model
 |
 v
Streaming AI Response
 |
 v
Chat Interface
```

---

## 📁 Project Structure

```text
nova-ai-chatbot/
│
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── .env                # Private environment variables (not committed)
├── .gitignore          # Files excluded from Git
└── README.md           # Project documentation
```

---

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/prajapatishubham336/nova-ai-chatbot.git
```

Navigate to the project directory:

```bash
cd nova-ai-chatbot
```


### 2. Create a Virtual Environment

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

Create a `requirements.txt` file containing:

```text
streamlit
groq
python-dotenv
```

Install the required packages:

```bash
pip install -r requirements.txt
```

### 4. Configure the Groq API Key

Get your API key from the [Groq Console](https://console.groq.com/).

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Replace `your_groq_api_key_here` with your actual API key.

**Security note:** Never commit your real API key to GitHub. Keep the `.env` file private and use environment variables or your deployment platform's secret manager in production.

### 5. Run the Application

Start the Streamlit server:

```bash
streamlit run app.py
```

Open the local URL shown in the terminal, typically:

```text
http://localhost:8501
```

Nova AI is now ready to use.

---

## 💬 Example Prompts

Try asking Nova AI questions such as:

- Explain machine learning in simple terms.
- Help me build a Python project.
- Prepare interview questions for a data science role.
- Explain a programming concept with code examples.
- Help me debug a Python error.
- Suggest ideas for an AI or machine learning project.

These examples demonstrate possible uses; the quality and accuracy of responses depend on the configured model and API service.

---

## 🔐 Environment Variables

| Variable | Required | Description |
|---|---|---|
| `GROQ_API_KEY` | Yes | API key used to authenticate with Groq |
| `GROQ_MODEL` | No | Optional model setting with a default in the application code |

**Implementation note:** The current `stream_answer()` function explicitly uses `openai/gpt-oss-120b`. Therefore, changing `GROQ_MODEL` in `.env` will not change the active model until the function is updated to use that variable. Confirm that the selected model is available to your Groq account.

---

## 🧠 Conversation Management

Nova AI maintains conversations using Streamlit session state.

Each conversation contains:

- A unique conversation ID.
- A conversation title.
- A list of user and assistant messages.
- A creation timestamp.

Users can create multiple conversations, switch between them, delete individual conversations, and clear the current conversation.

**Current limitation:** Conversations are stored in session state rather than a database. They are not designed for permanent storage across server restarts or independent user accounts. Database-backed persistence can be added in a future version.

---

## ⚠️ Error Handling

Nova AI includes handling for common API issues:

- **Authentication errors:** Check whether the API key is correct.
- **Rate limits:** Wait before making another request if the API limit is reached.
- **API errors:** Check the configured model and Groq service availability.
- **Missing API key:** Configure `GROQ_API_KEY` in your environment.
- **Unexpected errors:** Display a general error message instead of exposing technical details to the user.

---

## 🔒 Security Best Practices

- Store API credentials in environment variables.
- Add `.env` and virtual environment directories to `.gitignore`.
- Never publish API keys, access tokens, or other secrets.
- Configure secrets securely when deploying the application.
- Review error handling before using the application in production.
- Verify important AI-generated information before relying on it.

### Recommended `.gitignore`

```gitignore
# Environment variables
.env
.env.*

# Keep an example configuration file if you add one
!.env.example

# Virtual environments
venv/
.venv/
env/

# Python generated files
__pycache__/
*.py[cod]

# Test and tooling caches
.pytest_cache/
.mypy_cache/

# Operating system files
.DS_Store
Thumbs.db
```

---

## 🚧 Future Enhancements

Potential improvements for future versions include:

- Persistent conversation history using SQLite or PostgreSQL.
- Conversation export and import.
- User authentication and personalized chat history.
- Configurable model selection.
- Chat renaming and search.
- File uploads and document-based question answering.
- Voice input and text-to-speech.
- More granular API error messages and retry handling.
- Deployment with secure environment-variable configuration.
- Automated tests and continuous integration.

These are planned enhancement ideas and are not represented as existing functionality.

---

## 🤝 Contributing

Contributions, suggestions, and bug reports are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Make your changes.
4. Test the application locally.
5. Submit a pull request describing your changes.

Please do not include API keys or other private credentials in contributions.

---

## 📄 License

This project does not currently specify a license. Add a `LICENSE` file before distributing or reusing the code publicly. An open-source license such as the MIT License may be suitable if that matches your intentions.

---

## 👨‍💻 Author

**Shubham Prajapati**

AI/ML Engineer | Machine Learning | Generative AI

GitHub: [@prajapatishubham336](https://github.com/prajapatishubham336)


---

## ⭐ Support

If you find Nova AI useful, consider starring the repository on GitHub.

**Nova AI — Ask questions. Explore ideas. Build something amazing.**
