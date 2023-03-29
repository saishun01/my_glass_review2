import shutil
import os

#os.mkdir(r"D:\20230222\Data")
for i in range(10000):
    num = 15000 + i
    path = r"D:\20230222\014\Project.lif_Series014_t0" + str(num) + r".tif"
    shutil.copy(path,r"D:\20230222\Data")
