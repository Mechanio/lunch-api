from app.main import create_app


app = create_app()


@app.after_request
def apply_caching(response):
    response.headers["Build-Version"] = "1.0.0"
    return response


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
