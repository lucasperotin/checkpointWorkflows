import sys
import matplotlib
import matplotlib.pyplot as plt
import glob, os
import numpy as np

def plotplot(ident):
        typegr=["BLAST","Genome","Seismology","SRAS"]
        labtypegr=["BLAST","Gen.","Sei.","SRAS"]
        p=["4096","5800","8192","11600","16384","24200","35000","50000"]
        ppbase="16384"
        c=["15","21","30","42","60","85","120","170","240"]
        ccbase="60"
        u=["2","3","5","7","10","14","20","28","40"]
        uubase="10"
        n=["8840","12500","17680","25000","35350","50000","70700"]
        nnbase="50000"
        l=["yd","nyd","cm","cmd"]

        Msize=max(len(typegr),len(n),len(p),len(c),len(u),len(l))+1
        position1=[5*i+1 for i in range(Msize)]
        position2=[5*i+2 for i in range(Msize)]
        position3=[5*i+3 for i in range(Msize)]
        position4=[5*i+4 for i in range(Msize)]
        poslab=[5*i+2 for i in range(Msize)]
        width=[0.9 for i in range(Msize)]
        nbase=nnbase
        pbase=ppbase
        cbase=ccbase
        ubase=uubase
        nbase=nnbase
        

        PP1=[[] for i in range(len(typegr))]
        PP2=[[] for i in range(len(typegr))]
        PP3=[[] for i in range(len(typegr))]
        PP4=[[] for i in range(len(typegr))]
        ubase=(str) ((int)((float) (ubase)*100))

        for pp in range(len(typegr)):
                typeg=typegr[pp]
                if (pp==0):
                        os.chdir("./files/detailed_results/pegasus/"+typeg+"/")
                if (pp>0):
                        os.chdir("../"+typeg+"/")
                for fila in glob.glob(l[0]+"p"+pbase+"c"+cbase+"u"+ubase+"n"+nbase+"*"):
                        f= open(os.getcwd()+"/"+fila,"r")
                        Lines=f.readlines()
                        for j in range(len(Lines)):
                                PP1[pp].append((float) (Lines[j][:-1]))
                        
                for fila in glob.glob(l[1]+"p"+pbase+"c"+cbase+"u"+ubase+"n"+nbase+"*"):
                        f= open(os.getcwd()+"/"+fila,"r")
                        Lines=f.readlines()
                        for j in range(len(Lines)):
                                PP2[pp].append((float) (Lines[j][:-1]))

                for fila in glob.glob(l[2]+"p"+pbase+"c"+cbase+"u"+ubase+"n"+nbase+"*"):
                        f= open(os.getcwd()+"/"+fila,"r")
                        Lines=f.readlines()
                        for j in range(len(Lines)):
                                PP3[pp].append((float) (Lines[j][:-1]))

                for fila in glob.glob(l[3]+"p"+pbase+"c"+cbase+"u"+ubase+"n"+nbase+"*"):
                        f= open(os.getcwd()+"/"+fila,"r")
                        Lines=f.readlines()
                        for j in range(len(Lines)):
                                PP4[pp].append((float) (Lines[j][:-1]))
                        
                PP1[pp].sort()
                y=len(PP1[pp])//10
                comp=0
                for x in range(y):
                        comp+=PP1[pp][x]-PP1[pp][y]
                        PP1[pp][x]=PP1[pp][y]
                for x in range(len(PP1[pp])-y,len(PP1[pp])):
                        comp+=PP1[pp][x]-PP1[pp][len(PP1[pp])-y]
                        PP1[pp][x]=PP1[pp][len(PP1[pp])-y]
                #Trick to not alter quartiles medians, percentile 10 and 90, or average and to omit values outside of percetile 10-90
                PP1[pp][len(PP1[pp])-1]+=comp+100
                PP1[pp][0]-=100

                        
                PP2[pp].sort()
                y=len(PP2[pp])//10
                comp=0
                for x in range(y):
                        comp+=PP2[pp][x]-PP2[pp][y]
                        PP2[pp][x]=PP2[pp][y]
                for x in range(len(PP2[pp])-y,len(PP2[pp])):
                        comp+=PP2[pp][x]-PP2[pp][len(PP2[pp])-y]
                        PP2[pp][x]=PP2[pp][len(PP2[pp])-y]
                PP2[pp][len(PP2[pp])-1]+=comp+100
                PP2[pp][0]-=100


                PP3[pp].sort()
                y=len(PP3[pp])//10
                comp=0
                for x in range(y):
                        comp+=PP3[pp][x]-PP3[pp][y]
                        PP3[pp][x]=PP3[pp][y]
                for x in range(len(PP3[pp])-y,len(PP3[pp])):
                        comp+=PP3[pp][x]-PP3[pp][len(PP3[pp])-y]
                        PP3[pp][x]=PP3[pp][len(PP3[pp])-y]

                PP3[pp][len(PP3[pp])-1]+=comp+100
                PP3[pp][0]-=100
                
                PP4[pp].sort()
                y=len(PP4[pp])//10
                comp=0
                for x in range(y):
                        comp+=PP4[pp][x]-PP4[pp][y]
                        PP4[pp][x]=PP4[pp][y]
                for x in range(len(PP4[pp])-y,len(PP4[pp])):
                        comp+=PP4[pp][x]-PP4[pp][len(PP4[pp])-y]
                        PP4[pp][x]=PP4[pp][len(PP4[pp])-y]

                PP4[pp][len(PP4[pp])-1]+=comp+100
                PP4[pp][0]-=100


        c1="blue" 
        c2="green"
        c3="red"
        c4="black"
        c5="yellow"
        Legend=['Young/Daly', 'Lambert', 'BasicCheckMore','CheckMore']

        ax=plt.subplots()
        meanpointprops1 = dict(marker="*",markersize=7,markeredgecolor=c1, markerfacecolor=c1)
        meanpointprops2 = dict(marker="*",markersize=7,markeredgecolor=c2, markerfacecolor=c2)
        meanpointprops3 = dict(marker="*",markersize=7,markeredgecolor=c3, markerfacecolor=c3)
        meanpointprops4 = dict(marker="*",markersize=7,markeredgecolor=c5, markerfacecolor=c5)
        b1=plt.boxplot(PP1,showfliers=False,boxprops=dict(color=c1),capprops=dict(color=c1),whiskerprops=dict(color=c1),flierprops=dict(color=c1, markeredgecolor=c1),medianprops=dict(color=c4), showmeans=True, meanprops=meanpointprops1, positions=position1[:len(typegr)], widths = width[:len(typegr)])
        b2=plt.boxplot(PP2,showfliers=False,boxprops=dict(color=c2),capprops=dict(color=c2),whiskerprops=dict(color=c2),flierprops=dict(color=c2, markeredgecolor=c2),medianprops=dict(color=c4), showmeans=True, meanprops=meanpointprops2, positions=position2[:len(typegr)], widths = width[:len(typegr)])
        b3=plt.boxplot(PP3,showfliers=False,boxprops=dict(color=c3),capprops=dict(color=c3),whiskerprops=dict(color=c3),flierprops=dict(color=c3, markeredgecolor=c3),medianprops=dict(color=c4), showmeans=True, meanprops=meanpointprops3, positions=position3[:len(typegr)], widths = width[:len(typegr)])
        b4=plt.boxplot(PP4,showfliers=False,boxprops=dict(color=c5),capprops=dict(color=c5),whiskerprops=dict(color=c5),flierprops=dict(color=c5, markeredgecolor=c5),medianprops=dict(color=c4), showmeans=True, meanprops=meanpointprops4, positions=position4[:len(typegr)], widths = width[:len(typegr)])
        plt.xticks(poslab[:len(typegr)],labtypegr)

        plt.legend([b1["boxes"][0], b2["boxes"][0], b3["boxes"][0],b4["boxes"][0]], Legend, loc='upper left')
                
                # naming the x axis 
        plt.xlabel('Workflow') 
                # naming the y axis 
        plt.ylabel('Ratio') 
        #plt.ylim([1,1.9])
                # show a legend on the plot 
        plt.savefig("../../../../results/plots/all"+ident+".jpg")
        plt.clf()
        plt.close()

        for i in range(len(typegr)):
                typeg=typegr[i]
                os.chdir("../"+typeg+"/")
                
                PP1=[[] for i in range(len(p))]
                PP2=[[] for i in range(len(p))]
                PP3=[[] for i in range(len(p))]
                PP4=[[] for i in range(len(p))]
                for pp in range(len(p)):
                        pbase=p[pp]
                        for fila in glob.glob(l[0]+"p"+pbase+"c"+cbase+"u"+ubase+"n"+nbase+"*"):
                                f= open(os.getcwd()+"/"+fila,"r")
                                Lines=f.readlines()
                                for j in range(len(Lines)):
                                        if((float) (Lines[j][:-1])>2):
                                            print("RAHHHA")
                                        PP1[pp].append((float) (Lines[j][:-1]))

                        for fila in glob.glob(l[1]+"p"+pbase+"c"+cbase+"u"+ubase+"n"+nbase+"*"):
                                f= open(os.getcwd()+"/"+fila,"r")
                                Lines=f.readlines()
                                for j in range(len(Lines)):
                                        PP2[pp].append((float) (Lines[j][:-1]))


                        for fila in glob.glob(l[2]+"p"+pbase+"c"+cbase+"u"+ubase+"n"+nbase+"*"):
                                f= open(os.getcwd()+"/"+fila,"r")
                                Lines=f.readlines()
                                for j in range(len(Lines)):
                                    PP3[pp].append((float) (Lines[j][:-1]))
                                        
                        for fila in glob.glob(l[3]+"p"+pbase+"c"+cbase+"u"+ubase+"n"+nbase+"*"):
                                f= open(os.getcwd()+"/"+fila,"r")
                                Lines=f.readlines()
                                for j in range(len(Lines)):
                                    PP4[pp].append((float) (Lines[j][:-1]))
                                
                        
                        PP1[pp].sort()
                        y=len(PP1[pp])//10
                        comp=0
                        for x in range(y):
                                comp+=PP1[pp][x]-PP1[pp][y]
                                PP1[pp][x]=PP1[pp][y]
                        for x in range(len(PP1[pp])-y,len(PP1[pp])):
                                comp+=PP1[pp][x]-PP1[pp][len(PP1[pp])-y]
                                PP1[pp][x]=PP1[pp][len(PP1[pp])-y]
                        PP1[pp][len(PP1[pp])-1]+=comp+100
                        PP1[pp][0]-=100
                        
                        PP2[pp].sort()
                        y=len(PP2[pp])//10
                        comp=0
                        for x in range(y):
                                comp+=PP2[pp][x]-PP2[pp][y]
                                PP2[pp][x]=PP2[pp][y]
                        for x in range(len(PP2[pp])-y,len(PP2[pp])):
                                comp+=PP2[pp][x]-PP2[pp][len(PP2[pp])-y]
                                PP2[pp][x]=PP2[pp][len(PP2[pp])-y]
                        PP2[pp][len(PP2[pp])-1]+=comp+100
                        PP2[pp][0]-=100

                        
                        PP3[pp].sort()
                        y=len(PP3[pp])//10
                        comp=0
                        for x in range(y):
                                comp+=PP3[pp][x]-PP3[pp][y]
                                PP3[pp][x]=PP3[pp][y]
                        for x in range(len(PP3[pp])-y,len(PP3[pp])):
                                comp+=PP3[pp][x]-PP3[pp][len(PP3[pp])-y]
                                PP3[pp][x]=PP3[pp][len(PP3[pp])-y]
                        PP3[pp][len(PP3[pp])-1]+=comp+100
                        PP3[pp][0]-=100
                        
                        PP4[pp].sort()
                        y=len(PP4[pp])//10
                        comp=0
                        for x in range(y):
                                comp+=PP4[pp][x]-PP4[pp][y]
                                PP4[pp][x]=PP4[pp][y]
                        for x in range(len(PP4[pp])-y,len(PP4[pp])):
                                comp+=PP4[pp][x]-PP4[pp][len(PP4[pp])-y]
                                PP4[pp][x]=PP4[pp][len(PP4[pp])-y]
        
                        PP4[pp][len(PP4[pp])-1]+=comp+100
                        PP4[pp][0]-=100

                        
                b1=plt.boxplot(PP1,showfliers=False,boxprops=dict(color=c1),capprops=dict(color=c1),whiskerprops=dict(color=c1),flierprops=dict(color=c1, markeredgecolor=c1),medianprops=dict(color=c4), showmeans=True, meanprops=dict(meanpointprops1), positions=position1[:len(p)], widths = width[:len(p)])
                b2=plt.boxplot(PP2,showfliers=False,boxprops=dict(color=c2),capprops=dict(color=c2),whiskerprops=dict(color=c2),flierprops=dict(color=c2, markeredgecolor=c2),medianprops=dict(color=c4), showmeans=True, meanprops=dict(meanpointprops2), positions=position2[:len(p)], widths = width[:len(p)])
                b3=plt.boxplot(PP3,showfliers=False,boxprops=dict(color=c3),capprops=dict(color=c3),whiskerprops=dict(color=c3),flierprops=dict(color=c3, markeredgecolor=c3),medianprops=dict(color=c4), showmeans=True, meanprops=dict(meanpointprops3), positions=position3[:len(p)], widths = width[:len(p)])
                b4=plt.boxplot(PP4,showfliers=False,boxprops=dict(color=c5),capprops=dict(color=c5),whiskerprops=dict(color=c5),flierprops=dict(color=c5, markeredgecolor=c5),medianprops=dict(color=c4), showmeans=True, meanprops=dict(meanpointprops4), positions=position4[:len(p)], widths = width[:len(p)])
                plt.xticks(poslab[:len(p)],p)
                #plt.legend([b1["boxes"][0], b2["boxes"][0], b3["boxes"][0]], Legend, loc='upper left',ncol=3)
                
                #plt.legend([b1["boxes"][0], b2["boxes"][0], b3["boxes"][0]], Legend, loc='upper left')
                
                # naming the x axis 
                plt.xlabel('Number of processors') 
                # naming the y axis 
                plt.ylabel('Ratio')
                #plt.ylim([1,1.9]) 
                # giving a title to my graph 
                plt.title(typeg) 
                  
                # show a legend on the plot 
                plt.savefig("../../../../results/plots/"+typeg+"/"+typeg+"proc"+ident+".jpg")
                plt.clf()
                plt.close()
                ppbase="16384"
                pbase=ppbase

                
                PP1=[[] for i in range(len(c))]
                PP2=[[] for i in range(len(c))]
                PP3=[[] for i in range(len(c))]
                PP4=[[] for i in range(len(c))]
                for pp in range(len(c)):
                        cbase=c[pp]
                        for fila in glob.glob(l[0]+"p"+pbase+"c"+cbase+"u"+ubase+"n"+nbase+"*"):
                                f= open(os.getcwd()+"/"+fila,"r")
                                Lines=f.readlines()
                                for j in range(len(Lines)):
                                        PP1[pp].append((float) (Lines[j][:-1]))

                        for fila in glob.glob(l[1]+"p"+pbase+"c"+cbase+"u"+ubase+"n"+nbase+"*"):
                                f= open(os.getcwd()+"/"+fila,"r")
                                Lines=f.readlines()
                                for j in range(len(Lines)):
                                        PP2[pp].append((float) (Lines[j][:-1]))


                        for fila in glob.glob(l[2]+"p"+pbase+"c"+cbase+"u"+ubase+"n"+nbase+"*"):
                                f= open(os.getcwd()+"/"+fila,"r")
                                Lines=f.readlines()
                                for j in range(len(Lines)):
                                        PP3[pp].append((float) (Lines[j][:-1]))
                                        
                        for fila in glob.glob(l[3]+"p"+pbase+"c"+cbase+"u"+ubase+"n"+nbase+"*"):
                                f= open(os.getcwd()+"/"+fila,"r")
                                Lines=f.readlines()
                                for j in range(len(Lines)):
                                    PP4[pp].append((float) (Lines[j][:-1]))
                                    
                        PP1[pp].sort()
                        y=len(PP1[pp])//10
                        comp=0
                        for x in range(y):
                                comp+=PP1[pp][x]-PP1[pp][y]
                                PP1[pp][x]=PP1[pp][y]
                        for x in range(len(PP1[pp])-y,len(PP1[pp])):
                                comp+=PP1[pp][x]-PP1[pp][len(PP1[pp])-y]
                                PP1[pp][x]=PP1[pp][len(PP1[pp])-y]
                        PP1[pp][len(PP1[pp])-1]+=comp+100
                        PP1[pp][0]-=100

                        
                        PP2[pp].sort()
                        y=len(PP2[pp])//10
                        comp=0
                        for x in range(y):
                                comp+=PP2[pp][x]-PP2[pp][y]
                                PP2[pp][x]=PP2[pp][y]
                        for x in range(len(PP2[pp])-y,len(PP2[pp])):
                                comp+=PP2[pp][x]-PP2[pp][len(PP2[pp])-y]
                                PP2[pp][x]=PP2[pp][len(PP2[pp])-y]
                        PP2[pp][len(PP2[pp])-1]+=comp+100
                        PP2[pp][0]-=100

                        
                        PP3[pp].sort()
                        y=len(PP3[pp])//10
                        comp=0
                        for x in range(y):
                                comp+=PP3[pp][x]-PP3[pp][y]
                                PP3[pp][x]=PP3[pp][y]
                        for x in range(len(PP3[pp])-y,len(PP3[pp])):
                                comp+=PP3[pp][x]-PP3[pp][len(PP3[pp])-y]
                                PP3[pp][x]=PP3[pp][len(PP3[pp])-y]
                        PP3[pp][len(PP3[pp])-1]+=comp+100
                        PP3[pp][0]-=100
                        
                        
                        PP4[pp].sort()
                        y=len(PP4[pp])//10
                        comp=0
                        for x in range(y):
                                comp+=PP4[pp][x]-PP4[pp][y]
                                PP4[pp][x]=PP4[pp][y]
                        for x in range(len(PP4[pp])-y,len(PP4[pp])):
                                comp+=PP4[pp][x]-PP4[pp][len(PP4[pp])-y]
                                PP4[pp][x]=PP4[pp][len(PP4[pp])-y]
        
                        PP4[pp][len(PP4[pp])-1]+=comp+100
                        PP4[pp][0]-=100
                        
                b1=plt.boxplot(PP1,showfliers=False,boxprops=dict(color=c1),capprops=dict(color=c1),whiskerprops=dict(color=c1),flierprops=dict(color=c1, markeredgecolor=c1),medianprops=dict(color=c4), showmeans=True, meanprops=dict(meanpointprops1), positions=position1[:len(c)], widths = width[:len(c)])
                b2=plt.boxplot(PP2,showfliers=False,boxprops=dict(color=c2),capprops=dict(color=c2),whiskerprops=dict(color=c2),flierprops=dict(color=c2, markeredgecolor=c2),medianprops=dict(color=c4), showmeans=True, meanprops=dict(meanpointprops2), positions=position2[:len(c)], widths = width[:len(c)])
                b3=plt.boxplot(PP3,showfliers=False,boxprops=dict(color=c3),capprops=dict(color=c3),whiskerprops=dict(color=c3),flierprops=dict(color=c3, markeredgecolor=c3),medianprops=dict(color=c4), showmeans=True, meanprops=dict(meanpointprops3), positions=position3[:len(c)], widths = width[:len(c)])
                b4=plt.boxplot(PP4,showfliers=False,boxprops=dict(color=c5),capprops=dict(color=c5),whiskerprops=dict(color=c5),flierprops=dict(color=c5, markeredgecolor=c5),medianprops=dict(color=c4), showmeans=True, meanprops=dict(meanpointprops4), positions=position4[:len(c)], widths = width[:len(c)])
                plt.xticks(poslab[:len(c)],c)
                #plt.legend([b1["boxes"][0], b2["boxes"][0], b3["boxes"][0]], Legend, loc='upper left',ncol=3)
                #plt.legend([b1["boxes"][0], b2["boxes"][0], b3["boxes"][0]], Legend, loc='upper left')
                
                # naming the x axis 
                plt.xlabel('Checkpoint Time (in seconds)') 
                # naming the y axis 
                plt.ylabel('Ratio') 
                
                #plt.ylim([1,1.9])
                # giving a title to my graph 
                plt.title(typeg) 
                  
                # show a legend on the plot 
                plt.savefig("../../../../results/plots/"+typeg+"/"+typeg+"check"+ident+".jpg")
                plt.clf()
                plt.close()
                cbase=ccbase


                
                PP1=[[] for i in range(len(u))]
                PP2=[[] for i in range(len(u))]
                PP3=[[] for i in range(len(u))]
                PP4=[[] for i in range(len(u))]
                for pp in range(len(u)):
                        ubase=u[pp]
                        ubase=(str) ((int)((float) (ubase)*100))
                        for fila in glob.glob(l[0]+"p"+pbase+"c"+cbase+"u"+ubase+"n"+nbase+"*"):
                                f= open(os.getcwd()+"/"+fila,"r")
                                Lines=f.readlines()
                                for j in range(len(Lines)):
                                        PP1[pp].append((float) (Lines[j][:-1]))

                        for fila in glob.glob(l[1]+"p"+pbase+"c"+cbase+"u"+ubase+"n"+nbase+"*"):
                                f= open(os.getcwd()+"/"+fila,"r")
                                Lines=f.readlines()
                                for j in range(len(Lines)):
                                        PP2[pp].append((float) (Lines[j][:-1]))


                        for fila in glob.glob(l[2]+"p"+pbase+"c"+cbase+"u"+ubase+"n"+nbase+"*"):
                                f= open(os.getcwd()+"/"+fila,"r")
                                Lines=f.readlines()
                                for j in range(len(Lines)):
                                        PP3[pp].append((float) (Lines[j][:-1]))
                                        
                                        
                        for fila in glob.glob(l[3]+"p"+pbase+"c"+cbase+"u"+ubase+"n"+nbase+"*"):
                                f= open(os.getcwd()+"/"+fila,"r")
                                Lines=f.readlines()
                                for j in range(len(Lines)):
                                    PP4[pp].append((float) (Lines[j][:-1]))
                                    
                        PP1[pp].sort()
                        y=len(PP1[pp])//10
                        comp=0
                        for x in range(y):
                                comp+=PP1[pp][x]-PP1[pp][y]
                                PP1[pp][x]=PP1[pp][y]
                        for x in range(len(PP1[pp])-y,len(PP1[pp])):
                                comp+=PP1[pp][x]-PP1[pp][len(PP1[pp])-y]
                                PP1[pp][x]=PP1[pp][len(PP1[pp])-y]
                        PP1[pp][len(PP1[pp])-1]+=comp+100
                        PP1[pp][0]-=100

                        
                        PP2[pp].sort()
                        y=len(PP2[pp])//10
                        comp=0
                        for x in range(y):
                                comp+=PP2[pp][x]-PP2[pp][y]
                                PP2[pp][x]=PP2[pp][y]
                        for x in range(len(PP2[pp])-y,len(PP2[pp])):
                                comp+=PP2[pp][x]-PP2[pp][len(PP2[pp])-y]
                                PP2[pp][x]=PP2[pp][len(PP2[pp])-y]
                        PP2[pp][len(PP2[pp])-1]+=comp+100
                        PP2[pp][0]-=100

                        
                        PP3[pp].sort()
                        y=len(PP3[pp])//10
                        comp=0
                        for x in range(y):
                                comp+=PP3[pp][x]-PP3[pp][y]
                                PP3[pp][x]=PP3[pp][y]
                        for x in range(len(PP3[pp])-y,len(PP3[pp])):
                                comp+=PP3[pp][x]-PP3[pp][len(PP3[pp])-y]
                                PP3[pp][x]=PP3[pp][len(PP3[pp])-y]
                        PP3[pp][len(PP3[pp])-1]+=comp+100
                        PP3[pp][0]-=100
                        
                        
                        PP4[pp].sort()
                        y=len(PP4[pp])//10
                        comp=0
                        for x in range(y):
                                comp+=PP4[pp][x]-PP4[pp][y]
                                PP4[pp][x]=PP4[pp][y]
                        for x in range(len(PP4[pp])-y,len(PP4[pp])):
                                comp+=PP4[pp][x]-PP4[pp][len(PP4[pp])-y]
                                PP4[pp][x]=PP4[pp][len(PP4[pp])-y]
        
                        PP4[pp][len(PP4[pp])-1]+=comp+100
                        PP4[pp][0]-=100
                        
                b1=plt.boxplot(PP1,showfliers=False,boxprops=dict(color=c1),capprops=dict(color=c1),whiskerprops=dict(color=c1),flierprops=dict(color=c1, markeredgecolor=c1),medianprops=dict(color=c4), showmeans=True, meanprops=dict(meanpointprops1), positions=position1[:len(u)], widths = width[:len(u)])
                b2=plt.boxplot(PP2,showfliers=False,boxprops=dict(color=c2),capprops=dict(color=c2),whiskerprops=dict(color=c2),flierprops=dict(color=c2, markeredgecolor=c2),medianprops=dict(color=c4), showmeans=True, meanprops=dict(meanpointprops2), positions=position2[:len(u)], widths = width[:len(u)])
                b3=plt.boxplot(PP3,showfliers=False,boxprops=dict(color=c3),capprops=dict(color=c3),whiskerprops=dict(color=c3),flierprops=dict(color=c3, markeredgecolor=c3),medianprops=dict(color=c4), showmeans=True, meanprops=dict(meanpointprops3), positions=position3[:len(u)], widths = width[:len(u)])
                b4=plt.boxplot(PP4,showfliers=False,boxprops=dict(color=c5),capprops=dict(color=c5),whiskerprops=dict(color=c5),flierprops=dict(color=c5, markeredgecolor=c5),medianprops=dict(color=c4), showmeans=True, meanprops=dict(meanpointprops4), positions=position4[:len(u)], widths = width[:len(u)])
                plt.xticks(poslab[:len(u)],u)

                #plt.legend([b1["boxes"][0], b2["boxes"][0], b3["boxes"][0]], Legend, loc='upper left')
                
                # naming the x axis 
                plt.xlabel('MTBF (in years)') 
                # naming the y axis 
                plt.ylabel('Ratio') 
                
                #plt.ylim([1,1.9])
                # giving a title to my graph 
                plt.title(typeg) 
                  
                # show a legend on the plot 
                plt.savefig("../../../../results/plots/"+typeg+"/"+typeg+"fail"+ident+".jpg")
                plt.clf()
                plt.close()
                ubase=uubase

                
                PP1=[[] for i in range(len(n))]
                PP2=[[] for i in range(len(n))]
                PP3=[[] for i in range(len(n))]
                PP4=[[] for i in range(len(n))]
                ubase=(str) ((int)((float) (ubase)*100))
                for pp in range(len(n)):
                        nbase=n[pp]
                        for fila in glob.glob(l[0]+"p"+pbase+"c"+cbase+"u"+ubase+"n"+nbase+"*"):
                                f= open(os.getcwd()+"/"+fila,"r")
                                Lines=f.readlines()
                                for j in range(len(Lines)):
                                        PP1[pp].append((float) (Lines[j][:-1]))

                        for fila in glob.glob(l[1]+"p"+pbase+"c"+cbase+"u"+ubase+"n"+nbase+"*"):
                                f= open(os.getcwd()+"/"+fila,"r")
                                Lines=f.readlines()
                                for j in range(len(Lines)):
                                        PP2[pp].append((float) (Lines[j][:-1]))


                        for fila in glob.glob(l[2]+"p"+pbase+"c"+cbase+"u"+ubase+"n"+nbase+"*"):
                                f= open(os.getcwd()+"/"+fila,"r")
                                Lines=f.readlines()
                                for j in range(len(Lines)):
                                        PP3[pp].append((float) (Lines[j][:-1]))
                                        
                                        
                        for fila in glob.glob(l[3]+"p"+pbase+"c"+cbase+"u"+ubase+"n"+nbase+"*"):
                                f= open(os.getcwd()+"/"+fila,"r")
                                Lines=f.readlines()
                                for j in range(len(Lines)):
                                    PP4[pp].append((float) (Lines[j][:-1]))
                                    
                        PP1[pp].sort()
                        y=len(PP1[pp])//10
                        comp=0
                        for x in range(y):
                                comp+=PP1[pp][x]-PP1[pp][y]
                                PP1[pp][x]=PP1[pp][y]
                        for x in range(len(PP1[pp])-y,len(PP1[pp])):
                                comp+=PP1[pp][x]-PP1[pp][len(PP1[pp])-y]
                                PP1[pp][x]=PP1[pp][len(PP1[pp])-y]
                        PP1[pp][len(PP1[pp])-1]+=comp+100
                        PP1[pp][0]-=100

                        
                        PP2[pp].sort()
                        y=len(PP2[pp])//10
                        comp=0
                        for x in range(y):
                                comp+=PP2[pp][x]-PP2[pp][y]
                                PP2[pp][x]=PP2[pp][y]
                        for x in range(len(PP2[pp])-y,len(PP2[pp])):
                                comp+=PP2[pp][x]-PP2[pp][len(PP2[pp])-y]
                                PP2[pp][x]=PP2[pp][len(PP2[pp])-y]
                        PP2[pp][len(PP2[pp])-1]+=comp+100
                        PP2[pp][0]-=100

                        
                        PP3[pp].sort()
                        y=len(PP3[pp])//10
                        comp=0
                        for x in range(y):
                                comp+=PP3[pp][x]-PP3[pp][y]
                                PP3[pp][x]=PP3[pp][y]
                        for x in range(len(PP3[pp])-y,len(PP3[pp])):
                                comp+=PP3[pp][x]-PP3[pp][len(PP3[pp])-y]
                                PP3[pp][x]=PP3[pp][len(PP3[pp])-y]
                        PP3[pp][len(PP3[pp])-1]+=comp+100
                        PP3[pp][0]-=100
                        
                        
                        PP4[pp].sort()
                        y=len(PP4[pp])//10
                        comp=0
                        for x in range(y):
                                comp+=PP4[pp][x]-PP4[pp][y]
                                PP4[pp][x]=PP4[pp][y]
                        for x in range(len(PP4[pp])-y,len(PP4[pp])):
                                comp+=PP4[pp][x]-PP4[pp][len(PP4[pp])-y]
                                PP4[pp][x]=PP4[pp][len(PP4[pp])-y]
        
                        PP4[pp][len(PP4[pp])-1]+=comp+100
                        PP4[pp][0]-=100
                        
                b1=plt.boxplot(PP1,showfliers=False,boxprops=dict(color=c1),capprops=dict(color=c1),whiskerprops=dict(color=c1),flierprops=dict(color=c1, markeredgecolor=c1),medianprops=dict(color=c4), showmeans=True, meanprops=dict(meanpointprops1), positions=position1[:len(n)], widths = width[:len(n)])
                b2=plt.boxplot(PP2,showfliers=False,boxprops=dict(color=c2),capprops=dict(color=c2),whiskerprops=dict(color=c2),flierprops=dict(color=c2, markeredgecolor=c2),medianprops=dict(color=c4), showmeans=True, meanprops=dict(meanpointprops2), positions=position2[:len(n)], widths = width[:len(n)])
                b3=plt.boxplot(PP3,showfliers=False,boxprops=dict(color=c3),capprops=dict(color=c3),whiskerprops=dict(color=c3),flierprops=dict(color=c3, markeredgecolor=c3),medianprops=dict(color=c4), showmeans=True, meanprops=dict(meanpointprops3), positions=position3[:len(n)], widths = width[:len(n)])
                b4=plt.boxplot(PP4,showfliers=False,boxprops=dict(color=c5),capprops=dict(color=c5),whiskerprops=dict(color=c5),flierprops=dict(color=c5, markeredgecolor=c5),medianprops=dict(color=c4), showmeans=True, meanprops=dict(meanpointprops4), positions=position4[:len(n)], widths = width[:len(n)])
                plt.xticks(poslab[:len(n)],n)

                
                #plt.legend([b1["boxes"][0], b2["boxes"][0], b3["boxes"][0]], Legend, loc='upper left',ncol=3)
                
                # naming the x axis 
                plt.xlabel('Number of Tasks') 
                # naming the y axis 
                plt.ylabel('Ratio') 
                
                #plt.ylim([1,1.9])
                # giving a title to my graph 
                plt.title(typeg) 
                  
                # show a legend on the plot 
                plt.savefig("../../../../results/plots/"+typeg+"/"+typeg+"n"+ident+".jpg")
                plt.clf()
                plt.close()
                nbase=nnbase


plotplot(sys.argv[1])
    
# function to show the plot 
