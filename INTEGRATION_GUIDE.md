# ScholarSight Frontend-Backend Integration Guide

## ✅ Integration Complete

Your Streamlit frontend has been successfully integrated with your FastAPI backend. Here's what has been set up:

---

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│           STREAMLIT FRONTEND (Port 8501)                │
├─────────────────────────────────────────────────────────┤
│  • app.py (Login page)                                  │
│  • pages/                                               │
│    ├── dashboard.py (Staff overview & student portal)   │
│    ├── predict.py (Make predictions)                    │
│    ├── records.py (View all student records)            │
│    ├── analysis.py (SHAP analysis for any student)      │
│    ├── my_record.py (Student views their record)        │
│    └── my_analysis.py (Student views their analysis)    │
└────────────────────────┬────────────────────────────────┘
                         │
                HTTP Requests (JSON)
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│           FASTAPI BACKEND (Port 8000)                   │
├─────────────────────────────────────────────────────────┤
│  • POST   /predict                (Make prediction)     │
│  • GET    /students               (Get all students)    │
│  • GET    /students/{student_id}  (Get one student)     │
│  • DELETE /students/{student_id}  (Delete student)      │
│  • GET    /students/{student_id}/shap  (Get SHAP chart) │
│  • GET    /home                   (Health check)        │
└─────────────────────────────────────────────────────────┘
         │
         │ Uses ML Model & Database
         │
         ▼
   • stud_performance_classifier.joblib
   • stud_performance_preprocessor.joblib
   • StudentDetails.db (SQLite)
```

---

## Backend Endpoints Summary

### 1. Make a Prediction
**Endpoint:** `POST /predict`  
**Input:** Student academic profile (StudentDetails schema)  
**Output:** 
```json
{
  "prediction": "Pass",
  "student_id": "STU001",
  "confidence": 0.92
}
```

### 2. Get All Students
**Endpoint:** `GET /students`  
**Output:**
```json
{
  "students": [
    {
      "student_id": "STU001",
      "age": 17,
      "Prediction": "Pass",
      ...
    }
  ]
}
```

### 3. Get Specific Student
**Endpoint:** `GET /students/{student_id}`  
**Output:** Single student record as JSON

### 4. Delete Student Record
**Endpoint:** `DELETE /students/{student_id}`  
**Output:** Confirmation message

### 5. Get SHAP Analysis Chart
**Endpoint:** `GET /students/{student_id}/shap`  
**Output:** PNG image (SHAP bar chart)

---

## Running the System

### Terminal 1: Start the Backend
```powershell
cd "c:\Users\LENOVO\Documents\Student-Performance-Predictor"
& .\studentproject_venv\Scripts\Activate.ps1
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Backend will be available at: **http://127.0.0.1:8000**

### Terminal 2: Start the Frontend
```powershell
cd "c:\Users\LENOVO\Documents\Student-Performance-Predictor\frontend"
& "c:\Users\LENOVO\Documents\Student-Performance-Predictor\studentproject_venv\Scripts\Activate.ps1"
streamlit run app.py
```

Frontend will be available at: **http://localhost:8501**

---

## Demo Credentials

| Role    | Username | Password    |
|---------|----------|-------------|
| Admin   | admin    | admin123    |
| Teacher | teacher  | teacher123  |
| Student | student  | student123  |

---

## File Structure

```
Student-Performance-Predictor/
├── main.py                          ← FastAPI backend (UPDATED)
├── schema.py                        ← Pydantic schemas
├── models.py                        ← SQLAlchemy models
├── database.py                      ← Database config
├── requirements.txt                 ← Dependencies
├── ml_model/
│   ├── stud_performance_classifier.joblib
│   └── stud_performance_preprocessor.joblib
├── data/
│   ├── student-mat.csv
│   └── student-por.csv
├── frontend/
│   ├── app.py                       ← Login page (UNCHANGED)
│   ├── utils.py                     ← Shared utilities (UPDATED)
│   ├── config.toml
│   └── pages/                       ← NEW: Multi-page app
│       ├── dashboard.py             ← NEW: Staff overview
│       ├── predict.py               ← NEW: Make predictions
│       ├── records.py               ← NEW: View records
│       ├── analysis.py              ← NEW: SHAP analysis
│       ├── my_record.py             ← NEW: Student record
│       └── my_analysis.py           ← NEW: Student analysis
└── studentproject_venv/             ← Virtual environment
```

---

## Key Integration Changes

### Backend (main.py)
✅ **New unified `/predict` endpoint** - accepts StudentDetails, saves to DB, returns prediction with confidence  
✅ **New `/students` endpoint** - returns all student records as JSON list  
✅ **New `/students/{student_id}` endpoint** - returns single student record  
✅ **New `/students/{student_id}/shap` endpoint** - generates and returns SHAP chart  
✅ **CORS middleware enabled** - allows frontend requests from any origin  
✅ **Backward compatible** - kept legacy endpoints for reference

### Frontend (app.py & utils.py)
✅ **Updated API base URL** to `http://127.0.0.1:8000`  
✅ **API wrapper functions** - `api_predict()`, `api_get_all_students()`, `api_get_student()`, `api_delete_student()`, `api_get_shap_chart()`  
✅ **Authentication layer** - mock user system with roles (admin, teacher, student)  
✅ **Responsive dashboard** - shows stats, tables, and charts based on user role

### New Frontend Pages
✅ **pages/dashboard.py** - Main dashboard (shows stats for staff, portal for students)  
✅ **pages/predict.py** - Create new predictions  
✅ **pages/records.py** - View all records, search, export to CSV  
✅ **pages/analysis.py** - Generate SHAP analysis for any student  
✅ **pages/my_record.py** - Students view their own record  
✅ **pages/my_analysis.py** - Students view their SHAP explanation

---

## Testing the Integration

### 1. Health Check
```bash
curl http://127.0.0.1:8000/home
```

### 2. Make a Prediction (via Python)
```python
import requests

payload = {
    "student_id": "STU002",
    "sex": "M",
    "age": 18,
    "address": "U",
    "famsize": "GT3",
    "Pstatus": "T",
    "guardian": "mother",
    "traveltime": 1,
    "studytime": 2,
    "failures": 0,
    "schoolsup": "no",
    "famsup": "yes",
    "activities": "no",
    "nursery": "no",
    "famrel": 4,
    "health": 3,
    "absences": 2,
    "freetime": 3,
    "goout": 4,
    "internet": "yes",
    "romantic": "no"
}

response = requests.post("http://127.0.0.1:8000/predict", json=payload)
print(response.json())
```

### 3. Get All Students
```bash
curl http://127.0.0.1:8000/students
```

### 4. Get Specific Student
```bash
curl http://127.0.0.1:8000/students/STU001
```

### 5. Get SHAP Chart
```bash
curl http://127.0.0.1:8000/students/STU001/shap -o analysis.png
```

---

## Frontend Workflow

### For Teachers/Admins:
1. **Login** → Select "teacher" or "admin"
2. **Dashboard** → View summary stats
3. **Make Prediction** → Enter student data → See result
4. **Student Records** → View all records, search, export
5. **SHAP Analysis** → Select student → View feature importance chart

### For Students:
1. **Login** → Select "student"
2. **Dashboard** → See quick stats
3. **My Record** → View your stored record
4. **My Analysis** → See SHAP explanation of your prediction

---

## Troubleshooting

### Backend not responding?
- Check if FastAPI server is running on port 8000
- Verify with: `curl http://127.0.0.1:8000/home`

### Frontend can't connect to backend?
- Ensure backend is running first
- Check `API_BASE = "http://127.0.0.1:8000"` in `utils.py`
- Look for connection errors in browser console

### SHAP analysis not generating?
- Student must have a stored prediction first
- Check that `StudentDetails.db` exists and has records
- Verify ML model files exist in `ml_model/` directory

### Multi-page navigation not working?
- This is a Streamlit limitation with certain configurations
- Alternative: Use the sidebar links to navigate (they use `st.page_link()`)
- Or access pages directly: `http://localhost:8501/pages/dashboard`

---

## API Response Formats

### Prediction Response
```json
{
  "prediction": "Pass|Fail",
  "student_id": "STU001",
  "confidence": 0.85
}
```

### Students List Response
```json
{
  "students": [
    {
      "student_id": "STU001",
      "sex": "F",
      "age": 17,
      "Prediction": "Pass",
      ...
    }
  ]
}
```

### Error Response
```json
{
  "detail": "Error message describing what went wrong"
}
```

---

## Next Steps

1. **Add Database Persistence** - Verify database saves work correctly
2. **Add Real Authentication** - Replace mock auth with actual user database
3. **Add Data Validation** - Implement more robust input validation
4. **Performance Optimization** - Cache SHAP analyses for frequently accessed students
5. **Deployment** - Deploy to production with proper security settings (change CORS)

---

## Support & Documentation

- **FastAPI Docs:** Visit `http://127.0.0.1:8000/docs` for interactive API documentation
- **Streamlit Docs:** https://docs.streamlit.io
- **SHAP Docs:** https://shap.readthedocs.io

---

**Integration Status:** ✅ COMPLETE  
**Last Updated:** May 27, 2026  
**System Version:** 1.0.0
