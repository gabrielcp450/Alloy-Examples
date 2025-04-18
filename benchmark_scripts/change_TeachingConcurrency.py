from re import *
import sys

if len(sys.argv) != 2:
    print("Invalid arguments")
    sys.exit()


with open("Simple.cfg", "r") as f:
    x = f.read() 
x = sub(r'(CONSTANT N =) (\d+)', fr'\1 {sys.argv[1]}', x)

with open("Simple.cfg", "w") as f:
    f.write(x)

with open("Simple.als", 'r') as f:
    x = f.read()

x = sub(r'(for) (\d+) (but 1.. steps)', fr'\1 {sys.argv[1]} \3', x)

with open("Simple.als", 'w') as f:
    f.write(x)