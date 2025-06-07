
# Classes

# class User:
#     pass

# user_1 = User()

# class User:
#     pass
# user_1 = User()
# user_1.id = "001"
# user_1.username = "john_doe"

# print(user_1.id)
# print(user_1.username)

class User:
    def __init__(self, id, username):
        self.id = id
        self.username = username
        self.followers = 0
        self.following = 0
    
    def follow(self, user):
        user.followers += 1
        self.following += 1
        print(f"{self.username} followed {user.username}")

user_1 = User("001", "john_doe")
user_2 = User("002", "jane_doe")
print(user_1.id)
print(user_1.username)
print(user_1.followers)
print(user_2.id)
print(user_2.username)
user_1.follow(user_2)
print(user_1.following)
print(user_2.followers)
        