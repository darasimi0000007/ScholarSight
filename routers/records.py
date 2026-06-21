import matplotlib
matplotlib.use("Agg")
from fastapi import APIRouter, Depends, status, Response, HTTPException, Request
from sqlalchemy.orm import Session
from routers import user
import models, schema, database, oauth2
from database import get_db
from typing import List, Annotated
import pandas as pd
import shap
from services.model_loader import get_model, get_preprocessor
import matplotlib.pyplot as plt
import io
from fastapi.responses import StreamingResponse
from matplotlib.figure import Figure
from sqlalchemy.inspection import inspect as sqlalchemy_inspect

router = APIRouter(
    prefix = "/students",
    tags=["Records' Retrieval"]
)




#this is for getting all students' prediction data
@router.get("/get_all_records")
async def get_students(db: Session = Depends(get_db), current_user: schema.UserExtended = Depends(oauth2.get_current_user)):
    if current_user.role != "teacher":
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Only teachers can access students' records")
    
    blogs = db.query(models.Blog).all()
    return blogs



#wrapper for get all students' prediction data endpoint to maintain consistent URL structure
@router.get("")
async def get_all_student_default(db: Session = Depends(get_db), 
                                  current_user: schema.UserExtended = Depends(oauth2.get_current_user)):
    return await get_students(db, current_user)



# Get specific student by ID
@router.get("/one_student/{student_id}")
def get_student(student_id: str, response: Response, db: Session = Depends(get_db), current_user: schema.UserExtended = Depends(oauth2.get_current_user)):
    if current_user.role != "teacher":
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Only teachers can access students' records")
    

    blogs = db.query(models.Blog).filter(models.Blog.student_id == student_id.upper()).first()

    if not blogs:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Student record with id {student_id} is not available")
    
    return blogs



#wrapper for get student by id endpoint to maintain consistent URL structure
@router.get("/student/{student_id}")
async def get_one_student_default(student_id: str, response: Response, db: Session = Depends(get_db),
                                  current_user: schema.UserExtended = Depends(oauth2.get_current_user)):
    return get_student(student_id, response, db, current_user)







# Get SHAP analysis chart 
@router.get("/student/{student_id}/shap") 
async def get_shap_analysis(student_id: str, db: Session = Depends(get_db), clf = Depends(get_model), preproc = Depends(get_preprocessor),
                       current_user: schema.UserExtended = Depends(oauth2.get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.student_id == student_id.upper()).first()
    if not blog:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Student record with id {student_id} not available")
    

    data_in_dict = blog.__dict__.copy()
    data_in_dict.pop('_sa_instance_state', None)
    del data_in_dict["student_id"]
    del data_in_dict["institution_id"]
    del data_in_dict["Prediction"]
    


    # for k, v in data_in_dict.items():
    #     if isinstance(v, str):
    #         data_in_dict[k] = [v]
    #     else:
    #         data_in_dict[k] = [v] 

 

    #convert the prediction details to a dataframe for shap analysis
    student_data = pd.DataFrame([data_in_dict])
    student_data_transformed = clf[:-1].transform(student_data)   #preproc.transform(student_data)



    # OneHotEncoder can return a sparse matrix — SHAP needs dense input
    if hasattr(student_data_transformed, "toarray"):
        student_data_transformed = student_data_transformed.toarray()

    # pull real column names out of the fitted preprocessing steps so the chart
    # labels bars as "guardian_mother", "studytime", etc. instead of "Feature 0", "Feature 1"
    try:
        feature_names = clf[:-1].get_feature_names_out()
        feature_names = [n.split("__", 1)[1] if "__" in n else n for n in feature_names]
    except Exception:
        feature_names = None  # fall back to SHAP's default labels if names aren't available



    #refining the clf model
    model = clf.named_steps[clf.steps[-1][0]]  
    clf.set_output(transform = "default")

    try:
        #creating SHAP explainer and values
        explainer = shap.TreeExplainer(model)

        # Calculate SHAP values
        shap_values = explainer(student_data_transformed, check_additivity = False)
        


        # visualizing analysis plot
        # fig = Figure()
        # ax = fig.subplots(figsize=(10, 6))
        
        
        shap.summary_plot(shap_values, student_data_transformed, plot_type="bar", show = False, feature_names = feature_names)
        fig = plt.gcf()
        buffer = io.BytesIO()
        fig.savefig(buffer, format = "png", bbox_inches = "tight")
        buffer.seek(0)
        plt.clf()
        plt.close(fig)


        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"SHAP analysis failed. Error: {str(e)}"
        )
    

    #returning shap analysis and prediction for student's record
    
    return StreamingResponse(buffer, media_type = "image/png")
    




# wrapper endpoint for get SHAP analysis chart to maintain consistent URL structure
@router.get("/{student_id}/shap")
async def get_shap_analysis_default(student_id: str, db: Session = Depends(get_db), 
                                   clf = Depends(get_model), preproc = Depends(get_preprocessor),
                                   current_user: schema.UserExtended = Depends(oauth2.get_current_user)):
    return await get_shap_analysis(student_id, db, clf, preproc, current_user)











# Delete student record
@router.delete("/student/{student_id}", status_code=status.HTTP_200_OK)
async def delete_student(student_id: str, db: Session = Depends(get_db), current_user: schema.UserExtended = Depends(oauth2.get_current_user)):
    if current_user.role != "teacher":
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Only teachers can access students' records")
    

    blog = db.query(models.Blog).filter(models.Blog.student_id == student_id.upper())
    if not blog.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Student record with id {student_id} not available")
    

    blog.delete(synchronize_session = False)

    
    db.commit()
    return {"response": f"Student's record with id number {student_id} has been deleted"}






#wrapper for delete student record endpoint to maintain consistent URL structure
@router.delete("/{student_id}")
async def delete_student_default(student_id: str, db: Session = Depends(get_db), 
                                 current_user: schema.UserExtended = Depends(oauth2.get_current_user)):
    return await delete_student(student_id, db, current_user)








