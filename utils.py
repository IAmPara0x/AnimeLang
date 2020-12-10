def get_var_type(var):
    if var.type == "INTEGER":
        return "tsundere"
    elif var.type == "FLOAT":
        return "yandere"
    elif var.type == "STRING":
        return "kuudere"
    elif var.type == "SHIP":
        return "kuudere"
    elif var.type == "LIST":
        return "harem"


def get_exp_type(exp):
    if isinstance(exp, int):
        return "INTEGER"
    elif isinstance(exp, float):
        return "FLOAT"
    elif isinstance(exp, str):
        return "STRING"
    elif isinstance(exp, list):
        return "LIST"
    elif exp == "kawai" or exp == "baaka":
        return "BOOL"
