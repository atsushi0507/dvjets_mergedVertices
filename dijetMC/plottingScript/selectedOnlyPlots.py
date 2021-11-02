import ROOT as r
import sys, os
sys.path.append("/Users/amizukam/DVJets/atlasstyle")
from AtlasStyle import *
from AtlasLabel import *
from utils import *
from ctypes import c_double as double
import argparse

r.gROOT.SetBatch()
SetAtlasStyle()

parser = argparse.ArgumentParser()
parser.add_argument("-sr", "--SR", required=True, help="Signal region")
parser.add_argument("-tag", required=True, help="The campaign tag")
parser.add_argument("-sf", "--suffix", required=True, default="", help="File suffix if needed")
parser.add_argument("-label", default="Internal", help="Label for ATLASLabel")
parser.add_argument("-n", "--nbins", type=int, default=1, help="Rebin")
parser.add_argument("-logy", action="store_true", help="Use logy")
args = parser.parse_args()

tag = "mc16{}".format(args.tag)
SR = args.SR
suffix = args.suffix
label = args.label
logy = args.logy
nbins = args.nbins

dataSet = "{}_{}_{}".format(tag, SR, suffix)
inputFile = r.TFile("../outputFiles/extractFactor_{}_noAttached.root".format(dataSet), "READ")
if (not inputFile.IsOpen()):
    print(">> Warning! File is not opened successfully.")
    exit()

plotType = "selectedOnly"
directory = "pdfs/" + plotType + "/" + dataSet
if (not os.path.isdir(directory)):
    os.makedirs(directory)

ntrkList = ["Ntrk4", "Ntrk5", "Ntrk6"]
typeList = ["dvType1", "dvType2", "dvType3", "dvType5", "dvType6"]
legLabel = {"dvType1": "G4 DV",
            "dvType2": "G4 + PU DV",
            "dvType3": "G4 + Gen DV",
            "dvType4": "PU DV",
            "dvType5": "Gen + PU DV",
            "dvType6": "Gen DV",
            "dvType7": "Combination DV"
            }
colors = [r.kBlack, r.kRed, r.kBlue, r.kGreen, r.kOrange, r.kCyan, r.kViolet]
h_noSel = {}
h_DVSel = {}
h_fullSel = {}
h_tc = {}
h_chisq = {}
for ntrk in ntrkList:
    h_noSel[ntrk] = {}
    h_DVSel[ntrk] = {}
    h_fullSel[ntrk] = {}
    h_tc[ntrk] = {}
    h_chisq[ntrk] = {}
    for dvType in typeList:
        h_noSel[ntrk][dvType] = inputFile.Get("mvMass_{}_{}_{}".format(dvType, ntrk, "noSel")).Rebin(nbins)
        h_DVSel[ntrk][dvType] = inputFile.Get("mvMass_{}_{}_{}".format(dvType, ntrk, "DVSel")).Rebin(nbins)
        h_fullSel[ntrk][dvType] = inputFile.Get("mvMass_{}_{}_{}".format(dvType, ntrk, "fullSel")).Rebin(nbins)
        h_tc[ntrk][dvType] = inputFile.Get("mvMass_{}_{}_{}".format(dvType, ntrk, "trackCleaning")).Rebin(nbins)
        h_chisq[ntrk][dvType] = inputFile.Get("mvChiSq_{}_{}_noSel".format(dvType, ntrk)).Rebin(5)

c = r.TCanvas("c", "c", 800, 700)
c.cd()
sampleLabel = prepareLatex()
for ntrk in ntrkList:
    for dvType in typeList:
        if (logy):
            c.SetLogy(True)
        else:
            c.SetLogy(False)
        noSel = h_noSel[ntrk][dvType]
        DVSel = h_DVSel[ntrk][dvType]
        fullSel = h_fullSel[ntrk][dvType]
        tc = h_tc[ntrk][dvType]
        chisq = h_chisq[ntrk][dvType]

        endBin = noSel.FindBin(35.)
        noSel.GetXaxis().SetRange(1, endBin)
        DVSel.GetXaxis().SetRange(1, endBin)
        fullSel.GetXaxis().SetRange(1, endBin)
        tc.GetXaxis().SetRange(1, endBin)
        
        lastBin = noSel.GetNbinsX() + 1
        
        errMV = double(0.)
        nMV = noSel.IntegralAndError(1, lastBin, errMV)

        # Event selection only
        leg_noSel = r.TLegend(0.60, 0.65, 0.85, 0.80)
        decorateLeg(leg_noSel)
        leg_noSel.AddEntry(noSel, "Event selection only", "l")
        noSel.Draw("hist e0")
        ATLASLabel(0.20, 0.955, label)
        sampleLabel.DrawLatex(0.615, 0.90, "{}, {}".format(tag, SR))
        sampleLabel.DrawLatex(0.615, 0.85, getNtrkLabel(ntrk)+", "+legLabel[dvType])
        sampleLabel.DrawLatex(0.615, 0.80, "MV: {} #pm {:.2f}".format(nMV, errMV.value))
        leg_noSel.Draw()
        c.Print("{}/{}.pdf".format(directory, "mvMass_{}_{}_noSel".format(dvType, ntrk)))

        errMV = double(0.)
        nMV = DVSel.IntegralAndError(1, lastBin, errMV)
        # DV selection 
        leg_DVSel = r.TLegend(0.60, 0.65, 0.85, 0.80)
        decorateLeg(leg_DVSel)
        leg_DVSel.AddEntry(DVSel, "DV selection", "l")
        DVSel.Draw("hist e0")
        ATLASLabel(0.20, 0.955, label)
        sampleLabel.DrawLatex(0.615, 0.90, "{}, {}".format(tag, SR))
        sampleLabel.DrawLatex(0.615, 0.85, getNtrkLabel(ntrk)+", "+legLabel[dvType])
        sampleLabel.DrawLatex(0.615, 0.80, "MV: {} #pm {:.2f}".format(nMV, errMV.value))
        leg_DVSel.Draw()
        c.Print("{}/{}.pdf".format(directory, "mvMass_{}_{}_DVSel".format(dvType, ntrk)))

        errMV = double(0.)
        nMV = fullSel.IntegralAndError(1, lastBin, errMV)
        # Full selection 
        leg_fullSel = r.TLegend(0.60, 0.65, 0.85, 0.80)
        decorateLeg(leg_fullSel)
        leg_fullSel.AddEntry(fullSel, "Full selection", "l")
        fullSel.Draw("hist e0")
        ATLASLabel(0.20, 0.955, label)
        sampleLabel.DrawLatex(0.615, 0.90, "{}, {}".format(tag, SR))
        sampleLabel.DrawLatex(0.615, 0.85, getNtrkLabel(ntrk)+", "+legLabel[dvType])
        sampleLabel.DrawLatex(0.615, 0.80, "MV: {} #pm {:.2f}".format(nMV, errMV.value))
        leg_fullSel.Draw()
        c.Print("{}/{}.pdf".format(directory, "mvMass_{}_{}_fullSel".format(dvType, ntrk)))

        errMV = double(0.)
        nMV = tc.IntegralAndError(1, lastBin, errMV)
        # Track cleaning
        leg_tc = r.TLegend(0.60, 0.65, 0.85, 0.80)
        decorateLeg(leg_tc)
        leg_tc.AddEntry(tc, "Track cleaning", "l")
        tc.Draw("hist e0")
        ATLASLabel(0.20, 0.955, label)
        sampleLabel.DrawLatex(0.615, 0.90, "{}, {}".format(tag, SR))
        sampleLabel.DrawLatex(0.615, 0.85, getNtrkLabel(ntrk)+", "+legLabel[dvType])
        sampleLabel.DrawLatex(0.615, 0.80, "MV: {} #pm {:.2f}".format(nMV, errMV.value))
        leg_tc.Draw()
        c.Print("{}/{}.pdf".format(directory, "mvMass_{}_{}_tc".format(dvType, ntrk)))

        # ChiSq
        lastBin = chisq.GetNbinsX()
        bin5 = chisq.FindBin(5.)
        low = chisq.Integral(1, bin5-1)
        high = chisq.Integral(bin5, lastBin+1)
        chisq.SetBinContent(lastBin, chisq.GetBinContent(lastBin))
        chisq.SetBinContent(lastBin, chisq.GetBinContent(lastBin+1))
        chisq.Draw("hist")
        ATLASLabel(0.20, 0.955, label)
        sampleLabel.DrawLatex(0.615, 0.90, "{}, {}".format(tag, SR))
        sampleLabel.DrawLatex(0.615, 0.85, getNtrkLabel(ntrk)+ ", " + legLabel[dvType])
        sampleLabel.DrawLatex(0.615, 0.80, "#chi^{2}/n_{dof} < 5: " + str(low) + ", #chi^{2}/n_{dof} > 5: " + str(high))
        c.Print("{}/{}.pdf".format(directory, "chisq_{}_{}".format(dvType, ntrk)))

    c.SetLogy(True)
    # Evt sel only
    i = 0
    leg_dvType = r.TLegend(0.60, 0.55, 0.85, 0.80)
    decorateLeg(leg_dvType)
    for dvType in typeList:
        endBin = h_noSel[ntrk]["dvType1"].FindBin(35.)
        h_noSel[ntrk]["dvType1"].GetXaxis().SetRange(1, endBin)
        leg_dvType.AddEntry(h_noSel[ntrk][dvType], legLabel[dvType], "l")
        setHistColor(h_noSel[ntrk][dvType], colors[i])
        if (i == 0):
            h_noSel[ntrk][dvType].Draw("hist")
        else:
            h_noSel[ntrk][dvType].Draw("same hist")
        ATLASLabel(0.20, 0.955, label)
        sampleLabel.DrawLatex(0.615, 0.90, "{}, {}, {}".format(tag, SR, suffix))
        sampleLabel.DrawLatex(0.615, 0.85, getNtrkLabel(ntrk)+", event selection only")
        leg_dvType.Draw()
        i+= 1
    c.Print("{}/{}.pdf".format(directory, "dvMass_type_noSel_"+ntrk))

    # DV sel
    i = 0
    for dvType in typeList:
        endBin = h_DVSel[ntrk]["dvType1"].FindBin(35.)
        h_DVSel[ntrk]["dvType1"].GetXaxis().SetRange(1, endBin)
        setHistColor(h_DVSel[ntrk][dvType], colors[i])
        if (i == 0):
            h_DVSel[ntrk][dvType].Draw("hist")
        else:
            h_DVSel[ntrk][dvType].Draw("same hist")
        ATLASLabel(0.20, 0.955, label)
        sampleLabel.DrawLatex(0.615, 0.90, "{}, {}, {}".format(tag, SR, suffix))
        sampleLabel.DrawLatex(0.615, 0.85, getNtrkLabel(ntrk)+", DV selection")
        leg_dvType.Draw()
        i+= 1
    c.Print("{}/{}.pdf".format(directory, "dvMass_type_DVSel_"+ntrk))

    # Full sel
    i = 0
    for dvType in typeList:
        endBin = h_fullSel[ntrk]["dvType1"].FindBin(35.)
        h_fullSel[ntrk]["dvType1"].GetXaxis().SetRange(1, endBin)
        setHistColor(h_fullSel[ntrk][dvType], colors[i])
        if (i == 0):
            h_fullSel[ntrk][dvType].Draw("hist")
        else:
            h_fullSel[ntrk][dvType].Draw("same hist")
        ATLASLabel(0.20, 0.955, label)
        sampleLabel.DrawLatex(0.615, 0.90, "{}, {}, {}".format(tag, SR, suffix))
        sampleLabel.DrawLatex(0.615, 0.85, getNtrkLabel(ntrk)+", full selection")
        leg_dvType.Draw()
        i+= 1
    c.Print("{}/{}.pdf".format(directory, "dvMass_type_fullSel_"+ntrk))

    # track cleaning
    i = 0
    for dvType in typeList:
        endBin = h_tc[ntrk]["dvType1"].FindBin(35.)
        h_tc[ntrk]["dvType1"].GetXaxis().SetRange(1, endBin)
        setHistColor(h_tc[ntrk][dvType], colors[i])
        if (i == 0):
            h_tc[ntrk][dvType].Draw("hist")
        else:
            h_tc[ntrk][dvType].Draw("same hist")
        ATLASLabel(0.20, 0.955, label)
        sampleLabel.DrawLatex(0.615, 0.90, "{}, {}, {}".format(tag, SR, suffix))
        sampleLabel.DrawLatex(0.615, 0.85, getNtrkLabel(ntrk)+", track cleaning")
        leg_dvType.Draw()
        i+= 1
    c.Print("{}/{}.pdf".format(directory, "dvMass_type_trackCleaning_"+ntrk))
