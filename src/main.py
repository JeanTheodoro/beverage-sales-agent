import logging
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from api.routes.whatsapp_routes import router as whatsapp_router
from api.routes.admin_orders_router import router as admin_orders_router
from api.routes.admin_metrics_router import router as admin_dashbord

from core.config.logging import setup_logging

from core.redis import redis_lifespan
# =========================================================
# LOGGING
# =========================================================

setup_logging()

logger = logging.getLogger("bar_do_jaum")


# =========================================================
# PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent

TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"


logger.info("BASE_DIR: %s", BASE_DIR)
logger.info("TEMPLATES_DIR: %s", TEMPLATES_DIR)
logger.info("STATIC_DIR: %s", STATIC_DIR)

logger.info(
    "index.html existe: %s",
    (TEMPLATES_DIR / "index.html").exists(),
)


# =========================================================
# FASTAPI
# =========================================================

app = FastAPI(
    title="Bar do Jaum - Agente de Delivery",
    lifespan=redis_lifespan,
    description=(
        "API stateful com IA para atendimento via WhatsApp "
        "no Bar do Jaum."
    ),
    version="1.0.0",
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# STATIC FILES
# =========================================================

app.mount(
    "/static",
    StaticFiles(directory=STATIC_DIR),
    name="static",
)


# =========================================================
# TEMPLATES
# =========================================================

templates = Jinja2Templates(
    directory=TEMPLATES_DIR,
)


# =========================================================
# API ROUTES
# =========================================================

app.include_router(whatsapp_router)
app.include_router(admin_orders_router)
app.include_router(admin_dashbord)



# =========================================================
# WEB
# =========================================================

@app.get(
    "/",
    response_class=HTMLResponse,
)
async def home(request: Request):
    """
    Renderiza o painel administrativo do Bar do Jaum.
    """

    logger.info(
        "Painel administrativo acessado."
    )

    return templates.TemplateResponse(
        request=request,
        name="index.html",
    )


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")
async def health_check():
    """
    Endpoint de verificação de saúde da API.
    """

    logger.info(
        "Health check endpoint chamado com sucesso."
    )

    return {
        "status": "online",
        "message": (
            "Bar do Jaum API está operando a todo vapor!"
        ),
    }