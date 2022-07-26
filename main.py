from fastapi import FastAPI, UploadFile, File, Request, status
from matting import video_matting
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os

app=FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")

@app.post("/background-matting")
async def get_item(file: UploadFile = File(...)):
    file_location = "static/input.mp4"

    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())

    file_size_mb = os.path.getsize(file_location)/1000000
    if file_size_mb>5:
        os.remove(file_location)
        print("file size is greater than 5MB. Please select the smaller size.")
        return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
    
    video_matting()
    return RedirectResponse("/play", status_code=status.HTTP_303_SEE_OTHER)
    

@app.get("/play")
def main():
    def iterfile():  # 
        with open("static/com.mp4", mode="rb") as file_like:  # 
            yield from file_like  # 

    return StreamingResponse(iterfile(), media_type="video/mp4")



@app.get("/")
async def main():
    content = """
                <body>
                <h2>Input video</h2>
                <form action="/background-matting" enctype="multipart/form-data" method="post">
                <input name="file" type="file">
                <br><br><br>
                <input type="submit">
                </form>

                """

    return HTMLResponse(content=content)