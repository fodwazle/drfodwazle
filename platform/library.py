def write_file(file, message = "You need to add something as a message!"):
    writeFile = open(file, "w")
    writeFile.write(message)
    writeFile.close()
def read_file(file):
    readFile = open(file, "r")
    print(readFile.rstrip())
    readFile.close()
def append_file(file, message = "You need to add something as a message!"):
    appFile = open(file, "a")
    appFile.write(message)
    appFile.close()
