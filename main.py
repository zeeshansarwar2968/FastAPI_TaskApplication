import pyodbc 
from fastapi import FastAPI, Path, Request, File, UploadFile, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import os
from dotenv import load_dotenv
load_dotenv()


app = FastAPI()

templates = Jinja2Templates(directory="htmldir")

AZURE_SQL_SERVER = os.getenv('AZURE_SQL_SERVER')
AZURE_SQL_DATABASE = os.getenv('AZURE_SQL_DATABASE') 
AZURE_SQL_USER = os.getenv('AZURE_SQL_USER')
AZURE_SQL_PASSWORD = os.getenv('AZURE_SQL_PASSWORD')



cnxn = pyodbc.connect(f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={AZURE_SQL_SERVER};DATABASE={AZURE_SQL_DATABASE};ENCRYPT=yes;UID={AZURE_SQL_USER};PWD={AZURE_SQL_PASSWORD}")
cursor = cnxn.cursor()





# @app.get("/display")
# def write_home(request: Request):
#     return templates.TemplateResponse("displayEmp.html",{"request":request})

#################### Fetch Data

@app.get("/fetchdata/{id}")
def fetch_employee(request: Request, id: int ):
    try:    
        cursor.execute(f"SELECT * FROM dbo.empPayroll WHERE id=${id}") 
        emplist = [row for row in cursor]
        employee = {"id": emplist[0][0], "firstname":emplist[0][1], "lastname":emplist[0][2], "paygrade":emplist[0][3], "salary":emplist[0][4],"email":emplist[0][5]}
        return templates.TemplateResponse("displayEmp.html",{"request":request, "empdata":employee})
    except Exception as e:
        print(e)

@app.get("/fetch_emp/", response_class=HTMLResponse)
def fetch_employee(request: Request):
    try:
        cursor.execute("SELECT * FROM dbo.empPayroll") 
        emplist = [row for row in cursor]
        if emplist:
            datab = emplist
            return templates.TemplateResponse("displayEmp.html",{"request":request, "empdata":datab})
        else:
            return {'message': "Please check the input"}
    except Exception as e:
        print(e)




  
@app.get("/")
def write_home(request: Request):
    return templates.TemplateResponse("home.html",{"request":request})      


#################### Post Data        

@app.post("/add_emp")
def create_employee(id: int= Form(...), firstname:str= Form(...), lastname:str= Form(...), paygrade:str= Form(...), salary:int= Form(...),email:str= Form(...)):
    try:
        print(firstname, lastname)
        cursor.execute(f"INSERT INTO dbo.empPayroll VALUES ({int(id)},'{firstname}','{lastname}','{paygrade}',{salary},'{email}')") 
        cnxn.commit()
        print(firstname, lastname)
        return {'status':200, "message": "Employee Details added successfully"}
    except Exception as e:
        print(e)





#################### Edit Data

@app.get("/editdata")
def write_home(request: Request):
    return templates.TemplateResponse("editdata.html",{"request":request})

@app.post("/edit_emp")
async def update_employee(id: int= Form(...),  paygrade:str= Form(...), salary:int= Form(...)):
    try:
        cursor.execute(f"UPDATE dbo.empPayroll SET paygrade='{paygrade}',salary={salary} WHERE id={id}") 
        cnxn.commit()
        return {'status':200, "message": "Employee Details updated successfully"}
    except Exception as e:
        print(e)



#################### Delete Data


@app.get("/deletedata")
def write_home(request: Request):
    return templates.TemplateResponse("deleteEmp.html",{"request":request})


@app.post("/delete_emp/", response_class=HTMLResponse)
def delete_employee(id: int= Form(...)):
    try:
        cursor.execute(f"DELETE FROM dbo.empPayroll WHERE id={id}") 
        cnxn.commit()
        return {"message": "Employee Details deleted successfully"}
    except Exception as e:
        print(e)
