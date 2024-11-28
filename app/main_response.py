# from fastapi import FastAPI, Form
# from fastapi.responses import HTMLResponse
# from fastapi.staticfiles import StaticFiles
# from fastapi.templating import Jinja2Templates
# from fastapi.requests import Request
#
# app = FastAPI()
#
# # Mount templates directory
# templates = Jinja2Templates(directory="templates")
#
# @app.get("/", response_class=HTMLResponse)
# async def read_root(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})
#
# @app.post("/response")
# async def get_response(user_input: str = Form(...)):
#     response_message = f"You said: {user_input}"
#     return {"response": response_message}

from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

app = FastAPI()

# Mount templates directory
templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/response")
async def get_response(user_input: str = Form(...)):
    try:
        # Simulate an error for demonstration
        if not user_input.strip():
            raise ValueError("Input cannot be empty or whitespace!")

        response_message = f"The response for your question is : {user_input}"
        return {"response": response_message}

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))

    except Exception as e:
        # Catch-all for unexpected errors
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")
