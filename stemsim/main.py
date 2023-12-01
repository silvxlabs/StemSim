from fastapi import FastAPI
import numpy as np
import uvicorn

from .routers import stem_map_router, machine_router

app = FastAPI(title="StemSim", version="0.1.0")

# Connect API routers to the main app
app.include_router(stem_map_router.router, prefix="/stem-maps", tags=["Stem Maps"])
app.include_router(machine_router.router, prefix="/machines", tags=["Machines"])

# Dev server
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
