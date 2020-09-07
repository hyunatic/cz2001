import timeit

def main(text, find):
    n = len(text)
    m = len(find)

    for i in range(0, n-m + 1):
        j = 0
        while j < m and find[j] == text[i + j]:
            j += 1
        if j == m:
            return i

    return False


with open("CP000828.fna.txt", "r") as test_file:
    temp = ""

    for text in test_file:
        if "complete genome" not in text:
            temp += text
            #temp = temp.strip()

text = temp
print(text)

find = input("Find: ").upper()

# timer begins
start = timeit.default_timer()

loc = main(text, find)

if loc >= 1:
    print(find, "found at index", loc)
else:
    print("Empty!")

stop = timeit.default_timer()
print("Time taken: ", stop-start)
