from fastapi import APIRouter
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
# import mlflow

from app.schemas.request import RequestModel
from app.schemas.response import ResponseModel
from app.utils.utils import get_recommendations, load_svd_model


router = APIRouter()

# def check_model_version():
#     model_name = 'svd_model'
#     filter_msg = f"name = '{model_name}'"
#     version_list = mlflow.search_model_versions(filter_string=filter_msg)
#     version = list(filter(lambda x: x.current_stage == 'Production', version_list))[0].version

    # return version

def update_model():
    router.model = load_svd_model()

@router.on_event("startup")
def save_cache_model():
    router.model = load_svd_model()
    # router.model_ver = check_model_version()
    # print(router.model_ver)
    scheduler = BackgroundScheduler()
    
    trigger = CronTrigger(day_of_week="mon", hour=11, minute=15)
    scheduler.add_job(update_model, trigger=trigger)
    scheduler.start()
    
    
@router.post("/predict", response_model=ResponseModel)
def recsys(data: RequestModel):
    result = get_recommendations(router.model, data.collections)
    return ResponseModel(recommendations=result)
