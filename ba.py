import os
import subprocess
import shutil
from tqdm import tqdm

# 读取.par文件
par_file = "guji.par"
with open(par_file, "r") as par:
    par_lines = par.read().splitlines()

# 运行renumf90
renumf90_command = f"renumf90 {par_file}"
subprocess.run(renumf90_command, shell=True)

# 运行blupf90
blupf90_command = f"blupf90+ renf90.par"
subprocess.run(blupf90_command, shell=True)

# 从'solutions'中提取值为2的行的第三和第四列，生成文件A
solution_columns = []
with open("solutions", "r") as solution_file:
    for line in tqdm(solution_file, desc="Processing 'solutions'"):
        columns = line.split()
        if len(columns) >= 4 and columns[1] == "1":
            solution_columns.append([columns[2], columns[3]])

with open("A.txt", "w") as A:
    for data in solution_columns:
        A.write("\t".join(data) + "\n")
print("文件A包含两列内容，重编码id，育种值，默认育种值的level为2")

# 从'renadd02.ped'中提取第一列和第十列，生成文件B
ped_columns = []
with open("renadd01.ped", "r") as ped_file:
    for line in tqdm(ped_file, desc="Processing 'renadd02.ped'"):
        columns = line.split()
        if len(columns) >= 10:
            ped_columns.append([columns[0], columns[9]])

with open("B.txt", "w") as B:
    for data in ped_columns:
        B.write("\t".join(data) + "\n")
print("文件B主要包括重编码id，原始id")

# 从A文件中读取第一列的数据
with open("A.txt", "r") as file_a:
    lines_a = file_a.readlines()

# 从B文件中读取第一列的数据
with open("B.txt", "r") as file_b:
    lines_b = file_b.readlines()

# 创建一个字典，将A文件的第一列作为值，第二列和B文件的第一列作为建
b_data_dict = {}
for line_b in lines_b:
    columns_b = line_b.split()
    if len(columns_b) >= 2:
        key = columns_b[0]
        value = columns_b[1]
        b_data_dict[key] = value

# 合并数据并写入C文件
with open("C.txt", "w") as file_c:
    for line_a in lines_a:
        columns_a = line_a.split()
        if len(columns_a) >= 1:
            key = columns_a[0]
            if key in b_data_dict:
                combined_data = f"{key}\t{columns_a[1]}\t{b_data_dict[key]}\n"
                file_c.write(combined_data)
print("C文件包含三列，重编码id，育种值，原始id")

# 读取C文件并对第三列进行排序
with open("C.txt", "r") as file_c:
    lines_c = file_c.readlines()

# 对第三列排序
try:
    sorted_lines_c = sorted(lines_c, key=lambda x: int(x.split("\t")[2]))
except ValueError as e:
    print(f"An error occurred while sorting lines: {e}")
    sorted_lines_c = lines_c 

# 创建新文件并提取第二列和第三列，保存为solution_EBV.txt，文件输出时显示绿色进度条：
with open("solution_EBV.txt", "w") as file_solution_ebv:
    for line_c in tqdm(sorted_lines_c, desc="Processing 'solution_EBV.txt'", colour="green"):
        columns_c = line_c.split("\t")
        if len(columns_c) >= 3:
            data = f"{columns_c[1]}\t{columns_c[2]}"
            file_solution_ebv.write(data)
print("solution_EBV.txt file created with sorted and extracted data.")
print("育种值，原始id")

# 在屏幕上显示出solution_EBV的内容
with open("solution_EBV.txt", "r") as f:
    for line in f:
        print(line)
print("(●'◡'●)")
