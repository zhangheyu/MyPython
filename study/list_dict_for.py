my_dict = {}
my_list = []

my_dict1 = {
    '小明': 129,
    '小兰': 148,
    '小红': 89
}
my_dic2 = {
    '小明': 2,
    '小兰': 3,
    '小红': 99
}
my_list.append(my_dict1)
my_list.append(my_dic2)
# print(my_dict)
# print(my_list)

for i, li in enumerate(my_list):
    print(i, li)
    li['小明'] = 100
    my_list[i] = li
    print(my_list)

