from app import app


@app.route('/<string:user_name>')
def index(user_name: str):
    return f"Hello, {user_name}"
