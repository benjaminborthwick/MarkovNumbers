class math2:
    def __init__(self, size, shape):
        self.size = size
        self.shape = shape

    def getSize(self):
        return (int) self.size

math = math2(4, "square")
print(math.getSize)