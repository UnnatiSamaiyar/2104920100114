from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
from typing import List, Dict
import asyncio
import json
import os

app = FastAPI()

WINDOW_SIZE = 10
STORE_FILE = 'numbers_store.json'
MOCK_SERVER_URL = 'http://20.244.56.144'  # URL of the third-party server

class ResponseModel(BaseModel):
    windowPrevState: List[int]
    windowCurrState: List[int]
    numbers: List[int] = []

def read_store() -> Dict[str, List[int]]:
    if not os.path.exists(STORE_FILE):
        return {'p': [], 'f': [], 'e': [], 'r': []}
    with open(STORE_FILE, 'r') as file:
        return json.load(file)

def write_store(store: Dict[str, List[int]]):
    with open(STORE_FILE, 'w') as file:
        json.dump(store, file)

async def fetch_numbers(numberid: str, count: int) -> List[int]:
    url = f"{MOCK_SERVER_URL}/{numberid}"
    numbers = []
    async with httpx.AsyncClient() as client:
        tasks = [client.get(url) for _ in range(count)]
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        for response in responses:
            if isinstance(response, httpx.Response) and response.status_code == 200:
                numbers.append(response.json().get("number"))
    return numbers

@app.get("/numbers/{numberid}", response_model=ResponseModel)
async def get_number(numberid: str):
    if numberid not in ['p', 'f', 'e', 'r']:
        raise HTTPException(status_code=400, detail="Invalid number ID")
    
    store = read_store()
    windowPrevState = store[numberid].copy()
    
    new_numbers = await fetch_numbers(numberid, 4)
    
    for number in new_numbers:
        if number not in store[numberid]:
            if len(store[numberid]) >= WINDOW_SIZE:
                store[numberid].pop(0)
            store[numberid].append(number)
    
    write_store(store)
    
    windowCurrState = store[numberid]
    avg = sum(windowCurrState) / len(windowCurrState) if windowCurrState else 0.0

    # Customize ResponseModel based on numberid
    if numberid == 'e':
        return ResponseModel(windowPrevState=windowPrevState, windowCurrState=windowCurrState, numbers=new_numbers)
    else:
        return {"numbers": []}

