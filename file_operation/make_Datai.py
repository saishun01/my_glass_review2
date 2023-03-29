import shutil
import os

for i in range(10000):
    num = 15000 + i
    n_Data = num // 300 - 49
    n_Series = num % 300 + 1

    path1 = r"D:\20230222\Data\Project.lif_Series014_t0" + str(num) + r".tif"
    path2 = r"D:\20230222\Data_divided\Data" + str(n_Data)
    path3 = path2 + r"\Series"+'{:04}'.format(n_Series) + r".tif"

    if not os.path.exists(path2):
        os.mkdir(path2)

    shutil.copy(path1, path3)