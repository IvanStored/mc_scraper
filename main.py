import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from routers.products import products_router

app = FastAPI()

app.include_router(products_router)
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




if __name__ == '__main__':
    uvicorn.run("main:app")