from prefect_sqlalchemy import SqlAlchemyConnector

import mlflow
import pandas as pd

async def load_user_base_data():
    block = await SqlAlchemyConnector.load('gcp-mlops-sql-postgres')

    engine = block.get_engine()

    query = """
    SELECT
        owner_address,
        collection_name
    FROM alchemy_collection_for_buyer
    WHERE DATE(data_created_at) = DATE(NOW()) - INTERVAL '1' DAY
    """

    data =  pd.read_sql(query, engine)

    return data

def load_pyfunc_model(model_name: str):
    loaded_model = mlflow.pyfunc.load_model(f"models:/{model_name}/Production")    

    loaded_model =loaded_model.unwrap_python_model()

    return loaded_model