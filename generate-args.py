import sys
import os

def generate(nbsampl,nbscenar,nbmach): 
    
    pp=["4096","5800","8192","11600","16384","24200","35000","50000"]
    pbase="16384"
    cc=["15","21","30","42","85","120","170","240"]
    cbase="60"
    uu=["2","3","5","7","14","20","28","40"]
    ubase="10"
    nn=["8840","12500","17680","25000","35350","50000","70700"]
    nbase="50000"
    
    typegr=["BLAST","Genome","Seismology","SRAS"]
    nnbase=nbase
    ppbase=pbase
    ccbase=cbase
    uubase=ubase
    ffbase="8"

    f2=open(os.getcwd()+"/launch",'a')

    args=["/files/arguments/args"+(str)(i)+".txt" for i in range(nbmach)]
    for j in range(nbmach):
        argname=args[j]
        f = open(os.getcwd()+argname,'a')
        if (j<nbmach-1):
            f2.write("./a.out \"."+argname+"\"&\n")
        else:
            f2.write("./a.out \"."+argname+"\"\n")
            outfinalbis="n"+nnbase+"f"+ffbase+"p"+ppbase+"c"+ccbase+"u"+uubase+".txt"

        for i in range(j+30,nbsampl+30,nbmach):
            for t in range(len(typegr)):
                folder=typegr[t]+"/"
                folderbis="pegasus/"+folder

                for p in range(len(pp)):
                    ppbase=pp[p]
                    outfinalbis="n"+nnbase+"f"+ffbase+"p"+ppbase+"c"+ccbase+"u"+uubase+".txt"
                    fi="n"+nnbase+"f"+ffbase+"_"+(str) (i)+".txt"
                    f.write(fi+" rigid "+ppbase+" length "+nbscenar+" nyd "+folderbis+" nyd"+outfinalbis+" "+ccbase+" "+uubase+"\n")
                ppbase=pbase

                for c in range(len(cc)):
                    ccbase=cc[c]
                    if (ccbase !=cbase):
                        outfinalbis="n"+nnbase+"f"+ffbase+"p"+ppbase+"c"+ccbase+"u"+uubase+".txt"
                        fi="n"+nnbase+"f"+ffbase+"_"+(str) (i)+".txt"
                        f.write(fi+" rigid "+ppbase+" length "+nbscenar+" nyd "+folderbis+" nyd"+outfinalbis+" "+ccbase+" "+uubase+"\n")
                ccbase=cbase

                for u in range(len(uu)):
                    uubase=uu[u]
                    if (uubase !=ubase):
                        outfinalbis="n"+nnbase+"f"+ffbase+"p"+ppbase+"c"+ccbase+"u"+uubase+".txt"
                        fi="n"+nnbase+"f"+ffbase+"_"+(str) (i)+".txt"
                        f.write(fi+" rigid "+ppbase+" length "+nbscenar+" nyd "+folderbis+" nyd"+outfinalbis+" "+ccbase+" "+uubase+"\n")
                uubase=ubase

                for n in range(len(nn)):
                    nnbase=nn[n]
                    if (nnbase !=nbase):
                        outfinalbis="n"+nnbase+"f"+ffbase+"p"+ppbase+"c"+ccbase+"u"+uubase+".txt"
                        fi="n"+nnbase+"f"+ffbase+"_"+(str) (i)+".txt"
                        f.write(fi+" rigid "+ppbase+" length "+nbscenar+" nyd "+folderbis+" nyd"+outfinalbis+" "+ccbase+" "+uubase+"\n")
                nnbase=nbase

        f.close()
    f2.close()


generate((int) (sys.argv[1]), sys.argv[2], (int) (sys.argv[3]))

