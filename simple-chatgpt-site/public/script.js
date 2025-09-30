// Very small client script. Sends the user's message to /api/chat and shows the reply.
const form = document.getElementById('form');
const input = document.getElementById('input');
const chat = document.getElementById('chat');
const mockBadge = document.getElementById('mock-badge');
const darkToggle = document.getElementById('darkToggle');
const presetButtons = document.querySelectorAll('.preset');
const themeSelect = document.getElementById('themeSelect');

// Apply a button color preset by setting the --red-button CSS variable
function applyButtonPreset(preset){
  const root = document.documentElement;
  let color = '#d95b5b';
  if (preset === 'medium') color = '#bf4b4b';
  if (preset === 'vibrant') color = getComputedStyle(root).getPropertyValue('--red-canary').trim() || '#ff2b2b';
  root.style.setProperty('--red-button', color);
  localStorage.setItem('buttonPreset', preset);
}

function initButtonPresets(){
  const saved = localStorage.getItem('buttonPreset') || 'soft';
  applyButtonPreset(saved);
  presetButtons.forEach(btn => {
    btn.addEventListener('click', ()=>{
      const p = btn.dataset.preset;
      applyButtonPreset(p);
    });
  });
}

function addMessage(text, cls) {
  const el = document.createElement('div');
  el.className = 'msg ' + cls;
  el.textContent = text;
  chat.appendChild(el);
  chat.scrollTop = chat.scrollHeight;
}

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const text = input.value.trim();
  if (!text) return;
  addMessage(text, 'user');
  input.value = '';

  addMessage('...', 'bot'); // temporary placeholder
  const placeholder = chat.querySelector('.msg.bot:last-child');

  try {
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text })
    });
    const data = await res.json();
    if (data.reply) {
      placeholder.textContent = data.reply;
    } else {
      placeholder.textContent = 'Error: no reply';
    }
  } catch (err) {
    placeholder.textContent = 'Network error';
  }
});

// Check server info to detect mock mode and show badge if needed
async function checkServerInfo(){
  try{
    const res = await fetch('/api/info');
    const data = await res.json();
    // server now returns { provider: 'openai'|'huggingface'|'mock' }
    if (data.provider === 'mock') mockBadge.hidden = false;
    else mockBadge.hidden = true;
  }catch(e){
    // If info can't be fetched, keep badge hidden
    mockBadge.hidden = true;
  }
}

// Simple dark-mode toggle using data-theme on root and localStorage
function initDarkMode(){
  const saved = localStorage.getItem('theme');
  const root = document.documentElement;
  // saved can be 'light' (default), 'dark', or a variant like 'dark-crimson'
  if (saved && saved !== 'light'){
    root.setAttribute('data-theme', saved);
    darkToggle.checked = true;
    if (themeSelect) themeSelect.value = saved;
  }

  darkToggle.addEventListener('change', ()=>{
    if (darkToggle.checked){
      const sel = themeSelect ? themeSelect.value : 'dark';
      root.setAttribute('data-theme', sel);
      localStorage.setItem('theme', sel);
    } else {
      root.removeAttribute('data-theme');
      localStorage.setItem('theme','light');
    }
  });

  if (themeSelect){
    themeSelect.addEventListener('change', ()=>{
      const sel = themeSelect.value;
      // If dark mode is enabled, apply immediately
      if (darkToggle.checked){
        document.documentElement.setAttribute('data-theme', sel);
      }
      localStorage.setItem('theme', sel);
    });
  }
}

checkServerInfo();
initDarkMode();
initButtonPresets();
