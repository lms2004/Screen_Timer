class MyClass:
    @staticmethod
    def static_method(x, y):
        return x * y
    
    def instance_method(self, x, y):
        return x + y

obj = MyClass()
result = obj.instance_method(1, 2)
print(result)  # 输出: 3

result =  MyClass().static_method(1, 2)
print(result)  # 输出: 2