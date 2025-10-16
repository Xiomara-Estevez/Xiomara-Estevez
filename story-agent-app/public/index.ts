import express from 'express';
import cors from 'cors';
import { createServer as createAgentServer } from '@inngest/agent-kit/server';
import { createAgent, createNetwork, openai } from '@inngest/agent-kit';

const app = express();
app.use(cors());
app.use(express.json());

// Story generator agent
const storyAgent = createAgent({
  name: 'Story Agent',
  system: `You are a creative story writer assistant.
The user may say:
- "Start a story about a dragon in a fantasy world"
- "Change the genre to sci-fi"
- "Add a twist"
- "Continue"
Maintain the story context and modify it accordingly.`,
  model: openai('gpt-3.5-turbo')
});

const storyNetwork = createNetwork({
  name: 'StoryNetwork',
  agents: [storyAgent],
});

const agentServer = createAgentServer({ networks: [storyNetwork] });
app.use('/api/agent', agentServer);

// Simple endpoint to chat with the agent
app.post('/api/chat', async (req, res) => {
  const { message } = req.body;
  if (!message) return res.status(400).json({ error: 'Message is required' });

  const result = await storyNetwork.run(message, () => storyAgent);
  const content = result.output.at(-1)?.content || '';
  res.json({ reply: content });
});

// Serve the frontend
app.use(express.static('public'));

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`✅ Server running on http://localhost:${PORT}`));
