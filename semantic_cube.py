types = {
    "int": "Int",
    "float": "Float",
    "string": "String",
    "bool": "Bool"
}

class semantic_cube():
    sem_cube = {
        # Integer Values
        "+#ii": types["int"],
        "-#ii": types["int"],
        "*#ii": types["int"],
        "/#ii": types["int"],
        "==#ii": types["bool"],
        "=#ii": types["int"],
        ">#ii": types["bool"],
        "<#ii": types["bool"],
        ">=#ii": types["bool"],
        "<=#ii": types["bool"],
        "!=#ii": types["bool"],
        # Int and Float Values
        "+#if": types["float"],
        "-#if": types["float"],
        "*#if": types["float"],
        "/#if": types["float"],
        "==#if": types["bool"],
        "=#if" : types["int"],
        ">#if": types["bool"],
        "<#if": types["bool"],
        ">=#if": types["bool"],
        "<=#if": types["bool"],
        "!=#if": types["bool"],
        # Float and Int Values
        "+#fi": types["float"],
        "-#fi": types["float"],
        "*#fi": types["float"],
        "/#fi": types["float"],
        "==#fi": types["bool"],
        "=#fi" : types["float"],
        ">#fi": types["bool"],
        "<#fi": types["bool"],
        ">=#fi": types["bool"],
        "<=#fi": types["bool"],
        "!=#fi": types["bool"],
        # Float Values
        "+#ff": types["float"],
        "-#ff": types["float"],
        "*#ff": types["float"],
        "/#ff": types["float"],
        "==#ff": types["bool"],
        "=#ff" : types["float"],
        ">#ff": types["bool"],
        "<#ff": types["bool"],
        ">=#ff": types["bool"],
        "<=#ff": types["bool"],
        "!=#ff": types["bool"],
        # String values
        "+#ss": types["string"],
        "==#ss": types["bool"],
        "=#ss" : types["string"],
        "!=#ss": types["bool"],
        # Boolean Values
        "==#bb": types["bool"],
        "=#bb" : types["bool"],
        "&&#bb": types["bool"],
        "||#bb": types["bool"],
        "!=#bb": types["bool"],
    }
    # We use to get our format so that we can use it later to validate the expression
    def format_expression(self, left_op, right_op, operator):
        return operator + "#" + left_op[0] + right_op[0]

    # We use this to validate the expresion between two operands
    def validate_expression(self, left_op, right_op, operator):
        formatted_exp = self.format_expression(left_op,right_op,operator)
        #print(formatted_exp)
        if formatted_exp in self.sem_cube.keys():
            return self.sem_cube[formatted_exp]
        else:
            return "ERROR"