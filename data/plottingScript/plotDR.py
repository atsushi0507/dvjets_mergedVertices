import ROOT as r
import sys, os
sys.path.append("/Users/amizukam/DVJets/atlasstyle")
from AtlasStyle import *
from AtlasLabel import *
from utils import *

r.gROOT.SetBatch()
SetAtlasStyle()
label = "Internal"

plotType = "drRatio"
directory = "pdfs/" + plotType
if (not os.path.isdir(directory)):
    os.makedirs(directory)
if (not os.path.isdir("rootfiles")):
    os.makedirs("rootfiles")

inputFile = r.TFile("../outputFiles/drPlots.root", "READ")
outputFile = r.TFile("rootfiles/{}.root".format(plotType), "RECREATE")

ntrkList = ["Ntrk4", "Ntrk5", "Ntrk6", "Ntrk>6"]
dr1Same = {}
dr2Same = {}
dr1Mixed = {}
dr2Mixed = {}
for ntrk in ntrkList:
    dr1Same[ntrk] = inputFile.Get("dr1Same_"+ntrk).Rebin(5)
    dr2Same[ntrk] = inputFile.Get("dr2Same_"+ntrk).Rebin(5)
    dr1Mixed[ntrk] = inputFile.Get("dr1Mixed_"+ntrk).Rebin(5)
    dr2Mixed[ntrk] = inputFile.Get("dr2Mixed_"+ntrk).Rebin(5)

c = r.TCanvas("c", "c", 800, 700)
c.cd()
sampleLabel = prepareLatex()
for ntrk in ntrkList:
    h_dr1Same = dr1Same[ntrk]
    h_dr2Same = dr2Same[ntrk]
    h_dr1Mixed = dr1Mixed[ntrk]
    h_dr2Mixed = dr2Mixed[ntrk]

    h_dr1Same.Sumw2()
    h_dr2Same.Sumw2()
    h_dr1Mixed.Sumw2()
    h_dr2Mixed.Sumw2()

    h_dr1Same.Scale(1./ h_dr1Same.Integral())
    h_dr2Same.Scale(1./ h_dr2Same.Integral())
    h_dr1Mixed.Scale(1./ h_dr1Mixed.Integral())
    h_dr2Mixed.Scale(1./ h_dr2Mixed.Integral())

    h_dr1Same.SetLineColor(r.kBlack)
    h_dr1Same.SetMarkerColor(r.kBlack)
    h_dr2Same.SetLineColor(r.kBlack)
    h_dr2Same.SetMarkerColor(r.kBlack)
    h_dr1Mixed.SetLineColor(r.kRed)
    h_dr1Mixed.SetMarkerColor(r.kRed)
    h_dr2Mixed.SetLineColor(r.kRed)
    h_dr2Mixed.SetMarkerColor(r.kRed)

    leg = r.TLegend(0.60, 0.70, 0.85, 0.80)
    decorateLeg(leg)
    leg.AddEntry(h_dr1Same, "Same-event", "l")
    leg.AddEntry(h_dr1Mixed, "Mixed-event", "l")

    rp_dr1 = r.TRatioPlot(h_dr1Same, h_dr1Mixed)
    decorateRatioPlot(rp_dr1)
    ATLASLabel(0.20, 0.955, label)
    leg.Draw()
    c.Print("{}/{}.pdf".format(directory, "ratio_dR1_"+ntrk))

    rp_dr2 = r.TRatioPlot(h_dr2Same, h_dr2Mixed)
    decorateRatioPlot(rp_dr2)
    ATLASLabel(0.20, 0.955, label)
    leg.Draw()
    c.Print("{}/{}.pdf".format(directory, "ratio_dR2_"+ntrk))
