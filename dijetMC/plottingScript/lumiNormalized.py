import ROOT as r
import sys, os
sys.path.append("/Users/amizukam/DVJets/atlasstyle")
from AtlasStyle import *
from AtlasLabel import *
from ctypes import c_double as double
from utils import *
import argparse

r.gROOT.SetBatch()
SetAtlasStyle()

parser = argparse.ArgumentParser()
parser.add_argument("-sr", "--SR", required=True, help="Signal region, 'HighPtSR', or 'TracklessSR'")
parser.add_argument("-tag", required=True, help="The campaign tag, 'a', 'd', or 'e'")
parser.add_argument("-sf", "--suffix", default="", help="File suffix if needed")
parser.add_argument("-label", default="Internal", help="Label for ATLASLabel")
parser.add_argument("-n", "--nbins", type=int, default=1, help="Rebin")
parser.add_argument("-logy", action="store_true", help="Use logy?")
args = parser.parse_args()

tag = "mc16{}".format(args.tag)
SR = args.SR
suffix = args.suffix
label = args.label
logy = args.logy
nbins = args.nbins

dataSet = "{}_{}_{}".format(tag, SR, suffix) if (suffix != "") else "{}_{}".format(tag, SR)

if (args.tag == "a"):
    year = 1516
if (args.tag == "d"):
    year = 17
if (args.tag == "e"):
    year = 18

bgFile = r.TFile("../outputFiles/dvMass_{}_{}.root".format(tag, SR), "READ")
mvFile = r.TFile("../outputFiles/extractFactor_{}.root".format(dataSet), "READ")
weightFile = r.TFile("../outputFiles/extractFactor_{}_weighted.root".format(dataSet), "READ")
dataFile = r.TFile("/Users/amizukam/DVJets/trackCleaning/rootfiles/data{}_DV_mass_{}.root".format(year, SR), "READ")
sigFile = r.TFile("../outputFiles/significance_{}_{}.root".format(tag, SR), "READ")
if (not bgFile.IsOpen() or not mvFile.IsOpen()) or not dataFile.IsOpen() or not sigFile.IsOpen():
    print("File not found. Stop processing")
    exit()

plotType = "lumiNorm"
directory = "pdfs/" + plotType + "/" + dataSet
if (not os.path.isdir(directory)):
    os.makedirs(directory)

ntrkList = ["Ntrk4", "Ntrk5", "Ntrk6"]
#typeList = ["dvType1", "dvType2", "dvType3", "dvType4", "dvType5", "dvType6", "dvType7"]
typeList = ["dvType1", "dvType2", "dvType3", "dvType5", "dvType6"]
legLabel = {"dvType1": "G4 DV",
            "dvType2": "G4 + PU DV",
            "dvType3": "G4 + Gen DV",
            "dvType4": "PU DV",
            "dvType5": "Gen + PU DV",
            "dvType6": "Gen DV",
            "dvType7": "Combination DV",
            }
colors = [r.kBlack, r.kRed, r.kBlue, r.kGreen, r.kOrange, r.kCyan, r.kViolet]
h_bg_noSel = {}
h_bg_DVSel = {}
h_bg_fullSel = {}
h_mv_noSel = {}
h_mv_DVSel = {}
h_mv_fullSel = {}
h_data_noSel = {}
h_data_DVSel = {}
h_data_fullSel = {}
h_mvMass_type_noSel = {}
h_mvMass_type_DVSel = {}
h_mvMass_type_fullSel = {}
h_mvMass_type_tc = {}
h_sigMass = {}
h_weightMass_noSel = {}
h_weightMass_DVSel = {}
h_weightMass_fullSel = {}
for ntrk in ntrkList:
    h_bg_noSel[ntrk] = bgFile.Get("dvMass_noSelection_{}".format(ntrk)).Rebin(nbins)
    h_bg_DVSel[ntrk] = bgFile.Get("dvMass_DVSel_{}".format(ntrk)).Rebin(nbins)
    h_bg_fullSel[ntrk] = bgFile.Get("dvMass_fullSel_{}".format(ntrk)).Rebin(5)
    h_mv_noSel[ntrk] = mvFile.Get("mvMass_"+ntrk).Rebin(nbins)
    h_mv_DVSel[ntrk] = mvFile.Get("mvMass_DVSel_"+ntrk).Rebin(nbins)
    h_mv_fullSel[ntrk] = mvFile.Get("mvMass_fullSel_"+ntrk).Rebin(5)
    h_data_noSel[ntrk] = dataFile.Get("mDV_"+ntrk).Rebin(nbins)
    h_data_DVSel[ntrk] = dataFile.Get("mDV_DVSel_"+ntrk).Rebin(nbins)
    h_data_fullSel[ntrk] = dataFile.Get("mDV_fullSel_"+ntrk).Rebin(5)
    h_sigMass[ntrk] = sigFile.Get("mvMass_mixed_"+ntrk).Rebin(nbins)
    h_weightMass_noSel[ntrk] = weightFile.Get("mvMass_"+ntrk).Rebin(nbins)
    h_weightMass_DVSel[ntrk] = weightFile.Get("mvMass_DVSel_"+ntrk).Rebin(nbins)
    h_weightMass_fullSel[ntrk] = weightFile.Get("mvMass_fullSel_"+ntrk).Rebin(5)
    h_mvMass_type_noSel[ntrk] = {}
    h_mvMass_type_DVSel[ntrk] = {}
    h_mvMass_type_fullSel[ntrk] = {}
    h_mvMass_type_tc[ntrk] = {}
    for dvtype in typeList:
        h_mvMass_type_noSel[ntrk][dvtype] = mvFile.Get("mvMass_{}_{}_{}".format(dvtype, ntrk, "noSel")).Rebin(nbins)
        h_mvMass_type_DVSel[ntrk][dvtype] = mvFile.Get("mvMass_{}_{}_{}".format(dvtype, ntrk, "DVSel")).Rebin(nbins)
        h_mvMass_type_fullSel[ntrk][dvtype] = mvFile.Get("mvMass_{}_{}_{}".format(dvtype, ntrk, "fullSel")).Rebin(nbins)
        h_mvMass_type_tc[ntrk][dvtype] = mvFile.Get("mvMass_{}_{}_{}".format(dvtype, ntrk, "trackCleaning")).Rebin(nbins)

c = r.TCanvas("c", "c", 800, 700)
c.cd()
sampleLabel = prepareLatex()
if (logy):
    c.SetLogy(True)
for ntrk in ntrkList:
    bg_noSel = h_bg_noSel[ntrk]
    bg_DVSel = h_bg_DVSel[ntrk]
    bg_fullSel = h_bg_fullSel[ntrk]
    mv_noSel = h_mv_noSel[ntrk]
    mv_DVSel = h_mv_DVSel[ntrk]
    mv_fullSel = h_mv_fullSel[ntrk]
    data_noSel = h_data_noSel[ntrk]
    data_DVSel = h_data_DVSel[ntrk]
    data_fullSel = h_data_fullSel[ntrk]
    sigMass = h_sigMass[ntrk]
    weightMass_noSel = h_weightMass_noSel[ntrk]
    weightMass_DVSel = h_weightMass_DVSel[ntrk]
    weightMass_fullSel = h_weightMass_fullSel[ntrk]

    setHistColor(mv_noSel, r.kRed)
    setHistColor(mv_DVSel, r.kRed)
    setHistColor(mv_fullSel, r.kRed)
    setHistColor(bg_noSel, r.kBlue)
    setHistColor(bg_DVSel, r.kBlue)
    setHistColor(bg_fullSel, r.kBlue)
    setHistColor(weightMass_noSel, r.kRed)
    setHistColor(weightMass_DVSel, r.kRed)
    setHistColor(weightMass_fullSel, r.kRed)

    bg_noSel.SetMinimum(0.5)
    bg_DVSel.SetMinimum(0.5)
    bg_fullSel.SetMinimum(0.5)

    leg = r.TLegend(0.65, 0.65, 0.85, 0.80)
    decorateLeg(leg)

    leg.AddEntry(data_noSel, "Data", "pe")
    leg.AddEntry(bg_noSel, tag, "l")
    #leg.AddEntry(mv_noSel, "Merged Vertices", "l")
    leg.AddEntry(weightMass_noSel, "Merged Vetices", "l")

    # No selection
    bg_noSel.Draw("hist e0")
    data_noSel.Draw("e0 same")
    #mv_noSel.Draw("hist e0 same")
    weightMass_noSel.Draw("hist e0 same")
    ATLASLabel(0.20, 0.955, label)
    sampleLabel.DrawLatex(0.67, 0.90, "{}, {}".format(tag, SR))
    sampleLabel.DrawLatex(0.67, 0.85, getNtrkLabel(ntrk)+", no selection")
    leg.Draw()
    c.Print("{}/{}.pdf".format(directory, "mass_noSel_"+ntrk))

    # DV selection
    bg_DVSel.Draw("hist e0")
    data_DVSel.Draw("e0 same")
    #mv_DVSel.Draw("hist e0 same")
    weightMass_DVSel.Draw("hist e0 same")
    ATLASLabel(0.20, 0.955, label)
    sampleLabel.DrawLatex(0.67, 0.90, "{}, {}".format(tag, SR))
    sampleLabel.DrawLatex(0.67, 0.85, getNtrkLabel(ntrk)+", DV selection")
    leg.Draw()
    c.Print("{}/{}.pdf".format(directory, "mass_DVSel_"+ntrk))

    # Full selection
    bg_fullSel.GetXaxis().SetRange(1, bg_fullSel.FindBin(20.))
   
    bg_fullSel.Draw("hist e0")
    #mv_fullSel.Draw("hist e0 same")
    weightMass_fullSel.Draw("hist e0 same")
    data_fullSel.Draw("e0 same")
    ATLASLabel(0.20, 0.955, label)
    sampleLabel.DrawLatex(0.67, 0.90, "{}, {}".format(tag, SR))
    sampleLabel.DrawLatex(0.67, 0.85, getNtrkLabel(ntrk)+", full selection")
    leg.Draw()
    c.Print("{}/{}.pdf".format(directory, "mass_fullSel_"+ntrk))

    firstBin = 2
    endBin = mv_noSel.GetNbinsX() + 1
    
    errBG_noSel = double(0.)
    errBG_DVSel = double(0.)
    errBG_fullSel = double(0.)
    errMV_noSel = double(0.)
    errMV_DVSel = double(0.)
    errMV_fullSel = double(0.)

    nBG_noSel = bg_noSel.IntegralAndError(firstBin, endBin, errBG_noSel)
    nBG_DVSel = bg_DVSel.IntegralAndError(firstBin, endBin, errBG_DVSel)
    nBG_fullSel = bg_fullSel.IntegralAndError(firstBin, endBin, errBG_fullSel)
    """
    nMV_noSel = mv_noSel.IntegralAndError(firstBin, endBin, errMV_noSel)
    nMV_DVSel = mv_DVSel.IntegralAndError(firstBin, endBin, errMV_DVSel)
    nMV_fullSel = mv_fullSel.IntegralAndError(firstBin, endBin, errMV_fullSel)
    """
    nMV_noSel = weightMass_noSel.IntegralAndError(firstBin, endBin, errMV_noSel)
    nMV_DVSel = weightMass_DVSel.IntegralAndError(firstBin, endBin, errMV_DVSel)
    nMV_fullSel = weightMass_fullSel.IntegralAndError(firstBin, endBin, errMV_fullSel)

    rate_noSel, errRate_noSel = divideError(nMV_noSel, nBG_noSel, errMV_noSel.value, errBG_noSel.value)
    rate_DVSel, errRate_DVSel = divideError(nMV_DVSel, nBG_DVSel, errMV_DVSel.value, errBG_DVSel.value)
    rate_fullSel, errRate_fullSel = divideError(nMV_fullSel, nBG_fullSel, errMV_fullSel.value, errBG_fullSel.value)

    print("noSel: nMV = {:.2f} +- {:.2f}".format(nMV_noSel, errMV_noSel.value))
    print("DVSel: nMV = {:.2f} +- {:.2f}".format(nMV_DVSel, errMV_DVSel.value))
    print("Full Sel: nMV = {:.2f} +- {:.2f}".format(nMV_fullSel, errMV_fullSel.value))
    print("({:.3f} +- {:.3f})%".format(rate_noSel*100, errRate_noSel*100))
    print("({:.3f} +- {:.3f})%".format(rate_DVSel*100, errRate_DVSel*100))
    print("({:.3f} +- {:.3f})%".format(rate_fullSel*100, errRate_fullSel*100))

    i = 0
    leg_dvType = r.TLegend(0.60, 0.55, 0.85, 0.80)
    decorateLeg(leg_dvType)
    for dvtype in typeList:
        h_mvMass_type_noSel[ntrk]["dvType1"].GetXaxis().SetRange(1, h_mvMass_type_noSel[ntrk]["dvType1"].FindBin(35.))
        leg_dvType.AddEntry(h_mvMass_type_noSel[ntrk][dvtype], legLabel[dvtype], "l")
        setHistColor(h_mvMass_type_noSel[ntrk][dvtype], colors[i])
        if (i == 0):
            h_mvMass_type_noSel[ntrk][dvtype].Draw("hist")
        else:
            h_mvMass_type_noSel[ntrk][dvtype].Draw("hist same")
        ATLASLabel(0.20, 0.955, label)
        sampleLabel.DrawLatex(0.62, 0.90, "{}, {}, {}".format(tag, SR, suffix))
        sampleLabel.DrawLatex(0.62, 0.85, getNtrkLabel(ntrk)+", no DV selection")
        leg_dvType.Draw()
        i+= 1
    c.Print("{}/{}.pdf".format(directory, "dvMass_type_noSel_"+ntrk))

    leg_dvType_DVSel = r.TLegend(0.60, 0.55, 0.85, 0.80)
    decorateLeg(leg_dvType_DVSel)
    i = 0
    for dvtype in typeList:
        h_mvMass_type_DVSel[ntrk]["dvType1"].GetXaxis().SetRange(1, h_mvMass_type_DVSel[ntrk]["dvType1"].FindBin(35.))
        leg_dvType_DVSel.AddEntry(h_mvMass_type_DVSel[ntrk][dvtype], legLabel[dvtype], "l")
        setHistColor(h_mvMass_type_DVSel[ntrk][dvtype], colors[i])
        if (i == 0):
            h_mvMass_type_DVSel[ntrk][dvtype].Draw("hist")
        else:
            h_mvMass_type_DVSel[ntrk][dvtype].Draw("hist same")
        ATLASLabel(0.20, 0.955, label)
        sampleLabel.DrawLatex(0.62, 0.90, "{}, {}, {}".format(tag, SR, suffix))
        sampleLabel.DrawLatex(0.62, 0.85, getNtrkLabel(ntrk)+", DV selection")
        leg_dvType_DVSel.Draw()
        i+= 1
    c.Print("{}/{}.pdf".format(directory, "dvMass_type_DVSel_"+ntrk))

    leg_dvType_fullSel = r.TLegend(0.60, 0.55, 0.85, 0.80)
    decorateLeg(leg_dvType_fullSel)
    i = 0
    for dvtype in typeList:
        h_mvMass_type_fullSel[ntrk]["dvType1"].GetXaxis().SetRange(1, h_mvMass_type_fullSel[ntrk]["dvType1"].FindBin(35.))
        leg_dvType_fullSel.AddEntry(h_mvMass_type_fullSel[ntrk][dvtype], legLabel[dvtype], "l")
        setHistColor(h_mvMass_type_fullSel[ntrk][dvtype], colors[i])
        if (i == 0):
            h_mvMass_type_fullSel[ntrk][dvtype].Draw("hist")
        else:
            h_mvMass_type_fullSel[ntrk][dvtype].Draw("hist same")
        ATLASLabel(0.20, 0.955, label)
        sampleLabel.DrawLatex(0.62, 0.90, "{}, {}, {}".format(tag, SR, suffix))
        sampleLabel.DrawLatex(0.62, 0.85, getNtrkLabel(ntrk)+", DV selection")
        leg_dvType_fullSel.Draw()
        i+= 1
    c.Print("{}/{}.pdf".format(directory, "dvMass_type_fullSel_"+ntrk))

    leg_dvType_tc = r.TLegend(0.60, 0.55, 0.85, 0.80)
    decorateLeg(leg_dvType_tc)
    i = 0
    for dvtype in typeList:
        h_mvMass_type_tc[ntrk]["dvType1"].GetXaxis().SetRange(1, h_mvMass_type_tc[ntrk]["dvType1"].FindBin(35.))
        leg_dvType_tc.AddEntry(h_mvMass_type_tc[ntrk][dvtype], legLabel[dvtype], "l")
        setHistColor(h_mvMass_type_tc[ntrk][dvtype], colors[i])
        if (i == 0):
            h_mvMass_type_tc[ntrk][dvtype].Draw("hist")
            print(dvtype, h_mvMass_type_tc[ntrk][dvtype].Integral())
        else:
            h_mvMass_type_tc[ntrk][dvtype].Draw("hist same")
            print(dvtype, h_mvMass_type_tc[ntrk][dvtype].Integral())
        ATLASLabel(0.20, 0.955, label)
        sampleLabel.DrawLatex(0.62, 0.90, "{}, {}, {}".format(tag, SR, suffix))
        sampleLabel.DrawLatex(0.62, 0.85, getNtrkLabel(ntrk)+", track cleaning")
        leg_dvType_tc.Draw()
        i+= 1
    c.Print("{}/{}.pdf".format(directory, "dvMass_type_trackCleaning_"+ntrk))

    i = 0
    leg_sigMass = r.TLegend(0.60, 0.55, 0.85, 0.80)
    decorateLeg(leg_sigMass)
    lastBin = h_mvMass_type_noSel[ntrk]["dvType2"].GetNbinsX() + 1
    sf = h_mvMass_type_noSel[ntrk]["dvType2"].Integral(1, lastBin) / sigMass.Integral(1, lastBin)
    sigMass.Sumw2()
    sigMass.Scale(sf)
    setHistColor(sigMass, r.kCyan)
    leg_sigMass.AddEntry(sigMass, "Data-driven template", "l")
    for dvtype in typeList:
        h_mvMass_type_noSel[ntrk]["dvType1"].GetXaxis().SetRange(1, h_mvMass_type_noSel[ntrk]["dvType1"].FindBin(35.))
        leg_sigMass.AddEntry(h_mvMass_type_noSel[ntrk][dvtype], legLabel[dvtype], "l")
        setHistColor(h_mvMass_type_noSel[ntrk][dvtype], colors[i])
        if (i == 0):
            h_mvMass_type_noSel[ntrk][dvtype].Draw("hist e0")
        else:
            h_mvMass_type_noSel[ntrk][dvtype].Draw("hist e0 same")
        sigMass.Draw("hist e0 same")
        ATLASLabel(0.20, 0.955, label)
        sampleLabel.DrawLatex(0.62, 0.90, "{}, {}, {}".format(tag, SR, suffix))
        sampleLabel.DrawLatex(0.62, 0.85, getNtrkLabel(ntrk)+", no DV selection")
        leg_sigMass.Draw()
        i+= 1
    c.Print("{}/{}.pdf".format(directory, "dvMass_vs_ddTemplate_"+ntrk))
