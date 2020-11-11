class Integer():
    def __init__(self, value):
        self.value = value

    def eval(self):
        return int(self.value)


class Float():
    def __init__(self, value):
        self.value = value

    def eval(self):
        return float(self.value)


class BinaryOp():
    def __init__(self, left, right):
        self.left = left
        self.right = right


class Add(BinaryOp):
    def eval(self):
        return self.left.eval() + self.right.eval()


class Substract(BinaryOp):
    def eval(self):
        return self.left.eval() - self.right.eval()


class Multiply(BinaryOp):
    def eval(self):
        return self.left.eval() * self.right.eval()


class Divide(BinaryOp):
    def eval(self):
        if self.right.eval() == 0:
            print("Naaani? you were trying to divide by 0."
                  "B-Baaaaaaka that's not possible")
        return self.left.eval() / self.right.eval()


class S_expression():
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self.value.eval()


class Print():
    def __init__(self, value):
        self.value = value

    def eval(self):
        print(self.value.eval())


class Exit:
    def eval(self):
        print("Exiting . . .")
        quit()
