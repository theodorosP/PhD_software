def get_NELECT_INCAR(path):
    os.chdir(path)
    word = "NELECT = "
    with open("INCAR", "r") as file:
        for line_number, line in enumerate(file):
            if word in line:
                a = line
    return a
