import ROOT as r
import sys, os
sys.path.append("/Users/amizukam/DVJets/atlasstyle")
from AtlasStyle import *
from AtlasLabel import *
from utils import *

r.gROOT.SetBatch()
SetAtlasStyle()
label = "Internal"

plotType = "massTemplate"
directory = "pdfs/" + plotType
if (not os.path.isdir(directory)):
    os.makedirs(directory)

mvFile = r.TFile("rootfiles/sigAndMass_data.root", "READ")
axFile = r.TFile("/Users/amizukam/DVJets/accidentalCrossings/template/massTemplates.f.14122020.4trkcomb.root", "READ")

c = r.TCanvas("c", "c", 800, 700)
c.cd()

mvTemp = mvFile.Get("mergedMass_Ntrk4")
axTemp = axFile.Get("h_comb").Rebin(2)

bin50 = mvTemp.FindBin(50.)-1
mvTemp.GetXaxis().SetRange(1, bin50)

mvTemp.SetLineColor(r.kBlack)
axTemp.SetLineColor(r.kRed)

leg = r.TLegend(0.54, 0.55, 0.85, 0.78)
decorateLeg(leg)
leg.AddEntry(mvTemp, "Merged Vertices", "l")
leg.AddEntry(axTemp, "Accidental Crossings", "l")

mvTemp.DrawNormalized("hist")
axTemp.DrawNormalized("hist same")

sampleLabel = r.TLatex()
sampleLabel.SetNDC()
sampleLabel.SetTextFont(42)
sampleLabel.SetTextAlign(13)
sampleLabel.SetTextSize(0.03)
sampleLabel.DrawLatex(0.56, 0.83, getNtrkLabel("Ntrk4"))
leg.Draw()
ATLASLabel(0.20, 0.955, label)
c.Print("{}/{}.pdf".format(directory, "mv_vs_ax_massTemplate_Ntrk4"))


c.SetLogy(1)
mvTemp.DrawNormalized("hist")
axTemp.DrawNormalized("hist same")

sampleLabel = r.TLatex()
sampleLabel.SetNDC()
sampleLabel.SetTextFont(42)
sampleLabel.SetTextAlign(13)
sampleLabel.SetTextSize(0.03)
sampleLabel.DrawLatex(0.56, 0.83, getNtrkLabel("Ntrk4"))
leg.Draw()
ATLASLabel(0.20, 0.955, label)
c.Print("{}/{}.pdf".format(directory, "mv_vs_ax_massTemplate_Ntrk4_logy"))
