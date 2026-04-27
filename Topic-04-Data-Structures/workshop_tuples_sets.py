def calc(a:int, b: int) :
    min = a if a < b else b 
    max = a if a > b else b
    avg = (a+b)/2
    sum = a+b 
    return (min, max, avg, sum)

info = calc(5,10)
print(info[0])
print(info[-2:])

min, max, _, _ = calc(12,24)
print(f"Min: {min} - Max: {max}")



