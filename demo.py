# # from us_visa.logger import logging

# # logging.info("welcome to our custom log")



# # from us_visa.exception import us_visa_exception
# # import sys

# # try:
# #     a = 1/"e"

# # except Exception as error:
# #     raise us_visa_exception(error, sys) from error

# # from us_visa.constant import database_name

# # print(database_name)

# from us_visa.pipeline.train_pipeline import trainpipeline

# pipeline = trainpipeline().run_pipeline()
# # # pipeline.run_pipeline()

# # from dotenv import load_dotenv
# # import os

# # load_dotenv()

# # connection_url = os.getenv("connection_url")
# # print(connection_url)

# # print("welcome to our custom log")




from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "context": "Predicting"}
    )
