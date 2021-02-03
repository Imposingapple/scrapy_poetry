cipai_list = []
with open('../cipai.txt',encoding="utf-8") as f:
    for line in f:
        cipai_list.extend(line.strip().split())

print(cipai_list)