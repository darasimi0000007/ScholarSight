# ScholarSight Quick Start Guide

## 🚀 Quick Start (2 Minutes)

### Step 1: Start Backend (Terminal 1)
```powershell
cd "c:\Users\LENOVO\Documents\Student-Performance-Predictor"
& .\studentproject_venv\Scripts\Activate.ps1
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```
✅ Backend running at: `http://127.0.0.1:8000`

### Step 2: Start Frontend (Terminal 2)
```powershell
cd "c:\Users\LENOVO\Documents\Student-Performance-Predictor\frontend"
& "c:\Users\LENOVO\Documents\Student-Performance-Predictor\studentproject_venv\Scripts\Activate.ps1"
streamlit run app.py
```
✅ Frontend running at: `http://localhost:8501`

### Step 3: Login
Use demo credentials:
- **Admin:** admin / admin123
- **Teacher:** teacher / teacher123
- **Student:** student / student123

---

## 📚 API Cheat Sheet

### Check Backend Status
```bash
curl http://127.0.0.1:8000/home
```

### Make a Prediction
```bash
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "STU001",
    "sex": "M",
    "age": 17,
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
  }'
```

### Get All Students
```bash
curl http://127.0.0.1:8000/students
```

### Get One Student
```bash
curl http://127.0.0.1:8000/students/STU001
```

### Download SHAP Chart
```bash
curl http://127.0.0.1:8000/students/STU001/shap -o chart.png
```

### Delete Student
```bash
curl -X DELETE http://127.0.0.1:8000/students/STU001
```

---

## 🎯 Frontend Pages

| URL | Role | Purpose |
|-----|------|---------|
| `/` | All | Login page |
| `/pages/dashboard` | Admin/Teacher/Student | Main dashboard |
| `/pages/predict` | Admin/Teacher | Create predictions |
| `/pages/records` | Admin/Teacher | View all records |
| `/pages/analysis` | Admin/Teacher | SHAP analysis |
| `/pages/my_record` | Student | My record |
| `/pages/my_analysis` | Student | My SHAP analysis |

---

## 🐛 Common Issues & Fixes

| Issue | Solution |
|-------|----------|
| Backend connection error | Ensure backend runs on port 8000 first |
| Page navigation fails | Click sidebar links or access direct URLs |
| SHAP chart not showing | Make a prediction first, then check analysis |
| Database errors | Delete `StudentDetails.db` and restart backend |

---

## 📊 System Architecture

```
Frontend (Streamlit)
    ↓ HTTP/JSON
Backend (FastAPI)
    ↓ SQL
Database (SQLite)
    ↓
ML Model (Scikit-learn)
    ↓
SHAP Analysis
```

---

## ✨ Key Features

✅ **Dual Role System** - Teachers manage students, students view their results  
✅ **Real ML Model** - Gradient Boosting Classifier for predictions  
✅ **Explainable AI** - SHAP analysis shows why predictions were made  
✅ **Full CRUD** - Create, read, update, delete student records  
✅ **Professional UI** - Dark theme with gradients and animations  
✅ **REST API** - All features available via HTTP endpoints  

---

## 📝 Schema Reference

### StudentDetails (Required for predictions)
```
- student_id* (string): Unique identifier
- sex (M/F): Gender
- age (int): 10-30 years
- address (U/R): Urban/Rural
- famsize (<=3 or GT3): Family size
- Pstatus (T/A): Parent status
- guardian (mother/father/other): Guardian
- traveltime (1-4): Travel time (1=<15min, 4=>60min)
- studytime (1-4): Study time (1=<2hrs, 4=>10hrs)
- failures (0-4): Previous failures
- schoolsup (yes/no): School support
- famsup (yes/no): Family support
- activities (yes/no): Extracurricular activities
- nursery (yes/no): Attended nursery
- famrel (1-5): Family relationship quality
- health (1-5): Health status
- absences (0-93): Number of absences
- freetime (1-5): Free time rating
- goout (1-5): Going out rating
- internet (yes/no): Internet access
- romantic (yes/no): In romantic relationship
```

---

## 🔐 Security Notes

⚠️ **Current Setup** (Development Only)
- CORS: Allows all origins
- Auth: Mock authentication
- Database: Local SQLite

🔒 **For Production**
- Restrict CORS to specific domains
- Implement real authentication (JWT, OAuth)
- Use PostgreSQL instead of SQLite
- Enable HTTPS/TLS
- Add request rate limiting
- Implement proper logging

---

**For detailed documentation, see [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)**
