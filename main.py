import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI(title="FlareIdea Core Engine", version="1.0.0")

# Настройка CORS для предотвращения блокировок запросов
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Схема данных для валидации компонентов
class ComponentItem(BaseModel):
    id: str
    name: str
    html: str
    visual: str

# Централизованная база данных компонентов на стороне бэкенда
COMPONENTS_DB: List[ComponentItem] = [
    ComponentItem(
        id="glass-card",
        name="Glassmorphism Card",
        html='<div class="glass-card">\n  <span class="token-tag">&lt;div</span> <span class="token-keyword">class</span>=<span class="token-string">"panel"</span><span class="token-tag">&gt;</span>\n    Curated Architecture Canvas\n  <span class="token-tag">&lt;/div&gt;</span>\n</div>',
        visual='<div class="preview-glass-card"></div>'
    ),
    ComponentItem(
        id="split-nav",
        name="Split Navigation Bar",
        html='<nav class="split-nav">\n  <span class="token-tag">&lt;span</span> <span class="token-keyword">class</span>=<span class="token-string">"brand"</span><span class="token-tag">&gt;</span>F.<span class="token-tag">&lt;/span&gt;</span>\n  <span class="token-div">...</span>\n</nav>',
        visual='<div class="preview-split-nav"><span></span><span></span></div>'
    ),
    ComponentItem(
        id="tab-switch",
        name="Animated Tab Switcher",
        html='<div class="tab-box">\n  <span class="token-tag">&lt;button</span> <span class="token-keyword">class</span>=<span class="token-string">"active"</span><span class="token-tag">&gt;</span>UI<span class="token-tag">&lt;/button&gt;</span>\n  <span class="token-tag">&lt;button&gt;</span>Code<span class="token-tag">&lt;/button&gt;</span>\n</div>',
        visual='<div class="preview-tab-switcher"><div class="active"></div><div></div></div>'
    ),
    ComponentItem(
        id="terminal-view",
        name="Terminal Context Container",
        html='<pre class="shell">\n  <span class="token-punctuation">$</span> <span class="token-keyword">npm run</span> engine-boot\n</pre>',
        visual='<div style="width:110px; height:60px; border:1px solid #1A1A1A; background:#000; border-radius:3px; padding:6px; font-size:6px; color:#4DFFFF">>_ live execution</div>'
    )
]

@app.get("/api/components", response_model=List[ComponentItem])
async def get_components():
    """Асинхронный эндпоинт для получения всех UI компонентов."""
    return COMPONENTS_DB

@app.get("/", response_class=HTMLResponse)
async def render_ui():
    """Читает и возвращает главный интерфейс index.html."""
    file_path = "index.html"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Interface index.html not found")
        
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

if __name__ == "__main__":
    import uvicorn
    # Запуск сервера на localhost:8000
    uvicorn.run("main.py:app", host="127.0.0.1", port=8000, reload=True)
