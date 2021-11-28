
def hello_world():
    print('Hello World')

hello_world

# functor
x = hello_world 
x()

print(hello_world)

# hello_world = 'test'
# hello_world()

hello_world.x = 5
print(hello_world.x)