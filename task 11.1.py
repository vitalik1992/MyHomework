def get_file_size():
    count = 0
    while True:
        with open('text.txt','rb') as f:
            file = f.readline()
            for i in file:
                count += 1
        yield count
a = get_file_size()
print(a.__next__())
print(a.__next__())
print(a.__next__())
