from pydantic import BaseModel


class SensorDataModel(BaseModel):
    datetime: str
    payload: int
