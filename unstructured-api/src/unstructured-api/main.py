import os
import sys
import uuid

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from unstructured.partition.auto import partition

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = FastAPI()


@app.post("/extract-document")
async def extract_document(file: UploadFile = File(...)):
    file_extension = os.path.splitext(file.filename)[1]
    if file_extension == "":
        return JSONResponse(
            content={"error": "File extension is missing"}, status_code=400
        )
    temp_file_path = os.path.join("/tmp", f"{uuid.uuid4()}{file_extension}")
    try:
        with open(temp_file_path, "wb") as temp_file:
            content = await file.read()
            temp_file.write(content)
        elements = partition(
            filename=temp_file_path,
            strategy="hi_res",
            languages=["deu", "eng"],
            include_page_breaks=True,
        )
        stripped_elements = []
        for x_element_index, x_element in enumerate(elements):
            if x_element.category == "PageBreak":
                continue
            points = x_element.metadata.coordinates.points
            stripped_element = {
                "id": x_element_index,
                "text": x_element.text,
                "category": x_element.category,
                "points": {
                    "topLeft": {
                        "x": round(points[0][0]),
                        "y": round(points[0][1]),
                    },
                    "bottomLeft": {
                        "x": round(points[1][0]),
                        "y": round(points[1][1]),
                    },
                    "bottomRight": {
                        "x": round(points[2][0]),
                        "y": round(points[2][1]),
                    },
                    "topRight": {
                        "x": round(points[3][0]),
                        "y": round(points[3][1]),
                    },
                },
            }
            stripped_elements.append(stripped_element)
        return JSONResponse(content={"elements": stripped_elements})
    except Exception as exception:
        return JSONResponse(content={"error": str(exception)}, status_code=500)
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5011)
