import ROOT as r
import sys, os
sys.path.append("/Users/amizukam/DVJets/atlasstyle")
from AtlasStyle import *
from AtlasLabel import *
import ctypes
from utils import *

r.gROOT.SetBatch()
SetAtlasStyle()
label = "Internal"

dataSet = "mc16e"
#dataSet = "mc16e_trackCleaning"

plotType = "sigRegion"
directory = "pdfs/" + plotType + "/" + dataSet
if (not os.path.isdir(directory)):
    os.makedirs(directory)
if (not os.path.isdir("rootfiles")):
    os.makedirs("rootfiles")

inputFile = r.TFile("../outputFiles/significance_{}.root".format(dataSet), "READ")
tree = inputFile.Get("trees_SRDV_")

outputFile = r.TFile("rootfiles/{}_{}.root".format(plotType, dataSet), "RECREATE")

colors = [r.kBlack, r.kRed, r.kBlue, r.kOrange, r.kMagenta, r.kCyan]

ntrkList = ["Ntrk4", "Ntrk5", "Ntrk6", "Ntrk>6"]

def getRegionBin(rxy1, rxy2):
    regionBin = ""
    if (rxy1 < 120. and rxy2 < 120.):
        regionBin = "in-in"
    if (rxy1 >= 120. and rxy2 >= 120.):
        regionBin = "out-out"
    if ((rxy1 < 120. and rxy2 >= 120.) or (rxy1 >= 120. and rxy2 < 120.)):
        regionBin = "in-out"
    return regionBin

def getRegionBin2(rxy1):
    regionBin = ""
    if (rxy1 < 120.):
        regionBin = "in"
    else:
        regionBin = "out"
    return regionBin
       
regionList = ["in-in", "out-out", "in-out"]
regionList2 = ["in", "out"]

### Define histograms ###
sigSameDict = {}
sigMixedDict = {}
sigRegionSameDict = {}
sigRegionMixedDict = {}
sigRegionSameDict2 = {}
sigRegionMixedDict2 = {}
for ntrk in ntrkList:
    sigSameDict[ntrk] = r.TH1D("sigSame_{}".format(ntrk), ";Significance", 100, 0., 1000.)
    sigMixedDict[ntrk] = r.TH1D("sigMixed_{}".format(ntrk), ";Significance", 100, 0., 1000.)
    sigRegionSameDict[ntrk] = {}
    sigRegionMixedDict[ntrk] = {}
    sigRegionSameDict2[ntrk] = {}
    sigRegionMixedDict2[ntrk] = {}
    for region in regionList:
        sigRegionSameDict[ntrk][region] = r.TH1D("sigRegionSame_{}_{}".format(ntrk, region), ";Significance", 100, 0., 1000.)
        sigRegionMixedDict[ntrk][region] = r.TH1D("sigRegionMixed_{}_{}".format(ntrk, region), ";Significance", 100, 0., 1000.)
    for region2 in regionList2:
        sigRegionSameDict2[ntrk][region2] = r.TH1D("sigRegionSame2_{}_{}".format(ntrk, region2), ";Significance", 100, 0., 1000.)
        sigRegionMixedDict2[ntrk][region2] = r.TH1D("sigRegionMixed2_{}_{}".format(ntrk, region2), ";Significance", 100, 0., 1000.)

entries = tree.GetEntries()
evtCounter = 0
for dv in tree:
    evtCounter += 1
    if (evtCounter % 100000 == 0):
        print("Processed {}/{}".format(evtCounter, entries))
    ntrk = dv.ntrk
    sig = dv.significance
    mass = dv.mass
    isSame = dv.sameEvent
    rxy1 = dv.rxy1
    rxy2 = dv.rxy2

    ntrkBin = getNtrkBin(ntrk)
    regionBin = getRegionBin(rxy1, rxy2)
    regionBin2 = getRegionBin2(rxy1)
    if (isSame):
        sigSameDict[ntrkBin].Fill(sig)
        sigRegionSameDict[ntrkBin][regionBin].Fill(sig)
        sigRegionSameDict2[ntrkBin][regionBin2].Fill(sig)
    else:
        sigMixedDict[ntrkBin].Fill(sig)
        sigRegionMixedDict[ntrkBin][regionBin].Fill(sig)
        sigRegionMixedDict2[ntrkBin][regionBin2].Fill(sig)
    
# Prepare Latex
sampleLabel = r.TLatex()
sampleLabel.SetNDC()
sampleLabel.SetTextFont(42)
sampleLabel.SetTextAlign(13)
sampleLabel.SetTextSize(0.03)
dataLabel = dataSet + ", di-jet"

leg = r.TLegend(0.65, 0.55, 0.85, 0.70)
decorateLeg(leg)
leg.AddEntry(sigRegionSameDict["Ntrk4"]["in-in"], "Same", "l")
leg.AddEntry(sigRegionMixedDict["Ntrk4"]["in-in"], "Mixed", "l")

# Save histograms
c = r.TCanvas("c", "c", 800, 700)
c.cd()
for ntrk in ntrkList:
    sigSameHist = sigSameDict[ntrk]
    sigMixedHist = sigMixedDict[ntrk]
    
    nBins = sigSameHist.GetNbinsX()
    sigSameHist.SetBinContent(nBins, sigSameHist.GetBinContent(nBins) + sigSameHist.GetBinContent(nBins+1))
    sigMixedHist.SetBinContent(nBins, sigMixedHist.GetBinContent(nBins) + sigMixedHist.GetBinContent(nBins+1))

    bin100 = sigSameHist.FindBin(100.)
    sf = sigSameHist.Integral(bin100, nBins) / sigMixedHist.Integral(bin100, nBins)
    sigMixedHist.Sumw2()
    sigMixedHist.Scale(sf)

    sigSameHist.SetLineColor(r.kBlack)
    sigSameHist.SetMarkerColor(r.kBlack)
    sigMixedHist.SetLineColor(r.kRed)
    sigMixedHist.SetMarkerColor(r.kRed)

    sigSameHist.SetMaximum(sigMixedHist.GetMaximum()*1.2)
    leg_sig = r.TLegend(0.65, 0.55, 0.85, 0.70)
    decorateLeg(leg_sig)
    leg_sig.AddEntry(sigSameHist, "Same", "l")
    leg_sig.AddEntry(sigMixedHist, "Mixed", "l")

    sigSameHist.Draw("hist e")
    sigMixedHist.Draw("hist e same")
    ATLASLabel(0.20, 0.955, label)
    sampleLabel.DrawLatex(0.65, 0.85, dataLabel)
    sampleLabel.DrawLatex(0.65, 0.80, "Event preselection")
    sampleLabel.DrawLatex(0.65, 0.75, getNtrkLabel(ntrk))
    leg_sig.Draw()
    c.Print("{}/{}.pdf".format(directory, "significance_{}".format(ntrk)))

    rp_sig = r.TRatioPlot(sigSameHist, sigMixedHist)
    decorateRatioPlot(rp_sig)
    ATLASLabel(0.20, 0.955, label)
    sampleLabel.DrawLatex(0.65, 0.85, dataLabel)
    sampleLabel.DrawLatex(0.65, 0.80, "Event preselection")
    sampleLabel.DrawLatex(0.65, 0.75, getNtrkLabel(ntrk))
    leg_sig.Draw()
    c.Print("{}/{}.pdf".format(directory, "ratio_significance_"+ntrk))
    
    
    for region in regionList:
        sigRegionSameHist = sigRegionSameDict[ntrk][region]
        sigRegionMixedHist = sigRegionMixedDict[ntrk][region]

        bin100 = sigRegionSameHist.FindBin(100.)
        nBins = sigRegionSameHist.GetNbinsX()
        sigRegionSameHist.SetBinContent(nBins, sigRegionSameHist.GetBinContent(nBins) + sigRegionSameHist.GetBinContent(nBins+1))
        sigRegionMixedHist.SetBinContent(nBins, sigRegionMixedHist.GetBinContent(nBins) + sigRegionMixedHist.GetBinContent(nBins+1))

        sigRegionSameHist.SetLineColor(r.kBlack)
        sigRegionSameHist.SetMarkerColor(r.kBlack)
        sigRegionMixedHist.SetLineColor(r.kRed)
        sigRegionMixedHist.SetMarkerColor(r.kRed)

        sf = sigRegionSameHist.Integral(bin100, nBins+1) / sigRegionMixedHist.Integral(bin100, nBins+1)
        #sf = sigRegionSameHist.Integral(bin400, bin900) / sigRegionMixedHist.Integral(bin400, bin900)
        sigRegionMixedHist.Sumw2()
        sigRegionMixedHist.Scale(sf)

        sigRegionSameHist.SetMaximum(sigRegionMixedHist.GetMaximum()*1.2)

        sigRegionSameHist.Draw("hist e")
        sigRegionMixedHist.Draw("hist same e")
        ATLASLabel(0.20, 0.955, label)
        sampleLabel.DrawLatex(0.65, 0.85, dataLabel)
        sampleLabel.DrawLatex(0.65, 0.80, "Event preselection")
        sampleLabel.DrawLatex(0.65, 0.75, getNtrkLabel(ntrk)+region)
        leg.Draw()
        c.Print("{}/{}.pdf".format(directory, "significance_{}_{}".format(ntrk, region)))

        sigRegionSameIn = sigRegionSameDict2[ntrk]["in"]
        sigRegionSameOut = sigRegionSameDict2[ntrk]["out"]
        sigRegionMixedIn = sigRegionMixedDict2[ntrk]["in"]
        sigRegionMixedOut = sigRegionMixedDict2[ntrk]["out"]

        nBins = sigRegionSameIn.GetNbinsX()
        sigRegionSameIn.SetBinContent(nBins, sigRegionSameIn.GetBinContent(nBins)+sigRegionSameIn.GetBinContent(nBins+1))
        sigRegionSameOut.SetBinContent(nBins, sigRegionSameOut.GetBinContent(nBins)+sigRegionSameOut.GetBinContent(nBins+1))
        sigRegionMixedIn.SetBinContent(nBins, sigRegionMixedIn.GetBinContent(nBins)+sigRegionMixedIn.GetBinContent(nBins+1))
        sigRegionMixedOut.SetBinContent(nBins, sigRegionMixedOut.GetBinContent(nBins)+sigRegionMixedOut.GetBinContent(nBins+1))

        sigRegionSameIn.SetLineColor(r.kBlack)
        sigRegionSameIn.SetMarkerColor(r.kBlack)
        sigRegionSameOut.SetLineColor(r.kRed)
        sigRegionSameOut.SetMarkerColor(r.kRed)
        sigRegionMixedIn.SetLineColor(r.kBlack)
        sigRegionMixedIn.SetMarkerColor(r.kBlack)
        sigRegionMixedOut.SetLineColor(r.kRed)
        sigRegionMixedOut.SetMarkerColor(r.kRed)

        
        legSame = r.TLegend(0.65, 0.55, 0.85, 0.70)
        decorateLeg(legSame)
        legSame.AddEntry(sigRegionSameIn, "in", "l")
        legSame.AddEntry(sigRegionSameOut, "out", "l")

        sigRegionSameIn.SetMaximum(sigRegionSameOut.GetMaximum()*1.2)
        sf = sigRegionSameIn.Integral(bin100, nBins) / sigRegionSameOut.Integral(bin100, nBins)
        sigRegionSameOut.Scale(sf)
        
        sigRegionSameIn.Draw("hist e")
        sigRegionSameOut.Draw("hist e same")
        ATLASLabel(0.20, 0.955, label)
        sampleLabel.DrawLatex(0.65, 0.85, dataLabel)
        sampleLabel.DrawLatex(0.65, 0.80, "Event preselection")
        sampleLabel.DrawLatex(0.65, 0.75, getNtrkLabel(ntrk)+region)
        legSame.Draw()
        c.Print("{}/{}.pdf".format(directory, "sigRegionSame_inout_"+ntrk))

        legMixed = r.TLegend(0.65, 0.55, 0.85, 0.70)
        decorateLeg(legMixed)
        legMixed.AddEntry(sigRegionMixedIn, "in", "l")
        legMixed.AddEntry(sigRegionMixedOut, "out", "l")

        sigRegionMixedIn.SetMaximum(sigRegionMixedOut.GetMaximum()*1.2)
        sf = sigRegionMixedIn.Integral(bin100, nBins) / sigRegionMixedOut.Integral(bin100, nBins)
        sigRegionMixedOut.Scale(sf)
        
        sigRegionMixedIn.Draw("hist e")
        sigRegionMixedOut.Draw("hist e same")
        ATLASLabel(0.20, 0.955, label)
        sampleLabel.DrawLatex(0.65, 0.85, dataLabel)
        sampleLabel.DrawLatex(0.65, 0.80, "Event preselection")
        sampleLabel.DrawLatex(0.65, 0.75, getNtrkLabel(ntrk)+region)
        legMixed.Draw()
        c.Print("{}/{}.pdf".format(directory, "sigRegionMixed_inout_"+ntrk))
        
    for region2 in regionList2:
        sigRegionSameHist = sigRegionSameDict2[ntrk][region2]
        sigRegionMixedHist = sigRegionMixedDict2[ntrk][region2]

        sigRegionSameHist.SetLineColor(r.kBlack)
        sigRegionSameHist.SetMarkerColor(r.kBlack)
        sigRegionMixedHist.SetLineColor(r.kBlue)
        sigRegionMixedHist.SetMarkerColor(r.kBlue)

        bin100 = sigRegionSameHist.FindBin(100.)
        nBins = sigRegionSameHist.GetNbinsX()
        sigRegionSameHist.SetMaximum(sigRegionMixedHist.GetMaximum()*1.2)
        sf_region2 = sigRegionSameHist.Integral(bin100, nBins) / sigRegionMixedHist.Integral(bin100, nBins)
        sigRegionMixedHist.Sumw2()
        sigRegionMixedHist.Scale(sf_region2)

        sigRegionSameHist.Draw("hist e")
        sigRegionMixedHist.Draw("hist same e")
        ATLASLabel(0.20, 0.955, label)
        sampleLabel.DrawLatex(0.65, 0.85, dataLabel)
        sampleLabel.DrawLatex(0.65, 0.80, "Event preselection")
        sampleLabel.DrawLatex(0.65, 0.75, getNtrkLabel(ntrk)+", "+region2)
        leg.Draw()
        c.Print("{}/{}.pdf".format(directory, "significance_{}_{}".format(ntrk, region2)))

        rp_region2 = r.TRatioPlot(sigRegionSameHist, sigRegionMixedHist)
        decorateRatioPlot(rp_region2)
        ATLASLabel(0.20, 0.955, label)
        sampleLabel.DrawLatex(0.65, 0.85, dataLabel)
        sampleLabel.DrawLatex(0.65, 0.80, "Event preselection")
        sampleLabel.DrawLatex(0.65, 0.75, getNtrkLabel(ntrk)+", " + region2)
        leg.Draw()
        c.Print("{}/{}.pdf".format(directory, "ratio_significance_{}_{}".format(ntrk, region2)))
        

outputFile.Write()
outputFile.Close()
