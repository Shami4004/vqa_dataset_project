import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise Exception("API key not loaded. Please check your .env file or export the variable.")

client = Groq(api_key=api_key)

domain = "Physics"
subdomain = "Optics"
language = "Arabic"

prompt = f"""
You're a research assistant helping a team collect hard-to-find annotated images (with embedded text in the image) for machine learning dataset training.

Please return 3–5 rare or underused websites, galleries, or archives for:
- Domain: {domain}
- Subdomain: {subdomain}
- Language focus: {language}

Each result should include:
- A direct URL
- A one-line description
- Why it's a unique or uncommon visual source
Return only in JSON format like this:
[
  {{
    "url": "https://example.com",
    "desc": "Archived chemistry diagrams from 1960s",
    "reason": "Not indexed by mainstream search engines"
  }},
  ...
]
"""

chat_completion = client.chat.completions.create(
    messages=[{"role": "user", "content": prompt}],
    model="llama3-70b-8192"
)

print(chat_completion.choices[0].message.content.strip())