import ROOT as r
import sys, os
sys.path.append("/Users/amizukam/DVJets/atlasstyle")
from AtlasStyle import *
from AtlasLabel import *
from utils import *
import argparse

r.gROOT.SetBatch()
SetAtlasStyle()

parser = argparse.ArgumentParser()
parser.add_argument("-sr", "--SR", required=True, help="Signal region, 'HighPtSR' or 'TracklessSR'")
parser.add_argument("-tag", required=True, help="The campaign tag, 'a', 'd', or 'e'")
parser.add_argument("-sf", "--suffix", default="", help="File suffix")
parser.add_argument("-label", default="Internal", help="Label for ATLASLabel")
parser.add_argument("-n", "--nbins", type=int, default=1, help="Rebin")
parser.add_argument("-logy", action="store_true", help="User logy?")
args = parser.parse_args()

tag = "mc16{}".format(args.tag)
SR = args.SR
suffix = args.suffix
label = args.label
logy = args.logy
nbins = args.nbins

dataSet = "{}_{}_{}".format(tag, SR, suffix) if (suffix != "") else "{}_{}".format(tag, SR)
inputFile = r.TFile("../outputFiles/extractFactor_{}.root".format(dataSet), "READ")
if (not inputFile.IsOpen()):
    print("Input file: {} not opened, exit now.".format(inputFile.GetName()))
    exit()
plotType = "trackKinematics"
directory = "pdfs/" + plotType + "/" + dataSet
if (not os.path.isdir(directory)):
    os.makedirs(directory)

ntrkList = ["Ntrk4"]
cutList = ["noSel",
           "upstreamHitVeto",
           "allPtSel",
           "ptOutsideBP",
           "ptOutsidePixel",
           "d0InsideBP",
           "d0InsidePixel",
           "d0Selected",
           "angle",
           "lowPtForward"
           ]

h_allPtSel = {}
h_d0 = {}
h_d0sig = {}
for ntrk in ntrkList:
    h_allPtSel[ntrk] = {}
    h_d0[ntrk] = {}
    h_d0sig[ntrk] = {}
    for cut in cutList:
        h_allPtSel[ntrk][cut] = inputFile.Get("mvtrack_allPtSel_{}_{}".format(ntrk, cut)).Rebin(nbins)
        h_d0[ntrk][cut] = inputFile.Get("mvtrack_d0_all_{}_{}".format(ntrk, cut)).Rebin(nbins)
        h_d0sig[ntrk][cut] = inputFile.Get("mvtrack_d0sig_{}_{}".format(ntrk, cut)).Rebin(nbins)

c = r.TCanvas("c", "c", 800, 700)
c.cd()
if (logy):
    c.SetLogy(True)
sampleLabel = prepareLatex()
for ntrk in ntrkList:
    for cut in cutList:
        allPtSel = h_allPtSel[ntrk][cut]
        d0 = h_d0[ntrk][cut]
        d0sig = h_d0sig[ntrk][cut]

        # pT for all tracks
        allPtSel.SetMaximum(allPtSel.GetMaximum()*1.2)
        l_allPtSel = r.TLine(2, 0, 2, allPtSel.GetMaximum())
        l_allPtSel.SetLineColor(r.kRed)
        l_allPtSel.SetLineWidth(2)
        allPtSel.Draw("hist")
        ATLASLabel(0.20, 0.955, label)
        sampleLabel.DrawLatex(0.72, 0.80, "{}, {}".format(tag, SR))
        sampleLabel.DrawLatex(0.72, 0.75, getNtrkLabel(ntrk) + ", {}".format(cut))
        if (suffix != ""):
            sampleLabel.DrawLatex(0.72, 0.70, suffix)
        l_allPtSel.Draw()
        c.Print("{}/{}.pdf".format(directory, "allPtSel_{}_{}".format(cut, ntrk)))

        # d0 for all tracks
        d0.SetMaximum(d0.GetMaximum()*1.2)
        l_d0 = r.TLine(2, 0, 2, d0.GetMaximum())
        l_d0.SetLineColor(r.kRed)
        l_d0.SetLineWidth(2)
        d0.Draw("hist")
        ATLASLabel(0.20, 0.955, label)
        sampleLabel.DrawLatex(0.72, 0.80, "{}, {}".format(tag, SR))
        sampleLabel.DrawLatex(0.72, 0.75, getNtrkLabel(ntrk) + ", {}".format(cut))
        if (suffix != ""):
            sampleLabel.DrawLatex(0.72, 0.70, suffix)
        l_d0.Draw()
        c.Print("{}/{}.pdf".format(directory, "d0_{}_{}".format(cut, ntrk)))

        # d0sig for all tracks
        d0sig.SetMaximum(d0sig.GetMaximum()*1.2)
        l_d0sig = r.TLine(10, 0, 10, d0sig.GetMaximum())
        l_d0sig.SetLineColor(r.kRed)
        l_d0sig.SetLineWidth(2)
        d0sig.Draw("hist")
        ATLASLabel(0.20, 0.955, label)
        sampleLabel.DrawLatex(0.72, 0.80, "{}, {}".format(tag, SR))
        sampleLabel.DrawLatex(0.72, 0.75, getNtrkLabel(ntrk) + ", {}".format(cut))
        if (suffix != ""):
            sampleLabel.DrawLatex(0.72, 0.70, suffix)
        l_d0sig.Draw()
        c.Print("{}/{}.pdf".format(directory, "d0sig_{}_{}".format(cut, ntrk)))
