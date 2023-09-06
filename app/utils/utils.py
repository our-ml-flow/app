
import mlflow
import pandas as pd
from datetime import date, timedelta
import numpy as np
from prefect_sqlalchemy import SqlAlchemyConnector
from sqlalchemy import text
from surprise import Reader, Dataset


#학습이 완료된 모델을 불러온다
def load_svd_model():
    mlflow.set_tracking_uri('http://localhost:5000')

    model_name = "svd_model"
    svd_model = mlflow.sklearn.load_model(f'models:/{model_name}/Production')
    return svd_model


#학습에 사용된 데이터를 불러온다
def get_raw_data(start_date, end_date):
    
    engine = SqlAlchemyConnector.load("gcp-mlops-sql-postgres").get_engine()
    connection = engine.connect()

    try:
        query = f""" WITH owner_token_info AS (
                        SELECT 
                            owner_address,
                            collection_name AS collection,
                            num_distinct_tokens_owned AS num_token,
                            sum(num_distinct_tokens_owned) OVER (PARTITION BY owner_address) AS tot,
                            data_created_at::date AS created_at
                        FROM alchemy_collection_for_buyer
                        WHERE data_created_at::date BETWEEN '{start_date}' AND '{end_date}'
                        )
                        SELECT 
                            owner_address, 
                            collection,
                            sum(num_token/tot) AS token_ratio
                        FROM owner_token_info
                        GROUP BY owner_address, collection, created_at
                        ORDER BY owner_address;"""
        
        result = connection.execute(text(query))
        rows=result.fetchall()
        df=pd.DataFrame(rows)
    except Exception as e:
        print("error", e)
    return df


#학습에 사용된 데이터와 신규 입력받은 데이터를 합쳐서 테스트셋 생성 후 모델에 실행
def full_dataset_for_test(collections):
    #load 
    end_date = date.today() 
    start_date = end_date - timedelta(days=7)
    loaded_data=get_raw_data(start_date, end_date)
    reader = Reader(rating_scale=(0,1))
    #old_data = Dataset.load_from_df(loaded_data, reader)

    #### 신규로 받은 리스트 타입의 컬렉션을 DF로 변환
    new_data = [('new_user', item, 0) for item in collections]
    new_data_df = pd.DataFrame(new_data, columns=loaded_data.columns)
    
    #### 학습데이터와 concat 후 새로운 데이터셋 생성
    combined_data_df = pd.concat([loaded_data, new_data_df], ignore_index=True)
    combined_data = Dataset.load_from_df(combined_data_df, reader)
    trainset = combined_data.build_full_trainset()    
    # testset = trainset.build_testset()
    testset_unobserved = trainset.build_anti_testset()
    return testset_unobserved


#전체 프로세스 진행
def get_recommendations(model, collections):
    dataset = full_dataset_for_test(collections)
    svd_model = model 
    prediction = svd_model.test(dataset)
    
    # 해당 사용자의 예측값만 필터링
    user_predictions = [pred for pred in prediction if pred.uid == 'new_user']

    # 예측값 ('est')을 기준으로 내림차순 정렬
    sorted_predictions = sorted(user_predictions, key=lambda x: x.est, reverse=True)

    # 결과 출력
    result = [pred.iid for pred in sorted_predictions[:5]]
    return result