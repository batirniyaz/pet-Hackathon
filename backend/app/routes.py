from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
import crud, schemas, auth, email_utils
from sqlalchemy.orm import Session
import dependencies

router = APIRouter()


@router.post("/register/", response_model=schemas.UserResponse)
async def register_user(background_tasks: BackgroundTasks, user: schemas.UserCreate, db: Session = Depends(
    dependencies.get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    if user.password != user.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    # Generate a secure random verification code
    verification_code = crud.generate_verification_code()  # You'll need to implement this

    # Create user with hashed password (not storing plain password!)
    hashed_password = crud.get_password_hash(user.password)
    user_dict = user.dict()
    user_dict["hashed_password"] = hashed_password
    user_dict.pop("password")
    user_dict.pop("confirm_password")
    user_dict["verification_code"] = verification_code  # Store the code for later verification
    new_user = crud.create_user(db=db, user=user_dict)

    # Send verification email
    await email_utils.send_verification_email(background_tasks, new_user.email, verification_code)

    # Return the created user, excluding sensitive information like hashed_password
    return schemas.UserResponse(email=new_user.email, username=new_user.username)


@router.post("/login/", response_model=schemas.Token)
async def login_for_access_token(form_data: schemas.UserResponse, db: Session = Depends(dependencies.get_db())):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/verify-email/")
def verify_email(email: str, code: str, db: Session = Depends(dependencies.get_db())):
    if not email_utils.verify_code(email, code):
        raise HTTPException(status_code=400, detail="Invalid or expired code")
    crud.mark_email_as_verified(db, email)
    return {"message": "Email verified successfully."}

