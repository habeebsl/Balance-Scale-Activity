import os
from dotenv import load_dotenv
from fastapi import Header, HTTPException
from firebase_admin import credentials, auth, initialize_app


load_dotenv()
firebase_config = {
  "type": "service_account",
  "project_id": os.getenv("FIREBASE_PROJECT_ID"),
  "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
  "private_key": os.getenv("FIREBASE_PRIVATE_KEY"),
  "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
  "client_id": os.getenv("FIREBASE_CLIENT_ID"),
  "auth_uri": os.getenv("FIREBASE_AUTH_URI"),
  "token_uri": os.getenv("FIREBASE_TOKEN_URI"),
  "auth_provider_x509_cert_url": os.getenv("FIREBASE_AUTH_PROVIDER_X509_CERT_URL"),
  "client_x509_cert_url": os.getenv("FIREBASE_CLIENT_X509_CERT_URL"),
  "universe_domain": os.getenv("FIREBASE_UNIVERSE_DOMAIN")
}

cred = credentials.Certificate(firebase_config)
initialize_app(cred)

async def verify_token(authorization: str = Header(...)):
  try:
      token = authorization.split(" ")[1]  # Assumes format: "Bearer <token>" 
      decoded_token = auth.verify_id_token(token, check_revoked=True, clock_skew_seconds=10)
      return decoded_token
  except Exception as e:
      print(f"Token verification failed: {e}")
      raise HTTPException(status_code=401, detail="Invalid or expired token")