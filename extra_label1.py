import os
import time
data_dir = "ic-data//extra"

label_file = 'ic-data//extra2.label'
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
    if name > 60 and name < 101:
        write_content = str(name)+' '+str(7)
        print(write_content)
        write_label.writelines(write_content + '\n')

    if name > 355 and name < 396:
        write_content = str(name)+' '+str(2)
        print(write_content)
        write_label.writelines(write_content + '\n')

    if name > 660 and name < 701:
        write_content = str(name)+' '+str(6)
        print(write_content)
        write_label.writelines(write_content + '\n')

    if name > 1090 and name < 1131:
        write_content = str(name)+' '+str(5)
        print(write_content)
        write_label.writelines(write_content + '\n')

    if name > 1394 and name < 1435:
        write_content = str(name)+' '+str(10)
        print(write_content)
        write_label.writelines(write_content + '\n')

    if name > 1698 and name < 1739:
        write_content = str(name)+' '+str(4)
        print(write_content)
        write_label.writelines(write_content + '\n')

    if name > 2006 and name < 2047:
        write_content = str(name)+' '+str(1)
        print(write_content)
        write_label.writelines(write_content + '\n')

    if name > 2324 and name < 2365:
        write_content = str(name)+' '+str(8)
        print(write_content)
        write_label.writelines(write_content + '\n')

    if name > 2751 and name < 2792:
        write_content = str(name)+' '+str(9)
        print(write_content)
        write_label.writelines(write_content + '\n')

    if name > 3181 and name < 3222:
        write_content = str(name)+' '+str(3)
        print(write_content)
        write_label.writelines(write_content + '\n')

    if name > 66667 and name < 66708:
        write_content = str(name)+' '+str(11)
        print(write_content)
        write_label.writelines(write_content + '\n')

    if name > 73764:
        write_content = str(name)+' '+str(12)
        print(write_content)
        write_label.writelines(write_content + '\n')
write_label.close()