import os
import time
data_dir = "ic-data//extra"

label_file = 'ic-data//extra.label'
write_label = open(label_file, 'w+')

def file_list(data_dir):
    filenames = []
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.jpg':
                filenames.append(os.path.splitext(file)[0])
    return filenames

filenames = file_list(data_dir)
for filename in filenames:
    name = int(filename)
    print(name)
    if name > 0 and name < 101:
        write_content = str(name)+' '+str(7)
        print(write_content)
        write_label.writelines(write_content + '\n')

    if name > 295 and name < 396:
        write_content = str(name)+' '+str(2)
        print(write_content)
        write_label.writelines(write_content + '\n')

    if name > 600 and name < 701:
        write_content = str(name)+' '+str(6)
        print(write_content)
        write_label.writelines(write_content + '\n')

    if name > 1030 and name < 1131:
        write_content = str(name)+' '+str(5)
        print(write_content)
        write_label.writelines(write_content + '\n')

    if name > 1334 and name < 1435:
        write_content = str(name)+' '+str(10)
        print(write_content)
        write_label.writelines(write_content + '\n')

    if name > 1638 and name < 1739:
        write_content = str(name)+' '+str(4)
        print(write_content)
        write_label.writelines(write_content + '\n')

    if name > 1946 and name < 2047:
        write_content = str(name)+' '+str(1)
        print(write_content)
        write_label.writelines(write_content + '\n')

    if name > 2214 and name < 2365:
        write_content = str(name)+' '+str(8)
        print(write_content)
        write_label.writelines(write_content + '\n')

    if name > 2691 and name < 2792:
        write_content = str(name)+' '+str(9)
        print(write_content)
        write_label.writelines(write_content + '\n')

    if name > 3121 and name < 3222:
        write_content = str(name)+' '+str(3)
        print(write_content)
        write_label.writelines(write_content + '\n')

    if name > 63350 and name < 66708:
        write_content = str(name)+' '+str(11)
        print(write_content)
        write_label.writelines(write_content + '\n')

    if name > 72196:
        write_content = str(name)+' '+str(12)
        print(write_content)
        write_label.writelines(write_content + '\n')
write_label.close()
