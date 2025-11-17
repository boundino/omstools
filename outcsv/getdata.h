#include <TGraph.h>
#include <TH2F.h>
#include <fstream>
#include <vector>
#include "xjjrootuti.h"

class getdata {
public:
  getdata(std::string inputname, Color_t cc = kBlack);
  // void draw() { gr->Draw("psame"); gr2->Draw("psame"); }
  void draw() { gr->Draw("psame"); } 
  std::string tag() const { return tag_; }
  std::string tleg() const { return tleg_; }
  void setcolor(Color_t cc);
  TGraph* g() { return gr2; }
private:
  TGraph *gr, *gr2;
  std::string tag_, tleg_, filename_;
  void print();
};

getdata::getdata(std::string inputname, Color_t cc) {
  auto parts = xjjc::str_divide_trim(inputname, ":");
  filename_ = parts[0];
  tag_ = xjjc::str_erasestar(xjjc::str_erasestar(filename_, "*/"), ".*");
  tleg_ = parts.size() > 1 ? parts[1] : tag_;

  std::cout<<std::endl<<inputname<<std::endl;
  print();
  
  std::ifstream filein(filename_.c_str());
  std::vector<float> xx, yy;
  for(std::string line; std::getline(filein, line);) {
    line = xjjc::str_trim( xjjc::str_erasestar(line, "#*") );
    auto cells = xjjc::str_divide_trim(line, ",");
    // std::cout<<cells.size()<<std::endl;
    if (cells.size() != 11) continue;
    xx.push_back(atof(cells[4].c_str()));
    yy.push_back(atof(cells[9].c_str()) / 1.e+3);
  }
  gr = new TGraph(xx.size(), xx.data(), yy.data());
  gr->SetName(Form("gr_%s", inputname.c_str()));
  gr2 = (TGraph*)gr->Clone(Form("gr2_%s", inputname.c_str()));
  setcolor(cc);
}

void getdata::setcolor(Color_t cc) {
  xjjroot::setmarkerstyle(gr, cc, 20, 0.9, 0.3);
  // xjjroot::setmarkerstyle(gr2, cc, 24, 0.9, 1);
  xjjroot::setmarkerstyle(gr2, cc, 20, 0.9, 1);
}

void getdata::print() {
  std::cout<<"   filename: "<<filename_<<std::endl;
  std::cout<<"   tag: "<<tag_<<std::endl;
  std::cout<<"   tleg: "<<tleg_<<std::endl;
}
