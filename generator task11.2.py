def generator( ):
    number = 654321
    while True:
        yield number
        number = str(number)
        b = number[0:3]
        c = number[3:7]
        f = c + b
        num = int(number) * int(f)
        num = list(str(num))
        if len(num) < 12:
            while len(num) < 12:
                num.insert(0, '0')
        num2 = num[3:9]
        newSroka = ''
        for i in num2:
            newSroka += i
        number = int(newSroka)



a = generator()
def main():
    print(a.__next__())
    print(a.__next__())
    print(a.__next__())
    print(a.__next__())


if __name__ == '__main__':
    main()