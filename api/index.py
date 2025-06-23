from fastapi import FastAPI
from routes.login import login_router
from routes.verify_voter import verify_voter_router

app = FastAPI()

# Register routers
app.include_router(login_router, prefix="/api/nid")
app.include_router(verify_voter_router, prefix="/api/nid")
