print("Temp 1: ")
with open("/mnt/1wire/28.9607E5080000/temperature", "r")  as f:
    info = f.readlines()
print("     " + info[0].strip())
