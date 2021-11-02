import ROOT as r
import sys, os
sys.path.append("/Users/amizukam/DVJets/atlasstyle")
from AtlasStyle import *
from AtlasLabel import *
from utils import *

r.gROOT.SetBatch()
SetAtlasStyle()
label = "Internal"

plotType = "sigRatio"
directory = "pdfs/" + plotType
if (not os.path.isdir(directory)):
    os.makedirs(directory)
if (not os.path.isdir("rootfiles")):
    os.makedirs("rootfiles")

inputFile = r.TFile("../outputFiles/significance_newSamples.root", "READ")
outputFile = r.TFile("rootfiles/{}.root".format(plotType), "RECREATE")

ntrkList = ["Ntrk4", "Ntrk5", "Ntrk6", "Ntrk>6"]

sigSame = {}
sigMixed = {}
for ntrk in ntrkList:
    sigSame[ntrk] = inputFile.Get("sigSame_"+ ntrk)
    sigMixed[ntrk] = inputFile.Get("sigMixed_" + ntrk)

c = r.TCanvas("c", "c", 800, 700)
c.cd()
sampleLabel = prepareLatex()
for ntrk in ntrkList:
    h_sigSame = sigSame[ntrk]
    h_sigMixed = sigMixed[ntrk]

    h_sigSame.SetLineColor(r.kBlack)
    h_sigMixed.SetLineColor(r.kRed)

    h_sigMixed.Sumw2()

    bin100 = h_sigSame.FindBin(100.)
    nbins = h_sigSame.GetNbinsX() + 1

    sf = h_sigSame.Integral(bin100, nbins) / h_sigMixed.Integral(bin100, nbins)
    h_sigMixed.Scale(sf)

    leg = r.TLegend(0.60, 0.68, 0.85, 0.78)
    decorateLeg(leg)
    leg.AddEntry(h_sigSame, "Same-event", "l")
    leg.AddEntry(h_sigMixed, "Mixed-event", "l")

    rp_sig = r.TRatioPlot(h_sigSame, h_sigMixed)
    decorateRatioPlot(rp_sig)
    ATLASLabel(0.20, 0.955, label)
    leg.Draw()
    sampleLabel.DrawLatex(0.62, 0.88, "Event preselection")
    sampleLabel.DrawLatex(0.62, 0.83, getNtrkLabel(ntrk))

    outname = "sigRatio_" + ntrk
    c.Print("{}/{}.pdf".format(directory, outname))

    h_sigSame.GetXaxis().SetRange(1, bin100)
    h_sigMixed.GetXaxis().SetRange(1, bin100+1)
    maximum = h_sigSame.GetMaximum()
    h_sigSame.SetMaximum(maximum*2.0)
    decorateRatioPlot(rp_sig)
    ATLASLabel(0.20, 0.955, label)
    leg.Draw()
    sampleLabel.DrawLatex(0.62, 0.88, "Event preselection")
    sampleLabel.DrawLatex(0.62, 0.83, getNtrkLabel(ntrk))
    c.Print("{}/{}.pdf".format(directory, outname+"_zoomed"))
