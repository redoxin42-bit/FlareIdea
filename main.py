# File: main.py
import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

# Инициализация ASGI-приложения FastAPI
app = FastAPI(
    title="FlareIdea Core Backend",
    description="Стабильный бэкенд для управления UI-компонентами платформы",
    version="1.0.1"
)

# Настройка политик CORS для беспрепятственного взаимодействия с фронтендом
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Схема валидации структуры UI-компонента
class ComponentSchema(BaseModel):
    id: str
    name: str
    html: str
    visual: str

# Серверный массив данных (база моков) для вывода на фронтенд
STORED_COMPONENTS: List[ComponentSchema] = [
    ComponentSchema(
        id="glass-card",
        name="Glassmorphism Card",
        html='<div class="glass-card">\n  <span class="token-tag">&lt;div</span> <span class="token-keyword">class</span>=<span class="token-string">"panel"</span><span class="token-tag">&gt;</span>\n    Curated Architecture Canvas\n  <span class="token-tag">&lt;/div&gt;</span>\n</div>',
        visual='<div class="preview-glass-card"></div>'
    ),
    ComponentSchema(
        id="split-nav",
        name="Split Navigation Bar",
        html='<nav class="split-nav">\n  <span class="token-tag">&lt;span</span> <span class="token-keyword">class</span>=<span class="token-string">"brand"</span><span class="token-tag">&gt;</span>F.<span class="token-tag">&lt;/span&gt;</span>\n  <span class="token-div">...</span>\n</nav>',
        visual='<div class="preview-split-nav"><span></span><span></span></div>'
    ),
    ComponentSchema(
        id="tab-switch",
        name="Animated Tab Switcher",
        html='<div class="tab-box">\n  <span class="token-tag">&lt;button</span> <span class="token-keyword">class</span>=<span class="token-string">"active"</span><span class="token-tag">&gt;</span>UI<span class="token-tag">&lt;/button&gt;</span>\n  <span class="token-tag">&lt;button&gt;</span>Code<span class="token-tag">&lt;/button&gt;</span>\n</div>',
        visual='<div class="preview-tab-switcher"><div class="active"></div><div></div></div>'
    ),
    ComponentSchema(
        id="terminal-view",
        name="Terminal Context Container",
        html='<pre class="shell">\n  <span class="token-punctuation">$</span> <span class="token-keyword">npm run</span> engine-boot\n</pre>',
        visual='<div style="width:110px; height:60px; border:1px solid #1A1A1A; background:#000; border-radius:3px; padding:6px; font-size:6px; color:#4DFFFF">>_ live execution</div>'
    ),
    ComponentSchema(
        id="action-trigger",
        name="Micro-interaction Button",
        html='<button class="action-trigger">\n  Execute Trace\n</button>',
        visual='<div style="padding:6px 12px; border:1px solid #4DFFFF; color:#4DFFFF; font-size:10px; border-radius:2px; box-shadow:0 0 10px rgba(77,255,255,0.2)">TRIGGER</div>'
    ),
    ComponentSchema(
        id="data-grid",
        name="Surgical Layout Grid",
        html='<div class="surgical-grid">\n  <span class="token-tag">&lt;div&gt;</span>Trace Unit Matrix Nodes<span class="token-tag">&lt;/div&gt;</span>\n</div>',
        visual='<div style="display:grid; grid-template-columns:repeat(2,1fr); gap:4px; width:100px;"><div style="border:1px dashed #2A2A2A; height:20px;"></div><div style="border:1px dashed #2A2A2A; height:20px;"></div><div style="border:1px dashed #2A2A2A; height:20px;"></div><div style="border:1px dashed #2A2A2A; height:20px;"></div></div>'
    )
]

@app.get("/api/components", response_model=List[ComponentSchema])
async def get_components_list():
    """Возвращает валидированный список доступных UI-элементов интерфейса."""
    return STORED_COMPONENTS

@app.get("/", response_class=HTMLResponse)
async def serve_home_page():
    """Считывает и возвращает файл статической разметки index.html."""
    target_path = "index.html"
    
    if not os.path.exists(target_path):
        raise HTTPException(
            status_code=404, 
            detail="Критическая ошибка: Файл интерфейса 'index.html' не найден в корневой директории бэкенда."
        )
        
    try:
        with open(target_path, "r", encoding="utf-8") as web_file:
            return web_file.read()
    except Exception as read_error:
        raise HTTPException(
            status_code=500, 
            detail=f"Внутренняя ошибка чтения файловой системы: {str(read_error)}"
        )

# Блок инициализации локального сервера отладки.
# ВНИМАНИЕ: Строка импорта изменена на "main:app" для исключения ошибок импорта модуля.
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
