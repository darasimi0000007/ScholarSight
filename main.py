import matplotlib
matplotlib.use("Agg")
from fastapi import FastAPI, Request, Depends, status, Response, HTTPException
from pydantic import BaseModel
import os
import joblib
from sklearn.preprocessing import OneHotEncoder
import uvicorn
import pandas as pd
import schema
import models
import database
from sqlalchemy.orm import Session
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import shap
from sqlalchemy.inspection import inspect as sqlalchemy_inspect
import io
import matplotlib.pyplot as plt
from fastapi.responses import StreamingResponse
from matplotlib.figure import Figure
from fastapi.middleware.cors import CORSMiddleware
from routers import prediction, user, authentication, records
from contextlib import asynccontextmanager
from services.model_loader import load_model, load_preprocessor

from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from rate_limits import limiter
from typing import cast, Any
from config_file import origins



#loading the model and preprocessor from model_loader.py
@asynccontextmanager
async def lifespan(app: FastAPI):
    # This runs once on startup
    load_model()
    load_preprocessor()
    yield





app = FastAPI(title="ScholarSight",
              description="An API to predict student's academic perfomance based on the student's metrics",
              version="1.0.0", lifespan = lifespan)


# async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
#     return _rate_limit_exceeded_handler(request, exc)

# app.state.limiter = limiter
# app.add_exception_handler(RateLimitExceeded, cast(Any, rate_limit_handler))







app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)






database.Base.metadata.create_all(database.engine)




  




@app.get("/home")
async def home():
    return {"message": "Welcome to the Student Performance Predictor API!"}









#prediction endpoint
app.include_router(prediction.router)







#prediction using raw input and storing it into database
# @app.post("/predict_raw", status_code = status.HTTP_202_ACCEPTED, tags = ["Prediction"])
# async def predict_raw(item: schema.StudentDetails, db: Session = Depends(get_db)):

#     h = item.model_dump(exclude={"student_id"})
    
#     # Convert to DataFrame - the pipeline handles all preprocessing internally
#     df = pd.DataFrame([h])


#     # making prediction with the preprocessed json data and the ml model
#     try:
#         prediction = clf.predict(df)

#         prediction_final = ["Pass" if (x == 1) else "Fail" for x in prediction]


#         #save into student details database
#         new_blog = models.Blog(student_id = item.student_id, sex = item.sex, age = item.age, 
#                             address = item.address, famsize = item.famsize, 
#                             Pstatus = item.Pstatus, guardian = item.guardian, 
#                             traveltime = item.traveltime, studytime = item.studytime, 
#                             failures = item.failures, schoolsup = item.schoolsup, 
#                             famsup = item.famsup, activities = item.activities, 
#                             nursery = item.nursery, famrel = item.famrel, 
#                             health = item.health, absences = item.absences, 
#                             freetime = item.freetime, goout = item.goout, 
#                             internet = item.internet, romantic = item.romantic,
#                             Prediction = prediction_final[0])
        
#         # student_id = [item.student_id], sex = [item.sex], age = [item.age], 
#         #                     address = [item.address], famsize = [item.famsize], 
#         #                     Pstatus = [item.Pstatus], guardian = [item.guardian], 
#         #                     traveltime = [item.traveltime], studytime = [item.studytime], 
#         #                     failures = [item.failures], schoolsup = [item.schoolsup], 
#         #                     famsup = [item.famsup], activities = [item.activities], 
#         #                     nursery = [item.nursery], famrel = [item.famrel], 
#         #                     health = [item.health], absences = [item.absences], 
#         #                     freetime = [item.freetime], goout = [item.goout], 
#         #                     internet = [item.internet], romantic = [item.romantic],
#         #                     Prediction = [prediction_final[0]]


        
#         db.add(new_blog)
#         db.commit()
#         db.refresh(new_blog)
        
#         return {"Prediction": prediction_final[0]}



#     #dealing with incomplete filling of student details
#     except Exception as e:
#         raise HTTPException(
#             status_code = status.HTTP_422_UNPROCESSABLE_CONTENT,
#             detail = "Prediction failed. Ensure Input is all filled out and contains all required features"
#         )
    





#records' access endpoint
app.include_router(records.router)






















# ────────────────────────────────────────────────────────────────────────────
# LEGACY ENDPOINTS (for backward compatibility)
# ────────────────────────────────────────────────────────────────────────────

# #this is for getting all students' prediction data
# @app.get("/get_all_records", tags=["Students' Record"])
# async def get_all_records(db: Session = Depends(get_db)):
#     blogs = db.query(models.Blog).all()
#     return blogs







# #getting student's record according to student's student_id
# @app.get("/get_all_records/{id_number}", tags = ["Students' Record"])
# def get_record_by_id(id_number, response: Response, db: Session = Depends(get_db)):

#     blogs = db.query(models.Blog).filter(models.Blog.student_id == id_number).first()

#     if not blogs:
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Seudent record with id {id_number} is not available")
    
#     return blogs






# #deleting a student's record using his or her student_id
# @app.delete("/get_all_records/{id_number}", status_code = status.HTTP_200_OK, tags = ["Students' Record"])

# async def destroy(id_number, db: Session = Depends(get_db)):

#     blog = db.query(models.Blog).filter(models.Blog.student_id == id_number)
#     if not blog.first():
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Student record with id {id_number} not available")
    

#     blog.delete(synchronize_session = False)

    
#     db.commit()
#     return {"response": f"Student's record with id number {id_number} has been deleted"}

    



# #generating shap analysis for a student's prediction using the student's student_id
# @app.get("/shap_analysis/{id_number}", tags = ["SHAP Analysis"])

# def shap_analysis(id_number, db: Session = Depends(get_db)):

#     blog = db.query(models.Blog).filter(models.Blog.student_id == id_number).first()
#     if not blog:
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Student record with id {id_number} not available")
    

#     data_in_dict = blog.__dict__.copy()
#     data_in_dict.pop('_sa_instance_state', None)
#     del data_in_dict["student_id"] 


#     # for k, v in data_in_dict.items():
#     #     if isinstance(v, str):
#     #         data_in_dict[k] = [v]
#     #     else:
#     #         data_in_dict[k] = [v] 

 

#     #convert the prediction details to a dataframe for shap analysis
#     student_data = pd.DataFrame([data_in_dict])
#     student_data_transformed = preproc.fit_transform(student_data)

#     #refining the clf model
#     model = model = clf.named_steps[clf.steps[-1][0]]  
#     clf.set_output(transform = "default")


#     #creating SHAP explainer and values
#     explainer = shap.TreeExplainer(model)

#     # Calculate SHAP values
#     shap_values = explainer(student_data_transformed, check_additivity = False)


#     # visualizing analysis plot
#     # fig = Figure()
#     # ax = fig.subplots(figsize=(10, 6))
    
    
#     shap.summary_plot(shap_values, student_data_transformed, plot_type="bar", show = False)
#     fig = plt.gcf()
#     buffer = io.BytesIO()
#     fig.savefig(buffer, format = "png", bbox_inches = "tight")
#     buffer.seek(0)
#     plt.clf()
#     plt.close(fig)

#     #returning shap analysis and prediction for student's record
    
#     return StreamingResponse(buffer, media_type = "image/png")
#     return{"Prediction": blog.Prediction, "SHAP Analysis": "SHAP analysis plot generated successfully"}
# 




#router for user registration
app.include_router(user.router)




#router for authentication and login
app.include_router(authentication.router)








if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)









#look into shap to explain features that were vital to a prediction and 
#suggest advices based on predictions, 
# 
# 
# implement a teachers database for authentication, teachers are the only ones that can make predictions on behalf of students


#school admin for modifying student prediction records, 
# 
# 
# students database for authentication as well to allow students to just view their SHAP analysis on their respective predictions