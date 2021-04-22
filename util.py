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
    if cte == "Int":
        return "i"
    elif cte == "Float":
        return "f"
    elif cte == "String":
        return "s"
