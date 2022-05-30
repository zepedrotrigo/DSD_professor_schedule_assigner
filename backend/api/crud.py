def get_classes(cursor, id, year, uc_id, component, hours, prof_id):
    '''Returns all classes (allows combined filters: id, year, uc_id, component, hours, prof_id)'''
    
    cursor.execute(f"CALL FilterClasses({id}, {year}, {uc_id}, {component}, {hours}, {prof_id});")
    result = cursor.fetchall()
    keys = [i[0] for i in cursor.description]

    return {"classes": [dict(zip(keys, vals)) for vals in result]}

def get_departments(cursor, id, acronym, name, address, phone):
    '''Returns all departments (allows combined filters: id, acronym, name, address, phone)'''
    
    cursor.execute(f"CALL FilterDepartments({id}, {acronym}, {name}, {address}, {phone});")
    result = cursor.fetchall()
    keys = [i[0] for i in cursor.description]

    return {"departments": [dict(zip(keys, vals)) for vals in result]}

def get_professors(cursor, prof_id, nmec, email, phone, acronym, name, rank, situation, department):
    '''Returns all professors (allows combined filters: prof_id, nmec, email, phone, acronym, name, rank, situation, department)'''

    cursor.execute(f"CALL FilterProfessors({prof_id}, {nmec},{email},{phone},{acronym},{name},{rank},{situation},{department});")
    result = cursor.fetchall()
    keys = [i[0] for i in cursor.description]

    return {"professors": [dict(zip(keys, vals)) for vals in result]}

def get_dsders(cursor, id):
    '''Returns all dsders (allows filter: id)'''

    cursor.execute(f"CALL FilterDsders({id});")
    result = cursor.fetchall()
    keys = [i[0] for i in cursor.description]

    return {"dsders": [dict(zip(keys, vals)) for vals in result]}

def get_courses(cursor, id, acronym, name, department, director):
    '''Returns all courses (allows filter: id, acronym, name, department, director)'''

    cursor.execute(f"CALL FilterCourses({id}, {acronym}, {name}, {department}, {director});")
    result = cursor.fetchall()
    keys = [i[0] for i in cursor.description]

    return {"courses": [dict(zip(keys, vals)) for vals in result]}

def get_ucs(cursor, id, acronym, name, director):
    '''Returns all ucs (allows combined filters: id, acronym, name, director)'''

    cursor.execute(f"CALL FilterUcs({id}, {acronym}, {name}, {director});")
    result = cursor.fetchall()
    keys = [i[0] for i in cursor.description]

    return {"ucs": [dict(zip(keys, vals)) for vals in result]}

def get_wishlists(cursor, id, year, prof_id, class_id):
    '''Returns all wishlists (allows combined filters: id, year, prof_id, class_id)'''

    cursor.execute(f"CALL FilterWishlists({id}, {year}, {prof_id}, {class_id});")
    result = cursor.fetchall()
    keys = [i[0] for i in cursor.description]

    return {"wishlists": [dict(zip(keys, vals)) for vals in result]}

def classes_main_panel_info(cursor):
    '''Returns data used in UCs main panel'''

    cursor.execute(f"SELECT *  FROM classes_main_panel_info ORDER BY uc_name ASC, prof_acronym ASC;")
    result = cursor.fetchall()
    keys = [i[0] for i in cursor.description]

    return {"data": [dict(zip(keys, vals)) for vals in result]}

def professors_main_panel_info(cursor):
    '''Returns data used in Profs main panel'''

    cursor.execute(f"SELECT *  FROM professors_main_panel_info ORDER BY prof_acronym ASC;")
    result = cursor.fetchall()
    keys = [i[0] for i in cursor.description]

    return {"data": [dict(zip(keys, vals)) for vals in result]}

def get_prof_total_hours(cursor):
    '''Returns total hours assigned for each professor'''

    cursor.execute("SELECT * FROM prof_total_hours;")
    result = cursor.fetchall()
    keys = [i[0] for i in cursor.description]

    return {"data": [dict(zip(keys, vals)) for vals in result]}

def assign_prof_to_class(connection, cursor, class_id, prof_id):
    '''Assigns a teacher to a class'''
    if prof_id == -1:
        prof_id = "NULL"

    cursor.execute(f"UPDATE dsd.classes SET prof_id = {prof_id} WHERE class_id = {class_id}")
    connection.commit()

    return {"response": f"{cursor.rowcount} record(s) affected"}
