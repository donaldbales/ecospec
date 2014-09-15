import os

DATA_PATH = r"/home/ecospec/"
FILE_NAME = r"appendme.txt"

if not os.path.exists(DATA_PATH):
    os.makedirs(DATA_PATH)

appendme = open(DATA_PATH + FILE_NAME, "a")

appendme.write("some text")

appendme.close()
