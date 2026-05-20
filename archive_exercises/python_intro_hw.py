#Homework python_intro_hw

#Q1
my_list = ['Yitzhak', 'Maimon', '0509180690']
for i in my_list:
    print(i)

#Q2
user_data = {"first_name":"Yitzhak",
        "last_name":"Maimon",
        "phone":"0509180690",
        ("account","type"):"premium",
        ("account","status"): "active"}
print(user_data['last_name'], user_data[("account","status")])

#Q3
def my_lists(list_1,list_2):
    if len(list_1) != len(list_2):
        return "Not equal length"
    list_3 = []
    for i,j in zip(list_1,list_2):
        if i > j:
            list_3.append(i)
        else:
            list_3.append(j)
    return list_3

#Q4
def odd_even_list(my_list):
    
    count_odd = 0
    count_even = 0

    for i in my_list:
        
        if isinstance(i,str):
            print("It’s a string!")
            count_even = 0
            count_odd = 0
            break
        
        if i % 2 == 0:
            count_even += 1
        else:
            count_odd += 1

    print(f"Number of odd numbers: {count_odd}, Number of even numbers: {count_even}")

#list1= [1,3,2,3,"ER",45]
#odd_even_list(list1)

#Q5
def new_dict(n):
    dic ={}
    for i in range(1, n+1):
        dic [i] = i + 3
    return dic
#print(new_dict(5))

#Q6
def concatenate_dict(*dicts):
    new_dict = {}    
    for dic in dicts :
            new_dict.update(dic)
    return new_dict
# dict1={0:1222,3:"df"}
# dict2={134:12,3:"f"}
# dict3={1:178}
# print(concatenate_dict(dict1,dict2,dict3))

#Q7
def count_appearances(str):
    dict = {}
    for char in str:
        if char in dict:
            dict[char] += 1 
        else:
            dict[char] = 1
    return dict
#print(count_appearances("HANNA"))

#Q8
def combine(dict1, dict2):
    new_dict = dict1.copy()
    for i in dict2:
        if i in new_dict:
            new_dict[i] += dict2[i]
        else:
            new_dict[i] = dict2[i]
    return new_dict
#print(combine({1:2,34:7,9:5},{1:5,34:7,9:8} ))

#Q9
def list_unique(my_list):
    new_list=[]
    for i in my_list:
        if i not in new_list:
            new_list.append(i)
    return new_list
#print(list_unique([1,2,3,3,3,4,2,5]))

#Q10
def construct_pattern(n):
    for i in range(1, n + 1):
        for j in range(1, i + 1):
            print (j, end = "")
        print()
#construct_pattern(8)

#Q11
def print_patterns():
    print("****")
    print("*")
    print("*")
    print("  ***")
    print("     *")
    print("     *")
    print("****")
#print_patterns()

        

    




    
