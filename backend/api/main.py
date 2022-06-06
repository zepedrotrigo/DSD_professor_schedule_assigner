import mysql.connector, traceback, time
import crud
from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, FileResponse

app = FastAPI()

### add CORS headers ###
origins = ["http://172.18.0.2:3000", "http://localhost:3000"] # "*" -> all origins

app.add_middleware(CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

### DB connection ###
def connect_to_db():
    return mysql.connector.connect(host="172.18.0.4", user="user", passwd="password", database="dsd")

connection = connected = False
while not connected:
    try:
        connection = connect_to_db()
    except mysql.connector.Error as e:
        print(e)
        traceback.print_exc()
        time.sleep(30) # wait 30sec to try again
    else:
        connected = True

def reset_cursor():
    connection.close()
    connection.reconnect()


### API methods ###

@app.get("/")
def read_root():
    return RedirectResponse(url='/docs')

@app.get("/v1/classes/")
def get_classes(id: Optional[int] = -1, year: Optional[int]= -1, uc_id: Optional[int] = -1, component: Optional[str] = "NULL", hours: Optional[float] = -1.0, prof_id: Optional[int] = -1):
    '''Returns all classes (allows combined filters: id, year, uc_id, component, hours, prof_id)'''

    reset_cursor()
    with connection.cursor() as cursor:
        return crud.get_classes(cursor, id, year, uc_id, component, hours, prof_id)

@app.get("/v1/departments/")
def get_departments(id: Optional[int] = -1, acronym: Optional[str] = "NULL", name: Optional[str] = "NULL", address: Optional[str] = "NULL", phone: Optional[str] = "NULL"):
    '''Returns all classes (allows combined filters: id, acronym, name, address, phone)'''

    reset_cursor()
    with connection.cursor() as cursor:
        return crud.get_departments(cursor, id, acronym, name, address, phone)

@app.get("/v1/professors/")
def get_professors(prof_id: Optional[int] = -1, nmec: Optional[int] = -1, email: Optional[str] = "NULL", phone: Optional[str] = "NULL", acronym: Optional[str] = "NULL", name: Optional[str] = "NULL",rank: Optional[str]= "NULL",situation: Optional[str] = "NULL", department: Optional[int] = -1):
    '''Returns all professors (allows combined filters: prof_id, nmec, email, phone, acronym, name, rank, situation, department)'''

    reset_cursor()
    with connection.cursor() as cursor:
        return crud.get_professors(cursor, prof_id, nmec, email, phone, acronym, name, rank, situation, department)

@app.get("/v1/dsders/")
def get_dsders(id: Optional[int] = -1):
    '''Returns all dsders (allows filter: id)'''

    reset_cursor()
    with connection.cursor() as cursor:
        return crud.get_dsders(cursor, id)

@app.get("/v1/courses/")
def get_courses(id: Optional[int] = -1, acronym: Optional[str] = "NULL", name: Optional[str] = "NULL", department: Optional[int] = -1, director: Optional[int] = -1):
    '''Returns all courses (allows combined filters: id, acronym, name, department, director)'''

    reset_cursor()
    with connection.cursor() as cursor:
        return crud.get_courses(cursor, id, acronym, name, department, director)

@app.get("/v1/ucs/")
def get_ucs(id: Optional[int] = -1, acronym: Optional[str] = "NULL", name: Optional[str] = "NULL", director: Optional[int] = -1):
    '''Returns all ucs (allows combined filters: id, acronym, name, director)'''

    reset_cursor()
    with connection.cursor() as cursor:
        return crud.get_ucs(cursor, id, acronym, name, director)

@app.get("/v1/wishlists/")
def get_wishlists(id: Optional[int] = -1, year: Optional[int] = -1, prof_id: Optional[int] = -1, class_id: Optional[int] = -1):
    '''Returns all wishlists (allows combined filter: id, year, prof_id, class_id)'''

    reset_cursor()
    with connection.cursor() as cursor:
        return crud.get_wishlists(cursor, id, year, prof_id, class_id)

@app.get("/v1/classes_main_panel_info/")
def classes_main_panel_info(params: Optional[str] = "unassigned_classes desc"):
    '''Returns data used in UCs main panel'''

    reset_cursor()
    with connection.cursor() as cursor:
        return crud.classes_main_panel_info(cursor, params)

@app.get("/v1/professors_main_panel_info/")
def professors_main_panel_info(params: Optional[str] = "total_hours asc", prof_ids: Optional[str] = ""):
    '''Returns data used in Profs main panel'''

    reset_cursor()
    with connection.cursor() as cursor:
        return crud.professors_main_panel_info(cursor, params, prof_ids)

@app.get("/v1/prof_total_hours/")
def get_prof_total_hours():
    '''Returns total hours assigned for each professor'''

    reset_cursor()
    with connection.cursor() as cursor:
        return crud.get_prof_total_hours(cursor)

@app.put("/v1/classes/")
def assign_prof_to_class(class_id: int, prof_id: int):
    '''Assigns/Removes a teacher to a class'''

    reset_cursor()
    with connection.cursor() as cursor:
        return crud.assign_prof_to_class(connection, cursor, class_id, prof_id)

@app.put("/v1/professors/")
def update_prof_acronym(prof_id: int, acronym: str):
    '''Updates teacher acronym'''

    reset_cursor()
    with connection.cursor() as cursor:
        return crud.update_prof_acronym(connection, cursor, prof_id, acronym)

@app.get("/v1/validate_dsd/")
def validate_dsd(max_hours: int):
    '''Retrieves dsd warnings'''

    reset_cursor()
    with connection.cursor() as cursor:
        return crud.validate_dsd(cursor, max_hours)

@app.get("/v1/export_dsd/")
def export_dsd(file_type: str):
    '''Exports dsd as json/csv/xls'''

    reset_cursor()
    with connection.cursor() as cursor:
        filepath = crud.export_dsd(cursor, file_type)

    return FileResponse(path=filepath, filename=filepath)