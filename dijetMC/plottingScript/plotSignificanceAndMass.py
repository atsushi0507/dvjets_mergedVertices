import ROOT as r
import sys, os
sys.path.append("/Users/amizukam/DVJets/atlasstyle")
from AtlasStyle import *
from AtlasLabel import *
import ctypes
from utils import *
import argparse

r.gROOT.SetBatch()
SetAtlasStyle()
label = "Internal"

##### Settings #####
doSystStudy = False
normSig = 100.

parser = argparse.ArgumentParser()
parser.add_argument("-sr", "--SR", required=True, help="signal region, 'HighPtSR', or 'TracklessSR'")
parser.add_argument("-tag", required=True, help="The campaign tag, 'a', 'd', or 'e'")
parser.add_argument("-t", "--trackCleaning", action="store_true", help="Use track cleaning file")
args = parser.parse_args()

tag = "mc16{}".format(args.tag)
SR = args.SR
useTrackCleaningFile = args.trackCleaning

dataSet = "{}_{}_trackCleaning".format(tag, SR) if (useTrackCleaningFile) else "{}_{}".format(tag, SR)

plotType = "sigAndMass"
directory = "pdfs/" + plotType + "/" + dataSet
if (doSystStudy):
    directory += "_syst_norm{}".format(int(normSig))
if (not os.path.isdir(directory)):
    os.makedirs(directory)
if (not os.path.isdir("rootfiles")):
    os.makedirs("rootfiles")

inputFile = r.TFile("../outputFiles/significance_{}.root".format(dataSet), "READ")
tree = inputFile.Get("trees_SRDV_")

if (not doSystStudy):
    outputFile = r.TFile("rootfiles/{}_{}.root".format(plotType, dataSet), "RECREATE")
else:
    outputFile = r.TFile("rootfiles/{}_{}_syst_norm{}.root".format(plotType, dataSet, int(normSig)), "RECREATE")

colors = [r.kGreen, r.kRed, r.kBlue, r.kOrange, r.kMagenta, r.kCyan]

ntrkList = ["Ntrk4", "Ntrk5", "Ntrk6", "Ntrk>6"]

def plotSigRatio(same, mixed, sel, ntrkBin, canvas, directory, dataLabel, label, leg):
    sigRatio = same.Clone("sigRatio_{}".format(ntrkBin))
    bin1 = same.FindBin(normSig)
    bin2 = same.GetNbinsX()+1
    sf = same.Integral(bin1, bin2) / mixed.Integral(bin1, bin2)
    mixed.Sumw2()
    mixed.Scale(sf)
    sigRatio.Divide(mixed)

    sampleLabel = r.TLatex()
    sampleLabel.SetNDC()
    sampleLabel.SetTextFont(42)
    sampleLabel.SetTextAlign(13)
    sampleLabel.SetTextSize(0.03)

    canvas.SetLogy(0)
    sigRatio.Draw("histo")
    ATLASLabel(0.20, 0.955, label)
    sampleLabel.DrawLatex(0.65, 0.85, dataLabel)
    sampleLabel.DrawLatex(0.65, 0.80, "Event preselection")
    if (not sel == ""):
        sampleLabel.DrawLatex(0.65, 0.75, "Pass " + sel)
    sampleLabel.DrawLatex(0.65, 0.70, getNtrkLabel(ntrkBin))
    if (sel == ""):
        canvas.Print("{}/{}.pdf".format(directory, "sigRatio_"+ntrkBin))
    else:
        canvas.Print("{}/{}.pdf".format(directory, "sigRatio_"+sel+"_"+ntrkBin))

    mixed.SetLineColor(r.kRed)
    mixed.SetMarkerColor(r.kRed)
    same.Draw("histo")
    mixed.Draw("histo same")
    ATLASLabel(0.20, 0.955, label)
    sampleLabel.DrawLatex(0.65, 0.85, dataLabel)
    sampleLabel.DrawLatex(0.65, 0.80, "Event preselection")
    if (not sel == ""):
        sampleLabel.DrawLatex(0.65, 0.75, "Pass " + sel)
    sampleLabel.DrawLatex(0.65, 0.70, getNtrkLabel(ntrkBin))
    leg.Draw()
    if (sel == ""):
        canvas.Print("{}/{}.pdf".format(directory, "sig_"+ntrkBin))
    else:
        canvas.Print("{}/{}.pdf".format(directory, "sig_"+sel+"_"+ntrkBin))

    canvas.SetLogy(1)
    mixed.SetLineColor(r.kRed)
    mixed.SetMarkerColor(r.kRed)
    same.Draw("histo")
    mixed.Draw("histo same")
    ATLASLabel(0.20, 0.955, label)
    sampleLabel.DrawLatex(0.65, 0.85, dataLabel)
    sampleLabel.DrawLatex(0.65, 0.80, "Event preselection")
    if (not sel == ""):
        sampleLabel.DrawLatex(0.65, 0.75, "Pass " + sel)
    sampleLabel.DrawLatex(0.65, 0.70, getNtrkLabel(ntrkBin))
    leg.Draw()
    if (sel == ""):
        canvas.Print("{}/{}.pdf".format(directory, "sig_"+ntrkBin+"_logy"))
    else:
        canvas.Print("{}/{}.pdf".format(directory, "sig_"+sel+"_"+ntrkBin+"_logy"))

    # For normalizing study
    mixed.Add(same, -1)
    err = ctypes.c_double(0.)
    nMV = mixed.IntegralAndError(1, bin1-1, err)
    print(ntrkBin, nMV, err.value)
    
    return sigRatio

def plotdRRatio(same, mixed, sel, ntrkBin, canvas, dataLabel, label, leg):
    same.Sumw2()
    mixed.Sumw2()
    same.Scale(1./same.Integral())
    mixed.Scale(1./mixed.Integral())
    mixed.SetLineColor(r.kRed)
    mixed.SetMarkerColor(r.kRed)
    same.Draw("histo e")
    mixed.Draw("histo same e")
    ATLASLabel(0.20, 0.955, label)
    leg.Draw()
    sampleLabel.DrawLatex(0.65, 0.85, dataLabel)
    sampleLabel.DrawLatex(0.65, 0.80, "Event preselection")
    if (not sel == ""):
        sampleLabel.DrawLatex(0.65, 0.75, "Pass " + sel)
    sampleLabel.DrawLatex(0.65, 0.70, getNtrkLabel(ntrkBin))
    if (sel == ""):
        canvas.Print("{}/{}.pdf".format(directory, "dR_"+ntrkBin))
    else:
        canvas.Print("{}/{}.pdf".format(directory, "dR_"+sel+"_"+ntrkBin))

    drRatio = same.Clone("drRatio_"+ntrkBin)
    drRatio.Divide(mixed)
    drRatio.Draw("histo e")
    ATLASLabel(0.20, 0.955, label)
    if (not sel == ""):
        canvas.Print("{}/{}.pdf".format(directory, "dRratio_"+sel+ntrkBin))
    return drRatio

def plotMassHist(hist, sel, weightType, ntrkBin, canvas, sampleLabel, dataLabel, label):
    weigt = ""
    if (weightType == ""):
        weight = "noWeight_"
    if (weightType == "sigWeight"):
        weight = "sigWeight_"
    if (weightType == "drWeight"):
        weight = "drWeight_"
    if (weightType == "weight"):
        weight = "weight_"
       
    canvas.SetLogy(1)
    hist.Draw("hist")
    ATLASLabel(0.20, 0.955, label)
    sampleLabel.DrawLatex(0.65, 0.85, dataLabel)
    sampleLabel.DrawLatex(0.65, 0.80, getNtrkLabel(ntrkBin))
    if (sel == ""):
        sampleLabel.DrawLatex(0.65, 0.75, "Pass "+sel)
        canvas.Print("{}/{}.pdf".format(directory, "mergedMass_"+weight+ntrkBin+"_logy"))
    else:
        canvas.Print("{}/{}.pdf".format(directory, "mergedMass_"+weight+sel+"_"+ntrkBin+"_logy"))

    canvas.SetLogy(0)
    hist.Draw("hist")
    ATLASLabel(0.20, 0.955, label)
    sampleLabel.DrawLatex(0.65, 0.85, dataLabel)
    sampleLabel.DrawLatex(0.65, 0.80, getNtrkLabel(ntrkBin))
    if (sel == ""):
        sampleLabel.DrawLatex(0.65, 0.75, "Pass "+sel)
        canvas.Print("{}/{}.pdf".format(directory, "mergedMass_"+weight+ntrkBin))
    else:
        canvas.Print("{}/{}.pdf".format(directory, "mergedMass_"+weight+sel+"_"+ntrkBin))

### Define histograms ###
# No selection
sigSameDict = {}
sigMixedDict = {}
sigRatioDict = {}
dRSameDict = {}
dRMixedDict = {}
dRRatioDict = {}
mergedMassDict = {}
mergedMassDict_sigWeight = {}
mergedMassDict_drWeight = {}
mergedMassDict_weight = {}
dzSameDict = {}
dzMixedDict = {}
sig_vs_dz_sameDict = {}
sig_vs_dz_mixedDict = {}

# DV selection
sigSameDict_DVsel = {}
sigMixedDict_DVsel = {}
sigRatioDict_DVsel = {}
dRSameDict_DVsel = {}
dRMixedDict_DVsel = {}
dRRatioDict_DVsel = {}
mergedMassDict_DVsel = {}
mergedMassDict_DVsel_sigWeight = {}
mergedMassDict_DVsel_drWeight = {}
mergedMassDict_DVsel_weight = {}
for ntrk in ntrkList:
    # No selection
    sigSameDict[ntrk] = r.TH1D("sigSame_{}".format(ntrk), ";Significance", 40, 0., 1000.)
    sigMixedDict[ntrk] = r.TH1D("sigMixed_{}".format(ntrk), ";Significance", 40, 0., 1000.)
    dRSameDict[ntrk] = r.TH1D("dRSame_{}".format(ntrk), ";dR(jet,DV_{2})", 100, 0., 10.)
    dRMixedDict[ntrk] = r.TH1D("dRMixed_{}".format(ntrk), ";dR(jet,DV_{2})", 100, 0., 10.)
    mergedMassDict[ntrk] = r.TH1D("mergedMass_{}".format(ntrk), ";m_{MV} [GeV]", 200, 0., 100.)
    mergedMassDict_sigWeight[ntrk] = r.TH1D("mergedMass_sigWeight_{}".format(ntrk), ";m_{MV} [GeV]", 200, 0., 100.)
    mergedMassDict_drWeight[ntrk] = r.TH1D("mergedMass_drWeight_{}".format(ntrk), ";m_{MV} [GeV]", 200, 0., 100.)
    mergedMassDict_weight[ntrk] = r.TH1D("mergedMass_weight_{}".format(ntrk), ";m_{MV} [GeV]", 200, 0., 100.)
    dzSameDict[ntrk] = r.TH1D("deltaZ_same_{}".format(ntrk), "; |#Deltaz| [mm]", 300, 0., 1500.)
    dzMixedDict[ntrk] = r.TH1D("deltaZ_mixed_{}".format(ntrk), "; |#Deltaz| [mm]", 300, 0., 1500.)
    sig_vs_dz_sameDict[ntrk] = r.TH2D("sig_vs_dz_same_{}".format(ntrk), ";Significance;|#Deltaz| [mm]", 100, 0., 1000., 300, 0., 1500.)
    sig_vs_dz_mixedDict[ntrk] = r.TH2D("sig_vs_dz_mixed_{}".format(ntrk), ";Significance;|#Deltaz| [mm]", 100, 0., 1000., 300, 0., 1500.)

    # DV selection
    sigSameDict_DVsel[ntrk] = r.TH1D("sigSame_DVsel_{}".format(ntrk), ";Significance", 40, 0., 1000.)
    sigMixedDict_DVsel[ntrk] = r.TH1D("sigMixed_DVsel_{}".format(ntrk), ";Significance", 40, 0., 1000.)
    dRSameDict_DVsel[ntrk] = r.TH1D("dRSame_DVsel_{}".format(ntrk), ";dR(jet,DV_{2})", 100, 0., 10.)
    dRMixedDict_DVsel[ntrk] = r.TH1D("dRMixed_DVsel_{}".format(ntrk), ";dR(jet,DV_{2})", 100, 0., 10.)
    mergedMassDict_DVsel[ntrk] = r.TH1D("mergedMass_DVsel_{}".format(ntrk), ";m_{MV} [GeV]", 200, 0., 100.)
    mergedMassDict_DVsel_sigWeight[ntrk] = r.TH1D("mergedMass_DVsel_sigWeight_{}".format(ntrk), ";m_{MV} [GeV]", 200, 0., 100.)
    mergedMassDict_DVsel_drWeight[ntrk] = r.TH1D("mergedMass_DVsel_drWeight_{}".format(ntrk), ";m_{MV} [GeV]", 200, 0., 100.)
    mergedMassDict_DVsel_weight[ntrk] = r.TH1D("mergedMass_DVsel_weight_{}".format(ntrk), ";m_{MV} [GeV]", 200, 0., 100.)

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
    dR = dv.dR
    passFiducial = dv.dvPassFiducialCut
    passDist = dv.dvPassDistCut
    passChi2 = dv.dvPassChi2Cut
    passMatVeto = dv.dvPassMaterialVeto
    #dz = r.TMath.Abs(dv.deltaZ)
    
    ntrkBin = getNtrkBin(ntrk)
    if (isSame):
        sigSameDict[ntrkBin].Fill(sig)
        dRSameDict[ntrkBin].Fill(dR)
        
        if (passFiducial and passDist and passChi2 and passMatVeto):
            sigSameDict_DVsel[ntrkBin].Fill(sig)
            dRSameDict_DVsel[ntrkBin].Fill(dR)
    else:
        sigMixedDict[ntrkBin].Fill(sig)
        dRMixedDict[ntrkBin].Fill(dR)
        if (passFiducial and passDist and passChi2 and passMatVeto):
            sigMixedDict_DVsel[ntrkBin].Fill(sig)
            dRMixedDict_DVsel[ntrkBin].Fill(dR)
    
# Prepare Latex
sampleLabel = r.TLatex()
sampleLabel.SetNDC()
sampleLabel.SetTextFont(42)
sampleLabel.SetTextAlign(13)
sampleLabel.SetTextSize(0.03)
dataLabel = dataSet + ", di-jet"

leg = r.TLegend(0.65, 0.55, 0.85, 0.70)
leg.SetBorderSize(0)
leg.SetFillStyle(0)
leg.SetLineStyle(0)
leg.SetTextFont(42)
leg.SetTextSize(0.03)
leg.AddEntry(sigSameDict["Ntrk4"], "Same", "l")
leg.AddEntry(sigMixedDict["Ntrk4"], "Mixed", "l")
        
# Save histograms
c = r.TCanvas("c", "c", 800, 700)
c.cd()
for ntrkBin in ntrkList:
    # No selection
    sigSameHist = sigSameDict[ntrkBin]
    sigMixedHist = sigMixedDict[ntrkBin]
    dRSameHist = dRSameDict[ntrkBin]
    dRMixedHist = dRMixedDict[ntrkBin]

    # DV selection
    sigSameHist_DVsel = sigSameDict_DVsel[ntrkBin]
    sigMixedHist_DVsel = sigMixedDict_DVsel[ntrkBin]
    dRSameHist_DVsel = dRSameDict_DVsel[ntrkBin]
    dRMixedHist_DVsel = dRMixedDict_DVsel[ntrkBin]

    # Ratio
    ratio = plotSigRatio(sigSameHist, sigMixedHist, "", ntrkBin, c, directory, dataLabel, label, leg)
    sigRatioDict[ntrkBin] = ratio

    ratio_DVsel = plotSigRatio(sigSameHist_DVsel, sigMixedHist_DVsel, "DVsel", ntrkBin, c, directory, dataLabel, label, leg)
    sigRatioDict_DVsel[ntrkBin] = ratio_DVsel

    # dR
    c.SetLogy(0)
    drRatio = plotdRRatio(dRSameHist, dRMixedHist, "", ntrkBin, c, dataLabel, label, leg)
    dRRatioDict[ntrkBin] = drRatio

    drRatio_DVsel = plotdRRatio(dRSameHist_DVsel, dRMixedHist_DVsel, "DVsel", ntrkBin, c, dataLabel, label, leg)
    dRRatioDict_DVsel[ntrkBin] = drRatio_DVsel

# For merged mass with weight
print("Looping for merged mass")
evtCounter = 0
for dv in tree:
    evtCounter += 1
    if (evtCounter % 100000 == 0):
        print("Processed {}/{}".format(evtCounter, entries))
    dvMass = dv.mass
    ntrk = dv.ntrk
    isSame = dv.sameEvent
    sig = dv.significance
    dR = dv.dR
    passFiducial = dv.dvPassFiducialCut
    passDist = dv.dvPassDistCut
    passChi2 = dv.dvPassChi2Cut
    passMatVeto = dv.dvPassMaterialVeto

    ntrkBin = getNtrkBin(ntrk)
    sigBin = sigRatioDict[ntrkBin].FindBin(sig)
    drBin = dRRatioDict[ntrkBin].FindBin(dR)
    
    sigWeight = 1. - sigRatioDict[ntrkBin].GetBinContent(sigBin)
    sigWeight_DVsel = 1. - sigRatioDict_DVsel[ntrkBin].GetBinContent(sigBin)
    drWeight_DVsel = dRRatioDict_DVsel[ntrkBin].GetBinContent(drBin)
        
    if (sigWeight < 0.):
        sigWeight = 0
    if (sigWeight_DVsel < 0.):
        sigWeight_DVsel = 0
        
    drWeight = dRRatioDict[ntrkBin].GetBinContent(drBin)
    weight = sigWeight * drWeight
    weight_DVsel = sigWeight_DVsel * drWeight_DVsel
   
    if (not isSame):
        if (sig < normSig):
            mergedMassDict[ntrkBin].Fill(dvMass)
            mergedMassDict_sigWeight[ntrkBin].Fill(dvMass, sigWeight)
            mergedMassDict_drWeight[ntrkBin].Fill(dvMass, drWeight)
            mergedMassDict_weight[ntrkBin].Fill(dvMass, weight)

            if (passFiducial and passDist and passChi2 and passMatVeto):
                mergedMassDict_DVsel[ntrkBin].Fill(dvMass)
                mergedMassDict_DVsel_sigWeight[ntrkBin].Fill(dvMass, sigWeight_DVsel)
                mergedMassDict_DVsel_drWeight[ntrkBin].Fill(dvMass, drWeight_DVsel)
                mergedMassDict_DVsel_weight[ntrkBin].Fill(dvMass, weight_DVsel)

for ntrkBin in ntrkList:
    mergedMassHist = mergedMassDict[ntrkBin]
    mergedMassHist_sigWeight = mergedMassDict_sigWeight[ntrkBin]
    mergedMassHist_drWeight = mergedMassDict_drWeight[ntrkBin]
    mergedMassHist_weight = mergedMassDict_weight[ntrkBin]

    mergedMassHist_DVsel = mergedMassDict_DVsel[ntrkBin]
    mergedMassHist_DVsel_sigWeight = mergedMassDict_DVsel_sigWeight[ntrkBin]
    mergedMassHist_DVsel_drWeight = mergedMassDict_DVsel_drWeight[ntrkBin]
    mergedMassHist_DVsel_weight = mergedMassDict_DVsel_weight[ntrkBin]


    plotMassHist(mergedMassHist, "", "", ntrkBin, c, sampleLabel, dataLabel, label)
    plotMassHist(mergedMassHist_sigWeight, "", "sigWeight", ntrkBin, c, sampleLabel, dataLabel, label)
    plotMassHist(mergedMassHist_drWeight, "", "drWeight", ntrkBin, c, sampleLabel, dataLabel, label)
    plotMassHist(mergedMassHist_weight, "", "weight", ntrkBin, c, sampleLabel, dataLabel, label)

    plotMassHist(mergedMassHist_DVsel, "DVsel", "", ntrkBin, c, sampleLabel, dataLabel, label)
    plotMassHist(mergedMassHist_DVsel_sigWeight, "DVsel", "sigWeight", ntrkBin, c, sampleLabel, dataLabel, label)
    plotMassHist(mergedMassHist_DVsel_drWeight, "DVsel", "drWeight", ntrkBin, c, sampleLabel, dataLabel, label)
    plotMassHist(mergedMassHist_DVsel_weight, "DVsel", "weight", ntrkBin, c, sampleLabel, dataLabel, label)
   
    leg = r.TLegend(0.65, 0.50, 0.85, 0.70)
    leg.SetFillStyle(0)
    leg.SetLineStyle(0)
    leg.SetBorderSize(0)
    leg.SetTextSize(0.03)
    leg.SetTextFont(42)

    mergedMassHist.SetLineColor(colors[0])
    mergedMassHist_sigWeight.SetLineColor(colors[1])
    mergedMassHist_drWeight.SetLineColor(colors[2])
    mergedMassHist_weight.SetLineColor(colors[3])
    mergedMassHist.SetMarkerColor(colors[0])
    mergedMassHist_sigWeight.SetMarkerColor(colors[1])
    mergedMassHist_drWeight.SetMarkerColor(colors[2])
    mergedMassHist_weight.SetMarkerColor(colors[3])

    maximum = mergedMassHist_drWeight.GetMaximum()
    mergedMassHist.SetMaximum(maximum*1.2)

    c.SetLogy(1)
    mergedMassHist.Draw("hist")
    mergedMassHist_sigWeight.Draw("hist same e0")
    mergedMassHist_drWeight.Draw("hist same e0")
    mergedMassHist_weight.Draw("hist same e0")

    leg.AddEntry(mergedMassHist, "No weight", "l")
    leg.AddEntry(mergedMassHist_sigWeight, "Significance weight", "l")
    leg.AddEntry(mergedMassHist_drWeight, "dR weight", "l")
    leg.AddEntry(mergedMassHist_weight, "Sig#timesdR weight", "l")

    sampleLabel.DrawLatex(0.65, 0.85, dataLabel)
    sampleLabel.DrawLatex(0.65, 0.80, "Event preselection")
    sampleLabel.DrawLatex(0.65, 0.75, getNtrkLabel(ntrkBin))
    leg.Draw()
    ATLASLabel(0.20, 0.955, label)
    c.Print("{}/{}.pdf".format(directory, "mass_distribution_"+ntrkBin+"_logy"))

    c.SetLogy(0)
    mergedMassHist.Draw("hist")
    mergedMassHist_sigWeight.Draw("hist same e0")
    mergedMassHist_drWeight.Draw("hist same e0")
    mergedMassHist_weight.Draw("hist same e0")

    sampleLabel.DrawLatex(0.65, 0.85, dataLabel)
    sampleLabel.DrawLatex(0.65, 0.80, "Event preselection")
    sampleLabel.DrawLatex(0.65, 0.75, getNtrkLabel(ntrkBin))
    leg.Draw()
    ATLASLabel(0.20, 0.955, label)
    c.Print("{}/{}.pdf".format(directory, "mass_distribution_"+ntrkBin))

outputFile.Write()
outputFile.Close()
