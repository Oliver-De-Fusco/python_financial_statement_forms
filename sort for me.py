import os

PATH = os.getcwd()

for (dirpath, dirnames, filenames) in os.walk(PATH):
    for filename in filenames:
        if filename[1].lower() == "q":
            print(filename)
            
            year = filename[2:4]
            
            if not os.path.exists(os.path.join(PATH,year)):
                print(f"making directory for {year}")
                os.makedirs(year)
            
            print(f"moving {filename} to {year}")
            os.rename(os.path.join(PATH,filename),os.path.join(PATH,year,filename))