const fetch = require('node-fetch');

async function run() {
  try {
    const resp = await fetch('http://localhost:3000/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: 'Hello from smoke test' })
    });
    const data = await resp.json();
    console.log('smoke test response:', data);
  } catch (err) {
    console.error('smoke test error', err);
  }
}

run();
