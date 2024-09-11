from fastapi import FastAPI, Depends
from fastapi.params import Security

from application.utils import VerifyToken

from routers import customers_manager  # , employees_manager, entry_manager, rabbitmq, reporting_system, users_manager
from routers.customer_manager import slots, customers, visits, workday

auth = VerifyToken()


app = FastAPI()

app.include_router(customers_manager.router)
app.include_router(slots.router)
app.include_router(customers.router)
app.include_router(visits.router)
app.include_router(workday.router)

@app.get("/api/public/")
def public():
    """No access token required to access this route"""

    result = {
        "status": "success",
        "msg": ("Hello from a public endpoint! You don't need to be "
                "authenticated to see this.")
    }
    return result

@app.get("/api/private")
async def private(auth_result: str = Security(auth.verify)):
    print("inside of private function")
    """A valid access token is required to access this route"""



    return auth_result