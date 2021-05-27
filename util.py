# This is a utility function to format the type
def get_type_s(cte):
    if cte == "Int" or cte == "int":
        return "i"
    elif cte == "Float" or cte == "float":
        return "f"
    elif cte == "String" or cte == "string":
        return "s"
    elif cte == "Bool" or cte == "bool":
        return "b"
