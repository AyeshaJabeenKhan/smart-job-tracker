from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from pathlib import Path

from app.database import engine, Base
from app.models import job  
from app.routers import job

# Load environment configurations
load_dotenv() 

# 1. Instruct database engines to compile schemas if they do not exist
Base.metadata.create_all(bind=engine)

# 2. Initialize Primary FastAPI Application Context
app = FastAPI(
    title=os.getenv("PROJECT_NAME", "Smart Job Tracker API"),
    version=os.getenv("VERSION", "1.0.0"),
    description="Enterprise-grade REST API designed for tracking global job application lifecycles.",
    docs_url="/docs",  
    redoc_url="/redoc"
)

# 3. Configure CORS (Cross-Origin Resource Sharing) Middleware Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. Establish exact absolute path to your premium HTML frontend template
BASE_DIR = Path(__file__).resolve().parent
TEMPLATE_PATH = BASE_DIR / "templates" / "index.html"

# 5. SERVE PREMIUM CUSTOM HOMEPAGE (PUT THIS FIRST!)
@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def serve_home_dashboard():
    """
    Renders the custom Tailwind/JS front-end dashboard on the root domain address.
    """
    print("\n🚀 SUCCESS: FastAPI intercepted a homepage hit and loaded templates/index.html! 🚀\n")
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

# 6. Mount Application Sub-Routers (PUT THIS AFTER THE HOMEPAGE ROUTE)
app.include_router(job.router)