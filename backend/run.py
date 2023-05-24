from app import init_app

app = init_app()

if __name__ == "__main__":
    # NOTE: reminder that the `flask` cli tool does not use these configurations
    #       equivalent would be `FLASK_APP=run.py poetry run flask run --host "0.0.0.0" --port 8080 --debug`
    app.run(host="0.0.0.0", port=8080, debug=True)