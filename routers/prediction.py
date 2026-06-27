from fastapi import APIRouter, Depends, status, Response, HTTPException, Request
from sqlalchemy.orm import Session
from routers import user
import models, schema, database, oauth2
from database import get_db
from typing import List, Annotated
import pandas as pd
from services.model_loader import get_model, get_preprocessor
from rate_limits import limiter
import starlette

router = APIRouter(
    prefix = "/predict",
    tags=["Prediction"]
)



#this block of code is to predict with json. Dead code. Check it out later
# @router.get("/json")
# #prediction using json data
# async def predict_json(request: Request, clf = Depends(get_model), preproc = Depends(get_preprocessor), current_user: schema.UserExtended = Depends(oauth2.get_current_user)):
#     #user feeds json that contains the student details for prediction
#     if current_user.role != "teacher":
#         raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Only teachers can access students' records")
    

#     try:
#         input_data = await request.json()
#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Invalid JSON format. Please provide valid JSON data."
#         )
    
#     try:
#         input_df = pd.DataFrame(input_data)
#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Unable to convert JSON to DataFrame. Check data structure."
#         )
    
#     try:
#         #predicting with the json data
#         predicted_data = clf.predict(input_df)[0]
#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#             detail=f"Prediction failed. Ensure JSON contains all required features. Error: {str(e)}"
#         )

#     if predicted_data == 0:
#         return {"Prediction": "Fail"}
#     elif predicted_data == 1:
#         return {"Prediction": "Pass"}







#prediction using raw input and storing it into database
@router.post("/raw", status_code = status.HTTP_202_ACCEPTED)
#@limiter.limit("10/minute")  # limiting the number of predictions to 10 per minute
async def predict(item: schema.StudentDetails, 
                          db: Session = Depends(get_db), 
                          clf = Depends(get_model), 
                          current_user: schema.UserExtended = Depends(oauth2.get_current_user)):
    
    if current_user.role == "student":
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Only teachers can access students' records")
    

    h = item.model_dump(exclude={"student_id"})
    
    # Convert to DataFrame - the pipeline handles all preprocessing internally
    df = pd.DataFrame([h])


    # making prediction with the preprocessed json data and the ml model
    try:
        prediction = clf.predict(df)

        prediction_final = ["Pass" if (x == 1) else "Fail" for x in prediction]


        #save into student details database
        new_blog = models.Blog(student_id = item.student_id.upper(), sex = item.sex, age = item.age, 
                            address = item.address, famsize = item.famsize, 
                            Pstatus = item.Pstatus, guardian = item.guardian, 
                            traveltime = item.traveltime, studytime = item.studytime, 
                            failures = item.failures, schoolsup = item.schoolsup, 
                            famsup = item.famsup, activities = item.activities, 
                            nursery = item.nursery, famrel = item.famrel, 
                            health = item.health, absences = item.absences, 
                            freetime = item.freetime, goout = item.goout, 
                            internet = item.internet, romantic = item.romantic,
                            institution_id = current_user.institution_id.upper(),
                            Prediction = prediction_final[0])
        
        # student_id = [item.student_id], sex = [item.sex], age = [item.age], 
        #                     address = [item.address], famsize = [item.famsize], 
        #                     Pstatus = [item.Pstatus], guardian = [item.guardian], 
        #                     traveltime = [item.traveltime], studytime = [item.studytime], 
        #                     failures = [item.failures], schoolsup = [item.schoolsup], 
        #                     famsup = [item.famsup], activities = [item.activities], 
        #                     nursery = [item.nursery], famrel = [item.famrel], 
        #                     health = [item.health], absences = [item.absences], 
        #                     freetime = [item.freetime], goout = [item.goout], 
        #                     internet = [item.internet], romantic = [item.romantic],
        #                     Prediction = [prediction_final[0]]


        
        db.add(new_blog)
        db.commit()
        db.refresh(new_blog)
        
        return {"prediction": prediction_final[0]}



    #dealing with incomplete filling of student details
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail = "Prediction failed. {str(e)}}"
        )
        




# @router.post("/", status_code = status.HTTP_202_ACCEPTED, response_model = schema.returnPrediction) 
# async def predict_wrapper(item: schema.StudentDetails, 
#                           db: Session = Depends(get_db), 
#                           clf = Depends(get_model), 
#                           current_user: schema.UserExtended = Depends(oauth2.get_current_user)):
    

#     # Just call your existing predict() function
#     return await predict(item, db, clf, current_user)