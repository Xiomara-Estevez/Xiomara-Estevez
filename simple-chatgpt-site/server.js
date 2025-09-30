const express = require('express');
const fetch = require('node-fetch');
const path = require('path');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// Simple POST /api/chat that forwards the message to OpenAI Chat Completions
app.post('/api/chat', async (req, res) => {
  const userMessage = req.body.message;
  if (!userMessage) return res.status(400).json({ error: 'Message is required' });
  // Choose mode: OpenAI (preferred) -> Hugging Face -> Mock
  const openaiKey = process.env.OPENAI_API_KEY;
  const hfKey = process.env.HUGGINGFACE_API_KEY;
  const hfModel = process.env.HUGGINGFACE_MODEL || 'gpt2'; // small default model (free tier availability varies)
  const useMock = process.env.USE_MOCK === 'true';

  if (!openaiKey && !hfKey && useMock) {
    // Mock reply when explicitly requested and no keys available
    const reply = `Mock ChatGPT: I received your message: "${userMessage}"`;
    return res.json({ reply });
  }

  // If OpenAI key exists use it
  if (openaiKey) {
    try {
      const resp = await fetch('https://api.openai.com/v1/chat/completions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${openaiKey}`
        },
        body: JSON.stringify({
          model: 'gpt-3.5-turbo',
          messages: [
            { role: 'system', content: 'You are a helpful assistant.' },
            { role: 'user', content: userMessage }
          ],
          max_tokens: 200
        })
      });

      const data = await resp.json();
      if (data.error) return res.status(500).json({ error: data.error });

      const assistantReply = data.choices && data.choices[0] && data.choices[0].message && data.choices[0].message.content;
      return res.json({ reply: assistantReply });
    } catch (err) {
      console.error('OpenAI error', err);
      // fallthrough to HF or mock if available
    }
  }

  // If we have a Hugging Face key, use HF Inference API as a free alternative
  if (hfKey) {
    try {
      const hfResp = await fetch(`https://api-inference.huggingface.co/models/${encodeURIComponent(hfModel)}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${hfKey}`
        },
        body: JSON.stringify({ inputs: userMessage, parameters: { max_new_tokens: 200 } })
      });

      const hfData = await hfResp.json();
      // Hugging Face returns an array with generated_text for text-generation models
      let text = null;
      if (Array.isArray(hfData) && hfData[0] && hfData[0].generated_text) {
        text = hfData[0].generated_text;
      } else if (hfData && hfData.generated_text) {
        text = hfData.generated_text;
      } else if (hfData && hfData.error) {
        return res.status(500).json({ error: hfData.error });
      }

      if (text) return res.json({ reply: text });
    } catch (err) {
      console.error('HuggingFace error', err);
      // fallthrough to mock if available
    }
  }

  // Fallback to mock if nothing worked
  const reply = `Mock ChatGPT: I received your message: "${userMessage}"`;
  return res.json({ reply });
});

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Small info endpoint so frontend can detect mock mode
app.get('/api/info', (req, res) => {
  const openaiKey = process.env.OPENAI_API_KEY;
  const hfKey = process.env.HUGGINGFACE_API_KEY;
  const useMockFlag = process.env.USE_MOCK === 'true';
  let provider = 'mock';
  if (openaiKey) provider = 'openai';
  else if (hfKey) provider = 'huggingface';
  else if (useMockFlag) provider = 'mock';
  res.json({ provider });
});

app.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`));
