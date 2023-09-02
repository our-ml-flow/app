from fastapi import APIRouter
from starlette.concurrency import run_in_threadpool

from app.schemas.request import NftFeature
from app.schemas.response import NftPrediction
from app.schemas.response import ResponseNft
from app.utils import load_user_base_data, load_pyfunc_model

router = APIRouter()

@router.on_event("startup")
async def load_data_on_startup():
    router.data = await load_user_base_data()

@router.on_event("startup")
def load_model_on_startup():
    router.model = load_pyfunc_model("Daily_User_Based_Model")

@router.post("/predict", response_model = NftPrediction)
async def predict_nft(feature: NftFeature):
    # raw_prediction = router.model.predict_recommend(router.data,feature.feature1)
    
    raw_prediction = await run_in_threadpool(router.model.predict_recommend, router.data, feature.feature1 )

    
    prediction = [ResponseNft(name=item[0], count=item[1]) for item in raw_prediction]
    
    return NftPrediction(prediction=prediction)



# from fastapi import APIRouter, BackgroundTasks
# from starlette.concurrency import run_in_threadpool
# from datetime import datetime, timedelta
# import time

# from app.schemas.request import NftFeature
# from app.schemas.response import NftPrediction, ResponseNft
# from app.utils import load_user_base_data, load_pyfunc_model

# router = APIRouter()

# async def reload_data():
#     while True:
#         # Sleep until the next 11 o'clock
#         now = datetime.now()
#         if now.hour >= 11:  # if it's past 11, schedule for next day
#             next_reload_time = now + timedelta(days=1)
#         else:
#             next_reload_time = now
#         next_reload_time = next_reload_time.replace(hour=11, minute=0, second=0, microsecond=0)
#         sleep_duration = (next_reload_time - now).seconds
#         time.sleep(sleep_duration)
        
#         router.data = await load_user_base_data()

# @router.on_event("startup")
# async def load_data_on_startup():
#     router.data = await load_user_base_data()
#     # Schedule the data reloading in background
#     background_tasks = BackgroundTasks()
#     background_tasks.add_task(reload_data)

# @router.on_event("startup")
# def load_model_on_startup():
#     router.model = load_pyfunc_model("Daily_User_Based_Model")

# @router.post("/predict", response_model=NftPrediction)
# async def predict_nft(feature: NftFeature):
#     raw_prediction = await run_in_threadpool(router.model.predict_recommend, router.data, feature.feature1)
#     prediction = [ResponseNft(name=item[0], count=item[1]) for item in raw_prediction]
#     return NftPrediction(prediction=prediction)
