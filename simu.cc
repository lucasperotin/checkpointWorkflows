#include <iostream>
#include <iomanip>
#include <functional>
#include <vector>
#include <math.h>
#include <queue>
#include <time.h>
#include <sys/time.h>
#include <utility>
#include <fstream>
#include <string>
#include <limits>
#include <stdlib.h>
#include <ctime>
#include <fstream>
#include <algorithm>
#include <array>

#include <omp.h>

#define DEBUG(X) std::cerr << X << "\n";
using namespace std;

std::vector<double> PPREC;
double maxprio;

template<typename T> void print_queue(T& q)
{
    while (!q.empty())
    {
        std::string s = q.top().getName();
        std::cout << s << " ";
        q.pop();
    }
    std::cout << "\n";
}

struct taskOptions
{
    int rooftopLimit; //Limit for rooftop model
    double amdhalSeq; //Sequential fraction of the job for Amdhal model
    double comComm; //Communication overhead for communication model
};

class Task
{
public:
    Task(std::string n, std::vector<long> p, std::function<double(std::vector<double>,std::vector<double>,std::vector<long>)> s, std::vector<double> ss, std::vector<double> as, int i, int o, int par) : name(n), speedup(s), np(p), si(ss), ai(as), index(i), ord(o), para(par) {}
    void setName(std::string s)
    {
        name = s;
    }
    std::string getName() const
    {
        return name;
    }
    void setOrd(int order)
    {
        ord=order;
    }
    int getOrd()
    {
        return ord;
    }
    void setInd(int inda)
    {
        ind=inda;
    }
    int getInd()
    {
        return index;
    }
    double time() const;
    double getPriority()
    {
        return priority;
    }
    void setPriority(double p)
    {
        priority = p;
    }
    std::vector<long> getProcs() const
    {
        return np;
    }
    void setProcs(std::vector<long> n)
    {
        np=n;
    }
    std::vector<long> getPrec() const
    {
        return preclist;
    }
    void setPrec(std::vector<long> n)
    {
        preclist=n;
    }
    std::vector<long> getPrecinv() const
    {
        return preclistinv;
    }
    void setPrecinv(std::vector<long> n)
    {
        preclistinv=n;
    }
    std::vector<double> getSi() const
    {
        return si;
    }
    void setSi(std::vector<double> n)
    {
        si=n;
    }
    long getBef() const
    {
        return nbbef;
    }
    void setBef(long n)
    {
        nbbef=n;
    }
    int getPara() const
    {
        return para;
    }
    void setPara(int par)
    {
        para=par;
    }
    std::vector<double> getAi() const
    {
        return ai;
    }
    void setRealTime(double t)
    {
        realtime=t;
    }
    double getRealTime() const
    {
        return realtime;
    }
    void setAi(std::vector<double> n)
    {
        ai=n;
    }

    int getIndex() const
    {
        return index;
    }

private:
    std::string name;
    std::vector<long> np;
    std::vector<long> preclist;
    std::vector<long> preclistinv;
    std::vector<double> si;
    std::vector<double> ai;
    std::function<double(std::vector<double>,std::vector<double>,std::vector<long>)> speedup;
    long nbbef;
    int ord;
    int para;
    double priority;
    double realtime;
    int index;
    int ind;
    taskOptions options;
};

double Task::time() const
{
    return speedup(si,ai,np);
}

struct Result
{
    double exec_time;
    std::vector<Task> tasks;
    std::vector<int> ordering;
};


void printResults(Result r)
{
    std::cout << "Execution time: " << r.exec_time << " seconds.\n";
}

void printResultsSHORT(Result r,std::vector<long> p, std::string outfile)
{

    std::ofstream myfile;
    myfile.open(outfile,std::ofstream::app);
    myfile.close();
}

class Event
{
public:
    Event(double t, bool tp, Task rt) : time(t), related_task(rt), type(tp) {}
    bool type; //false = start, true = end
    double time;
    Task related_task;
};
auto cmpEvent = [](Event left, Event right)
{
    return left.time > right.time;
};

void printEvent(Event e)
{
    std::cerr << e.related_task.getName() << " " << e.time << " " << e.type << "\n";
}
void printEventQueue(std::priority_queue<Event,std::vector<Event>,decltype(cmpEvent)> eventQueue)
{
    return;
    std::priority_queue<Event,std::vector<Event>,decltype(cmpEvent)> tmpEventQueue(cmpEvent);
    while (!eventQueue.empty())
    {
        Event e = eventQueue.top();
        eventQueue.pop();
        printEvent(e);
        tmpEventQueue.push(e);
    }
    while (!tmpEventQueue.empty())
    {
        Event e = tmpEventQueue.top();
        tmpEventQueue.pop();
        eventQueue.push(e);
    }

}

class Simulator
{
public:
    Simulator(int s, double l, double v) : seed(s), lambda(l), verif_time(v) {}
    void init() {  }
    bool fail(Task t);
    double getLambda() const
    {
        return lambda;
    }
    double getVerif() const
    {
        return verif_time;
    }
    void setSeed(double s)
    {
        seed=s;
    }
    void setLambda(double l)
    {
        lambda = l;
    }
    void setVerif(double v)
    {
        verif_time = v;
    }
    std::function<double(Task)> priority_fun;
    bool batch()
    {
        return batchVar>0;
    }
    bool naive()
    {
        return naiveVar>0;
    }
    bool shelves()
    {
        return shelfVar>0;
    }
    void setBatch(int b)
    {
        batchVar=b;
    }
    void setNaive(int b)
    {
        naiveVar=b;
    }
    void setShelves(int b)
    {
        shelfVar=b;
    }
private:
    double seed;
    double lambda;
    double verif_time;
    int batchVar, naiveVar, shelfVar;
};

bool compareTask(Task i1, Task i2)
{
    return (i1.getPriority() > i2.getPriority());
}

Result simulate(Simulator& s, std::vector<Task>& jobs, std::vector<long> nbProcs, int d, bool free, Result w)
{
    double cTime = 0;
    maxprio=0;
    s.init();

    PPREC.clear();
    for (unsigned i=0; i<jobs.size(); i++)
    {
        PPREC.push_back(jobs[i].getBef());
    }
    Result r;
    r.ordering= {};
    //Init the priority queue of jobs
    if(free)
    {
        for (unsigned i=0; i<jobs.size(); i++)
        {
            jobs[i].setPriority(s.priority_fun(jobs[i]));
            if(maxprio<s.priority_fun(jobs[i])+1.0)
            {
                maxprio=s.priority_fun(jobs[i])+1.0;
            }
        }
    }
    else
    {
        for (unsigned i=0; i<w.ordering.size(); i++)
        {
            jobs[w.ordering[i]].setPriority(w.ordering.size()-i);
        }
        maxprio=(double) (jobs.size())+1.0;

    }

    auto cmpTask = [](Task left, Task right)
    {
        return left.getPriority() < right.getPriority();
    };
    auto cmpTask2 = [](Task left, Task right)
    {
        return left.getOrd() < right.getOrd();
    };

    std::priority_queue<Task,std::vector<Task>,decltype(cmpTask)> jobQueue(cmpTask);
    std::priority_queue<Task,std::vector<Task>,decltype(cmpTask)> tmpJobQueue(cmpTask);

    for (int i=0; i<jobs.size(); i++)
    {
        if (PPREC[i]==0)
        {
            jobQueue.push(jobs[i]);
        }
    }
    int sched=0;

    std::vector<long> pAvail=nbProcs;
    std::vector<long> tmpProcs;

    bool Completed[jobs.size()];

    for (int k=0; k<jobs.size(); k++)
    {
        Completed[k]=false;
    }

    //Create a priority queue for the events (ends of tasks)
    std::priority_queue<Event,std::vector<Event>,decltype(cmpEvent)> eventQueue(cmpEvent);
    std::priority_queue<Event,std::vector<Event>,decltype(cmpEvent)> tmpEventQueue(cmpEvent);

begin:
    //Schedule the first tasks

    int cpt = 0;

    std::vector<long> Prec;
    std::vector<std::tuple<double,double,int>> delay;

    int order=0;
    int xxx=0;
    int ind;
    bool cont=true;
    bool printo=true;
    //r.ordering={};
    while (!jobQueue.empty() and cont)
    {
        Task first = jobQueue.top();
        jobQueue.pop();
        tmpProcs=first.getProcs();
        bool isPossible=true;
        printo=false;
        for (int k=0; k<tmpProcs.size(); k++)
        {
            isPossible=isPossible and pAvail[k]>=tmpProcs[k];
        }
        if (not free)
        {
            isPossible=isPossible and (jobs.size()-first.getPriority()==xxx);
        }
        if (isPossible)
        {
            xxx++;
            tmpProcs=first.getProcs();
            for (int k=0; k<tmpProcs.size(); k++)
            {
                pAvail[k]-=tmpProcs[k];
            }
            ind=first.getIndex();
            delay.push_back(std::make_tuple(cTime,cTime+first.getRealTime(),ind));
            r.ordering.push_back(ind);
            Event e(cTime+first.getRealTime()+s.getVerif(),true,first);
            eventQueue.push(e);
        }
        else
        {
            //otherwise needs to be rescheduled later
            tmpJobQueue.push(first);

            cont=free;
            if (pAvail[0]==0)
            {
                cont=false;
            }
        }
    }

    //Put the non-scheduled jobs back in the queue
    while (!tmpJobQueue.empty())
    {
        jobQueue.push(tmpJobQueue.top());
        tmpJobQueue.pop();
    }
    //MAIN LOOP
    while (!eventQueue.empty())
    {
        cont=true;
        Event e = eventQueue.top();
        eventQueue.pop();
        cTime = e.time;

        if (e.type)
        {
            //It is an ending event so we need to schedule new tasks

            r.tasks.push_back(e.related_task);
            Completed[e.related_task.getIndex()]=true;
            tmpProcs=e.related_task.getProcs();
            for (int k=0; k<tmpProcs.size(); k++)
            {
                pAvail[k]+=tmpProcs[k];
            }
            Prec=e.related_task.getPrecinv();
            for (int k=0; k<Prec.size(); k++)
            {
                PPREC[Prec[k]]--;
                if (PPREC[Prec[k]]==0)
                {
                    jobQueue.push(jobs[Prec[k]]);
                }
            }

            int cpt = 0;

            //Other jobs to schedule (backfilling)
            while (!jobQueue.empty() and cont)
            {
                Task first = jobQueue.top();
                jobQueue.pop();
                tmpProcs=first.getProcs();
                Prec=first.getPrec();
                bool isPossible=true;
                for (int k=0; k<tmpProcs.size(); k++)
                {
                    isPossible=isPossible and pAvail[k]>=tmpProcs[k];
                }

                if (not free)
                {
                    isPossible=isPossible and (jobs.size()-first.getPriority()==xxx);
                }

                if (isPossible) //check with the existing reservations
                {
                    xxx++;
                    ind=first.getIndex();
                    r.ordering.push_back(ind);
                    delay.push_back(std::make_tuple(cTime,cTime+first.getRealTime(),ind));
                    for (int k=0; k<tmpProcs.size(); k++)
                    {
                        pAvail[k]-=tmpProcs[k];
                    }
                    Event e(cTime+first.getRealTime()+s.getVerif(),true,first);
                    eventQueue.push(e);
                }
                else   //otherwise needs to be rescheduled later
                {

                    tmpJobQueue.push(first);
                    cont=free;
                    if (pAvail[0]==0)
                    {
                        cont=false;
                    }
                }
            }
            //Put the non-scheduled jobs back in the queue
            while (!tmpJobQueue.empty())
            {
                jobQueue.push(tmpJobQueue.top());
                tmpJobQueue.pop();
            }
        }
    }


    r.exec_time = cTime;
    std::sort(delay.begin(),delay.end());

    if (free)
    {
        int i,j,n;
        n=delay.size();
        i=0;
        j=0;
        int values[jobs.size()];
        for(int i=0; i<n; i++)
        {
            values[i]=0;
        }
        i=0;
        double stoit,enoit;
        while(i<n)
        {
            stoit=std::get<0>(delay[i]);
            enoit=std::get<1>(delay[i]);
            j=i+1;
            values[std::get<2>(delay[i])]++;
            while(std::get<0>(delay[j])<enoit && j<n)
            {
                values[std::get<2>(delay[j])]++;
                values[std::get<2>(delay[i])]++;
                j++;
            }
            j=i;
            i++;
        }
        i=0;
        while(i<n)
        {
            if(values[i]>nbProcs[0])
            {
                values[i]=nbProcs[0];
            }
            jobs[i].setPara(values[i]);
            i++;
        }
    }
    return r;
}

double pTaskLength(Task t)
{
    return t.time();
}

double pTaskArea(Task t)
{

    int k;
    long tot=0;
    for (int k=0; k<t.getProcs().size(); k++)
    {
        tot+=t.getProcs()[k];
    }
    return tot*t.time();
}

double pTaskProcs(Task t)
{
    int k;
    long tot=0;
    for (int k=0; k<t.getProcs().size(); k++)
    {
        tot+=t.getProcs()[k];
    }
    return tot;
}

double pTaskLengthS(Task t)
{
    return -t.time();
}

double pTaskAreaS(Task t)
{

    int k;
    long tot=0;
    for (int k=0; k<t.getProcs().size(); k++)
    {
        tot-=t.getProcs()[k];
    }
    return -tot*t.time();
}

double pTaskProcsS(Task t)
{
    int k;
    long tot=0;
    for (int k=0; k<t.getProcs().size(); k++)
    {
        tot-=t.getProcs()[k];
    }
    return tot;
}

double pTaskRandom(Task t)
{
    return rand()/(double)RAND_MAX;
}

double amdSum(std::vector<double> si, std::vector<double> ai, std::vector<long> pi)
{
    double tot=si[0];
    long totprocs=0;
    for(int i=1; i<si.size(); i++)
    {
        tot+=si[i]/pi[i-1];
        totprocs+=pi[i-1];
    }
    tot=1/(tot*totprocs);
    return(tot);
}

double amdProd(std::vector<double> si,std::vector<double> ai, std::vector<long> pi)
{
    double tot=si[0];
    double prod=1;
    long totprocs=0;
    for(int i=0; i<ai.size(); i++)
    {
        prod*=pi[i];
        totprocs+=pi[i];
    }
    tot=1/((tot+(1-tot)/prod)*totprocs);
    return(tot);
}


double amdMax(std::vector<double> si, std::vector<double> ai, std::vector<long> pi)
{
    double tot=0;
    long totprocs=0;
    for(int i=1; i<si.size(); i++)
    {
        tot=std::max(tot,si[i]/pi[i-1]);
        totprocs+=pi[i-1];
    }
    tot+=si[0];
    return(1/(tot*totprocs));
}

double powSum(std::vector<double> si, std::vector<double> ai, std::vector<long> pi)
{
    double tot=0;
    long totprocs=0;
    for(int i=1; i<si.size(); i++)
    {
        tot=tot+si[i]/(std::pow(pi[i-1],ai[i-1]));
        totprocs+=pi[i-1];
    }
    tot=1/(tot*totprocs);
    return(tot);
}

double powProd(std::vector<double> si,std::vector<double> ai, std::vector<long> pi)
{
    double prod=1;
    long totprocs=0;
    for (int i=0; i<ai.size(); i++)
    {
        prod*=pow(pi[i],ai[i]);
        totprocs+=pi[i];
    }
    return (prod/totprocs);
}

double powMax(std::vector<double> si, std::vector<double> ai, std::vector<long> pi)
{
    double tot=0;
    long totprocs=0;
    for (int i=1; i<si.size(); i++)
    {
        tot=std::max(tot,si[i]/pow(pi[i-1],ai[i-1]));
        totprocs+=pi[i-1];
    }
    return (1/(tot*totprocs));
}

double rigid(std::vector<double> si, std::vector<double> ai,std::vector<long> pi)
{
    return(si[0]);
}

void assignProcRigid(std::vector<Task>& jobs,std::string filename)
{

    std::ofstream myfile;
    myfile.open(filename);
    int i;
    long n;
    long proc;
    std::vector<double> ai;
    n=jobs.size();
    for (i=0; i<n; i++)
    {
        ai=jobs[i].getAi();
        proc=(long) (ai[0]);
        myfile << jobs[i].getName() << " " << proc << "\n";
    }
    myfile.close();
}

int readInput(std::string filename, std::vector<Task> &v, int d, std::function<double(std::vector<double>,std::vector<double>,std::vector<long>)> speedup,long totproc)
{
    std::string name;
    int proc;
    std::vector<double> si;
    std::vector<double> ai;
    std::vector<long> pi;
    std::string speedupmod;
    pi= {};
    double s;
    double a;
    int k=0;
    int n;

    std::ifstream input(filename,std::ios::in);
    while (input >> name)
    {
        si= {};
        ai= {};
        input >> s;
        si.push_back(s);
        ai.push_back(1);


        v.push_back(Task(name,pi,speedup,si,ai,k,0,totproc));
        k=k+1;
    }
    input.close();

    return 1;
}



int readPrecs(std::string filename, std::vector<Task> &v, int d)
{
    std::vector<long> Precs[v.size()];
    std::vector<long> Precsinv[v.size()];
    int i;
    int j;
    long m=0;
    std::ifstream input(filename,std::ios::in);
    while (input >> i >> j)
    {
        Precs[j].push_back(i);
        Precsinv[i].push_back(j);
        m+=1;
    }

    for (int i=0; i<v.size(); i++)
    {
        v[i].setPrec(Precs[i]);
        v[i].setBef(Precs[i].size());
        v[i].setPrecinv(Precsinv[i]);

    }
    input.close();
    return m;
}

std::vector<double> getAlloc(std::vector<Task>& jobs, int d, std::string filename, double mu,double C, std::vector<long> num_procs)
{
    std::ifstream input(filename,std::ios::in);
    std::string name;
    std::vector<long> Procs;
    long tmpProcs;
    std::vector<double> LB;
    double area=0;
    double longestjob=0;
    int i,j;
    long totprocs=0;
    i=0;

    while (input >> name)
    {
        Procs= {};
        for (j=0; j<d; j++)
        {
            input >> tmpProcs;
            totprocs+=tmpProcs;
            Procs.push_back(tmpProcs);
        }
        jobs[i].setProcs(Procs);
        if (longestjob<jobs[i].time()+C)
        {
            longestjob=jobs[i].time()+C;
        }
        area+=(jobs[i].time()+C)*tmpProcs;
        i++;
    }
    totprocs/=i;
    LB.push_back(longestjob);
    LB.push_back(area/(double) (num_procs[0]));
    LB.push_back(num_procs[0]/totprocs);
    return(LB);
}


// Given x, compute W such that x = W exp(W)
// Taken from http://www.whim.org/nebula/math/lambertw.html
long double Lambert(long double x)
{
    long double wnew, wold;

    wold = -1;

    if (((x>=0)&&(x<=10)) || ((x<0)&&(x>=-1/exp(1))))
    {
        wnew = 0;
    }
    else
    {
        wnew = log(x) - log(log(x));
    }

    while(abs(wold-wnew)>0.000000001)
    {
        wold=wnew;
        wnew=(x*exp(-wold)+wold*wold)/(wold+1);
    }

    return wnew;
}


long double exp_optimal_period(long double W, long double checkpoint, long double recovery, long double downtime,
                               long double lambda)
{

//    cout << "appel a exp optimal period avec W = " << W << endl;
    long double w = Lambert(-exp(-(1+lambda*checkpoint)));
    long double Tcand = (w+1)/lambda;
    long double Topt;
    long double nopt;

    if (Tcand > W)
    {
        Topt = W;
        nopt=1;
    }
    else
    {
        long double Topttheory = Tcand;
        long double nopttheory=W/Topttheory;
        long double nval[2], expval[2];
        nval[0]=floor(nopttheory);
        nval[1]=ceil(nopttheory);


        for(int i=0; i<2; i++)
        {
            expval[i] = nval[i] * (exp(lambda*(W/nval[i]+checkpoint))-1) ;
        }
        if (expval[0]<expval[1])
        {
            nopt=nval[0];
        }
        else
        {
            nopt=nval[1];
        }
        Topt = W/nopt;
    }

    return nopt;
}

void assignCheckpoints(std::vector<Task>& jobs, double muche,double C,std::vector<double> LB,long num_procs,std::string checkpoint_strat,std::string filename, int parallelism)
{

    std::ofstream myfile;
    myfile.open(filename);
    int i;
    long n;
    long Nc;
    long proc;
    double timi;
    double W;
    double Psuc;
    double Q;

    double logq;
    double Cp;
    double Rp;
    double Dp;
    double realtimi;
    double lambda;
    double multi;
    std::vector<double> ai;
    //std::cout << "Time for checkpoints "<<filename <<" \n";
    n=jobs.size();
    bool strat[n];
    int nblong=0;
    for (i=0; i<n; i++)
    {
        timi=jobs[i].time();
        proc=jobs[i].getProcs()[0];
        Cp=C;
        Rp=Cp;
        Dp=0;
        W=sqrt(2*muche*C/proc);
        Nc=ceil(timi/W);
        if (checkpoint_strat=="yd")
        {
            myfile << jobs[i].getName() << " " << Nc << "\n";
        }
        else if(checkpoint_strat=="cm")
        {
            multi=log(jobs[i].getPara());
            if (multi<1)
            {
                multi=1;
            }
            Nc=ceil(timi/W*multi);
            myfile << jobs[i].getName() << " " << Nc << "\n";
        }
        else if (checkpoint_strat=="nyd"){
            Nc=exp_optimal_period(timi,Cp,Rp,Dp,1/muche);
            myfile << jobs[i].getName() << " " << Nc << "\n";
        }

    }
    myfile.close();
}

void FailureFreeTimes(std::vector<Task>& jobs,double C)
{
    int i, n;
    n=jobs.size();
    for (i=0; i<n; i++)
    {
        jobs[i].setRealTime(jobs[i].time());
    }

}


void getRealTimes(std::vector<Task>& jobs, double muche,double C, std::string filename)
{
    std::ifstream input(filename,std::ios::in);
    std::string name;
    long proc;
    long Nc;
    double Cr;
    long tmpProcs;
    double basetime;
    double realtime;
    double segsize;
    long segdone;
    double timedone;
    double nextfail;
    double R,D,a;
    int i,j;
    int n;
    struct timeval time;
    i=0;

    a=(double) (rand())/(double) (RAND_MAX);
    nextfail=-muche*log(a);
    while (input >> name)
    {
        if (jobs[i].getName()!=name)
        {
            std::cout << "Major issue " << jobs[i].getName() << " " << name  << "\n";
        }
        input >> Nc;
        proc=jobs[i].getProcs()[0];
        Cr=C;
        R=Cr;
        D=0;
        realtime=0;
        basetime=jobs[i].time()+Cr*Nc;
        segsize=basetime/Nc;
        j=0;
        while (basetime>0)
        {
            segdone=(floor) (nextfail/segsize);
            timedone=segdone*segsize;
            if (timedone>=basetime)
            {
                realtime+=basetime;
                nextfail-=basetime;
                basetime=0;
            }
            else
            {
                realtime+=nextfail+D+R;
                basetime-=timedone;

                a=(double) (rand())/(double) (RAND_MAX);
                nextfail=-muche*log(a)/proc;
            }
            j++;
        }
        jobs[i].setRealTime(realtime);
        i+=1;
    }
}

int main(int argc, char** argv)
{
    //std::cout<<"Itried at least\n";
    struct timeval time;
    int ok=0;
    int ok1=0;

    long m;
    double val = (time.tv_sec * 1000) + (time.tv_usec / 1000);
    Simulator s(val, 0,0);
    std::vector<Task> jobs;
    double muche;
    std::string priority;
    srand((int) time.tv_sec*1000 + (time.tv_usec / 1000));

    std::ifstream input(argv[1],std::ios::in);
    std::string filename;
    std::string alloc;
    std::string preclist;
    std::string rule;
    std::string checkfile;
    std::string outfile;
    std::string checkpoint_strat;
    std::string outfinal;
    std::string outmax;
    std::string folder;
    long d;
    long nb_iters;
    double rho;
    int C2;
    double C;
    double mu;
    //C=30;
    //int C2=30;
    while(input>>filename)
    {
        //std::cout<<"could get something\n";
        //std::cout<<filename<<'\n';
        input >> rule;
        d=1;
        std::vector<long> num_procs = {};
        long p;

        for (int k=0; k<d; k++)
        {
            input >> p;
            num_procs.push_back(p);
        }
        input >> priority;
        input >> nb_iters;
        input >> checkpoint_strat;
        input >> folder;
        std::cout<<folder << " ";
        std::cout<<filename<<"\n";
        input >> outfinal;
        input >> C2;
        C=C2;
        input >> muche;
        checkfile="files/checkpoints/"+folder+checkpoint_strat+std::to_string(num_procs[0])+std::to_string(C2)+filename;

        preclist="files/precedence_constraints/"+folder+filename;
        alloc="files/allocation/"+folder+checkpoint_strat+std::to_string(num_procs[0])+'c'+std::to_string(C2)+filename;
        outfile="files/detailed_results/"+folder+checkpoint_strat+'p'+std::to_string(num_procs[0])+'c'+std::to_string(C2)+'u'+std::to_string((int) (muche*100))+filename;
        muche=muche*31536000;
        filename="files/tasks_parameters/"+folder+filename;
        outmax="resultsmax/"+folder+outfinal;
        outfinal="results/"+folder+outfinal;
        remove(&outfile[0]);
        double maxivalue;
        if (rule=="amdSum")
        {
            ok = readInput(filename,jobs,d,amdSum,num_procs[0]);
        }
        else if (rule=="amdProd")
        {
            ok = readInput(filename,jobs,d,amdProd,num_procs[0]);
        }
        else if (rule=="amdMax")
        {
            ok = readInput(filename,jobs,d,amdMax,num_procs[0]);
        }
        else if (rule=="powSum")
        {
            ok = readInput(filename,jobs,d,powSum,num_procs[0]);
        }
        else if (rule=="powProd")
        {
            ok = readInput(filename,jobs,d,powProd,num_procs[0]);
        }
        else if (rule=="powMax")
        {
            ok = readInput(filename,jobs,d,powMax,num_procs[0]);
        }
        else if (rule=="rigid")
        {
            ok = readInput(filename,jobs,d,rigid,num_procs[0]);
        }
        else
        {
            std::cerr << "Unrecognized time rule: " << rule << ".\n";
            return -1;
        }


        if (priority == "length")
            s.priority_fun = pTaskLength;
        else if (priority == "procs")
            s.priority_fun = pTaskProcs;
        else if (priority == "area")
            s.priority_fun = pTaskArea;
        else if (priority == "rlength")
            s.priority_fun = pTaskLengthS;
        else if (priority == "rprocs")
            s.priority_fun = pTaskProcsS;
        else if (priority == "rarea")
            s.priority_fun = pTaskAreaS;
        else if (priority == "rand")
            s.priority_fun = pTaskRandom;
        else
        {
            std::cerr << "Unrecognized priority function: " << priority << ".\n";
            return -1;
        }
        double area;
        m=readPrecs(preclist,jobs,d);
        std::vector<long> tempprocs;
        std::vector<double> LB;
        double AV=0;
        double bound=0;
        std::vector<long> num_procs2 = {};
        num_procs2.push_back(INT32_MAX);
        double criticalpath;
        std::string beststratheur;
        if (ok)
        {

            double avg_time = 0;
            int nb_fail_tmp = 0;
            assignProcRigid(jobs,alloc);
            LB=getAlloc(jobs,d,alloc,mu,C,num_procs);
            //std::cout<<"\n"<<num_procs[0] << " " << LB[0] << " " << LB[1] << " " <<LB[2] <<"\n\n";
            if (LB[2]>jobs.size())
            {
                LB[2]=jobs.size();
            }
            std::cout<< " p:" << num_procs[0] << " c:"<<C2<< " u:" << muche<<"\n";
            if(checkpoint_strat=="sm")
            {
                if (LB[0]>LB[1])
                {
                    checkpoint_strat="cm";
                }
                else
                {
                    checkpoint_strat="yd";
                }
            }
            FailureFreeTimes(jobs,C);
            Result r;
            r=simulate(s,jobs,num_procs,d,true,r);
            bound=r.exec_time;
            if (checkpoint_strat=="cm")
            {
                for (int i=0; i<jobs.size(); i++)
                {
                    jobs[i].setPara(num_procs[0]);
                }
            }
            int maxipar=0;
            if(checkpoint_strat=="cmd")
            {
                for (int i=0; i<jobs.size(); i++)
                {
                    if (jobs[i].getPara()>maxipar)
                    {
                        maxipar=jobs[i].getPara();
                    }
                }
                checkpoint_strat="cm";
            }
            assignCheckpoints(jobs,muche,C,LB,num_procs[0],checkpoint_strat,checkfile,(int) (LB[2]));
            std::ofstream myfile2;
            maxivalue=0;
            myfile2.open(outfile,std::ofstream::app);
            for (int i=0; i<nb_iters; i++)
            {
                getRealTimes(jobs,muche,C,checkfile);
                r=simulate(s,jobs,num_procs,d,false,r);
                printResultsSHORT(r,num_procs,outfile);
                myfile2 << r.exec_time/bound<<"\n";

                if(r.exec_time/bound>maxivalue)
                {
                    maxivalue=r.exec_time/bound;
                }

                AV+=r.exec_time;
            }
            myfile2.close();

            AV/=nb_iters;

            std::ofstream myfile;
            myfile.open(outfinal,std::ofstream::app);
            myfile << AV/bound<<"\n";
            myfile.close();

            std::ofstream myfile3;
            myfile3.open(outmax,std::ofstream::app);
            myfile3 << maxivalue<<"\n";
            myfile3.close();
            jobs= {};
        }

    }
    return 0;
}
