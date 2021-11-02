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
parser.add_argument("-sr", "--SR", required=True, help="Signal region")
parser.add_argument("-tag", required=True, help="The campaign tag")
parser.add_argument("-label", default="Internal", help="Label for ATLASLabel")
parser.add_argument("-n", "--nbins", type=int, default=1, help="Rebin")
parser.add_argument("-sf", "--suffix", default="", help="File suffix if needed")
args = parser.parse_args()

label = args.label
tag = "mc16{}".format(args.tag)
SR = args.SR
suffix = args.suffix
nbins = args.nbins

dataSet = "{}_{}_{}".format(tag, SR, suffix) if (suffix != "") else "{}_{}".format(tag, SR)

plotType = "truthMV"
directory = "pdfs/" + plotType + "/" + dataSet + "_" + SR
if (not os.path.isdir(directory)):
    os.makedirs(directory)

inputFile = r.TFile("../outputFiles/extractFactor_{}.root".format(dataSet), "READ")
if (not inputFile.IsOpen()):
    print(">> File not exist")
    exit()

ntrkList = ["Ntrk4", "Ntrk5", "Ntrk6", "Ntrk>6"]
typeList = ["dvType1", "dvType2", "dvType3", "dvType5", "dvType6"]
legLabel = {"dvType1": "G4 DV",
            "dvType2": "G4 + PU DV",
            "dvType3": "G4 + Gen DV",
            "dvType4": "PU DV",
            "dvType5": "Gen + PU DV",
            "dvType6": "Gen DV",
            "dvType7": "Combination DV"
            }
colors = [r.kBlack, r.kRed, r.kBlue, r.kGreen, r.kOrange, r.kViolet, r.kCyan]
dvSelList = ["passFiducial", "passDist", "passChiSq", "passMaterial", "passMaterial_strict"]
trkSelList = ["1p2", "1p4", "1p6", "1p8", "allPtSel"]

# Get histograms
h_mvMass_dvSel = {}
h_mvMass_trkSel = {}
for ntrk in ntrkList:
    h_mvMass_dvSel[ntrk] = {}
    h_mvMass_trkSel[ntrk] = {}
    for dvType in typeList:
        h_mvMass_dvSel[ntrk][dvType] = {}
        h_mvMass_trkSel[ntrk][dvType] = {}
        for dvSel in dvSelList:
            h_mvMass_dvSel[ntrk][dvType][dvSel] = inputFile.Get("mvMass_{}_{}_{}".format(dvType, ntrk, dvSel)).Rebin(nbins)
        for trkSel in trkSelList:
            h_mvMass_trkSel[ntrk][dvType][trkSel] = inputFile.Get("mvMass_{}_{}_{}".format(dvType, ntrk, trkSel)).Rebin(nbins)

c = r.TCanvas("c", "c", 800, 700)
c.cd()
sampleLabel = prepareLatex()
for ntrk in ntrkList:
    for dvType in typeList:
        for dvSel in dvSelList:
            mvMass_dvSel = h_mvMass_dvSel[ntrk][dvType][dvSel]
            mvMass_dvSel.Draw("hist")
            ATLASLabel(0.20, 0.955, label)
            sampleLabel.DrawLatex(0.615, 0.90, "{}, {}".format(tag, SR))
            sampleLabel.DrawLatex(0.615, 0.85, getNtrkLabel(ntrk)+", {}".format(dvSel))
            sampleLabel.DrawLatex(0.615, 0.80, dvType)
            c.Print("{}/{}.pdf".format(directory, "mvMass_{}_{}_{}".format(ntrk, dvSel, dvType)))

        for trkSel in trkSelList:
            mvMass_trkSel = h_mvMass_trkSel[ntrk][dvType][trkSel]
            mvMass_trkSel.Draw("hist")
            ATLASLabel(0.20, 0.955, label)
            sampleLabel.DrawLatex(0.615, 0.90, "{}, {}".format(tag, SR))
            sampleLabel.DrawLatex(0.615, 0.85, getNtrkLabel(ntrk)+", {}".format(trkSel))
            sampleLabel.DrawLatex(0.615, 0.80, dvType)
            c.Print("{}/{}.pdf".format(directory, "mvMass_{}_{}_{}".format(ntrk, trkSel, dvType)))
