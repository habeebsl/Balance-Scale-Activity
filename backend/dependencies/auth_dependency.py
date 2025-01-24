from fastapi import Header, HTTPException
from firebase_admin import credentials, auth, initialize_app

cred = credentials.Certificate("serviceAccountKey.json")
initialize_app(cred)

async def verify_token(authorization: str = Header(...)):
    try:
        token = authorization.split(" ")[1]  # Assumes format: "Bearer <token>" 
        decoded_token = auth.verify_id_token(token, check_revoked=True, clock_skew_seconds=10)
        return decoded_token
    except Exception as e:
        print(f"Token verification failed: {e}")
        raise HTTPException(status_code=401, detail="Invalid or expired token")