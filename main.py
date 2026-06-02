"""A web server for controlling the state of 3 buttons.

It also has a view page and an admin page.
"""

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

from fastapi.staticfiles import StaticFiles

app = FastAPI()

# State defined as a list
game_state = [False, False, False]
game_stage = "holding"

@app.get("/state")
def get_state():
    return game_state

@app.post("/set-stage/{stage}")
def set_stage(stage: str):
    game_stage = stage
    return {"status": "ok", "stage": game_stage}

@app.post("/artefact-found/{artefact_id}/{found}")
def set_the_state_of_an_artefact(artefact_id: int, found: bool):
    game_state[artefact_id] = found
    return game_state[artefact_id]

# game_state = {
#     "stage": stage,
#     "sliders": {
#         "slider1": False,
#         "slider2": False,
#         "slider3": False
#     }
# }

# @app.post("/set-slider/{slider}/{value}")
# def set_slider(slider: str, value: bool):
#     if slider in game_state["sliders"]:
#         game_state["sliders"][slider] = value
#     return game_state



class ArtefactUpdateSchema(BaseModel):
    """The Schema for updating a colour."""

    index: int  # Using integer index for the list
    found: bool

class ArtefactReturnSchema(BaseModel):
    """The schema for returning a colour."""

    found: list[bool]


# @app.get("/colors") makes it so that you can
# view the output of get_all_colors in a web browser when you go to /colors.
@app.get("/colors")
def get_all_colors() -> ArtefactReturnSchema:
    """Return all the button states."""

    return {"found": game_state}


# @app.post("/update-color")
# def update_color(updated_colour: ColourUpdateSchema) -> ColourReturnSchema:
#     """Update a colour, given the index and the new colour."""
#     # Ensure the index is within the list range
#     if 0 <= updated_colour.index < len(state):
#         state[updated_colour.index] = updated_colour.new_color
#     else:
#         raise HTTPException(
#             status_code=400,
#             detail=f"Index {updated_colour.index} is out of range.Use 0 to {len(state) - 1}.",  # noqa: E501
#         )
#     return {"colors": state}


@app.get("/")
def read_index() -> FileResponse:
    """Return the index html file."""
    return FileResponse("index.html")

@app.get("/lights")
def show_lights_page() -> FileResponse:
    """Return the index html file."""
    return FileResponse("lights.html")


@app.get("/password-entry")
def show_password_page() -> FileResponse:
    """Return the index html file."""
    return FileResponse("password-entry.html")


# @app.get("/admin") makes it so that you can
# interact with the asdmin page in a web browser when you go to /admin.
@app.get("/admin")
def show_admin_page() -> FileResponse:
    """Return the admin html file."""
    return FileResponse("admin.html")

# Serve everything in /static
app.mount("/", StaticFiles(directory="static"), name="static")

# If main.py is the application being run, then start a server.
if __name__ == "__main__":
    uvicorn.run("main:app",
                host="127.0.0.1",
                port=8000,
                reload=True)
