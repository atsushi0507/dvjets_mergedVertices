import ROOT as r
import sys, os
sys.path.append("/Users/amizukam/DVJets/atlasstyle")
from AtlasStyle import *
from AtlasLabel import *
from utils import *

r.gROOT.SetBatch()
SetAtlasStyle()
label = "Internal"

doHIrejection = False
dataSet = "mc16e"
plotType = "truthMass"
directory = "pdfs/" + plotType + "/" + dataSet
if (doHIrejection):
    directory += "_HIrejection"
if (not os.path.isdir(directory)):
    os.makedirs(directory)
if (not os.path.isdir("rootfiles")):
    os.makedirs("rootfiles")

def getMaximum(histList):
    maximum = -1e10
    for hist in histList:
        if (hist.GetMaximum() > maximum):
            maximum = hist.GetMaximum()
    return maximum

nominalFile = r.TFile("rootfiles/mass_{}.root".format(dataSet), "READ")
if (not doHIrejection):
    tcFile = r.TFile("rootfiles/mass_{}_trackCleaning.root".format(dataSet), "READ")
else:
    tcFile = r.TFile("rootfiles/mass_{}_trackCleaning_HIrejection.root".format(dataSet), "READ")

colors = [r.kBlack, r.kRed, r.kBlue, r.kGreen, r.kOrange-2]
ntrkList = ["Ntrk4", "Ntrk5", "Ntrk6", "Ntrk>6"]

# Get histograms
noDVSelDict = {}
DVSelDict = {}
trackCleaningDict = {}
fullSelDict = {}

# Prepare Latex
sampleLabel = r.TLatex()
sampleLabel.SetNDC()
sampleLabel.SetTextFont(42)
sampleLabel.SetTextAlign(13)
sampleLabel.SetTextSize(0.03)
dataLabel = "mc16e, di-jet"

c = r.TCanvas("c", "c", 800, 700)
c.cd()

normValueDict = {"Ntrk4":7.5, "Ntrk5":8.0, "Ntrk6":8.0, "Ntrk>6":9.5}
countValueDict = {"Ntrk4":20., "Ntrk5":10., "Ntrk6":10., "Ntrk>6":10.}
for ntrk in ntrkList:
    noDVSelDict[ntrk] = nominalFile.Get("mass_MVcand_noDVsel_{}".format(ntrk))
    DVSelDict[ntrk] = nominalFile.Get("mass_MVcand_{}".format(ntrk))

    trackCleaningDict[ntrk] = tcFile.Get("mass_MVcand_noDVsel_{}".format(ntrk))
    fullSelDict[ntrk] = tcFile.Get("mass_MVcand_{}".format(ntrk))


    noDVSelDict[ntrk].SetLineColor(colors[0])
    noDVSelDict[ntrk].SetMarkerColor(colors[0])
    DVSelDict[ntrk].SetLineColor(colors[1])
    DVSelDict[ntrk].SetMarkerColor(colors[1])

    trackCleaningDict[ntrk].SetLineColor(colors[2])
    trackCleaningDict[ntrk].SetMarkerColor(colors[2])
    fullSelDict[ntrk].SetLineColor(colors[3])
    fullSelDict[ntrk].SetMarkerColor(colors[3])

    normValue = normValueDict[ntrk]
    countValue = countValueDict[ntrk]

    firstBin = noDVSelDict[ntrk].FindBin(normValue)
    secondBin = noDVSelDict[ntrk].FindBin(countValue)
    nbins = noDVSelDict[ntrk].GetNbinsX()+1

    try:
        sf = noDVSelDict[ntrk].Integral(firstBin, secondBin) / DVSelDict[ntrk].Integral(firstBin, secondBin)
    except ZeroDivisionError:
        print("ZeroDivisionError")
        sf = 1.0
    try:
        sf_tc = noDVSelDict[ntrk].Integral(firstBin, secondBin) / trackCleaningDict[ntrk].Integral(firstBin, secondBin)
    except ZeroDivisionError:
        print("ZeroDivisionError for track cleaning")
        sf_tc = 1.0
    try:
        sf_full = noDVSelDict[ntrk].Integral(firstBin, secondBin) / fullSelDict[ntrk].Integral(firstBin, secondBin)
    except ZeroDivisionError:
        print("ZeroDivisionError for full selection")
        sf_full = 1.0
        
    DVSelDict[ntrk].Sumw2()
    DVSelDict[ntrk].Scale(sf)
    trackCleaningDict[ntrk].Sumw2()
    trackCleaningDict[ntrk].Scale(sf_tc)
    fullSelDict[ntrk].Sumw2()
    fullSelDict[ntrk].Scale(sf_full)

    c.SetLogy(1)

    leg = r.TLegend(0.54, 0.53, 0.85, 0.68)
    decorateLeg(leg)
    leg.AddEntry(noDVSelDict["Ntrk4"], "No DV selection", "l")
    leg.AddEntry(DVSelDict["Ntrk4"], "Pass DV selection", "l")
    leg.AddEntry(trackCleaningDict["Ntrk4"], "Pass track cleaning", "l")
    leg.AddEntry(fullSelDict["Ntrk4"], "Pass DV sel and track cleaning", "l")

    maximum = getMaximum([noDVSelDict[ntrk], DVSelDict[ntrk], trackCleaningDict[ntrk], fullSelDict[ntrk]])
    noDVSelDict[ntrk].SetMaximum(maximum * 2.5)
    
    noDVSelDict[ntrk].Draw("hist e0")
    DVSelDict[ntrk].Draw("hist e0 same")
    trackCleaningDict[ntrk].Draw("hist e0 same")
    fullSelDict[ntrk].Draw("hist e0 same")
    ATLASLabel(0.20, 0.955, label)
    sampleLabel.DrawLatex(0.56, 0.88, dataLabel)
    sampleLabel.DrawLatex(0.56, 0.83, "Normalized to No DV selection hist")
    sampleLabel.DrawLatex(0.56, 0.78, "in mass: [{}, {}] GeV".format(normValue, countValue))
    sampleLabel.DrawLatex(0.56, 0.73, "Truth method, " + getNtrkLabel(ntrk))
    leg.Draw()
    c.Print("{}/{}.pdf".format(directory, "massCompare_"+ntrk+"_logy"))

    c.SetLogy(0)
    noDVSelDict[ntrk].SetMaximum(maximum * 1.2)
    noDVSelDict[ntrk].Draw("hist e0")
    DVSelDict[ntrk].Draw("hist e0 same")
    trackCleaningDict[ntrk].Draw("hist e0 same")
    fullSelDict[ntrk].Draw("hist e0 same")
    ATLASLabel(0.20, 0.955, label)
    sampleLabel.DrawLatex(0.56, 0.88, dataLabel)
    sampleLabel.DrawLatex(0.56, 0.83, "Normalized to No DV selection hist")
    sampleLabel.DrawLatex(0.56, 0.78, "in mass: [{}, {}] GeV".format(normValue, countValue))
    sampleLabel.DrawLatex(0.56, 0.73, "Truth method, " + getNtrkLabel(ntrk))
    leg.Draw()
    c.Print("{}/{}.pdf".format(directory, "massCompare_"+ntrk))
