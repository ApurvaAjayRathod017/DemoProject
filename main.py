from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from models import EmployeeDetails
from database import get_db

app = FastAPI()

# Request models
class EmployeeCreate(BaseModel):
    name: str
    designation: str

class EmployeeUpdate(BaseModel):
    name: str
    designation: str

@app.get("/employees")
def get_employees(db: Session = Depends(get_db)):
    employees = db.query(EmployeeDetails).all()
    return [dict(id=e.id, name=e.name, designation=e.designation) for e in employees]

@app.get("/employees/{emp_id}")
def get_employees(emp_id: int, db: Session = Depends(get_db)):
    emp = db.query(EmployeeDetails).filter(EmployeeDetails.id == emp_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")

    return {
        "id": emp.id,
        "name": emp.name,
        "designation": emp.designation
    }

@app.post("/employees")
def create_employee(emp: EmployeeCreate, db: Session = Depends(get_db)):
    new_emp = EmployeeDetails(name=emp.name, designation=emp.designation)
    db.add(new_emp)
    db.commit()
    db.refresh(new_emp)
    return {"message": "Employee added successfully", "id": new_emp.id}

@app.put("/employees/{emp_id}")
def update_employee(emp_id: int, updated: EmployeeUpdate, db: Session = Depends(get_db)):
    emp = db.query(EmployeeDetails).filter(EmployeeDetails.id == emp_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    emp.name = updated.name
    emp.designation = updated.designation
    db.commit()
    return {"message": "Employee updated successfully"}

@app.delete("/employees/{emp_id}")
def delete_employee(emp_id: int, db: Session = Depends(get_db)):
    emp = db.query(EmployeeDetails).filter(EmployeeDetails.id == emp_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    db.delete(emp)
    db.commit()
    return {"message": "Employee deleted successfully"}