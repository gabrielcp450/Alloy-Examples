from re import *
import sys
import os


if len(sys.argv) != 3:
    print("Invalid arguments")
    sys.exit()

n = sys.argv[1]
i = int(sys.argv[2])

subfolder_count = 0
if os.path.exists(f"echo_n{n}"):
    subfolder_count = len([name for name in os.listdir(f"echo_n{n}") 
                            if os.path.isdir(os.path.join(f"echo_n{n}", name))])

print(subfolder_count)
if i > 0:
    tla_config_filename = f"echo_n{n}/echo_n{n}_{i}/MCEcho.tla"

    with open(tla_config_filename, "r") as f:
        x = f.read() 

    with open("MCEcho.tla", "w") as f:
        f.write(x)

with open("echo.als", 'r') as f:
    x = f.read()

x = sub(r'(for)\s*(\d+)\s*(but)\s*(1)\s*(..)\s*(steps)', fr'\1 {n} \3 \4\5\6', x)

with open("echo.als", 'w') as f:
    f.write(x)