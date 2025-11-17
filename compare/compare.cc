#include <TH2F.h>
#include "xjjrootuti.h"
#include "config.h"
#include "getdata.h"

int macro(std::string inputconfig) {
  auto conf = xjjc::config(inputconfig);
  auto inputs = xjjc::str_divide_trim(conf.get("INPUT"), ",");
  auto outputname = conf.has("OUTPUT") ? conf.get("OUTPUT") : "compare" ;

  std::vector<std::string> ccs = { "azure", "red" };
  if (inputs.size() > ccs.size()) return 2;
  std::vector<getdata*> lists;

  float x = 0.18, y = 0.80;
  auto leg = new TLegend(x, y-inputs.size()*0.048, x+0.15, y);
  xjjroot::setleg(leg, 0.038);
  for (auto ii : inputs) {
    auto i = lists.size();
    auto gd = new getdata(ii, xjjroot::mycolor_satmiddle[ccs[i]]);
    lists.push_back(gd);
    leg->AddEntry(gd->g(), gd->tleg().c_str(), "p");
  }

  float maxy = conf.has("MAXRATE") ? conf.get<float>("MAXRATE") : 70.;
  auto hempty = new TH2F("hempty", ";Instantaneous luminosity [10^{33} cm^{-2} s^{-1}]; Rate [kHz]", 10, 0, 6.5e-6, 10, 0, maxy);
  xjjroot::sethempty(hempty, 0, -0.2);
  xjjroot::setgstyle(1);
  xjjroot::adjustmargin(1, 2.5, 1, 0.7);
  if (maxy > 100)
    hempty->GetYaxis()->SetMaxDigits(2);
  
  auto c = new TCanvas("c", "", 600, 600);
  hempty->Draw("axis");
  for (const auto& l : lists)
    l->draw();
  leg->Draw();
  xjjroot::drawtex(x+0.01, y+0.02, conf.get("TAG_2").c_str(), 0.038, 11, 62);
  xjjroot::drawCMS(xjjroot::CMS::internal, conf.get("TAG_1"));
  std::cout<<std::endl;
  xjjroot::saveas(c, "../figs/" + outputname + ".pdf", "");

  return 0;
}

int main(int argc, char* argv[]) {
  if (argc == 2) {
    return macro(argv[1]);
  }
  return 1;
}
