# remaps coco dataset id's for only the things we want to detect in coco.names
import sys
import os

remap = open("remap.txt", "r")
mappings = []
with remap as f:
    for line in f:
        mappings.append(line.split())

print(mappings)
numbers_to_replace = [row[0] for row in mappings]
print(numbers_to_replace)
path_to_labels = sys.argv[1]
print(path_to_labels)
labels = os.listdir(path_to_labels)
print(labels)
for label in labels:
    file_path = os.path.join(path_to_labels, label)
    text = []
    label_file_read = open(file_path, "r+")
    for line in label_file_read:
        text.append(line.split())
    label_file_read.truncate(0)
    label_file_read.close()

    for line_index in range(0, len(text)):
        try:
            index = numbers_to_replace.index(text[line_index][0])
            text[line_index][0] = (mappings[index][1])
        except ValueError:
            print("No number to replace")
    print("\n\n")

    label_file_write = open(file_path, "a")
    for line in text:
        to_append = ""
        for i in line:
            to_append += (i + " ")
        label_file_write.write(to_append + "\n")
