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
        ">#ff": types["bool"],
        "<#ff": types["bool"],
        ">=#ff": types["bool"],
        "<=#ff": types["bool"],
        "!=#ff": types["bool"],
        # String values
        "+#ss": types["string"],
        "==#ss": types["string"],
        "!=#ss": types["string"],
        # Boolean Values
        "==#bb": types["bool"],
        "&&#bb": types["bool"],
        "||#bb": types["bool"],
        "!=#bb": types["bool"],
    }

    def format_expression(self, left_op, right_op, operand):
        return operand + "#" + left_op[0] + right_op[0]

    def validate_expression(self, left_op, right_op, operand):
        formatted_exp = self.format_expression(left_op,right_op,operand)
        print(formatted_exp)
        if formatted_exp in self.sem_cube.keys():
            print(self.sem_cube[formatted_exp])
        else:
            print("error")