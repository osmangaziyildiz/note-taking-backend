from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.core.firebase import firebase_auth
from src.core.error_handling import UnauthorizedError
from src.modules.auth.models import TokenData
import logging

security = HTTPBearer()

class AuthService:
    @staticmethod
    def get_current_user_uid(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
        """
        Verify the Bearer token from the header and return the Firebase user ID (uid).
        If it is not verified, it will throw a HTTP 401 error.
        """
        try:
            decoded_token = firebase_auth.verify_id_token(credentials.credentials)
            uid = decoded_token['uid']
            logging.info(f"User {uid} authenticated successfully")
            return uid
        except firebase_auth.InvalidIdTokenError:
            logging.warning("Invalid or expired token provided")
            raise UnauthorizedError("Invalid or expired token. Please login again.")
        except firebase_auth.ExpiredIdTokenError:
            logging.warning("Expired token provided")
            raise UnauthorizedError("Token has expired. Please login again.")
        except Exception as e:
            logging.error(f"Authentication error: {str(e)}")
            raise UnauthorizedError("Invalid authentication credentials")

    @staticmethod
    def get_current_user_data(credentials: HTTPAuthorizationCredentials = Depends(security)) -> TokenData:
        """
        Verify the Bearer token and return full user data.
        """
        try:
            decoded_token = firebase_auth.verify_id_token(credentials.credentials)
            uid = decoded_token['uid']
            email = decoded_token.get('email')
            name = decoded_token.get('name')
            
            user_data = TokenData(
                uid=uid,
                email=email,
                name=name
            )
            
            logging.info(f"User {uid} data retrieved successfully")
            return user_data
        except firebase_auth.InvalidIdTokenError:
            logging.warning("Invalid or expired token provided")
            raise UnauthorizedError("Invalid or expired token. Please login again.")
        except firebase_auth.ExpiredIdTokenError:
            logging.warning("Expired token provided")
            raise UnauthorizedError("Token has expired. Please login again.")
        except Exception as e:
            logging.error(f"Authentication error: {str(e)}")
            raise UnauthorizedError("Invalid authentication credentials")
