# Infosys_BizHacks2025_AgenticAI

Problem Statement: 


🔑 Getting a Groq API Key
Go to https://console.groq.com/keys.

Sign in and create a new Custom API Key.

Copy the generated key.

🛠️ Replacing the API Key
Open the api_key.py file and replace the placeholder with your new key:

```python
GROQ_API_KEY = "your-api-key-here"
```

Make sure not to commit your key to version control if this file is tracked. Add it to .gitignore or use environment variables for better security.