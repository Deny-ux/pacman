import os
try:
    os.mkdir("dd")
except FileExistsError:
    pass