from typing import Dict, Any

from fastapi import HTTPException, status


class UserNotFoundException(HTTPException):
    def __init__(self,
                 user_id=None,
                 status_code=status.HTTP_400_BAD_REQUEST,
                 detail: Any = None,
                 headers: Dict[str, str] | None = None) -> None:
        detail = f"User of id: {user_id} not found" if user_id else "User not found"
        super().__init__(status_code, detail, headers)
