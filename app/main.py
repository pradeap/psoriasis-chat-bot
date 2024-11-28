import openai
import sqlite3
from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

# Initialize FastAPI
app = FastAPI()

# Mount templates directory
templates = Jinja2Templates(directory="app/templates")

# Set your OpenAI API key
openai.api_key = "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"  # Replace with your actual API key or use environment variables

# Database connection function
def query_database(sql_query: str):
    try:
        conn = sqlite3.connect("psoriasis.db")
        cursor = conn.cursor()
        cursor.execute(sql_query)
        results = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]
        conn.close()
        return {"columns": column_names, "rows": results}
    except sqlite3.Error as e:
        raise ValueError(f"Database error: {str(e)}")
    except Exception as e:
        raise ValueError(f"Unexpected error: {str(e)}")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/response")
async def get_openai_response(user_input: str = Form(...)):
    try:
        if not user_input.strip():
            raise ValueError("Input cannot be empty or whitespace!")

        # Generate SQL query using OpenAI
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use gpt-4 if needed
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a database expert. Convert natural language questions into SQL queries "
                        "for a SQLite database. Ensure the SQL query is properly formatted and valid."
                    ),
                },
                {"role": "user", "content": user_input},
            ],
            temperature=0.3,
        )

        sql_query = completion["choices"][0]["message"]["content"].strip()

        # Execute the SQL query on the database
        query_results = query_database(sql_query)

        # Format results for output
        formatted_results = {
            "columns": query_results["columns"],
            "rows": query_results["rows"],
            "sql_query": sql_query,
        }
        return {"response": formatted_results}

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))

    except openai.error.APIError as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API returned an API error: {e}")
    except openai.error.AuthenticationError as e:
        raise HTTPException(status_code=401, detail=f"Authentication error: {e}")
    except openai.error.InvalidRequestError as e:
        raise HTTPException(status_code=400, detail=f"Invalid request: {e}")
    except openai.error.RateLimitError as e:
        raise HTTPException(status_code=429, detail=f"Rate limit exceeded: {e}")
    except openai.error.OpenAIError as e:  # Generic OpenAI error
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")


    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")

