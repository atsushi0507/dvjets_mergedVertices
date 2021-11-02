import ROOT as r
import sys, os
sys.path.append("/Users/amizukam/DVJets/atlasstyle")
from AtlasStyle import *
from AtlasLabel import *
from utils import *

r.gROOT.SetBatch()
SetAtlasStyle()
label = "Internal"

dataSet = "mc16e"
plotType = "DVproperties"
directory = "pdfs/" + plotType + "/" + dataSet
if (not os.path.isdir(directory)):
    os.makedirs(directory)

inputFile = r.TFile("../outputFiles/significance_{}.root".format(dataSet), "READ")
tree = inputFile.Get("trees_SRDV_")

colors = [r.kBlack, r.kRed, r.kBlue, r.kOrange, r.kMagenta]
ntrkList = ["Ntrk4", "Ntrk5", "Ntrk6", "Ntrk>6"]

# Define histograms
rxy1_sameDict = {}
rxy2_sameDict = {}
rxy1_mixedDict = {}
rxy2_mixedDict = {}
rxy1_passDVSameDict = {}
rxy2_passDVSameDict = {}
rxy1_passDVMixedDict = {}
rxy2_passDVMixedDict = {}
for ntrk in ntrkList:
    rxy1_sameDict[ntrk] = r.TH1D("rxy1_same_"+ntrk, ";rxy_{1} mm", 300, 0., 300.)
    rxy2_sameDict[ntrk] = r.TH1D("rxy2_same_"+ntrk, ";rxy_{2} mm", 300, 0., 300.)
    rxy1_mixedDict[ntrk] = r.TH1D("rxy1_mixed_"+ntrk, ";rxy_{1} mm", 300, 0., 300.)
    rxy2_mixedDict[ntrk] = r.TH1D("rxy2_mixed_"+ntrk, ";rxy_{2} mm", 300, 0., 300.)
    rxy1_passDVSameDict[ntrk] = r.TH1D("rxy1_passDVSame_"+ntrk, ";rxy_{1} mm", 300, 0., 300.)
    rxy2_passDVSameDict[ntrk] = r.TH1D("rxy2_passDVSame_"+ntrk, ";rxy_{2} mm", 300, 0., 300.)
    rxy1_passDVMixedDict[ntrk] = r.TH1D("rxy1_passDVMixed_"+ntrk, ";rxy_{1} mm", 300, 0., 300.)
    rxy2_passDVMixedDict[ntrk] = r.TH1D("rxy2_passDVMixed_"+ntrk, ";rxy_{2} mm", 300, 0., 300.)

evtTotal = tree.GetEntries()
evtCounter = 0
for dv in tree:
    evtCounter += 1
    if (evtCounter % 100000 == 0):
        print("Processed {}/{}".format(evtCounter, evtTotal))
    
    rxy1 = dv.rxy1
    rxy2 = dv.rxy2
    isSame = dv.sameEvent
    ntrk = dv.ntrk

    passFiducialCut = dv.dvPassFiducialCut
    passDistCut = dv.dvPassDistCut
    passChi2Cut = dv.dvPassChi2Cut
    passMaterialVeto = dv.dvPassMaterialVeto

    if ntrk < 2:
        continue
    ntrkBin = getNtrkBin(ntrk)
    if (isSame):
        rxy1_sameDict[ntrkBin].Fill(rxy1)
        rxy2_sameDict[ntrkBin].Fill(rxy2)
        if (passFiducialCut and passDistCut and passChi2Cut and passMaterialVeto):
            rxy1_passDVSameDict[ntrkBin].Fill(rxy1)
            rxy2_passDVSameDict[ntrkBin].Fill(rxy2)
    else:
        rxy1_mixedDict[ntrkBin].Fill(rxy1)
        rxy2_mixedDict[ntrkBin].Fill(rxy2)
        if (passFiducialCut and passDistCut and passChi2Cut and passMaterialVeto):
            rxy1_passDVMixedDict[ntrkBin].Fill(rxy1)
            rxy2_passDVMixedDict[ntrkBin].Fill(rxy2)


c = r.TCanvas("c", "c", 800, 700)
# Print histograms
for ntrk in ntrkList:
    rxy1SameHist = rxy1_sameDict[ntrk]
    rxy2SameHist = rxy2_sameDict[ntrk]
    rxy1MixedHist = rxy1_mixedDict[ntrk]
    rxy2MixedHist = rxy2_mixedDict[ntrk]

    rxy1_passDVSameHist = rxy1_passDVSameDict[ntrk]
    rxy2_passDVSameHist = rxy2_passDVSameDict[ntrk]
    rxy1_passDVMixedHist = rxy1_passDVMixedDict[ntrk]
    rxy2_passDVMixedHist = rxy2_passDVMixedDict[ntrk]

    rxy1SameHist.SetLineColor(colors[0])
    rxy2SameHist.SetLineColor(colors[1])
    rxy1MixedHist.SetLineColor(colors[0])
    rxy2MixedHist.SetLineColor(colors[1])

    rxy1_passDVSameHist.SetLineColor(colors[0])
    rxy2_passDVSameHist.SetLineColor(colors[1])
    rxy1_passDVMixedHist.SetLineColor(colors[0])
    rxy2_passDVMixedHist.SetLineColor(colors[1])

    nbins = rxy1SameHist.GetNbinsX()
    rxy1SameHist.SetBinContent(nbins, rxy1SameHist.GetBinContent(nbins)+rxy1SameHist.GetBinContent(nbins+1))
    rxy2SameHist.SetBinContent(nbins, rxy2SameHist.GetBinContent(nbins)+rxy2SameHist.GetBinContent(nbins+1))
    rxy1MixedHist.SetBinContent(nbins, rxy1MixedHist.GetBinContent(nbins)+rxy1MixedHist.GetBinContent(nbins+1))
    rxy2MixedHist.SetBinContent(nbins, rxy2MixedHist.GetBinContent(nbins)+rxy2MixedHist.GetBinContent(nbins+1))

    rxy1_passDVSameHist.SetBinContent(nbins, rxy1_passDVSameHist.GetBinContent(nbins)+rxy1_passDVSameHist.GetBinContent(nbins+1))
    rxy2_passDVSameHist.SetBinContent(nbins, rxy2_passDVSameHist.GetBinContent(nbins)+rxy2_passDVSameHist.GetBinContent(nbins+1))
    rxy1_passDVMixedHist.SetBinContent(nbins, rxy1_passDVMixedHist.GetBinContent(nbins)+rxy1_passDVMixedHist.GetBinContent(nbins+1))
    rxy2_passDVMixedHist.SetBinContent(nbins, rxy2_passDVMixedHist.GetBinContent(nbins)+rxy2_passDVMixedHist.GetBinContent(nbins+1))
    
    leg = r.TLegend(0.75, 0.75, 0.85, 0.85)
    decorateLeg(leg)
    leg.AddEntry(rxy1_sameDict["Ntrk4"], "DV1", "l")
    leg.AddEntry(rxy2_sameDict["Ntrk4"], "DV2", "l")

    c.SetLogy(1)
    rxy1SameHist.Draw("hist")
    rxy2SameHist.Draw("hist same")
    leg.Draw()
    ATLASLabel(0.20, 0.955, label)
    c.Print("{}/{}.pdf".format(directory, "same_dv1_vs_dv2_"+ntrk))

    rp_same = r.TRatioPlot(rxy1SameHist, rxy2SameHist)
    decorateRatioPlot(rp_same)
    ATLASLabel(0.20, 0.955, label)
    leg.Draw()
    c.Print("{}/{}.pdf".format(directory, "ratio_same_dv1_vs_dv2_"+ntrk))

    rxy1MixedHist.Draw("hist")
    rxy2MixedHist.Draw("hist same")
    leg.Draw()
    ATLASLabel(0.20, 0.955, label)
    c.Print("{}/{}.pdf".format(directory, "mixed_dv1_vs_dv2_"+ntrk))

    rp_mixed = r.TRatioPlot(rxy1MixedHist, rxy2MixedHist)
    decorateRatioPlot(rp_mixed)
    ATLASLabel(0.20, 0.955, label)
    leg.Draw()
    c.Print("{}/{}.pdf".format(directory, "ratio_mixed_dv1_vs_dv2_"+ntrk))

    # Pass DV selection
    rxy1_passDVSameHist.Draw("hist")
    rxy2_passDVSameHist.Draw("hist same")
    leg.Draw()
    ATLASLabel(0.20, 0.955, label)
    c.Print("{}/{}.pdf".format(directory, "DVsel_same_dv1_vs_dv2_"+ntrk))

    rp_same_passDV = r.TRatioPlot(rxy1_passDVSameHist, rxy2_passDVSameHist)
    decorateRatioPlot(rp_same_passDV)
    ATLASLabel(0.20, 0.955, label)
    leg.Draw()
    c.Print("{}/{}.pdf".format(directory, "ratio_DVsel_same_dv1_vs_dv2_"+ntrk))

    rxy1_passDVMixedHist.Draw("hist")
    rxy2_passDVMixedHist.Draw("hist same")
    leg.Draw()
    ATLASLabel(0.20, 0.955, label)
    c.Print("{}/{}.pdf".format(directory, "DVsel_mixed_dv1_vs_dv2_"+ntrk))

    rp_mixed_passDV = r.TRatioPlot(rxy1_passDVMixedHist, rxy2_passDVMixedHist)
    decorateRatioPlot(rp_mixed_passDV)
    ATLASLabel(0.20, 0.955, label)
    leg.Draw()
    c.Print("{}/{}.pdf".format(directory, "ratio_DVsel_mixed_dv1_vs_dv2_"+ntrk))
