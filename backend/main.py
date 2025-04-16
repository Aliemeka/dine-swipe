from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def health_check():
    return {"is_active": True}
