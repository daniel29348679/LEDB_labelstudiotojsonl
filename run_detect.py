# %%
from os import *

path = getcwd()
path += "/images"
for file_name in listdir("images"):
    if file_name.endswith(".jpg"):
        print(f"Processing {file_name}")
        print(f"ocrs {path}\\{file_name} -o {path}\\{file_name[:-4]}.txt")
        err = system(f"ocrs {path}\\{file_name} -o {path}\\{file_name[:-4]}.txt")
        if err:
            print(f"Error processing {file_name}")
# %%
