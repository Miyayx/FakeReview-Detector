
with open('mantualdata/annotation_fake2.dat','r') as f:
    lines = []
    for line in f.readlines():
        line = line.strip("\n")
        try:
            line = eval(line)
        except:
            print line
        if not isinstance(line,int):
            print line
        else:
            lines.append(line)

with open('mantualdata/annotation_fake2.dat','w') as f:
    for line in lines:
        f.write(str(line)+"\n")
            

