import ROOT as r
import sys, os
sys.path.append("/Users/amizukam/DVJets/atlasstyle")
from AtlasStyle import *
from AtlasLabel import *
from utils import *

r.gROOT.SetBatch()
SetAtlasStyle()
label = "Internal"

plotType = "compareSR"
directory = "pdfs/" + plotType
if (not os.path.isdir(directory)):
    os.makedirs(directory)

highPtFile = r.TFile("rootfiles/mvTemplate_highPtSR.root", "READ")
tracklessFile = r.TFile("rootfiles/mvTemplate_tracklessSR.root", "READ")

ntrkList = ["Ntrk4", "Ntrk5", "Ntrk6", "Ntrk>6"]

tempDict_highPt = {}
tempDict_trackless = {}
for ntrk in ntrkList:
    tempDict_highPt[ntrk] = highPtFile.Get("mergedMass_"+ntrk)
    tempDict_trackless[ntrk] = tracklessFile.Get("mergedMass_"+ntrk)

c = r.TCanvas("c", "c", 800, 700)
c.SetLogy()
sampleLabel = prepareLatex()
for ntrk in ntrkList:
    h_highPt = tempDict_highPt[ntrk]
    h_trackless = tempDict_trackless[ntrk]

    h_trackless.SetLineColor(r.kRed)
    h_trackless.SetMarkerColor(r.kRed)

    h_highPt.Sumw2()
    h_trackless.Sumw2()

    leg = r.TLegend(0.60, 0.70, 0.80, 0.80)
    decorateLeg(leg)
    leg.AddEntry(h_highPt, "High-p_{T} SR", "l")
    leg.AddEntry(h_trackless, "Trackless SR", "l")

    h_highPt.DrawNormalized("hist e0")
    h_trackless.DrawNormalized("hist e0 same")
    ATLASLabel(0.20, 0.955, label)
    sampleLabel.DrawLatex(0.61, 0.84, "Data, {}".format(getNtrkLabel(ntrk)))
    leg.Draw()
    c.Print("{}/{}.pdf".format(directory, "compareSR_"+ntrk))
