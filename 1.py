import sys
present_in_mem= {}
var_dict= {}
disk={}
mem={}
trans={}
order=[]
def print_values(out,temp):
    ans = ""
    for i in sorted(temp):
        ans+=i+" "+str(temp[i])+" "
    ans=ans[:-1]
    out.write(ans+"\n")

def perform(curr,x,start,out):
    ins = trans[curr][start:start+x]
    if start==0:
        out.write("<START "+curr+">"+"\n")
        print_values(out,mem)
        print_values(out,disk)
    
    for line in ins:
        temp=line.split("(")
        if temp[0] == "READ":
            c=temp[1].split(",")
            var = c[0]
            value =c[1].split(")")[0].strip()
            if var not in present_in_mem.keys():
                present_in_mem[var] = value
                var_dict[value] = disk[var]
                mem[var] = disk[var]
            else:
                var_dict[value] = mem[var]
                present_in_mem[var] = value
        elif temp[0] == "WRITE":
            c=temp[1].split(",")
            var = c[0]
            value =c[1].split(")")[0].strip()
            out.write("<"+curr+", "+var+", "+str(mem[var])+">"+"\n")
            mem[var] = int(var_dict[value])
            print_values(out,mem)
            print_values(out,disk)
        elif temp[0] == "OUTPUT":
            var = temp[1].split(")")[0]
            disk[var]=mem[var]
        else:
            temp=temp[0].split(":=")
            # print(temp)
            var1 = temp[0].strip()
            op = None
            if '+' in temp[1]:
                op='+'
            elif '-' in temp[1]:
                op='-'
            elif '*' in temp[1]:
                op='*'
            elif '/' in temp[1]:
                op='/'

            var2 = temp[1].split(op)[0].strip()
            val = int(temp[1].split(op)[1].strip())
            res=0
            o1=int(var_dict[var2])
            o2=int(val)
            if op=='+':
                res=o1+o2
            if op=='-':
                res=o1-o2
            if op=='*':
                res=o1*o2
            if op=='/':
                res=float(o1)/float(o2)
            var_dict[var1]=res
            
    if start+x >= len(trans[curr]):
        out.write("<COMMIT "+curr+">"+"\n")
        print_values(out,mem)
        print_values(out,disk)
file=sys.argv[1]
x=int(sys.argv[2])
begin=True
tname=None
for l in open(file):
    temp=l.split(" ")
    if begin:
        begin=False
        # print(len(temp))
        for i in range(0,len(temp),2):
            disk[temp[i]]=temp[i+1].strip("\n")
    else:
        if temp[0][0] is 'T':
            # print(temp[0])
            order.append(temp[0])
            trans[temp[0]]=[]
            tname=temp[0]
        else:
            t=temp[0].split("(")
            if t[0] is '\n':
                pass
            else:
                if tname is not None and l[:-1] is not '':
                    trans[tname].append(l[:-1])
finish={}
for key in trans.keys():
    finish[key]=0

out=open("20171196_1.txt","w")

start=0
t=0
# print(trans)
while sum(finish.values())<len(trans):
    curr = order[t]
    if start>=len(trans[curr]):
        finish[curr]=1
    if finish[curr]==0:
        perform(curr,x,start,out)
    t+=1
    if t%len(order) == 0:
        start+=x
        t=0
