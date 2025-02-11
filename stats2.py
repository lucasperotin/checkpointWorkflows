
import glob, os
import math

os.chdir("./results/pegasus/BLAST/")
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

rat=0
rat2=0
rat3=0
rbet=0
rworse=0
rsame=0
for fila2 in glob.glob("yd*"):
    fila="n"+fila2
    f= open(os.getcwd()+"/"+fila,"r")
    Lines=f.readlines()
    f2=open(os.getcwd()+"/"+fila2,"r")
    Lines2=f2.readlines()
    
    issame=True
    for j in range(30):
        card+=1
        line=Lines[j].split()
        line2=Lines2[j].split()
        A=(float) (line[0])
        B=(float)(line2[0])
        rbet+=A>B
        rworse+=A<B
        rsame+=A==B
        rat+=math.log(A/B)
    
rat/=card
card=0

for fila2 in glob.glob("yd*"):
    fila="n"+fila2
    f= open(os.getcwd()+"/"+fila,"r")
    Lines=f.readlines()
    f2=open(os.getcwd()+"/"+fila2,"r")
    Lines2=f2.readlines()
    
    issame=True
    for j in range(30):
        card+=1
        line=Lines[j].split()
        line2=Lines2[j].split()
        A=(float) (line[0])
        B=(float)(line2[0])
        
        rat2=math.log(A/B)
        rat3+=(rat2-rat)**2
rat3/=card

rat3=math.exp(math.sqrt(rat3))
        
print(math.exp(rat))
print(rat3)
print(rbet)
print(rworse)
print(rsame)
print(card)

card=0
rat=0
rbet=0
rworse=0
rsame=0
rat3=0


os.chdir("../Genome/")
for fila2 in glob.glob("yd*"):
    fila="n"+fila2
    f= open(os.getcwd()+"/"+fila,"r")
    Lines=f.readlines()
    f2=open(os.getcwd()+"/"+fila2,"r")
    Lines2=f2.readlines()
    
    issame=True
    for j in range(30):
        card+=1
        line=Lines[j].split()
        line2=Lines2[j].split()
        A=(float) (line[0])
        B=(float)(line2[0])
        rbet+=A>B
        rworse+=A<B
        rsame+=A==B
        rat+=math.log(A/B)
    
rat/=card

card=0

for fila2 in glob.glob("yd*"):
    fila="n"+fila2
    f= open(os.getcwd()+"/"+fila,"r")
    Lines=f.readlines()
    f2=open(os.getcwd()+"/"+fila2,"r")
    Lines2=f2.readlines()
    
    issame=True
    for j in range(30):
        card+=1
        line=Lines[j].split()
        line2=Lines2[j].split()
        A=(float) (line[0])
        B=(float)(line2[0])
        
        rat2=math.log(A/B)
        rat3+=(rat2-rat)**2
rat3/=card

rat3=math.exp(math.sqrt(rat3))
print(math.exp(rat))
print(rat3)
print(rbet)
print(rworse)
print(rsame)
print(card)

card=0
rat=0
rbet=0
rworse=0
rsame=0
rat3=0
            
os.chdir("../Seismology/")
for fila2 in glob.glob("yd*"):
    fila="n"+fila2
    f= open(os.getcwd()+"/"+fila,"r")
    Lines=f.readlines()
    f2=open(os.getcwd()+"/"+fila2,"r")
    Lines2=f2.readlines()
    
    issame=True
    for j in range(30):
        card+=1
        line=Lines[j].split()
        line2=Lines2[j].split()
        A=(float) (line[0])
        B=(float)(line2[0])
        rbet+=A>B
        rworse+=A<B
        rsame+=A==B
        rat+=math.log(A/B)
    

rat/=card
card=0

rat3=math.exp(math.sqrt(rat3))
for fila2 in glob.glob("yd*"):
    fila="n"+fila2
    f= open(os.getcwd()+"/"+fila,"r")
    Lines=f.readlines()
    f2=open(os.getcwd()+"/"+fila2,"r")
    Lines2=f2.readlines()
    
    issame=True
    for j in range(30):
        card+=1
        line=Lines[j].split()
        line2=Lines2[j].split()
        A=(float) (line[0])
        B=(float)(line2[0])
        
        rat2=math.log(A/B)
        rat3+=(rat2-rat)**2
rat3/=card
       
rat3=math.exp(math.sqrt(rat3))
print(math.exp(rat))
print(rat3)
print(rbet)
print(rworse)
print(rsame)
print(card)

card=0
rat=0
rbet=0
rworse=0
rsame=0
rat3=0
 
os.chdir("../SRAS/")
for fila2 in glob.glob("yd*"):
    fila="n"+fila2
    f= open(os.getcwd()+"/"+fila,"r")
    Lines=f.readlines()
    f2=open(os.getcwd()+"/"+fila2,"r")
    Lines2=f2.readlines()
    
    issame=True
    for j in range(30):
        card+=1
        line=Lines[j].split()
        line2=Lines2[j].split()
        A=(float) (line[0])
        B=(float)(line2[0])
        rbet+=A>B
        rworse+=A<B
        rsame+=A==B
        rat+=math.log(A/B)
    

rat/=card
card=0

for fila2 in glob.glob("yd*"):
    fila="n"+fila2
    f= open(os.getcwd()+"/"+fila,"r")
    Lines=f.readlines()
    f2=open(os.getcwd()+"/"+fila2,"r")
    Lines2=f2.readlines()
    
    issame=True
    for j in range(30):
        card+=1
        line=Lines[j].split()
        line2=Lines2[j].split()
        A=(float) (line[0])
        B=(float)(line2[0])
        
        rat2=math.log(A/B)
        rat3+=(rat2-rat)**2
rat3/=card
        
rat3=math.exp(math.sqrt(rat3))
print(math.exp(rat))
print(rat3)
print(rbet)
print(rworse)
print(rsame)
print(card)

card=0
rat=0
rbet=0
rworse=0
rsame=0
rat3=0

