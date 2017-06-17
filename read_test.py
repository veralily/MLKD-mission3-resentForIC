import os
import time
data_dir = "ic-data//train"


def file_list(data_dir):
    filenames = []
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.jpg':
                filenames.append(file)
            if os.path.splitext(file)[1] == '.label':
                labelname = os.path.join(root, file)

    return filenames, labelname

filenames, labelname = file_list(data_dir)
print(filenames)
print(len(filenames))

data = []
print "listing files in", data_dir
start_time = time.time()
files, labelname = file_list(data_dir)
labels_map = {}
label_reader = open(labelname)
labels_content = label_reader.readlines()
for i, label_content in enumerate(labels_content):
    label_index = label_content.split(' ')[0]
    label = label_content.split(' ')[1]
    labels_map[label_index] = {"order":i+1, "label": label}

duration = time.time() - start_time
print "took %f sec" % duration

for img_fn in files:
    label_index = os.path.splitext(img_fn)[0]
    label_name = labels_map[label_index].get("label")
    fn = os.path.join(data_dir, img_fn)

    data.append({
        "filename": fn,
        "label_name": label_name,
        "label_num": int(label_name),
    })

print(data)
print(len(data))
