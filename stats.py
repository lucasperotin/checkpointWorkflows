
import glob, os


os.chdir("./files/checkpoints/pegasus/BLAST/")
same=0
dif=0
tdif=0
t1=0
t1b=0
to=0
tob=0
amax=0
atot=0
card=0

rsame=0
rdif=0
print("B")
for fila in glob.glob("yd*"):
    fila2="n"+fila
    f= open(os.getcwd()+"/"+fila,"r")
    Lines=f.readlines()
    f2=open(os.getcwd()+"/"+fila2,"r")
    Lines2=f2.readlines()
    
    issame=True
    for j in range(len(Lines)):
        card+=1
        line=Lines[j].split()
        line2=Lines2[j].split()
        if (line[1]==line2[1]):
            same+=1
        elif ((int) (line[1])==(int) (line2[1])+1):
            dif+=1
            issame=False
        else:
            print(fila)
            print(j)
            tdif+=1
            issame=False
        
        if((int) (line2[1])==1):
            t1+=1
        else:
            to+=1
            
            
        if((int) (line[1])==1):
            t1b+=1
        else:
            tob+=1
        
    if (issame and fila[2]!='1'):
        rsame+=1
    elif(fila[2]!='1'):
        rdif+=1

print(same)
print(dif)
print(tdif)

print(rsame)
print(rdif)
same=0
dif=0
tdif=0
t1=0
t1b=0
to=0
tob=0
amax=0
atot=0
card=0

rsame=0
rdif=0

print("G")
os.chdir("../Genome/")
for fila in glob.glob("yd*"):
    fila2="n"+fila
    f= open(os.getcwd()+"/"+fila,"r")
    Lines=f.readlines()
    f2=open(os.getcwd()+"/"+fila2,"r")
    Lines2=f2.readlines()

    issame=True
    for j in range(len(Lines)):
        card+=1
        line=Lines[j].split()
        line2=Lines2[j].split()
        if (line[1]==line2[1]):
            same+=1
        elif ((int) (line[1])==(int) (line2[1])+1):
            dif+=1
            issame=False
        else:
            print(fila)
            print(j)
            tdif+=1
            issame=False
            
        if((int) (line2[1])==1):
            t1+=1
        else:
            to+=1

            
        if((int) (line[1])==1):
            t1b+=1
        else:
            tob+=1
     
    
    if (issame and fila[2]!='1'):
        rsame+=1
    elif(fila[2]!='1'):
        rdif+=1

print(same)
print(dif)
print(tdif)

print(rsame)
print(rdif)
same=0
dif=0
tdif=0
t1=0
t1b=0
to=0
tob=0
amax=0
atot=0
card=0

rsame=0
rdif=0
       
print("Se")     
os.chdir("../Seismology/")
for fila in glob.glob("yd*"):
    fila2="n"+fila
    f= open(os.getcwd()+"/"+fila,"r")
    Lines=f.readlines()
    f2=open(os.getcwd()+"/"+fila2,"r")
    Lines2=f2.readlines()

    issame=True
    for j in range(len(Lines)):
        line=Lines[j].split()
        line2=Lines2[j].split()
        card+=1
        if (line[1]==line2[1]):
            same+=1
        elif ((int) (line[1])==(int) (line2[1])+1):
            dif+=1
            issame=False
        else:
            print(fila)
            print(j)
            tdif+=1
            issame=False

        if((int) (line2[1])==1):
            t1+=1
        else:
            to+=1
              
            
        if((int) (line[1])==1):
            t1b+=1
        else:
            tob+=1
    
   
    if (issame and fila[2]!='1'):
        rsame+=1
    elif(fila[2]!='1'):
        rdif+=1
            
 
print(same)
print(dif)
print(tdif)

print(rsame)
print(rdif)
same=0
dif=0
tdif=0
t1=0
t1b=0
to=0
tob=0
amax=0
atot=0
card=0

rsame=0
rdif=0
print("SR")
os.chdir("../SRAS/")
for fila in glob.glob("yd*"):
    fila2="n"+fila
    f= open(os.getcwd()+"/"+fila,"r")
    Lines=f.readlines()
    f2=open(os.getcwd()+"/"+fila2,"r")
    Lines2=f2.readlines()

    issame=True
    for j in range(len(Lines)):
        line=Lines[j].split()
        line2=Lines2[j].split()
        card+=1
        if (line[1]==line2[1]):
            same+=1
        elif ((int) (line[1])==(int) (line2[1])+1):
            dif+=1
            issame=False
        else:
            print(fila)
            print(j)
            tdif+=1
            issame=False

        if((int) (line2[1])==1):
            t1+=1
        else:
            to+=1
              
            
        if((int) (line[1])==1):
            t1b+=1
        else:
            tob+=1
   
    if (issame and fila[2]!='1'):
        rsame+=1
    elif(fila[2]!='1'):
        rdif+=1


print(same)
print(dif)
print(tdif)

print(rsame)
print(rdif)

