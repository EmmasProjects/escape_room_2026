"""A web server for controlling the state of 3 buttons.

It also has a view page and an admin page.
"""

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI()

# State defined as a list
state = ["red", "red", "red"]


class ColourUpdateSchema(BaseModel):
    """The Schema for updating a colour."""

    index: int  # Using integer index for the list
    new_color: str

class ColourReturnSchema(BaseModel):
    """The schema for returning a colour."""

    colors: list[str]


# @app.get("/colors") makes it so that you can
# view the output of get_all_colors in a web browser when you go to /colors.
@app.get("/colors")
def get_all_colors() -> ColourReturnSchema:
    """Return all the button states."""
    return {"colors": state}


@app.post("/update-color")
def update_color(updated_colour: ColourUpdateSchema) -> ColourReturnSchema:
    """Update a colour, given the index and the new colour."""
    # Ensure the index is within the list range
    if 0 <= updated_colour.index < len(state):
        state[updated_colour.index] = updated_colour.new_color
    else:
        raise HTTPException(
            status_code=400,
            detail=f"Index {updated_colour.index} is out of range.Use 0 to {len(state) - 1}.",  # noqa: E501
        )
    return {"colors": state}


@app.get("/")
def read_index() -> FileResponse:
    """Return the index html file."""
    return FileResponse("index.html")


# @app.get("/admin") makes it so that you can
# interact with the asdmin page in a web browser when you go to /admin.
@app.get("/admin")
def show_admin_page() -> FileResponse:
    """Return the admin html file."""
    return FileResponse("admin.html")

# If main.py is the application being run, then start a server.
if __name__ == "__main__":
    uvicorn.run("main:app",
                host="127.0.0.1",
                port=8000,
                reload=True)
