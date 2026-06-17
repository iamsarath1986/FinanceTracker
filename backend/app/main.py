from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from starlette.types import ASGIApp, Receive, Scope, Send

from app.api import accounts, auth, budgets, categories, dashboard, recurring, transactions
from app.core.limiter import limiter
from app.db.seed import seed_categories
from app.db.session import SessionLocal

ALLOW_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:8086",
    "https://ssfwj.assmt.munnich.it",
]


class EnsureCorsOnErrors:
    """
    Outermost user middleware — guarantees CORS headers reach the browser
    even when inner layers (auth middleware, unhandled exceptions) return
    responses before CORSMiddleware can inject them.

    Starlette stack (outside → in):
      ServerErrorMiddleware → EnsureCorsOnErrors → CORSMiddleware
        → ExceptionMiddleware → Router
    """

    def __init__(self, app: ASGIApp, allow_origins: list[str]) -> None:
        self.app = app
        self.origins = set(allow_origins)

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        origin = dict(scope.get("headers", [])).get(b"origin", b"").decode()
        if origin not in self.origins:
            await self.app(scope, receive, send)
            return

        cors_patch = [
            (b"access-control-allow-origin", origin.encode()),
            (b"access-control-allow-credentials", b"true"),
        ]

        async def send_with_cors(message: dict) -> None:
            if message["type"] == "http.response.start":
                existing = {k for k, _ in message.get("headers", [])}
                if b"access-control-allow-origin" not in existing:
                    message = {
                        **message,
                        "headers": [*message.get("headers", []), *cors_patch],
                    }
            await send(message)

        try:
            await self.app(scope, receive, send_with_cors)
        except Exception:
            response = JSONResponse(
                status_code=500,
                content={"detail": "Internal server error"},
                headers={
                    "Access-Control-Allow-Origin": origin,
                    "Access-Control-Allow-Credentials": "true",
                },
            )
            await response(scope, receive, send)


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = SessionLocal()
    try:
        seed_categories(db)
    finally:
        db.close()
    yield


app = FastAPI(title="FinanceTracker API", version="1.0.0", redirect_slashes=False, lifespan=lifespan)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORSMiddleware added first = inner user middleware (handles preflight OPTIONS).
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# EnsureCorsOnErrors added second = outermost user middleware.
# Patches CORS onto any response CORSMiddleware never saw (auth 401s, 500s).
app.add_middleware(EnsureCorsOnErrors, allow_origins=ALLOW_ORIGINS)

app.include_router(auth.router)
app.include_router(accounts.router)
app.include_router(categories.router)
app.include_router(transactions.router)
app.include_router(recurring.router)
app.include_router(budgets.router)
app.include_router(dashboard.router)


@app.get("/health")
def health():
    return {"status": "ok"}