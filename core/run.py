import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="localhost",
        port=7069,
        reload=True,
        ssl_certfile="certs/localhost+2.pem",
        ssl_keyfile="certs/localhost+2-key.pem"
    )
