import sys
from copy import deepcopy
disk = {}
def undo_traversal(logs,start,end):
    commited = []
    trans=[]
    check=False
    if start != -1 and end == -1:
        trans = logs[start].split("(")[1].split(")")[0].split(",")
        for t in trans:
            t.strip(" ")
        check=True
    if start != -1 and end != 1:
        logs = logs[start+1:]
    # print(logs)
    for i in range(len(logs)):
        if len(trans)==0:
            break
        line = logs[-i-1]
        if line[0] == "T":
            words = [b.strip(" ") for b in line.split(",")]
            if words[0] not in commited:
                disk[words[1]] = int(words[2].strip("\n"))
        elif "COMMIT" in line:
            commited.append(line.split(' ')[1])
        elif check == 1 and "START" in line and "CKPT" not in line and line.split(' ')[1] in trans:
            trans.remove(line.split(' ')[1])
inp = sys.argv[1]
begin = True
logs = []
start=-1
end=-1
for line in open(inp):
    temp=line.split(" ")
    if begin is True:
        begin=False
        for i in range(0,len(temp),2):
            disk[temp[i]]=temp[i+1]
    else:
        if line!='\n':
            s1 = line.split('<')[1]
            s2=s1.split('>')[0]
            # print(s2)
            logs.append(s2)
            if "START" in s2 and "CKPT" in s2:
                start = len(logs)-1
            elif "END" in s2 and "CKPT" in s2:
                end = len(logs)-1
if(start>end): end=-1
# print(logs)
undo_traversal(deepcopy(logs),start,end)
out = open("20171196_2.txt","w")
st = ""
for i in sorted(disk):
    st+=i+" "+str(disk[i])+" "
st=st[:-1]
out.write(st)
