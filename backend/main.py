# ============================================================
# FinControl – Ponto de Entrada da API
# ============================================================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, categorias, transacoes

app = FastAPI(
    title="FinControl API",
    description="API REST para gestão financeira pessoal",
    version="1.0.0"
)

# CORS — permite que o front-end consuma a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router)
app.include_router(categorias.router)
app.include_router(transacoes.router)


@app.get("/", tags=["Health Check"])
def health_check():
    return {"status": "online", "sistema": "FinControl API v1.0"}