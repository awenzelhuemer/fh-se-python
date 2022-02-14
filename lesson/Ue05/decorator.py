from functools import wraps

def my_dec(func):
    @wraps(func)
    def my_dec_wrapper(x):
        square = func(x)
        print("before exec")
        print(square)
        print("after exec")
        return square
    return my_dec_wrapper

@my_dec
def square(x):
    ''' Square returns the square of parameter x'''
    return x**2

# square(5)
# help(square)

print('----------')
square = my_dec(square)
square(5)
help(square)

print(square.__wrapped__)
