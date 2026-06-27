from fastapi import APIRouter, Depends, status, Response, HTTPException, Header, Request
from sqlalchemy.orm import Session
import models, schema, database, hashing, oauth2
from database import get_db
from typing import List
from rate_limits import limiter

router = APIRouter(
    prefix = "/user",
    tags=["User"]
)


temp_verification_store = {}

# Dependency to check for the token
def verify_access_token(x_verify_token: str = Header(...)):
    if x_verify_token not in temp_verification_store:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Role not verified. Please call /verify-role first."
        )
    return temp_verification_store[x_verify_token]




@router.post("/verify-role")
#@limiter.limit("5/minute")  # number of verification requests per minute
async def verify_role(institution_id: str):
    # Logic: Validate the code against your business rules
    if institution_id.upper().startswith("STU"):
        role = "student"
    elif institution_id.upper().startswith("TEA"):
        role = "teacher"
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Invalid role code format."
        )

    # Generate a unique token
    import uuid
    token = str(uuid.uuid4())
    
    # Store the role associated with this specific token
    temp_verification_store[token] = role 
    
    return {"message": f"Verified as {role}", "token": token}




#creating user profile and storing it in database
@router.post("/signup", status_code = status.HTTP_201_CREATED)
#@limiter.limit("5/minute")  # number of signup requests per minute
def create_User(request: schema.User, role: str = Depends(verify_access_token), db: Session = Depends(get_db)):
    if request.password == request.confirm_password:
        new_user = models.User(firstname = request.firstname.capitalize(), lastname = request.lastname.capitalize(), role = role,
                               institution_id = request.institution_id.upper(), 
                           email = request.email.lower(), password = hashing.Hash().bcrypt(request.password))  #this particular piece of code is for hashing passwords that users put in. Using a class Hash to convert it to hashed passwords
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"message" : "Successfully created user. You can head over to login"}


    else:
        raise HTTPException(status_code = status.HTTP_406_NOT_ACCEPTABLE, detail = "Password details do not match. Try again")