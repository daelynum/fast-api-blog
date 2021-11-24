import uvicorn
from fastapi import FastAPI

from blog import models
from blog.database import engine
from blog.routers import blog, user, authentification

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(blog.router)
app.include_router(user.router)
app.include_router(authentification.router)


if __name__ == '__main__':
    models.Base.metadata.create_all(bind=engine)
    uvicorn.run(app, host='127.0.0.1', port=8080)
