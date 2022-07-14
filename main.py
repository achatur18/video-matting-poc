from fastapi import FastAPI, UploadFile, File, Request
from matting import video_matting
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from fastapi.templating import Jinja2Templates


app=FastAPI()
templates = Jinja2Templates(directory="templates")

@app.post("/background-matting")
async def get_item(request: Request, file: UploadFile = File(...)):
    file_location = "input.mp4"
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())
    
    video_matting()
    return {"message":"Open '/play' for viewing matted video"}
    

@app.get("/play")
def main():
    def iterfile():  # 
        with open("com.mp4", mode="rb") as file_like:  # 
            yield from file_like  # 

    return StreamingResponse(iterfile(), media_type="video/mp4")
