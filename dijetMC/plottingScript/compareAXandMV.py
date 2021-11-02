import ROOT as r
import ctypes
import sys, os
sys.path.append("/Users/amizukam/DVJets/atlasstyle")
from AtlasStyle import *
from AtlasLabel import *

r.gROOT.SetBatch()
SetAtlasStyle()
label = "Internal"

#dataSet = "mc16e"
dataSet = "mc16e_new"
#dataSet = "mc16e_trackCleaning"

plotType = "axAndMV"
directory = "pdfs/" + plotType + "/" + dataSet
if (not os.path.isdir(directory)):
    os.makedirs(directory)
if (not os.path.isdir("rootfiles")):
    os.makedirs("rootfiles")

axFile = r.TFile("rootfiles/truthAXMass_{}.root".format(dataSet), "READ")
mvFile = r.TFile("rootfiles/truthMVMass_{}.root".format(dataSet), "READ")

colors = [r.kBlack, r.kRed]
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
truthMVDict = {}
truthAXDict = {}

# Prepare Latex
sampleLabel = r.TLatex()
sampleLabel.SetNDC()
sampleLabel.SetTextFont(42)
sampleLabel.SetTextAlign(13)
sampleLabel.SetTextSize(0.03)
dataLabel = dataSet + ", di-jet"

c = r.TCanvas("c", "c", 800, 700)
c.cd()

normValueDict = {"Ntrk4": 7.5, "Ntrk5": 8.0, "Ntrk6": 8.0, "Ntrk>6": 9.5}
countValueDict = {"Ntrk4": 20., "Ntrk5": 10., "Ntrk6": 10., "Ntrk>6": 10.}
for ntrk in ntrkList:
    truthMVDict[ntrk] = mvFile.Get("mv_{}".format(ntrk))
    truthAXDict[ntrk] = axFile.Get("ax_{}".format(ntrk))

    truthMVDict[ntrk].SetLineColor(colors[0])
    truthMVDict[ntrk].SetMarkerColor(colors[0])
    truthAXDict[ntrk].SetLineColor(colors[1])
    truthAXDict[ntrk].SetMarkerColor(colors[1])

    c.SetLogy(1)

    normValue = normValueDict[ntrk]
    countValue = countValueDict[ntrk]

    firstBin = truthMVDict[ntrk].FindBin(normValue)
    secondBin = truthMVDict[ntrk].FindBin(countValue)
    nbins = truthMVDict[ntrk].GetNbinsX() + 1
    """
    sf = truthMVDict[ntrk].Integral(firstBin, nbins) / truthAXDict[ntrk].Integral(firstBin, nbins)
    truthAXDict[ntrk].Scale(sf)
    """
    
    truthMVDict[ntrk].DrawNormalized("histo e0")
    truthAXDict[ntrk].DrawNormalized("histo same e0")
    ATLASLabel(0.20, 0.955, label)
    sampleLabel.DrawLatex(0.61, 0.93, dataLabel + ", " + getNtrkLabel(ntrk))
    sampleLabel.DrawLatex(0.61, 0.88, "Event preselection")
    sampleLabel.DrawLatex(0.61, 0.83, "Norlalized in m_{MV} \geq " + str(normValue) + " GeV")

    leg = r.TLegend(0.60, 0.70, 0.80, 0.79)
    leg.SetFillStyle(0)
    leg.SetBorderSize(0)
    leg.SetLineStyle(0)
    leg.SetTextFont(42)
    leg.SetTextSize(0.035)
    leg.AddEntry(truthMVDict[ntrkList[0]], "Merged vertices", "l")
    leg.AddEntry(truthAXDict[ntrkList[0]], "Accidental crossings", "l")
    leg.Draw()

    line = r.TLine(firstBin, 0., firstBin, truthMVDict[ntrk].GetMaximum()*2.2)
    line.SetLineWidth(3)
    line.SetLineStyle(2)
    line.Draw()

    
    errTruthMV = ctypes.c_double(0.)
    truthMV = truthMVDict[ntrk].IntegralAndError(secondBin, nbins, errTruthMV)
    errTruthAX = ctypes.c_double(0.)
    truthAX = truthAXDict[ntrk].IntegralAndError(secondBin, nbins, errTruthAX)

    sampleLabel.DrawLatex(0.61, 0.68, "MV: {:.1f} \pm {:.1f}".format(truthMV, errTruthMV.value))
    sampleLabel.DrawLatex(0.61, 0.63, "AX: {:.1f} \pm {:.1f}".format(truthAX, errTruthAX.value))
    sampleLabel.DrawLatex(0.61, 0.58, "Count in m_{MV} \geq " + str(countValue) + " GeV")
    
    c.Print("{}/{}.pdf".format(directory, "mv_vs_ax_{}".format(ntrk)))
