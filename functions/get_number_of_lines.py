def get_number_of_lines_for_huge_files()
  number_of_lines = sum(1 for i in open('file'))
  return number_of_lines

def get_number_of_lines()
  number_of_lines = 0
  for i in open("file"):
    number_of_lines += 1
  print("number_of_line: ", number_of_lines)
  return number_of_lines
