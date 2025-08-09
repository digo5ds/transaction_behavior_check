"""FastAPI application entry point."""

from fastapi import APIRouter, FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, RedirectResponse

from app.__version__ import get_version
from app.core.config import FASTAPI_CONFIG
from app.routes.customer_routes import router as customer_router
from app.routes.transaction_routes import router as transaction_router

app = FastAPI(**FASTAPI_CONFIG)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.errors()},
    )


@app.get("/", include_in_schema=False)
def docs():
    """Redirects the root URL to the API documentation.

    This endpoint is not included in the OpenAPI schema, serving only as
    a convenience for users to quickly access the documentation.
    """

    return RedirectResponse(url="/docs")


@app.get("/version", include_in_schema=False)
def version():
    """Returns the version of the application.

    This endpoint is not included in the OpenAPI schema, serving only as
    a convenience for users to check the current version of the application.
    """

    return {"version": get_version()}


api_router = APIRouter()
api_router.include_router(customer_router, tags=["customers"])
api_router.include_router(transaction_router, tags=["transaction"])
app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.api:app", host="0.0.0.0", port=5001, reload=True)
