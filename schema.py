from pydantic import BaseModel, Field, AfterValidator, model_validator
from typing import Optional, List, Union, Annotated, Any
from enum import Enum


class SexType(str, Enum):
    female ="F"
    male = "M"


class addressType(str, Enum):
    urban = "U"
    rural = "R"

class famSize(str, Enum):
    greater_than_three = "GT3"
    less_than_three = "LE3"

class pStatus(str, Enum):
    living_together = "T"
    living_apart = "A"


class Guardian(str, Enum):
    mother = "mother"
    father = "father"
    other = "other"


class travel_time(int, Enum):
    less_than_15_minutes = 1
    between_15_and_30_minutes = 2
    between_30_minutes_and_1_hour = 3
    more_than_1_hour = 4


class study_time(int, Enum):
    less_than_2_hours = 1
    between_2_and_5_hours = 2
    between_5_and_10_hours = 3
    more_than_10_hours = 4

class Failures(int, Enum):
    none = 0
    one = 1
    two = 2
    three_or_more = 3

class Schoolsup(str, Enum):
    no = "no"
    yes = "yes"


class Famsup(str, Enum):
    no = "no"
    yes = "yes"


class Activities(str, Enum):
    no = "no"
    yes = "yes"


class Nursery(str, Enum):
    no = "no"
    yes = "yes"


class FamilyRelationship(int, Enum):
    very_poor = 1
    poor = 2
    average = 3
    good = 4
    very_good = 5


class HealthStatus(int, Enum):
    very_poor = 1
    poor = 2
    average = 3
    good = 4
    very_good = 5




class FreeTime(int, Enum):
    very_low = 1
    low = 2
    average = 3
    free = 4
    very_free = 5



class GoOut(int, Enum):
    very_low = 1
    low = 2
    average = 3
    high = 4
    very_high = 5


class Internet(str, Enum):
    no = "no"
    yes = "yes"



class Romantic(str, Enum):
    no = "no"
    yes = "yes"



# class ListWrapperModel(BaseModel):
#     @model_validator(mode='before')
#     @classmethod
#     def wrap_all_fields_in_lists(cls, data: Any) -> Any:
#         if isinstance(data, dict):
#             for key, value in data.items():
#                 # Wrap in list if it's not a list, None, or a dict
#                 if value is not None and not isinstance(value, (list, dict)):
#                     data[key] = [value]
#         return data




class StudentDetails(BaseModel):
    student_id: str = Field(..., description = "Student's Identification Number")
    sex: SexType = Field(..., description = "Sex of the student; M or F")
    age: int = Field(..., description = "Student's age")
    address: addressType = Field(..., description = "Rural(R) or Urban(U)")
    famsize: famSize = Field(..., description = "Family size: Greater than 3(GT3) or Less than 3(LE3)")
    Pstatus: pStatus = Field(..., description = "Parent Status: Living Together(T) or Apart(A)")
    guardian: Guardian = Field(..., description = "Is Student's guardian mother or father or other person")
    traveltime: travel_time = Field(..., description = "Traveltime: Time to travel to school; Less than 15 minutes(1), Between 15 and 30 minutes(2), " \
    "Between 30 minutes and 1 hour(3), More than 1 hour(4)")
    studytime: study_time = Field(..., description = "Studytime: Time spent studying; Less than 2 hours(1), Between 2 and 5 hours(2), " \
    "Between 5 and 10 hours(3), More than 10 hours(4)")
    failures: Failures = Field(..., description = "Number of past class failures; None(0), One(1), Two(2), Three or more(3)")
    schoolsup: Schoolsup = Field(..., description = "Extra educational support; No(no), Yes(yes)")
    famsup: Famsup = Field(..., description = "Family educational support; No(no), Yes(yes)")
    activities: Activities = Field(..., description = "Extracurricular activities; No(no), Yes(yes)")
    nursery: Nursery = Field(..., description = "Attended nursery school; No(no), Yes(yes)")
    famrel: FamilyRelationship = Field(..., description = "Family relationship quality; Very Poor(1), Poor(2), Average(3), Good(4), Very Good(5)")  
    health: HealthStatus = Field(..., description = "Health status; Very Poor(1), Poor(2), Average(3), Good(4), Very Good(5)")
    absences: int = Field(..., description = "Number of school absences")
    freetime: FreeTime = Field(..., description = "Free time after school; Very Low(1), Low(2), Average(3), Free(4), Very Free(5)")
    goout: GoOut = Field(..., description = "Going out with friends; Very Low(1), Low(2), Average(3), High(4), Very High(5)")
    internet: Internet = Field(..., description = "Internet access at home; No(no), Yes(yes)")
    romantic: Romantic = Field(..., description = "In a romantic relationship; No(no), Yes(yes)")






class StudentUpdate(BaseModel):
    sex: Optional[SexType] = None
    age: Optional[int] = None
    address: Optional[addressType] = None
    famsize: Optional[famSize] = None
    Pstatus: Optional[pStatus] = None
    guardian: Optional[Guardian] = None
    traveltime: Optional[travel_time] = None
    studytime: Optional[study_time] = None
    failures: Optional[Failures] = None
    schoolsup: Optional[Schoolsup] = None
    famsup: Optional[Famsup] = None
    activities: Optional[Activities] = None
    nursery: Optional[Nursery] = None
    famrel: Optional[FamilyRelationship] = None
    health: Optional[HealthStatus] = None
    absences: Optional[int] = None
    freetime: Optional[FreeTime] = None
    goout: Optional[GoOut] = None
    internet: Optional[Internet] = None
    romantic: Optional[Romantic] = None

    class Config:
        extra = "forbid"


class SHAPAnalysisData(StudentDetails):
    
    sex: list[SexType] 
    age: list[int] 
    address: list[addressType] 
    famsize: list[famSize] 
    Pstatus: list[pStatus] 
    guardian: list[Guardian] 
    traveltime: list[travel_time] 
    studytime: list[study_time] 
    failures: list[Failures] 
    schoolsup: list[Schoolsup] 
    famsup: list[Famsup]  
    activities: list[Activities] 
    nursery: list[Nursery] 
    famrel: list[FamilyRelationship] 
    health: list[HealthStatus] 
    absences: list[int] 
    freetime: list[FreeTime] 
    goout: list[GoOut] 
    internet: list[Internet] 
    romantic: list[Romantic] 
    Prediction: list[str]

    class Config():
        from_attributes = True





#response model for predict wrapper
class returnPrediction(StudentDetails):
    prediction: str

    class Config():
    
        from_attributes = True





class User(BaseModel):
    firstname: str
    lastname: str
    institution_id: str
    email: str
    password: str
    confirm_password: str






class UserExtended(User):
    firstname: str
    lastname: str
    role: str
    institution_id: str
    email: str
    password: str
    confirm_password: str

    class Config():
        from_attributes = True





#pydantic schema for authentication
class Token(BaseModel):
    access_token: str
    token_type: str
    institution_id: str


class TokenData(BaseModel):
    email: str | None = None
    scopes: list[str] = []



class RoleCheck(BaseModel):
    email: str
    institution_id: str #STU123 #TEA999
