import uvicorn

from fastapi import FastAPI

from settings.common import HOST, PORT

app = FastAPI()

if __name__ == '__main__':
    uvicorn.run(app, host=HOST, port=PORT)
