#include <TGraph.h>
#include <TH2F.h>
#include <fstream>
#include <vector>
#include "xjjrootuti.h"

class getdata {
public:
  getdata(std::string inputname, Color_t cc=kBlack);
  void draw() { gr->Draw("psame"); gr2->Draw("psame"); }
  void setcolor(Color_t cc);
  TGraph* g() { return gr2; }
private:
  TGraph *gr, *gr2;
};

getdata::getdata(std::string inputname, Color_t cc) {
  std::ifstream filein(inputname.c_str());
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
  xjjroot::setmarkerstyle(gr, cc, 20, 0.9, 0.2);
  xjjroot::setmarkerstyle(gr2, cc, 24, 0.9, 1);
}

int macro(std::string inputnames) {
  auto inputs = xjjc::str_divide(inputnames, ",");
  std::vector<std::string> ccs = {"azure", "red"},
    legts = {"HF only", "HF + ZDC"};
  std::vector<getdata*> lists;

  float x = 0.2, y = 0.77;
  auto leg = new TLegend(x, y-2*0.048, x+0.15, y);
  xjjroot::setleg(leg, 0.04);
  for (auto ii : inputs) {
    // auto isplit = xjjc::str_divide_trim(ii, ":");
    auto i = lists.size();
    auto gd = new getdata(ii, xjjroot::mycolor_satmiddle[ccs[i]]);
    lists.push_back(gd);
    leg->AddEntry(gd->g(), legts[i].c_str(), "p");
  }
  
  auto hempty = new TH2F("hempty", ";Instantaneous luminosity [10^{33} cm^{-2} s^{-1}]; Rate [kHz]", 10, 0, 6.5e-6, 10, 0, 70);
  xjjroot::sethempty(hempty, 0, -0.2);
  xjjroot::setgstyle(1);
  xjjroot::adjustmargin(1, 2., 1, 0.7);
  auto c = new TCanvas("c", "", 700, 500);
  hempty->Draw("axis");
  for (const auto& l : lists)
    l->draw();
  leg->Draw();
  xjjroot::drawtex(x+0.01, y+0.02, "MinimumBias trigger", 0.04, 11, 62);
  xjjroot::drawCMS(xjjroot::CMS::pre, "(2024 PbPb 5.36 TeV)");
  xjjroot::saveas(c, "../figs/compare.pdf", "");

  return 0;
}

int main(int argc, char* argv[]) {
  if (argc == 2) {
    return macro(argv[1]);
  }
  return 1;
}
