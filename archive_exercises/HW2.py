#Q1
class Vehicle:
    def __init__(self, name, max_speed, mileage):
        self.name = name
        self.max_speed = max_speed
        self.mileage = mileage

my_vehicle = Vehicle("bmw", 100, 90)
# print(my_vehicle.name, my_vehicle.max_speed, my_vehicle.mileage)

#Q2
class Bus (Vehicle):
    
    def __init__(self, name, max_speed, mileage):
        super().__init__(name, max_speed, mileage)
my_bus = Bus("volvo",80,80)
#print(f"Vehicle: {my_bus.name},max_speed: {my_bus.max_speed}, mileage: {my_bus.mileage}")

#Q3
class StringHandler:
    
    def __init__(self):
        self.msg = ""

    def get_String(self):
        self.msg = input("Enter message: ")
    
    def print_String(self):
        print(self.msg.upper())

handler = StringHandler()

#Q4
with open("my_id.txt", "w", encoding="utf-8") as file:
    file.write("full name:Yitzhak Maimon\n")
    file.write("phone: 0509180690")

#Q5
def counter_words_txt(path_file):
    word_count = {}
    with open(path_file, "r", encoding="utf-8") as file:
        text = file.read()
        words = text.split()

    for word in words:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1
    return word_count
#print(counter_words_txt(r"C:\Users\yitzhama\vnv\my_id.txt"))

#Q6
def get_longest_word(path_file):
    with open(path_file, "r", encoding="utf-8") as file:
        text = file.read()
        words = text.split()
        longest = ""
    for word in words:
        if len(word) > len(longest):
            longest = word
    return longest
# print(get_longest_word(r"C:\Users\yitzhama\vnv\my_id.txt"))

#Q7
def sum_list(list_integer):
    total = 0
    for i in list_integer:
        total += i
    return total

#list_integer = [10, 200, 10, 40]
#result = sum_list(list_integer)
#print(f"The sum is:{result}")

#Q8
def multiply_list(list_integer):
    total = 1
    for i in list_integer:
        total *= i
    return total

#list_integer = [10, 2, 10, 10]
#result = multiply_list(list_integer)
#print(f"The sum is:{result}")

#Q9
def min_list(list_integer):
    
    if not list_integer:
        return None
    
    min_val = list_integer[0]
    for i in list_integer:
        if i < min_val:
            min_val = i
    return min_val

#list_integer = [3,54,5,2,0.5]
#result = min_list(list_integer)
#print(f"The minimum is:{result}")

#Q10
def count_string(string):
    upper = 0
    lower = 0
    for char in string:
        if char.isupper():
            upper += 1
        elif char.islower():
            lower += 1
    return f"lower: {lower}, upper: {upper}"
#print(count_string("1T12@EE#q1"))

#Q11
import numpy as np

arr = np.arange(10)
print (arr)
        
#Q12
import numpy as np
arr = np.arange(50)
arr_odd = arr [arr % 2 != 0]
print(arr_odd)

#Q13
import numpy as np
matrix = np.eye(5)
print (matrix)
matrix [matrix > 0] = -1
print(matrix)

#Q14
def pow_recursive(a,b):
    if b < 0:
        return 1 / pow_recursive(a, -b)
    if b == 0:
        return 1
    return a * pow_recursive (a, b-1)

#print(pow_recursive(3,5))
#print(pow_recursive(2,-6))

#Q15
def is_open_close(my_str):

    my_dict = { ")" : "(" ,
                "]" : "[" ,
                "}" : "{" }
    stack = []

    for char in my_str:
        if char in my_dict:
            top_element = stack.pop() if stack else "#"
            if top_element!= my_dict[char]:
                return False
        else:
            stack.append(char)
    return len(stack) == 0

















