from fastapi import FastAPI

from app.core.config import settings

def main():
    app = FastAPI(title=settings["APP_NAME"])


if __name__ == "__main__":
    main()
