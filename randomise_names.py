import os
from random import randint

report_list = [filename for filename in os.listdir(".")
               if os.path.isfile(filename) if filename[-4:] == ".pdf"]


for x in report_list:
    try:
        os.rename(x, f"{randint(0,10000)}.pdf")
    except FileExistsError:  # Yes, this condition was met once
        os.rename(x, f"{randint(10001,100000)}.pdf")
