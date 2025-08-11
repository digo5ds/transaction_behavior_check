"""FastAPI application entry point."""

from fastapi import APIRouter, FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, RedirectResponse

from app.__version__ import get_version
from app.core.config import APPLICATION_PORT, FASTAPI_CONFIG
from app.helpers.mongo_helper import MongoHelper
from app.models.collections.rules_model import Rule
from app.routes.customer_routes import router as customer_router
from app.routes.transaction_routes import router as transaction_router

app = FastAPI(**FASTAPI_CONFIG)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handles request validation errors.

    This exception handler is called when a request contains invalid data that
    fails the validation defined in the endpoint. It returns a JSON response with
    the same status code and error details as the original `RequestValidationError`.

    Args:
        request (Request): The request object that contains the invalid data.
        exc (RequestValidationError): The exception raised due to the invalid data.

    Returns:
        JSONResponse: A JSON response with the error details.
    """
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.errors()},
    )


@app.get("/rules")
def get_rules():
    """
    Retrieves the list of known destinations.

    This endpoint is used to retrieve the list of known destination accounts,
    which are used to evaluate the risk of a transaction.

    Returns:
        List[KnowlegedDestinations]: A list of known destination accounts.
    """
    mongo_helper = MongoHelper()
    result = [rule.to_mongo().to_dict() for rule in mongo_helper.find_documents(Rule)]
    for item in result:
        item.pop("_id")
    return result


@app.get("/", include_in_schema=False)
def docs():
    """
    Redirects the root URL to the API documentation.

    This endpoint is not included in the OpenAPI schema, serving only as
    a convenience for users to quickly access the documentation.
    """
    return RedirectResponse(url="/docs")


@app.get("/version", include_in_schema=False)
def version():
    """
    Returns the version of the application.

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

    uvicorn.run("app.api:app", host="0.0.0.0", port=APPLICATION_PORT, reload=True)
