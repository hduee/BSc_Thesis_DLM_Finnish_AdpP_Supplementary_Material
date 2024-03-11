import math

x = float(input("Enter the value for x: "))
y = float(input("Enter the value for y: "))

total = x+y

rx = x / total
ry = y / total
h = - ( ( rx * ( math.log(rx, 2.0) ) ) + ( ry * ( math.log(ry, 2.0) ) ) )

print(h)
