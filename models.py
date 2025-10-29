from sqlalchemy.ext.automap import automap_base
from sqlalchemy import MetaData
from database import engine

metadata = MetaData()
Base = automap_base()
Base.prepare(autoload_with=engine)

# Reflect the existing table
EmployeeDetails = Base.classes.EmployeeDetails