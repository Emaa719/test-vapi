import pandas as pd
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class NameInput(BaseModel):
    name: str

"""@app.get('/')
def read_root():
    return {"message": "Welcome to the Name Checker API"}"""

@app.post('/check_and_add_name')
def check_and_add_name(data: NameInput):
    filename = os.path.join(os.path.dirname(__file__), 'names.csv')
    user_name = data.name

    if not user_name:
        raise HTTPException(status_code=400, detail="Name not provided")

    # Check if the CSV file exists and has content
    if os.path.exists(filename):
        # Load names from the CSV file
        df = pd.read_csv(filename)
    else:
        # Create an empty DataFrame if the file does not exist
        df = pd.DataFrame(columns=['name'])

    # Check if the name already exists in the DataFrame
    if user_name in df['name'].values:
        return {"message": "Name already exists"}

    # Add the new name to the DataFrame
    new_data = pd.DataFrame([{'name': user_name}])
    df = pd.concat([df, new_data], ignore_index=True)

    # Save the updated DataFrame back to the CSV
    df.to_csv(filename, index=False)
    return {"message": "Name added successfully"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8080)
