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








app = FastAPI(title="Student Performance Predictor Application",
              description="An API to predict student's academic perfomance based on the student's metrics",
              version="1.0.0")




app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)




#calling the student details database
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


database.Base.metadata.create_all(database.engine)


#loading the preprocessor for SHAP analysis
with open("ml_model/stud_performance_preprocessor.joblib", "rb") as g:
    preproc = joblib.load(g)

#loading the model
with open("ml_model/stud_performance_classifier.joblib", "rb") as f:
    clf = joblib.load(f)  




@app.get("/home")
async def home():
    return {"message": "Welcome to the Student Performance Predictor API!"}









#prediction using json data
@app.post("/predict_json", status_code = status.HTTP_202_ACCEPTED, tags = ["Prediction"])
async def predict_json(request: Request):
    #user feeds json that contains the student details for prediction
    
    try:
        input_data = await request.json()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid JSON format. Please provide valid JSON data."
        )
    
    try:
        input_df = pd.DataFrame(input_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to convert JSON to DataFrame. Check data structure."
        )
    
    try:
        #predicting with the json data
        predicted_data = clf.predict(input_df)[0]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Prediction failed. Ensure JSON contains all required features. Error: {str(e)}"
        )

    if predicted_data == 0:
        return {"Prediction": "Fail"}
    elif predicted_data == 1:
        return {"Prediction": "Pass"}







#prediction using raw input and storing it into database
@app.post("/predict_raw", status_code = status.HTTP_202_ACCEPTED, tags = ["Prediction"])
async def predict_raw(item: schema.StudentDetails, db: Session = Depends(get_db)):

    h = item.model_dump(exclude={"student_id"})
    
    # Convert to DataFrame - the pipeline handles all preprocessing internally
    df = pd.DataFrame([h])


    # making prediction with the preprocessed json data and the ml model
    try:
        prediction = clf.predict(df)

        prediction_final = ["Pass" if (x == 1) else "Fail" for x in prediction]


        #save into student details database
        new_blog = models.Blog(student_id = item.student_id, sex = item.sex, age = item.age, 
                            address = item.address, famsize = item.famsize, 
                            Pstatus = item.Pstatus, guardian = item.guardian, 
                            traveltime = item.traveltime, studytime = item.studytime, 
                            failures = item.failures, schoolsup = item.schoolsup, 
                            famsup = item.famsup, activities = item.activities, 
                            nursery = item.nursery, famrel = item.famrel, 
                            health = item.health, absences = item.absences, 
                            freetime = item.freetime, goout = item.goout, 
                            internet = item.internet, romantic = item.romantic,
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
        
        return {"Prediction": prediction_final[0]}



    #dealing with incomplete filling of student details
    except Exception as e:
        raise HTTPException(
            status_code = status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail = "Prediction failed. Ensure Input is all filled out and contains all required features"
        )
    












# ────────────────────────────────────────────────────────────────────────────
# UPDATED ENDPOINTS FOR FRONTEND INTEGRATION
# ────────────────────────────────────────────────────────────────────────────

# Unified predict endpoint (accepts both JSON and form data)
@app.post("/predict", status_code=status.HTTP_202_ACCEPTED, tags=["Prediction"])
async def predict(item: schema.StudentDetails, db: Session = Depends(get_db)):
    """Make a prediction and store the result in the database."""
    h = item.model_dump(exclude={"student_id"})
    df = pd.DataFrame([h])

    try:
        prediction = clf.predict(df)
        prediction_final = ["Pass" if (x == 1) else "Fail" for x in prediction]

        # Save into student details database
        new_blog = models.Blog(
            student_id=item.student_id, sex=item.sex, age=item.age,
            address=item.address, famsize=item.famsize,
            Pstatus=item.Pstatus, guardian=item.guardian,
            traveltime=item.traveltime, studytime=item.studytime,
            failures=item.failures, schoolsup=item.schoolsup,
            famsup=item.famsup, activities=item.activities,
            nursery=item.nursery, famrel=item.famrel,
            health=item.health, absences=item.absences,
            freetime=item.freetime, goout=item.goout,
            internet=item.internet, romantic=item.romantic,
            Prediction=prediction_final[0]
        )

        db.add(new_blog)
        db.commit()
        db.refresh(new_blog)

        return {
            "prediction": prediction_final[0],
            "student_id": item.student_id,
            "confidence": float(clf.predict_proba(df)[0].max())
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Prediction failed. Ensure all required features are provided. Error: {str(e)}"
        )


# Get all students
@app.get("/students", tags=["Students"])
async def get_students(db: Session = Depends(get_db)):
    """Retrieve all student records."""
    blogs = db.query(models.Blog).all()
    students = []
    for blog in blogs:
        student_dict = {c.name: getattr(blog, c.name) for c in blog.__table__.columns}
        students.append(student_dict)
    return {"students": students}


# Get specific student by ID
@app.get("/students/{student_id}", tags=["Students"])
def get_student(student_id: str, response: Response, db: Session = Depends(get_db)):
    """Retrieve a specific student record by student ID."""
    blog = db.query(models.Blog).filter(models.Blog.student_id == student_id).first()

    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student record with ID {student_id} not found"
        )

    student_dict = {c.name: getattr(blog, c.name) for c in blog.__table__.columns}
    return student_dict


# Delete student record
@app.delete("/students/{student_id}", status_code=status.HTTP_200_OK, tags=["Students"])
async def delete_student(student_id: str, db: Session = Depends(get_db)):
    """Delete a student record by student ID."""
    blog = db.query(models.Blog).filter(models.Blog.student_id == student_id)

    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student record with ID {student_id} not found"
        )

    blog.delete(synchronize_session=False)
    db.commit()

    return {"message": f"Student record with ID {student_id} has been deleted"}


# Get SHAP analysis chart for a student
@app.get("/students/{student_id}/shap", tags=["SHAP Analysis"])
def get_shap_analysis(student_id: str, db: Session = Depends(get_db)):
    """Generate and return SHAP analysis chart for a student's prediction."""
    blog = db.query(models.Blog).filter(models.Blog.student_id == student_id).first()

    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student record with ID {student_id} not found"
        )

    data_in_dict = blog.__dict__.copy()
    data_in_dict.pop('_sa_instance_state', None)
    del data_in_dict["student_id"]

    # Convert the prediction details to a dataframe for shap analysis
    student_data = pd.DataFrame([data_in_dict])
    student_data_transformed = preproc.fit_transform(student_data)

    # Refining the clf model
    model = clf.named_steps[clf.steps[-1][0]]
    clf.set_output(transform="default")

    # Creating SHAP explainer and values
    explainer = shap.TreeExplainer(model)
    shap_values = explainer(student_data_transformed, check_additivity=False)

    # Visualizing analysis plot
    shap.summary_plot(shap_values, student_data_transformed, plot_type="bar", show=False)
    fig = plt.gcf()
    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", bbox_inches="tight")
    buffer.seek(0)
    plt.clf()
    plt.close(fig)

    return StreamingResponse(buffer, media_type="image/png")


# ────────────────────────────────────────────────────────────────────────────
# LEGACY ENDPOINTS (for backward compatibility)
# ────────────────────────────────────────────────────────────────────────────

#this is for getting all students' prediction data
@app.get("/get_all_records", tags=["Students' Record"])
async def get_all_records(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs







#getting student's record according to student's student_id
@app.get("/get_all_records/{id_number}", tags = ["Students' Record"])
def get_record_by_id(id_number, response: Response, db: Session = Depends(get_db)):

    blogs = db.query(models.Blog).filter(models.Blog.student_id == id_number).first()

    if not blogs:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Seudent record with id {id_number} is not available")
    
    return blogs






#deleting a student's record using his or her student_id
@app.delete("/get_all_records/{id_number}", status_code = status.HTTP_200_OK, tags = ["Students' Record"])

async def destroy(id_number, db: Session = Depends(get_db)):

    blog = db.query(models.Blog).filter(models.Blog.student_id == id_number)
    if not blog.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Student record with id {id_number} not available")
    

    blog.delete(synchronize_session = False)

    
    db.commit()
    return {"response": f"Student's record with id number {id_number} has been deleted"}

    



#generating shap analysis for a student's prediction using the student's student_id
@app.get("/shap_analysis/{id_number}", tags = ["SHAP Analysis"])

def shap_analysis(id_number, db: Session = Depends(get_db)):

    blog = db.query(models.Blog).filter(models.Blog.student_id == id_number).first()
    if not blog:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Student record with id {id_number} not available")
    

    data_in_dict = blog.__dict__.copy()
    data_in_dict.pop('_sa_instance_state', None)
    del data_in_dict["student_id"] 


    # for k, v in data_in_dict.items():
    #     if isinstance(v, str):
    #         data_in_dict[k] = [v]
    #     else:
    #         data_in_dict[k] = [v] 

 

    #convert the prediction details to a dataframe for shap analysis
    student_data = pd.DataFrame([data_in_dict])
    student_data_transformed = preproc.fit_transform(student_data)

    #refining the clf model
    model = model = clf.named_steps[clf.steps[-1][0]]  
    clf.set_output(transform = "default")


    #creating SHAP explainer and values
    explainer = shap.TreeExplainer(model)

    # Calculate SHAP values
    shap_values = explainer(student_data_transformed, check_additivity = False)


    # visualizing analysis plot
    # fig = Figure()
    # ax = fig.subplots(figsize=(10, 6))
    
    
    shap.summary_plot(shap_values, student_data_transformed, plot_type="bar", show = False)
    fig = plt.gcf()
    buffer = io.BytesIO()
    fig.savefig(buffer, format = "png", bbox_inches = "tight")
    buffer.seek(0)
    plt.clf()
    plt.close(fig)

    #returning shap analysis and prediction for student's record
    
    return StreamingResponse(buffer, media_type = "image/png")
    return{"Prediction": blog.Prediction, "SHAP Analysis": "SHAP analysis plot generated successfully"}
    





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