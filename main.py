import uvicorn

if __name__ == "__main__":
    uvicorn.run("akaike:app", host="0.0.0.0", port=7860, reload=True)
