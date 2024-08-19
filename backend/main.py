
import io
from skimage import io as sk_io
from imageio import v3 as iio
from fastapi import FastAPI, Response

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/return-image-test/")
async def image_test():
    chosenImg = sk_io.imread("test.jpg")
    with io.BytesIO() as buf:
        iio.imwrite(buf, chosenImg, plugin="pillow", format="JPEG")
        im_bytes = buf.getvalue()
        
    headers = {'Content-Disposition': 'inline; filename="test.jpeg"'}
    return Response(im_bytes, headers=headers, media_type='image/jpeg')