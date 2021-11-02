import ROOT as r
import sys, os
sys.path.append("/Users/amizukam/DVJets/atlasstyle")
from AtlasStyle import *
from AtlasLabel import *
from utils import *
from ctypes import c_double as double
import math

r.gROOT.SetBatch()
SetAtlasStyle()
label = "Internal"

#SR = "highPtSR"
SR = "tracklessSR"

plotType = "estimateMV"
directory = "pdfs/" + plotType + "/" + SR
if (not os.path.isdir(directory)):
    os.makedirs(directory)

dataFile = r.TFile("/Users/amizukam/DVJets/trackCleaning/rootfiles/DV_mass_{}.root".format(SR), "READ")
mcFile = r.TFile("../../dijetMC/outputFiles/dvMass_mc16e_{}.root".format(SR), "READ")
sigFile = r.TFile("../../dijetMC/plottingScript/rootfiles/sigAndMass_mc16e_{}.root".format(SR), "READ")
truthFile = r.TFile("../../dijetMC/plottingScript/rootfiles/mass_mc16e_{}_HIrejection.root".format(SR), "READ")
truth_tcFile = r.TFile("../../dijetMC/plottingScript/rootfiles/mass_mc16e_trackCleaning_{}_HIrejection.root".format(SR), "READ")

ntrkList = ["Ntrk4", "Ntrk5", "Ntrk6"]

# Histograms
dataMassDict = {}
mcMassDict = {}
mcMassDict_DVsel = {}
mcMassDict_fullSel = {}
sigMassDict = {}
sigMassDict_sigWeight = {}
sigMassDict_weight = {}
truthMassDict = {}
truthMassDict_DVsel = {}
truthMassDict_fullSel = {}

def get_nTracks(ntrk):
    n = ""
    if ntrk == "Ntrk4":
        n = "4track"
    if ntrk == "Ntrk5":
        n = "5track"
    if ntrk == "Ntrk6":
        n = "6track"
    return n


for ntrk in ntrkList:
    #dataMassDict[ntrk] = dataFile.Get("DV_m_{}".format(get_nTracks(ntrk))).Rebin(10)
    dataMassDict[ntrk] = dataFile.Get("mDV_"+ntrk).Rebin(10)
    mcMassDict[ntrk] = mcFile.Get("dvMass_"+ntrk).Rebin(10)
    mcMassDict_DVsel[ntrk] = mcFile.Get("dvMass_DVsel_"+ntrk).Rebin(10)
    mcMassDict_fullSel[ntrk] = mcFile.Get("dvMass_fullSel_"+ntrk).Rebin(10)
    sigMassDict[ntrk] = sigFile.Get("mergedMass_"+ntrk).Rebin(2)
    sigMassDict_sigWeight[ntrk] = sigFile.Get("mergedMass_sigWeight_"+ntrk).Rebin(2)
    sigMassDict_weight[ntrk] = sigFile.Get("mergedMass_weight_"+ntrk).Rebin(2)
    truthMassDict[ntrk] = truthFile.Get("mass_MVcand_noDVsel_"+ntrk)
    truthMassDict_DVsel[ntrk] = truthFile.Get("mass_MVcand_"+ntrk)
    truthMassDict_fullSel[ntrk] = truth_tcFile.Get("mass_MVcand_"+ntrk)
    
c = r.TCanvas("c", "c", 800, 700)
c.cd()

sampleLabel = prepareLatex()
countValueDict = {"Ntrk4": 20., "Ntrk5": 10., "Ntrk6": 10.}

for ntrk in ntrkList:
    mcMassHist_fullSel = mcMassDict_fullSel[ntrk]
    countValue = countValueDict[ntrk]

    bin1 = mcMassHist_fullSel.FindBin(countValue)
    nbins = mcMassHist_fullSel.GetNbinsX() + 1

    lowMassFrac = mcMassHist_fullSel.Integral(1, bin1-1) / mcMassHist_fullSel.Integral(1, nbins)
    highMassFrac = mcMassHist_fullSel.Integral(bin1, nbins) / mcMassHist_fullSel.Integral(1, nbins)

    truthMassHist_fullSel = truthMassDict_fullSel[ntrk]

    mvErr = double(0.)
    totalErr = double(0.)
    nMV = truthMassHist_fullSel.Integral(1, nbins)
    nTotal = mcMassHist_fullSel.Integral(1, nbins)
    mvFrac = truthMassHist_fullSel.IntegralAndError(1, nbins, mvErr) / mcMassHist_fullSel.IntegralAndError(1, nbins, totalErr)
    a = mvErr.value / nTotal
    b = (nMV * totalErr.value) / (nTotal * nTotal)
    error = math.sqrt(a*a + b*b)
    
    print(nTotal, nMV, totalErr.value, mvErr.value)
    print("Merged rate: {:.5f}".format(mvFrac))
    print("Merged rate error: {:.5f}".format(error))

    truthMassHist_DVsel = truthMassDict_DVsel[ntrk]
    mvLowMassFrac_DVsel = truthMassHist_DVsel.Integral(1, bin1-1) / truthMassHist_DVsel.Integral(1, nbins)
    mvHighMassFrac = truthMassHist_DVsel.Integral(bin1, nbins) / truthMassHist_DVsel.Integral(1, nbins)
    
    dataMassHist = dataMassDict[ntrk]
    dataDV = dataMassHist.Integral(1, bin1-1)
    estimateTotalDV = dataDV / lowMassFrac

    totalMV = estimateTotalDV * mvFrac
    mvInSR = totalMV * mvHighMassFrac

    dvInSR = estimateTotalDV - dataDV
    try:
        mvRatio = mvInSR / dvInSR
    except ZeroDivisionError:
        mvRatio = 0.

    sigMassHist = sigMassDict[ntrk]
    sigMassHist_sigWeight = sigMassDict_sigWeight[ntrk]
    sigMassHist_weight = sigMassDict_weight[ntrk]

    sf_nominal = dataDV / sigMassHist.Integral(1, bin1-1) * mvFrac
    sf_sigWeight = dataDV / sigMassHist_sigWeight.Integral(1, bin1-1) * mvFrac
    sf_weight = dataDV / sigMassHist_weight.Integral(1, bin1-1)*mvFrac

    sigMassHist.Sumw2()

    sigMassHist.Scale(sf_nominal)
    sigMassHist_sigWeight.Scale(sf_sigWeight)
    sigMassHist_weight.Scale(sf_weight)

    mvInSR_nominal = sigMassHist.Integral(bin1, nbins)
    mvInSR_sigWeight = sigMassHist_sigWeight.Integral(bin1, nbins)
    mvInSR_weight = sigMassHist_weight.Integral(bin1, nbins)

    bin8 = sigMassHist.FindBin(8.)
    err = double(0.)
    mvInVR_nominal = sigMassHist.IntegralAndError(bin8, bin1, err)
    dataVR = dataMassHist.Integral(bin8, bin1)

    print(ntrk)
    print(dataDV, estimateTotalDV)
    print(totalMV, mvHighMassFrac)
    print(mvInSR, mvInSR_nominal, mvInSR_sigWeight, mvInSR_weight)
    print(dvInSR, mvRatio)
    print(dataVR, "{} +- {}".format(mvInVR_nominal, err.value))

    print("\n")

    dataMassHist.SetLineColor(r.kBlack)
    sigMassHist.SetLineColor(r.kRed)
    sigMassHist_sigWeight.SetLineColor(r.kBlue)
    sigMassHist_weight.SetLineColor(r.kGreen)

    dataMassHist.SetMarkerColor(r.kBlack)
    sigMassHist.SetMarkerColor(r.kRed)
    sigMassHist_sigWeight.SetMarkerColor(r.kBlue)
    sigMassHist_weight.SetMarkerColor(r.kGreen)

    dataMassHist.SetMinimum(0.1)

    leg = r.TLegend(0.54, 0.60, 0.85, 0.78)
    decorateLeg(leg)
    leg.AddEntry(dataMassHist, "Data", "l")
    leg.AddEntry(sigMassHist, "MV, wo weight", "l")
    leg.AddEntry(sigMassHist_sigWeight, "MV with significance weight", "l")
    leg.AddEntry(sigMassHist_weight, "MV  with sig and dR weight", "l")

    c.SetLogy(1)
    dataMassHist.Draw("e0")
    sigMassHist.Draw("hist e0 same")
    sigMassHist_sigWeight.Draw("hist e0 same")
    sigMassHist_weight.Draw("hist e0 same")
    ATLASLabel(0.20, 0.955, label)
    sampleLabel.DrawLatex(0.56, 0.88, "Data")
    sampleLabel.DrawLatex(0.56, 0.83, getNtrkLabel(ntrk))
    leg.Draw()
    c.Print("{}/{}.pdf".format(directory, "DV_"+ntrk))
