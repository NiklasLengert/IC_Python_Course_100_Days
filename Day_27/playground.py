# def add(*args):
#     sum = 0
#     for n in args:
#         sum += n
#     return sum

# print(add(1, 2, 3))

# def calculate(n, **kwargs):
#     print(kwargs)
    # for key, value in kwargs.items():
    #     print(key)
    #     print(value)
#     print(kwargs['add'])
#     n += kwargs['add']
#     n *= kwargs['multiply']
#     n /= kwargs['divide']
#     print(n)

# calculate(2, add=1, multiply=2, divide=3)


class Car: 
    def __init__(self, **kwargs):
        self.make = kwargs.get('make')
        self.model = kwargs.get('model')
        self.color = kwargs.get('color')
        self.seats = kwargs.get('seats', 4)

my_car = Car(make='Nissan', model='Altima', color='blue')
print(my_car.make)
print(my_car.model)
print(my_car.color)
print(my_car.seats)