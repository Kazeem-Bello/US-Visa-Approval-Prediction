from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import JSONResponse
from uvicorn import run as app_run
from typing import Optional
import time

from us_visa.constant import APP_HOST, APP_PORT
from us_visa.pipeline.prediction_pipeline import UsvisaData, USvisaClassifier
from us_visa.pipeline.train_pipeline import trainpipeline
from pydantic import BaseModel

app = FastAPI()

app.mount("/static", StaticFiles(directory = "static"), name = "static")

templates = Jinja2Templates( directory = 'templates')

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

class DataForm(BaseModel):
    continent: str
    education_of_employee: str
    has_job_experience: str
    requires_job_training: str
    no_of_employees: int
    company_age: int
    region_of_employment: str
    prevailing_wage: int
    unit_of_wage: str
    full_time_position: str



@app.get("/", tags=["Home"], status_code = status.HTTP_200_OK)
async def index(request: Request):

    return templates.TemplateResponse(request = request, 
                                      name = "index.html", 
                                      context = {"request": request, "context": "Waiting...", "status_code": None})


@app.get("/train", status_code = status.HTTP_200_OK)
async def trainRouteClient():
    try:
        train_pipeline = trainpipeline()

        train_pipeline.run_pipeline()

        return Response("Training successful !!")

    except Exception as e:
        raise HTTPException(detail = f"Error Occurred! {str(e)}", status_code = status.HTTP_500_INTERNAL_SERVER_ERROR)


@app.post("/predict", status_code = status.HTTP_200_OK)
async def predictRouteClient(form: DataForm):
    try:        
        usvisa_data = UsvisaData(
                                continent= form.continent,
                                education_of_employee = form.education_of_employee,
                                has_job_experience = form.has_job_experience,
                                requires_job_training = form.requires_job_training,
                                no_of_employees= form.no_of_employees,
                                company_age= form.company_age,
                                region_of_employment = form.region_of_employment,
                                prevailing_wage= form.prevailing_wage,
                                unit_of_wage= form.unit_of_wage,
                                full_time_position= form.full_time_position,
                                )
        
        usvisa_df = usvisa_data.get_usvisa_input_data_frame()

        model_predictor = USvisaClassifier()

        start_time = time.time()
        prediction = (model_predictor.predict(dataframe=usvisa_df)[0])
        end_time = time.time()
        prediction_time = end_time - start_time
        prediction_time = f"{prediction_time:.4f}s"

        model_accuracy = model_predictor.accuracy()
        model_accuracy = f"{model_accuracy * 100:.2f}%"

        status = None
        if int(prediction) == 1:
            status = "Approved" 
        else:
            status = "Denied"

        return JSONResponse(content = {"prediction": status, "model_accuracy": model_accuracy, "prediction_time": prediction_time})
        
    except Exception as e:
        raise HTTPException(detail = f"Error Occurred! {str(e)}", status_code = status.HTTP_500_INTERNAL_SERVER_ERROR)
