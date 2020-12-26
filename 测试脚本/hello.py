# print("hello world")
# # print(1 + 2)
# score = 88
# if score > 80:
#     print("good")
# else:
#     print("bad")

from typing import List

def twoSum(nums: List[int], target: int) -> List[int]:
    hashtable = dict()
    for i, num in enumerate(nums):
        if target - num in hashtable:
            return [hashtable[target - num], i]
        hashtable[nums[i]] = i
    return []


# result = twoSum([2, 7, 11, 15], 9)
# print(result)

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time

ua = UserAgent()
headers = {"User-Agent": ua.random}
resp = requests.get(url='http://wb99.xyz/portal.php?x=786946', headers=headers)
print(resp.text)