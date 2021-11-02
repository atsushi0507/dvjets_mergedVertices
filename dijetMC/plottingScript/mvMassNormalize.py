import ROOT as r
import ctypes
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
parser.add_argument("-m", "--materialVeto", action="store_true", help="Use material veto file")
parser.add_argument("-d", "--DVSel", action="store_true", help="Use DV selection file")
args = parser.parse_args()

label = args.label
tag = "mc16{}".format(args.tag)
SR = args.SR
suffix = args.suffix
nbins = args.nbins
matVeto = args.materialVeto
DVSel = args.DVSel
if (matVeto and DVSel):
    print(">> Warning! You can't turn on both matVeto and DVSel.")
    print(">> Switch off for the flag")
    matVeto = False
    DVSel = False

lastSuffix = ""
if matVeto:
    lastSuffix += "_matVeto"
if DVSel:
    lastSuffx += "_DVSel"

dataSet = "{}_{}_{}".format(tag, SR, suffix) if (suffix != "") else "{}_{}".format(tag, SR)

plotType = "massNormalize"
directory = "pdfs/" + plotType + "/" + dataSet + "_" + SR
if (not os.path.isdir(directory)):
    os.makedirs(directory)

massFile = r.TFile("../outputFiles/dvMass_{}_{}.root".format(tag, SR), "READ")
mvFile = r.TFile("../outputFiles/extractFactor_{}.root".format(dataSet), "READ")
weightedFile = r.TFile("../outputFiles/extractFactor_{}_weighted.root".format(dataSet), "READ")
noEvtSelFile = r.TFile("../outputFiles/extractFactor_{}_noEvtSel.root".format(dataSet), "READ")
dataDrivenFile = r.TFile("../outputFiles/significance_{}_{}.root".format(tag, SR+lastSuffix), "READ")

if (not massFile.IsOpen() or not mvFile.IsOpen() or not dataDrivenFile.IsOpen() or not noEvtSelFile.IsOpen()):
    print(">> File not opened successfully, check the files are exist.")
    exit()

ntrkList = ["Ntrk4", "Ntrk5", "Ntrk6", "Ntrk>6"]
#typeList = ["dvType1", "dvType2", "dvType3", "dvType4", "dvType5", "dvType6", "dvType7"]
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

# Get histograms
h_truthMass = {}
h_truthMass_DVSel = {}
h_truthMass_fullSel = {}
h_truthMass_w = {}
h_truthMass_DVSel_w = {}
h_truthMass_fullSel_w = {}
h_sigMass = {}
h_bg = {}
h_bg_DVSel = {}
h_bg_fullSel = {}
h_truthMass_noEvtSel = {}
h_truthMass_DVSel_noEvtSel = {}
h_truthMass_fullSel_noEvtSel = {}
for ntrk in ntrkList:
    h_sigMass[ntrk] = dataDrivenFile.Get("mvMass_mixed_"+ntrk).Rebin(nbins)
    h_bg[ntrk] = massFile.Get("dvMass_noSelection_"+ntrk).Rebin(nbins)
    h_bg_DVSel[ntrk] = massFile.Get("dvMass_DVSel_"+ntrk).Rebin(nbins)
    h_bg_fullSel[ntrk] = massFile.Get("dvMass_fullSel_"+ntrk).Rebin(nbins)
    h_truthMass[ntrk] = {}
    h_truthMass_DVSel[ntrk] = {}
    h_truthMass_fullSel[ntrk] = {}
    h_truthMass_w[ntrk] = {}
    h_truthMass_DVSel_w[ntrk] = {}
    h_truthMass_fullSel_w[ntrk] = {}
    h_truthMass_noEvtSel[ntrk] = {}
    h_truthMass_DVSel_noEvtSel[ntrk] = {}
    h_truthMass_fullSel_noEvtSel[ntrk] = {}
    for dvtype in typeList:
        h_truthMass[ntrk][dvtype] = mvFile.Get("mvMass_{}_{}_noSel".format(dvtype, ntrk)).Rebin(nbins)
        h_truthMass_DVSel[ntrk][dvtype] = mvFile.Get("mvMass_{}_{}_DVSel".format(dvtype, ntrk)).Rebin(nbins)
        h_truthMass_fullSel[ntrk][dvtype] = mvFile.Get("mvMass_{}_{}_fullSel".format(dvtype, ntrk)).Rebin(nbins)
        h_truthMass_w[ntrk][dvtype] = weightedFile.Get("mvMass_{}_{}_noSel".format(dvtype, ntrk)).Rebin(nbins)
        h_truthMass_DVSel_w[ntrk][dvtype] = weightedFile.Get("mvMass_{}_{}_DVSel".format(dvtype, ntrk)).Rebin(nbins)
        h_truthMass_fullSel_w[ntrk][dvtype] = weightedFile.Get("mvMass_{}_{}_fullSel".format(dvtype, ntrk)).Rebin(nbins)
        h_truthMass_noEvtSel[ntrk][dvtype] = noEvtSelFile.Get("mvMass_{}_{}_noSel".format(dvtype, ntrk)).Rebin(nbins)
        h_truthMass_DVSel_noEvtSel[ntrk][dvtype] = noEvtSelFile.Get("mvMass_{}_{}_DVSel".format(dvtype, ntrk)).Rebin(nbins)
        h_truthMass_fullSel_noEvtSel[ntrk][dvtype] = noEvtSelFile.Get("mvMass_{}_{}_fullSel".format(dvtype, ntrk)).Rebin(nbins)

c = r.TCanvas("c", "c", 800, 700)
c.cd()
sampleLabel = prepareLatex()

h_truthMV = {}
h_lowMass = {}
h_truthMV_weight = {}
h_lowMass_weight = {}
for ntrk in ntrkList:
    sigMass = h_sigMass[ntrk]
    sigMass_noEvtSel = sigMass.Clone("sigMass_noEvtSel")

    setHistColor(sigMass, r.kRed)
    setHistColor(sigMass_noEvtSel, r.kRed)
    
    h_truthMV[ntrk] = h_truthMass[ntrk]["dvType1"].Clone("h_truthMV_"+ntrk)
    h_lowMass[ntrk] = h_truthMass[ntrk]["dvType1"].Clone("h_lowMass_"+ntrk)
    h_lowMass[ntrk].Add(h_truthMass[ntrk]["dvType3"])
    h_truthMV_weight[ntrk] = h_truthMass_w[ntrk]["dvType1"].Clone("h_truthMV_w_"+ntrk)
    h_lowMass_weight[ntrk] = h_truthMass_w[ntrk]["dvType1"].Clone("h_lowMass_w_"+ntrk)
    h_lowMass_weight[ntrk].Add(h_truthMass_w[ntrk]["dvType3"])
    for dvType in typeList:
        if (dvType != "dvType1"):
            h_truthMV[ntrk].Add(h_truthMass[ntrk][dvType])
            h_truthMV_weight[ntrk].Add(h_truthMass_w[ntrk][dvType])

    h_truthMV[ntrk].Draw("hist")
    c.Print("{}/{}.pdf".format(directory, "truthMV_"+ntrk))
    h_truthMV_weight[ntrk].Draw("hist")
    c.Print("{}/{}.pdf".format(directory, "truthMV_weight_"+ntrk))

    leg_noWeight = r.TLegend(0.60, 0.70, 0.85, 0.80)
    decorateLeg(leg_noWeight)
    leg_noWeight.AddEntry(h_truthMass[ntrk]["dvType2"], "Truth: G4+PU DV", "l")
    leg_noWeight.AddEntry(sigMass, "Data-driven template", "l")
    lastBin = sigMass.GetNbinsX() + 1
    c.SetLogy(True)
    setHistColor(sigMass, r.kRed)
    h_truthMass[ntrk]["dvType2"].GetXaxis().SetRange(1, h_truthMass[ntrk]["dvType2"].FindBin(35.))
    h_truthMass[ntrk]["dvType2"].SetMinimum(0.5)
    h_truthMass[ntrk]["dvType2"].Draw("hist e0")
    sigMass.Scale(h_truthMass[ntrk]["dvType2"].Integral()/sigMass.Integral(1, lastBin))
    sigMass.Draw("hist same e0")
    ATLASLabel(0.20, 0.955, label)
    sampleLabel.DrawLatex(0.615, 0.90, "{}, {}".format(tag, SR))
    sampleLabel.DrawLatex(0.615, 0.85, getNtrkLabel(ntrk))
    leg_noWeight.Draw()
    c.Print("{}/{}.pdf".format(directory, "dvType2Mass_sigMass_"+ntrk))

    leg_noEvtSel = r.TLegend(0.60, 0.70, 0.85, 0.80)
    decorateLeg(leg_noEvtSel)
    leg_noEvtSel.AddEntry(h_truthMass_noEvtSel[ntrk]["dvType2"], "Truth: G4+PU DV", "l")
    leg_noEvtSel.AddEntry(sigMass, "Data-driven template", "l")
    bin10 = sigMass_noEvtSel.FindBin(10.)
    lastBin = sigMass_noEvtSel.GetNbinsX() + 1
    h_truthMass_noEvtSel[ntrk]["dvType2"].SetMinimum(0.5)
    h_truthMass_noEvtSel[ntrk]["dvType2"].Draw("hist e0")
    sigMass_noEvtSel.Scale(h_truthMass_noEvtSel[ntrk]["dvType2"].Integral(bin10, lastBin)/sigMass_noEvtSel.Integral(bin10, lastBin))
    sigMass_noEvtSel.Draw("hist e0 same")
    ATLASLabel(0.20, 0.955, label)
    sampleLabel.DrawLatex(0.615, 0.90, "{}, no event selection".format(tag))
    sampleLabel.DrawLatex(0.615, 0.85, getNtrkLabel(ntrk))
    leg_noEvtSel.Draw()
    c.Print("{}/{}.pdf".format(directory, "noEvtSel_dvType2Mass_sigMass_"+ntrk))
    
    frac = h_truthMass[ntrk]["dvType2"].Integral() / h_truthMV[ntrk].Integral()
    legFrac = r.TLegend(0.60, 0.60, 0.85, 0.70)
    decorateLeg(legFrac)
    legFrac.AddEntry(h_truthMV[ntrk], "Total MV", "l")
    legFrac.AddEntry(h_truthMass[ntrk]["dvType2"], "G4+PU DV", "l")
    setHistColor(h_truthMass[ntrk]["dvType2"], r.kRed)
    h_truthMV[ntrk].GetXaxis().SetRange(1, h_truthMV[ntrk].FindBin(30.))
    h_truthMV[ntrk].Draw("hist")
    h_truthMass[ntrk]["dvType2"].Draw("hist same")
    ATLASLabel(0.20, 0.955, label)
    sampleLabel.DrawLatex(0.615, 0.85, "{}, {}".format(tag, SR))
    sampleLabel.DrawLatex(0.615, 0.80, getNtrkLabel(ntrk))
    sampleLabel.DrawLatex(0.615, 0.75, "Fraction: {:.3f}".format(frac))
    legFrac.Draw()
    c.Print("{}/{}.pdf".format(directory, "highMassFrac_"+ntrk))

    # MV Fraction calc
    frac = sigMass.Integral(1, lastBin) / h_bg[ntrk].Integral(1, h_bg[ntrk].GetNbinsX()+1)
    leg_est = r.TLegend(0.60, 0.55, 0.85, 0.70)
    decorateLeg(leg_est)
    leg_est.AddEntry(h_bg[ntrk], "Inclusive DV", "l")
    leg_est.AddEntry(h_truthMV[ntrk], "Merged Vertices", "l")
    leg_est.AddEntry(sigMass, "Data-driven template", "l")
    sigMass.Scale(h_truthMass_w[ntrk]["dvType2"].Integral() / sigMass.Integral(1, lastBin))
    setHistColor(h_truthMV[ntrk], r.kBlue)
    h_bg[ntrk].Draw("hist e0")
    h_truthMV[ntrk].Draw("hist e0 same")
    sigMass.Draw("same hist e0")
    ATLASLabel(0.20, 0.955, label)
    sampleLabel.DrawLatex(0.615, 0.90, "{}, {}".format(tag, SR))
    totalDV = h_bg[ntrk].Integral(1, h_bg[ntrk].GetNbinsX()+1)
    sampleLabel.DrawLatex(0.615, 0.85, getNtrkLabel(ntrk)+", nDV = {:.2f}".format(totalDV))
    sampleLabel.DrawLatex(0.615, 0.80, "MV (high mass): {:.3f}%".format(frac*100))
    highMassMV = h_bg[ntrk].Integral(1, h_bg[ntrk].GetNbinsX()+1) * frac
    sampleLabel.DrawLatex(0.615, 0.75, "MV (high mass): {:.1f}".format(highMassMV))
    leg_est.Draw()
    c.Print("{}/{}.pdf".format(directory, "estimate_noSel_"+ntrk))
    print(highMassMV, h_bg[ntrk].Integral(1, h_bg[ntrk].GetNbinsX()+1), frac)
    print(h_truthMass_w[ntrk]["dvType2"].Integral())


    bin20 = sigMass.FindBin(20.)
    lastBin = sigMass.GetNbinsX() + 1
    highMassFrac = sigMass.Integral(bin20, lastBin) / sigMass.Integral(1, lastBin)
    print(highMassFrac)
