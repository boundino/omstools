#include <TGraph.h>
#include <TH2F.h>
#include <fstream>
#include <vector>
#include "xjjrootuti.h"

class getdata {
public:
  getdata(std::string inputname, std::string run, std::string name, Color_t cc=kBlack);
  void drawandfit();
  void setcolor(Color_t cc);
  TGraph* g() { return m_gr; }
  float slope() { return m_f->GetParameter(1); }
  std::string getname() { return m_name; }
private:
  TGraph *m_gr;
  TF1 *m_f;
  std::string m_name;
};

getdata::getdata(std::string inputname, std::string run, std::string name, Color_t cc) : m_name(name) {
  std::ifstream filein(inputname.c_str());
  std::vector<float> xx, yy;
  int trun = 0;
  float rate_min = 1.e10, rate_max = 0;
  for(std::string line; std::getline(filein, line);) {
    line = xjjc::str_trim( xjjc::str_erasestar(line, "#*") );
    auto cells = xjjc::str_divide_trim(line, ",");
    const auto ncol = cells.size();
    if (ncol == 2) {
      if (cells[0] == run) {
        trun = atoi(run.c_str());
        std::cout<<trun<<" starts."<<std::endl;
        continue;
      } else {
        if (trun == 0) continue;
        else {
          std::cout<<trun<<" end."<<std::endl;
          trun = 0;
          break;
        } 
      }
    } else if (ncol == 11) {
      if (cells[1] != "True") continue;
      if (trun == 0) continue;
    } else {
      continue;
    }
    xx.push_back(atof(cells[4].c_str()));
    float rate = atof(cells[9].c_str()) / 1.e+3;
    yy.push_back(rate);
    rate_min = std::min(rate, rate_min);
    rate_max = std::max(rate, rate_max);
  }
  m_gr = new TGraph(xx.size(), xx.data(), yy.data());
  m_gr->SetName(Form("gr_%s", m_name.c_str()));
  m_f = new TF1(Form("f_%s", m_name.c_str()), "[0]+[1]*x", rate_min, rate_max);
  setcolor(cc);
}

void getdata::setcolor(Color_t cc) {
  xjjroot::setmarkerstyle(m_gr, cc, 20, 0.9, 0.2);
  xjjroot::setlinestyle(m_f, cc, 2, 2);
}

void getdata::drawandfit() {
  m_gr->Draw("psame");
  m_gr->Fit(m_f);
  // m_f->Draw("lsame");
}


int macro(std::string inputname) {
  std::vector<std::string> ccs = {"azure", "red"},
    runs = {"394153", "394270"},
    legts = {"OO", "NeNe"};
  std::vector<getdata*> gds(ccs.size(), 0);

  for (int i=0; i<ccs.size(); i++) {
    gds[i] = new getdata(inputname, runs[i], runs[i], xjjroot::mycolor_satmiddle[ccs[i]]);
  }

  auto hempty = new TH2F("hempty", ";Instantaneous luminosity; Rate [kHz]", 10, 0, 8e-5, 10, 0, 90);
  xjjroot::sethempty(hempty, 0, -0.2);
  xjjroot::setgstyle(1);
  xjjroot::adjustmargin(1, 2., 1, 0.7);
  auto c = new TCanvas("c", "", 600, 500);
  hempty->Draw("axis");
  for (const auto& g : gds)
    g->drawandfit();
  float x = 0.2, y = 0.77;
  auto leg = new TLegend(x, y-2*0.048, x+0.3, y);
  xjjroot::setleg(leg, 0.04);
  for (int i=0; i<ccs.size(); i++) {
    leg->AddEntry(gds[i]->g(), Form("%s (slope %.2f)", legts[i].c_str(), gds[i]->slope()), "p");
  }
  leg->Draw();
  xjjroot::drawtex(x+0.01, y+0.02, "L1_MinimumBiasHF1_AND_BptxAND", 0.04, 11, 62);
  xjjroot::drawCMS(xjjroot::CMS::preliminary, "(2025 5.36 TeV)");
  xjjroot::saveas(c, "../figs/fit.pdf", "");

  return 0;
}

int main(int argc, char* argv[]) {
  if (argc == 2) {
    return macro(argv[1]);
  }
  return 1;
}
