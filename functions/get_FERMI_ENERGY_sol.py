def get_EFERMI():
        word = "EFERMI "
        with open("OUTCAR", "r") as file:
                for line_number, line in enumerate(file):
                        if word in line:
                                a = line
        b = a.replace("    EFERMI              = ", "")
        c = b.replace("eV", "")
        c = float(c)
        print(c)
        return c
