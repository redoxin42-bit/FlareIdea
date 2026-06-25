import os
from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Инициализация FastAPI приложения
app = FastAPI(
    title="FlareIdea API",
    description="Production-ready бэкенд, оптимизированный для Cloudflare Workers",
    version="1.1.0"
)

# Настройка CORS для предотвращения блокировок со стороны браузера
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Схема данных для валидации UI компонентов
class UiComponent(BaseModel):
    id: str
    name: str
    html: str
    visual: str

# Статические демонстрационные данные компонентов FlareIdea
MOCK_COMPONENTS: List[UiComponent] = [
    UiComponent(
        id="glass-card",
        name="Glassmorphism Card",
        html='<div class="glass-card">\n  <span class="token-tag">&lt;div</span> <span class="token-keyword">class</span>=<span class="token-string">"panel"</span><span class="token-tag">&gt;</span>\n    Curated Architecture Canvas\n  <span class="token-tag">&lt;/div&gt;</span>\n</div>',
        visual='<div class="preview-glass-card"></div>'
    ),
    UiComponent(
        id="split-nav",
        name="Split Navigation Bar",
        html='<nav class="split-nav">\n  <span class="token-tag">&lt;span</span> <span class="token-keyword">class</span>=<span class="token-string">"brand"</span><span class="token-tag">&gt;</span>F.<span class="token-tag">&lt;/span&gt;</span>\n  <span class="token-div">...</span>\n</nav>',
        visual='<div class="preview-split-nav"><span></span><span></span></div>'
    ),
    UiComponent(
        id="tab-switch",
        name="Animated Tab Switcher",
        html='<div class="tab-box">\n  <span class="token-tag">&lt;button</span> <span class="token-keyword">class</span>=<span class="token-string">"active"</span><span class="token-tag">&gt;</span>UI<span class="token-tag">&lt;/button&gt;</span>\n  <span class="token-tag">&lt;button&gt;</span>Code<span class="token-tag">&lt;/button&gt;</span>\n</div>',
        visual='<div class="preview-tab-switcher"><div class="active"></div><div></div></div>'
    )
]

@app.get("/api/components", response_model=List[UiComponent])
async def get_components():
    """Возвращает валидированный список доступных интерфейсных компонентов."""
    return MOCK_COMPONENTS

@app.get("/", response_class=HTMLResponse)
async def render_homepage():
    """Считывает и отдает index.html. При отсутствии файла генерирует резервный интерфейс."""
    file_path = "index.html"
    
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
        except Exception as error:
            raise HTTPException(status_code=500, detail=f"Ошибка чтения файла: {str(error)}")
            
    # Резервный HTML-код (Fallback UI), если index.html не был развернут воркером
    fallback_html = """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>FlareIdea Core</title>
        <style>
            body { background: #0b0b0f; color: #e2e8f0; font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
            .container { text-align: center; border: 1px solid #1e1e2f; padding: 2.5rem; border-radius: 12px; background: #13131a; box-shadow: 0 4px 30px rgba(0,0,0,0.5); }
            h1 { color: #4dffff; margin-bottom: 0.5rem; }
            p { color: #94a3b8; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>FlareIdea API v1.1.0</h1>
            <p>Бэкенд успешно запущен в среде Cloudflare Workers.</p>
            <small style="color: #475569;">Статический index.html не найден в корне, запущен резервный режим.</small>
        </div>
    </body>
    </html>
    """
    return fallback_html

# Блок конфигурации локального сервера (не мешает деплою в Cloudflare)
# Исправлена строка запуска с "main.py:app" на легитимный модуль "main:app"
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
