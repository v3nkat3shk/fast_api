from fastapi import FastAPI


class Server:
    def __init__(self, db, router) -> None:
        self.app = FastAPI(debug=True)
        self.db = db
        self.router = router
