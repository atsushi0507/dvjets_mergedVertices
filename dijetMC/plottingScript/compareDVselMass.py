import ROOT as r
import sys, os
sys.path.append("/Users/amizukam/DVJets/atlasstyle")
from AtlasStyle import *
from AtlasLabel import *
from utils import*
import ctypes

r.gROOT.SetBatch()
SetAtlasStyle()
label = "Internal"

dataSet = "mc16e_trackCleaning"
plotType = "dvSelMass"
directory = "pdfs/" + plotType + "/" + dataSet
if (not os.path.isdir(directory)):
    os.makedirs(directory)
if (not os.path.isdir("rootfiles")):
    os.makedirs(rootfiles)

def getMaximum(histList):
    maximum = -1e10
    for hist in histList:
        if (hist.GetMaximum() > maximum):
            maximum = hist.GetMaximum()
    return maximum

truthFile = r.TFile("rootfiles/mass_{}.root".format(dataSet), "READ")
sigFile = r.TFile("rootfiles/sigAndMass_{}.root".format(dataSet), "READ")

colors = [r.kBlack, r.kRed, r.kBlue, r.kGreen]
ntrkList = ["Ntrk4", "Ntrk5", "Ntrk6", "Ntrk>6"]

# Get histograms
truthMassDict = {}
sigMassDict = {}

# Prepare Latex
sampleLabel = r.TLatex()
sampleLabel.SetNDC()
sampleLabel.SetTextFont(42)
sampleLabel.SetTextAlign(13)
sampleLabel.SetTextSize(0.03)
dataLabel = "{}, di-jet".format(dataSet)

c = r.TCanvas("c", "c", 800, 700)
c.cd()

normValueDict = {"Ntrk4":7.5, "Ntrk5":8.0, "Ntrk6":8.0, "Ntrk>6":9.5}
countValueDict = {"Ntrk4":20., "Ntrk5":10., "Ntrk6":10., "Ntrk>6":10.}
for ntrk in ntrkList:
    truthMassDict[ntrk] = truthFile.Get("mass_MVcand_{}".format(ntrk))
    sigMassDict[ntrk] = sigFile.Get("mergedMass_DVsel_{}".format(ntrk))

    truthMassDict[ntrk].SetLineColor(colors[0])
    truthMassDict[ntrk].SetMarkerColor(colors[0])
    sigMassDict[ntrk].SetLineColor(colors[1])
    sigMassDict[ntrk].SetMarkerColor(colors[1])

    normValue = normValueDict[ntrk]
    countValue = countValueDict[ntrk]

    firstBin = truthMassDict[ntrk].FindBin(normValue)
    secondBin = truthMassDict[ntrk].FindBin(countValue)
    nbins = truthMassDict[ntrk].GetNbinsX() + 1

    try:
        sf = truthMassDict[ntrk].Integral(firstBin, secondBin) / sigMassDict[ntrk].Integral(firstBin, secondBin)
    except ZeroDivisionError:
        print("ZeroDivisionError")
        sf = 1.0

    sigMassDict[ntrk].Sumw2()
    sigMassDict[ntrk].Scale(sf)

    errTruth = ctypes.c_double(0.)
    errSig = ctypes.c_double(0.)
    truthMV = truthMassDict[ntrk].IntegralAndError(secondBin, nbins, errTruth)
    sigMV = sigMassDict[ntrk].IntegralAndError(secondBin, nbins, errSig)

    c.SetLogy(1)

    leg = r.TLegend(0.54, 0.65, 0.85, 0.73)
    decorateLeg(leg)

    leg.AddEntry(truthMassDict["Ntrk4"], "Truth method", "l")
    leg.AddEntry(sigMassDict["Ntrk4"], "Significance method", "l")

    maximum = getMaximum([truthMassDict[ntrk], sigMassDict[ntrk]])
    truthMassDict[ntrk].SetMaximum(maximum * 2.5)
    truthMassDict[ntrk].Draw("hist e0")
    sigMassDict[ntrk].Draw("hist e0 same")
    ATLASLabel(0.20, 0.955, label)
    sampleLabel.DrawLatex(0.56, 0.88, dataLabel)
    sampleLabel.DrawLatex(0.56, 0.83, "Normalized to truth in [{},{}] GeV".format(normValue, countValue))
    sampleLabel.DrawLatex(0.56, 0.78, getNtrkLabel(ntrk))
    leg.Draw()

    sampleLabel.DrawLatex(0.56, 0.63, "Truth MV: {:.1f} \pm {:.1f}".format(truthMV, errTruth.value))
    sampleLabel.DrawLatex(0.56, 0.58, "Sig MV: {:.1f} \pm {:.1f}".format(sigMV, errSig.value))
    sampleLabel.DrawLatex(0.56, 0.53, "Count in m_{MV} \geq " + str(countValue) + " GeV")
    
    c.Print("{}/{}.pdf".format(directory, "truth_sig_mass_"+ntrk + "_logy"))

    c.SetLogy(0)
    truthMassDict[ntrk].SetMaximum(maximum * 1.2)
    truthMassDict[ntrk].Draw("hist e0")
    sigMassDict[ntrk].Draw("hist e0 same")
    ATLASLabel(0.20, 0.955, label)
    sampleLabel.DrawLatex(0.56, 0.88, dataLabel)
    sampleLabel.DrawLatex(0.56, 0.83, "Normalized to truth in [{},{}] GeV".format(normValue, countValue))
    sampleLabel.DrawLatex(0.56, 0.78, getNtrkLabel(ntrk))
    leg.Draw()
    sampleLabel.DrawLatex(0.56, 0.63, "Truth MV: {:.1f} \pm {:.1f}".format(truthMV, errTruth.value))
    sampleLabel.DrawLatex(0.56, 0.58, "Sig MV: {:.1f} \pm {:.1f}".format(sigMV, errSig.value))
    sampleLabel.DrawLatex(0.56, 0.53, "Count in m_{MV} \geq " + str(countValue) + " GeV")
    
    c.Print("{}/{}.pdf".format(directory, "truth_sig_mass_"+ntrk))
