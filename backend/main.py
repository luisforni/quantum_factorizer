from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from backend.shor_simulator import run_shor_factorization

app = FastAPI()

class FactorRequest(BaseModel):
    number: int

class FactorResponse(BaseModel):
    number: int
    factors: List[int]
    method: str

@app.post("/factor", response_model=FactorResponse)
def factor_number(data: FactorRequest):
    try:
        number = data.number
        result = run_shor_factorization(number)

        return FactorResponse(
            number=number,
            factors=result["factors"],
            method=result["method"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))