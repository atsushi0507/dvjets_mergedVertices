import ROOT as r
import sys, os
sys.path.append("/Users/amizukam/DVJets/atlasstyle")
from AtlasStyle import *
from AtlasLabel import *
from utils import *
import ctypes

r.gROOT.SetBatch()
SetAtlasStyle()
label = "Internal"

#SR = "highPtSR"
SR = "tracklessSR"

plotType = "mcAndData"
directory = "pdfs/" + plotType + "/"+ SR
if (not os.path.isdir(directory)):
    os.makedirs(directory)

#dataFile = r.TFile("rootfiles/sigAndMass_data_newTrackCleaning.root", "READ")
#dataFile = r.TFile("rootfiles/sigAndMass_data_newSamples.root", "READ")
dataFile = r.TFile("rootfiles/sigAndMass_"+SR+".root", "READ")
#mcFile = r.TFile("../../dijetMC/plottingScript/rootfiles/mass_mc16e_HIrejection_newSample.root", "READ")
mcFile = r.TFile("../../dijetMC/plottingScript/rootfiles/mass_mc16e_"+SR+"_HIrejection.root", "READ")

ntrkList = ["Ntrk4", "Ntrk5", "Ntrk6", "Ntrk>6"]

# Get Histograms
mcMassDict = {}
dataMassDict = {}

c = r.TCanvas("c", "c", 800, 700)
c.cd()

# Prepare Latex
sampleLabel = r.TLatex()
sampleLabel.SetNDC()
sampleLabel.SetTextFont(42)
sampleLabel.SetTextAlign(13)
sampleLabel.SetTextSize(0.03)

normValueDict = {"Ntrk4": 7.5, "Ntrk5": 8.0, "Ntrk6": 8.0, "Ntrk>6":9.5}
countValueDict = {"Ntrk4": 20., "Ntrk5": 10., "Ntrk6": 10., "Ntrk>6":10.}
for ntrk in ntrkList:
    mcMassDict[ntrk] = mcFile.Get("mass_MVcand_noDVsel_"+ntrk)
    #mcMassDict[ntrk] = mcFile.Get("mass_MVcand_"+ntrk)
    dataMassDict[ntrk] = dataFile.Get("mergedMass_"+ntrk).Rebin(2)

    mcMassDict[ntrk].SetLineColor(r.kBlack)
    mcMassDict[ntrk].SetMarkerColor(r.kBlack)
    dataMassDict[ntrk].SetLineColor(r.kRed)
    dataMassDict[ntrk].SetMarkerColor(r.kRed)

    leg = r.TLegend(0.64, 0.54, 0.85, 0.64)
    decorateLeg(leg)
    leg.AddEntry(mcMassDict[ntrkList[0]], "MC truth", "l")
    leg.AddEntry(dataMassDict[ntrkList[0]], "Data", "l")

    normValue = normValueDict[ntrk]
    countValue = countValueDict[ntrk]

    firstBin = mcMassDict[ntrk].FindBin(normValue)
    secondBin = mcMassDict[ntrk].FindBin(countValue)
    nbins = mcMassDict[ntrk].GetNbinsX()+1

    sf = mcMassDict[ntrk].Integral(firstBin, secondBin) / dataMassDict[ntrk].Integral(firstBin, secondBin)
    dataMassDict[ntrk].Sumw2()
    dataMassDict[ntrk].Scale(sf)
    
    c.SetLogy(1)
    
    mcMassDict[ntrk].Draw("hist e0")
    dataMassDict[ntrk].Draw("hist e0 same")
    sampleLabel.DrawLatex(0.65, 0.88, "Data, {}".format(SR))
    sampleLabel.DrawLatex(0.65, 0.83, "Event preselection")
    sampleLabel.DrawLatex(0.65, 0.78, getNtrkLabel(ntrk))
    sampleLabel.DrawLatex(0.65, 0.73, "Normalized to truth mass")
    sampleLabel.DrawLatex(0.65, 0.68, "in mass: [{}, {}] GeV".format(normValue, countValue))
    leg.Draw()
    ATLASLabel(0.20, 0.955, label)
    c.Print("{}/{}.pdf".format(directory, "noDVsel_"+ntrk+"_logy"))

    c.SetLogy(0)

    mcMassDict[ntrk].Draw("hist e0")
    dataMassDict[ntrk].Draw("hist e0 same")
    sampleLabel.DrawLatex(0.65, 0.88, "Data, {}".format(SR))
    sampleLabel.DrawLatex(0.65, 0.83, "Event preselection")
    sampleLabel.DrawLatex(0.65, 0.78, getNtrkLabel(ntrk))
    sampleLabel.DrawLatex(0.65, 0.73, "Normalized to truth mass")
    sampleLabel.DrawLatex(0.65, 0.68, "in mass: [{}, {}] GeV".format(normValue, countValue))
    leg.Draw()
    ATLASLabel(0.20, 0.955, label)
    c.Print("{}/{}.pdf".format(directory, "noDVsel_"+ntrk))

    errTruth = ctypes.c_double(0.)
    nMV_truth = mcMassDict[ntrk].IntegralAndError(secondBin, nbins, errTruth)
    errData = ctypes.c_double(0.)
    nMV_Data = dataMassDict[ntrk].IntegralAndError(secondBin, nbins, errData)

    print("nMV for "+ntrk)
    print("Truth: {} +- {}".format(nMV_truth, errTruth.value))
    print("Data: {} +- {}".format(nMV_Data, errData.value))
