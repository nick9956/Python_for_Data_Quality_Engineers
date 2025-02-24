import random


def average(lst):
    return sum(lst) / len(lst) if lst else 0


random_numbers = [random.randint(0, 1000) for i in range(0, 100)]

for i in range(len(random_numbers)):
    swapped = False
    for j in range(0, len(random_numbers) - i - 1):
        if random_numbers[j] > random_numbers[j + 1]:
            random_numbers[j], random_numbers[j + 1] = random_numbers[j + 1], random_numbers[j]
            swapped = True
    if not swapped:
        break

avg_odd_list = [num for num in random_numbers if num % 2 != 0]
avg_even_list = [num for num in random_numbers if num % 2 == 0]

print("Average value for the even list is {0}".format(average(avg_even_list)))
print("Average value for the odd list is {0}".format(average(avg_odd_list)))
