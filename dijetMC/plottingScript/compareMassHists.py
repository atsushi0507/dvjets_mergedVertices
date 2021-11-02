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
parser.add_argument("-sr", "--SR", required=True, help="Signal region, 'HighPtSR' or 'TracklessSR'")
parser.add_argument("-tag", required=True, help="The campaign tag, 'a', 'd', or 'e'")
parser.add_argument("-sf", "--suffix", default="", help="File suffix if needed")
parser.add_argument("-label", default="Internal", help="Label for ATLASLabel")
args = parser.parse_args()

label = args.label
SR = args.SR
tag = "mc16{}".format(args.tag)
suffix = args.suffix
dataSet = "{}_{}_{}".format(tag, SR, suffix) if (suffix != "") else "{}_{}".format(tag, SR)

plotType = "mergedMass"
directory = "pdfs/" + plotType + "/" + dataSet
if (not os.path.isdir(directory)):
    os.makedirs(directory)
if (not os.path.isdir("rootfiles")):
    os.makedirs("rootfiles")

truthFile = r.TFile("../outputFiles//extractFactor_{}.root".format(dataSet), "READ")
sigFile = r.TFile("rootfiles/sigAndMass_{}_{}.root".format(tag, SR), "READ")

colors = [r.kBlack, r.kRed, r.kBlue, r.kGreen, r.kOrange]
ntrkList = ["Ntrk4", "Ntrk5", "Ntrk6", "Ntrk>6"]

def getNtrkLabel(ntrk):
    ntrkLabel = ""
    if ntrk == "Ntrk4":
        ntrkLabel = "N_{trk} = 4"
    if ntrk == "Ntrk5":
        ntrkLabel = "N_{trk} = 5"
    if ntrk == "Ntrk6":
        ntrkLabel = "N_{trk} = 6"
    if ntrk ==  "Ntrk>6":
        ntrkLabel = "N_{trk} > 6"
    return ntrkLabel

# Get Histograms
truthMassDict = {}
truthMassDict_DVsel = {}
sigMassDict = {}
sigMassDict_noWeight = {}
sigMassDict_sigWeight = {}
sigMassDict_DVsel = {}

# Prepare Latex
sampleLabel = r.TLatex()
sampleLabel.SetNDC()
sampleLabel.SetTextFont(42)
sampleLabel.SetTextAlign(13)
sampleLabel.SetTextSize(0.03)
dataLabel = dataSet.replace("_HIrejection", "") + ", di-jet"

c = r.TCanvas("c", "c", 800, 700)
c.cd()

normValueDict = {"Ntrk4": 7.5, "Ntrk5": 8.0, "Ntrk6": 8.0, "Ntrk>6": 9.5}
countValueDict = {"Ntrk4": 20., "Ntrk5": 10., "Ntrk6": 10., "Ntrk>6": 10.}
for ntrk in ntrkList:
    truthMassDict[ntrk] = truthFile.Get("mvMass_{}".format(ntrk)).Rebin(10)
    truthMassDict_DVsel[ntrk] = truthFile.Get("mvMass_DVSel_{}".format(ntrk)).Rebin(10)
    sigMassDict[ntrk] = sigFile.Get("mergedMass_weight_{}".format(ntrk)).Rebin(2)
    sigMassDict_noWeight[ntrk] = sigFile.Get("mergedMass_{}".format(ntrk)).Rebin(2)
    sigMassDict_sigWeight[ntrk] = sigFile.Get("mergedMass_sigWeight_{}".format(ntrk)).Rebin(2)
    sigMassDict_DVsel[ntrk] = sigFile.Get("mergedMass_DVsel_{}".format(ntrk)).Rebin(2)

    truthMassDict[ntrk].SetLineColor(colors[0])
    truthMassDict[ntrk].SetMarkerColor(colors[0])
    truthMassDict_DVsel[ntrk].SetLineColor(colors[1])
    truthMassDict_DVsel[ntrk].SetMarkerColor(colors[1])
    sigMassDict[ntrk].SetLineColor(colors[1])
    sigMassDict[ntrk].SetMarkerColor(colors[1])
    sigMassDict_noWeight[ntrk].SetLineColor(colors[2])
    sigMassDict_noWeight[ntrk].SetMarkerColor(colors[2])
    sigMassDict_sigWeight[ntrk].SetLineColor(colors[3])
    sigMassDict_sigWeight[ntrk].SetMarkerColor(colors[3])
    sigMassDict_DVsel[ntrk].SetLineColor(colors[4])
    sigMassDict_DVsel[ntrk].SetMarkerColor(colors[4])

    c.SetLogy(1)

    """
    normValue = normValueDict[ntrk]
    countValue = countValueDict[ntrk]

    firstBin = truthMassDict[ntrk].FindBin(normValue)
    secondBin = truthMassDict[ntrk].FindBin(countValue)
    nbins = truthMassDict[ntrk].GetNbinsX()+1
    """
    firstBin = 1
    nbins = truthMassDict[ntrk].GetNbinsX()+1
    secondBin = truthMassDict[ntrk].FindBin(countValueDict[ntrk])
    normValue = normValueDict[ntrk]
    countValue = countValueDict[ntrk]

    try:
        sf = truthMassDict[ntrk].Integral(firstBin, 10) / sigMassDict[ntrk].Integral(firstBin, 10)
    except ZeroDivisionError:
        sf = 1.0
    sigMassDict[ntrk].Scale(sf)
    try:
        sf_noWeight = truthMassDict[ntrk].Integral(firstBin, nbins) / sigMassDict_noWeight[ntrk].Integral(firstBin, nbins)
    except ZeroDivisionError:
        sf_noWeight = 1.0
    sigMassDict_noWeight[ntrk].Scale(sf_noWeight)
    try:
        sf_sigWeight = truthMassDict[ntrk].Integral(firstBin, nbins) / sigMassDict_sigWeight[ntrk].Integral(firstBin, nbins)
    except ZeroDivisionError:
        sf_sigWeight = 1.0
    sigMassDict_sigWeight[ntrk].Scale(sf_sigWeight)
    try:
        sf_DVsel = truthMassDict[ntrk].Integral(firstBin, nbins) / sigMassDict_DVsel[ntrk].Integral(firstBin, nbins)
    except ZeroDivisionError:
        sf_DVsel = 1.0
    sigMassDict_DVsel[ntrk].Scale(sf_DVsel)
    
    truthMassDict[ntrk].Draw("histo e0")
    sigMassDict_noWeight[ntrk].Draw("histo same e0")
    #sigMassDict_sigWeight[ntrk].Draw("histo same e0")
    #sigMassDict[ntrk].Draw("histo same e0")
    
    ATLASLabel(0.20, 0.955, label)
    sampleLabel.DrawLatex(0.56, 0.93, dataLabel + ", " + getNtrkLabel(ntrk))
    sampleLabel.DrawLatex(0.56, 0.88, "Event preselection")
    sampleLabel.DrawLatex(0.56, 0.83, "Norlalized to truth in [{},{}] GeV".format(normValue, countValue))

    leg = r.TLegend(0.55, 0.65, 0.80, 0.79)
    decorateLeg(leg)
    leg.AddEntry(truthMassDict[ntrkList[0]], "Truth method", "l")
    leg.AddEntry(sigMassDict_noWeight[ntrkList[0]], "No weight", "l")
    #leg.AddEntry(sigMassDict_sigWeight[ntrkList[0]], "Sig. weight", "l")
    #leg.AddEntry(sigMassDict[ntrkList[0]], "Sig. and dR weight", "l")
    leg.Draw()

    line = r.TLine(firstBin, 0., firstBin, truthMassDict[ntrk].GetMaximum()*2.2)
    line.SetLineWidth(3)
    line.SetLineStyle(2)
    #line.Draw()

    errTruthMV = ctypes.c_double(0.)
    truthMV = truthMassDict[ntrk].IntegralAndError(secondBin, nbins, errTruthMV)
    errSigMV = ctypes.c_double(0.)
    sigMV = sigMassDict[ntrk].IntegralAndError(secondBin, nbins, errSigMV)
    errSigNoWeight = ctypes.c_double(0.)
    sigMV_noWeight = sigMassDict_noWeight[ntrk].IntegralAndError(secondBin, nbins, errSigNoWeight)
    errSigSigWeight = ctypes.c_double(0.)
    sigMV_sigWeight = sigMassDict_sigWeight[ntrk].IntegralAndError(secondBin, nbins, errSigSigWeight)

    sampleLabel.DrawLatex(0.56, 0.63, "Truth MV: {:.1f} \pm {:.1f}".format(truthMV, errTruthMV.value))
    sampleLabel.DrawLatex(0.56, 0.58, "Sig w/o weight MV: {:.1f} \pm {:.1f}".format(sigMV_noWeight, errSigNoWeight.value))
    """
    sampleLabel.DrawLatex(0.56, 0.53, "Sig  weight MV: {:.1f} \pm {:.1f}".format(sigMV_sigWeight, errSigSigWeight.value))
    sampleLabel.DrawLatex(0.56, 0.48, "Sig and dR weight MV: {:.1f} \pm {:.1f}".format(sigMV, errSigMV.value))
    sampleLabel.DrawLatex(0.56, 0.43, "Count in m_{MV} \geq " + str(countValue) + " GeV")
    """
    
    c.Print("{}/{}.pdf".format(directory, "mergedMass_{}_logy".format(ntrk)))


    c.SetLogy(0)
    truthMassDict[ntrk].Draw("histo e0")
    sigMassDict_noWeight[ntrk].Draw("histo same e0")
    #sigMassDict_sigWeight[ntrk].Draw("histo same e0")
    #sigMassDict[ntrk].Draw("histo same e0")
    
    ATLASLabel(0.20, 0.955, label)
    sampleLabel.DrawLatex(0.56, 0.93, dataLabel + ", " + getNtrkLabel(ntrk))
    sampleLabel.DrawLatex(0.56, 0.88, "Event preselection")
    sampleLabel.DrawLatex(0.56, 0.83, "Normalized to truth MV: {}".format(truthMassDict[ntrk].Integral()))
    #sampleLabel.DrawLatex(0.56, 0.83, "Norlalized to truth in [{},{}] GeV".format(normValue, countValue))

    leg = r.TLegend(0.55, 0.65, 0.80, 0.79)
    leg.SetFillStyle(0)
    leg.SetBorderSize(0)
    leg.SetLineStyle(0)
    leg.SetTextFont(42)
    leg.SetTextSize(0.030)
    leg.AddEntry(truthMassDict[ntrkList[0]], "Truth method", "l")
    leg.AddEntry(sigMassDict_noWeight[ntrkList[0]], "No weight", "l")
    """
    leg.AddEntry(sigMassDict_sigWeight[ntrkList[0]], "Sig. weight", "l")
    leg.AddEntry(sigMassDict[ntrkList[0]], "Sig. and dR weight", "l")
    """
    leg.Draw()

    line = r.TLine(firstBin, 0., firstBin, truthMassDict[ntrk].GetMaximum()*2.2)
    line.SetLineWidth(3)
    line.SetLineStyle(2)
    #line.Draw()

    errTruthMV = ctypes.c_double(0.)
    truthMV = truthMassDict[ntrk].IntegralAndError(secondBin, nbins, errTruthMV)
    errSigMV = ctypes.c_double(0.)
    sigMV = sigMassDict[ntrk].IntegralAndError(secondBin, nbins, errSigMV)
    errSigNoWeight = ctypes.c_double(0.)
    sigMV_noWeight = sigMassDict_noWeight[ntrk].IntegralAndError(secondBin, nbins, errSigNoWeight)
    errSigSigWeight = ctypes.c_double(0.)
    sigMV_sigWeight = sigMassDict_sigWeight[ntrk].IntegralAndError(secondBin, nbins, errSigSigWeight)

    sampleLabel.DrawLatex(0.56, 0.63, "Truth MV: {:.1f} \pm {:.1f}".format(truthMV, errTruthMV.value))
    sampleLabel.DrawLatex(0.56, 0.58, "Sig w/o weight MV: {:.1f} \pm {:.1f}".format(sigMV_noWeight, errSigNoWeight.value))
    """
    sampleLabel.DrawLatex(0.56, 0.53, "Sig  weight MV: {:.1f} \pm {:.1f}".format(sigMV_sigWeight, errSigSigWeight.value))
    sampleLabel.DrawLatex(0.56, 0.48, "Sig and dR weight MV: {:.1f} \pm {:.1f}".format(sigMV, errSigMV.value))
    sampleLabel.DrawLatex(0.56, 0.43, "Count in m_{MV} \geq " + str(countValue) + " GeV")
    """
    
    c.Print("{}/{}.pdf".format(directory, "mergedMass_{}".format(ntrk)))
