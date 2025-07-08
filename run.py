print("Starting Flask App...")

from app.routes import app

if __name__ == "__main__":
    print("Running Flask App...")
    app.run(debug=True)
