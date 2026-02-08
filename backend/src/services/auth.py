from fastapi import Header, HTTPException

def get_current_user_id(x_user_id: str = Header(..., alias="user-id")) -> str:
    # In a real app, this would verify the JWT/Session via Better Auth
    # For this prototype, we'll accept it from the header
    if not x_user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return x_user_id
