ChatterBox

This is a minimal red-themed website called ChatterBox (frontend + Node/Express backend) that forwards messages to a language model. The UI uses a "canary red" palette (brighter canary red accents and deeper red shapes) and a glassy card for a modern look. You can edit `public/style.css` variables at the top to change colors.

Quickstart (Windows PowerShell):

1. Open PowerShell and cd into the project folder:
   cd "c:\Users\User\OneDrive\Desktop\2025 Fall\Cs 360 Software Engineering\simple-chatgpt-site"

2. Install dependencies:
   npm install

3. Start the server. You have three simple options:

- OpenAI (if you have an OpenAI key):
    $env:OPENAI_API_KEY = 'YOUR_OPENAI_KEY'; npm start

- Hugging Face Inference API (free tier available):
    # sign up at https://huggingface.co, create an access token (Settings → Access Tokens)
    $env:HUGGINGFACE_API_KEY = 'hf_xxx'; npm start

  You can optionally set a model (default: `gpt2`) before starting:
    $env:HUGGINGFACE_MODEL = 'gpt2'; $env:HUGGINGFACE_API_KEY = 'hf_xxx'; npm start

- Mock mode (no API keys required; best for classrooms):
    $env:USE_MOCK = 'true'; npm start

4. Open http://localhost:3000 in your browser and type a message.

Behavior notes:
- The server prefers OpenAI when `OPENAI_API_KEY` is set.
- If OpenAI is not configured and you set `HUGGINGFACE_API_KEY`, the server will forward messages to the Hugging Face Inference API and return generated text from the selected model.
- If neither API key is available or calls fail, the server falls back to a safe mock reply so students can still experiment without any keys or cost.

Notes / caveats:
- Keep your API keys secret. Don't commit them to Git or share publicly.
- Hugging Face free-tier is good for experimentation but may be slower and rate limited. Model availability and latency vary.
- For classroom demos the mock mode (`USE_MOCK=true`) is the simplest no-cost option.

Environment variables the project respects:
 - OPENAI_API_KEY (optional)
 - HUGGINGFACE_API_KEY (optional)
 - HUGGINGFACE_MODEL (optional, default: gpt2)
 - USE_MOCK (optional, set to 'true' to force mock replies)
