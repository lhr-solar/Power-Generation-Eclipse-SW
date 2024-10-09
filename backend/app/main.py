from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from routers.pvcaprouters import pvcap_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pvcap_router)

if __name__ == "__main__":
    print(pvcap_router.routes)
    uvicorn.run(app, host="localhost", port=4242)