def get_type(cte):
    if type(cte) is str:
        return "s"
    elif type(cte) is int:
        return "i"
    elif type(cte) is float:
        return "f"
    elif type(cte) is bool:
        return "b"


def get_type_s(cte):
    if cte == "Int" or cte == "int":
        return "i"
    elif cte == "Float" or cte == "float":
        return "f"
    elif cte == "String" or cte == "string":
        return "s"
