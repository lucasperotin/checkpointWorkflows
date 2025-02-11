#include<iostream>
#include<vector>
#include<string>
#include <fstream>
#include <glob.h>
#include <map>
using std::vector;

using namespace std;


vector<string> globVector(const string& pattern){
  glob_t glob_result;
  glob(pattern.c_str(),GLOB_TILDE,NULL,&glob_result);
  vector<string> files;
  for(unsigned int i=0;i<glob_result.gl_pathc;++i){
    files.push_back(string(glob_result.gl_pathv[i]));
  }
  globfree(&glob_result);
  return files;
}


int main(int argc, char** argv){
  string word;
  string filenamein,filenameout;
  string filenametask,filenameprec;
  string basefolder;
  string path;
  bool swi;
  bool swichi;
  int i,j,k,l,x;
  double avlength;
  double totalength;
  string jobname;
  string joblength;
  string proc;


  string folder[9];
  folder[0]="BLAST/";
  folder[1]="BWAR/";
  folder[2]="Cycles/";
  folder[3]="Epigenomics/";
  folder[4]="Genome/";
  folder[5]="Montage/";
  folder[6]="Seismology/";
  folder[7]="SoyKBR/";
  folder[8]="SRAS/";

  //Parsing json into easier format put into transformed
  for (i=0;i<9;i++){
    vector<string> filesla = globVector("./workflowhub/files/"+folder[i]+"n*");
    avlength=0;
    for (j=0;j<filesla.size();j++){
      totalength=0;
      ifstream input(filesla[j],std::ios::in);
      filenameout="./workflowhub/transformed/"+filesla[j].substr(20,filesla[j].size()-8);
      ofstream output;
      output.open(filenameout,std::ofstream::out);
      while (input>> word){
	if (word=="\"jobs\":"){
	  break;
	}
      }
      swi=true;
      while(input>>word){
	if (word=="\"name\":"&&swi){
	  input>>word;
	  word=word.substr(1,word.size()-3);
	  output<<word<<" ";
	  swi=false;
	}
	if(word=="\"cores\":"){
	  swi=true;
	  input>>word;
	  output<<word<<"\n";
	}
	if(word=="\"runtime\":"){
	  input>>word;
	  word=word.substr(0,word.size()-1);
	  output << word << " ";
	  totalength+=stof(word); 
	}
	if(word=="\"children\":"){
	  input>>word;
	  swichi=true;
	  while (input>>word && swichi){
	    if (word[word.size()-1]!=','){
	      //cout << word<<"\n";
	      word=word.substr(1,word.size()-2);
	      if (word!="files\""){
		output<< word;
	      }
	      output<< " end ";
	      swichi=false;
	    }
	    else{
	      word=word.substr(1,word.size()-3);
	      cout<<word[-1];
	      output << word << " ";
	    }
	  }
	}
      }
      input.close();
      output.close();
    }
  }

  //From transformed folder, fill task_parameters and precedence_constraints
  for (i=0;i<9;i++){
    vector<string> filesla = globVector("./workflowhub/transformed/"+folder[i]+"n*");
    avlength=0;
    for (j=0;j<filesla.size();j++){
      totalength=0;
      ifstream input(filesla[j],std::ios::in);
      filenametask="./files/tasks_parameters/pegasus/"+filesla[j].substr(26,filesla[j].size()-26);
      filenameprec="./files/precedence_constraints/pegasus/"+filesla[j].substr(26,filesla[j].size()-26);
      ofstream outputtask;
      ofstream outputprec;
      outputtask.open(filenametask,std::ofstream::out);
      outputprec.open(filenameprec,std::ofstream::out);

      map<string, int> names;
      x=0;
      while(input>>jobname){
	//update dict
	outputtask << jobname << " rgd ";
	names[jobname]=x;
	input>>joblength;
	outputtask << joblength << " ";
	swichi=true;
	while(input>>word and swichi){
	  if (word=="end"){
	    swichi=false;
	  }
	}
	outputtask << word<<"\n";
	x++;
      }

      input.close();
	  
      ifstream input2(filesla[j],std::ios::in);
	  
      while(input2>>jobname){
	input2>>joblength;
	swichi=true;
	while(input2>>word and swichi){
	  if (word=="end"){
	    swichi=false;
	  }
	  else{
	    outputprec << names[jobname] << " " << names[word]<<"\n";
	  }
	}
      }
	  
      input2.close();
      outputtask.close();
      outputprec.close();
    }
  }
  return 0;
}
