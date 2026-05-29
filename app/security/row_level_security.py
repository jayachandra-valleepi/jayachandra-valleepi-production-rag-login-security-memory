def check_department_access(user_department, pdf_department):
    if user_department == "all":
     return True
    if user_department == pdf_department:
     return True
    return False
