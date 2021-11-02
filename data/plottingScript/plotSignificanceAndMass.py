import ROOT as r
import sys, os
sys.path.append("/Users/amizukam/DVJets/atlasstyle")
from AtlasStyle import *
from AtlasLabel import *
import ctypes
import argparse

r.gROOT.SetBatch()
SetAtlasStyle()

parser = argparse.ArgumentParser()
parser.add_argument("-sr", "--SR", required=True, help="Signal region, 'HighPtSR', or 'TracklessSR'")
parser.add_argument("-t", "--trackCleaning", action="store_true", help="Use track cleaning file")
parser.add_argument("-l", "--label", default="Internal", help="Label for ATLASLabel")
args = parser.parse_args()

label = args.label
SR = args.SR
useTrackCleaningFile = args.trackCleaning
dataSet = SR + "_trackCleaning" if useTrackCleaningFile else SR

plotType = "sigAndMass"
directory = "pdfs/" + plotType + "/" + dataSet
if (not os.path.isdir(directory)):
    os.makedirs(directory)
if (not os.path.isdir("rootfiles")):
    os.makedirs("rootfiles")

inputFile = r.TFile("../outputFiles/significance_{}.root".format(dataSet), "READ")
tree = inputFile.Get("trees_SRDV_")

outputFile = r.TFile("rootfiles/{}_{}.root".format(plotType, dataSet), "RECREATE")

colors = [r.kGreen, r.kRed, r.kBlue, r.kOrange, r.kMagenta, r.kCyan]

ntrkList = ["Ntrk4", "Ntrk5", "Ntrk6", "Ntrk>6"]

def determineNtrkBin(ntrk):
    ntrkBin = ""
    if ntrk == 4:
        ntrkBin = "Ntrk4"
    if ntrk == 5:
        ntrkBin = "Ntrk5"
    if ntrk == 6:
        ntrkBin = "Ntrk6"
    if ntrk > 6:
        ntrkBin = "Ntrk>6"
    return ntrkBin

def getNtrkLabel(ntrkBin):
    ntrkLabel = ""
    if ntrkBin == "ntrk4":
        ntrkLabel = "N_{trk} = 4"
    if ntrkBin == "ntrk5":
        ntrkLabel = "N_{trk} = 5"
    if ntrkBin == "ntrk6":
        ntrkLabel = "N_{trk} = 6"
    if ntrkBin == "ntrk>6":
        ntrkLabel = "N_{trk} > 6"
    return ntrkLabel

def plotSigRatio(same, mixed, sel, ntrkBin, canvas, directory, dataLabel, label, leg):
    sigRatio = same.Clone("sigRatio_{}".format(ntrkBin))
    bin1 = same.FindBin(100.)
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
    nMV = mixed.IntegralAndError(1, bin1, err)
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

def decorateRatioPlot(rp):
    rp.SetH2DrawOpt("hist")
    rp.Draw()
    rp.GetLowerRefGraph().SetMaximum(2.0)
    rp.GetLowerRefGraph().SetMinimum(0.0)
    rp.GetLowYaxis().SetNdivisions(4)
    rp.SetSeparationMargin(0.02)
    rp.SetLeftMargin(0.1575)
    rp.SetLowBottomMargin(0.50)

def decorateLeg(leg):
    leg.SetFillStyle(0)
    leg.SetBorderSize(0)
    leg.SetLineStyle(0)
    leg.SetTextSize(0.035)
    leg.SetTextFont(42)

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
"""
# Fiducial cut
sigSameDict_fiducial = {}
sigMixedDict_fiducial = {}
sigRatioDict_fiducial = {}
dRSameDict_fiducial = {}
dRMixedDict_fiducial = {}
dRRatioDict_fiducial = {}
mergedMassDict_fiducial = {}
mergedMassDict_fiducial_sigWeight = {}
mergedMassDict_fiducial_drWeight = {}
mergedMassDict_fiducial_weight = {}
# Dist cut
sigSameDict_dist = {}
sigMixedDict_dist = {}
sigRatioDict_dist = {}
dRSameDict_dist = {}
dRMixedDict_dist = {}
dRRatioDict_dist = {}
mergedMassDict_dist = {}
mergedMassDict_dist_sigWeight = {}
mergedMassDict_dist_drWeight = {}
mergedMassDict_dist_weight = {}
# Chi2 cut
sigSameDict_chi2 = {}
sigMixedDict_chi2 = {}
sigRatioDict_chi2 = {}
dRSameDict_chi2 = {}
dRMixedDict_chi2 = {}
dRRatioDict_chi2 = {}
mergedMassDict_chi2 = {}
mergedMassDict_chi2_sigWeight = {}
mergedMassDict_chi2_drWeight = {}
mergedMassDict_chi2_weight = {}
# matVeto
sigSameDict_matVeto = {}
sigMixedDict_matVeto = {}
sigRatioDict_matVeto = {}
dRSameDict_matVeto = {}
dRMixedDict_matVeto = {}
dRRatioDict_matVeto = {}
mergedMassDict_matVeto = {}
mergedMassDict_matVeto_sigWeight = {}
mergedMassDict_matVeto_drWeight = {}
mergedMassDict_matVeto_weight = {}
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
"""
for ntrk in ntrkList:
    # No selection
    sigSameDict[ntrk] = r.TH1D("sigSame_{}".format(ntrk), ";Significance", 100, 0., 1000.)
    sigMixedDict[ntrk] = r.TH1D("sigMixed_{}".format(ntrk), ";Significance", 100, 0., 1000.)
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
    """
    # Fiducial cut
    sigSameDict_fiducial[ntrk] = r.TH1D("sigSame_fiducial_{}".format(ntrk), ";Significance", 100, 0., 1000.)
    sigMixedDict_fiducial[ntrk] = r.TH1D("sigMixed_fiducial_{}".format(ntrk), ";Significance", 100, 0., 1000.)
    dRSameDict_fiducial[ntrk] = r.TH1D("dRSame_fiducial_{}".format(ntrk), ";dR(jet,DV_{2})", 100, 0., 10.)
    dRMixedDict_fiducial[ntrk] = r.TH1D("dRMixed_fiducial_{}".format(ntrk), ";dR(jet,DV_{2})", 100, 0., 10.)
    mergedMassDict_fiducial[ntrk] = r.TH1D("mergedMass_fiducial_{}".format(ntrk), ";m_{MV} [GeV]", 100, 0., 100.)
    mergedMassDict_fiducial_sigWeight[ntrk] = r.TH1D("mergedMass_fiducial_sigWeight_{}".format(ntrk), ";m_{MV} [GeV]", 100, 0., 100.)
    mergedMassDict_fiducial_drWeight[ntrk] = r.TH1D("mergedMass_fiducial_drWeight_{}".format(ntrk), ";m_{MV} [GeV]", 100, 0., 100.)
    mergedMassDict_fiducial_weight[ntrk] = r.TH1D("mergedMass_fiducial_weight_{}".format(ntrk), ";m_{MV} [GeV]", 100, 0., 100.)
    # Distance cut
    sigSameDict_dist[ntrk] = r.TH1D("sigSame_dist_{}".format(ntrk), ";Significance", 100, 0., 1000.)
    sigMixedDict_dist[ntrk] = r.TH1D("sigMixed_dist_{}".format(ntrk), ";Significance", 100, 0., 1000.)
    dRSameDict_dist[ntrk] = r.TH1D("dRSame_dist_{}".format(ntrk), ";dR(jet,DV_{2})", 100, 0., 10.)
    dRMixedDict_dist[ntrk] = r.TH1D("dRMixed_dist_{}".format(ntrk), ";dR(jet,DV_{2})", 100, 0., 10.)
    mergedMassDict_dist[ntrk] = r.TH1D("mergedMass_dist_{}".format(ntrk), ";m_{MV} [GeV]", 100, 0., 100.)
    mergedMassDict_dist_sigWeight[ntrk] = r.TH1D("mergedMass_dist_sigWeight_{}".format(ntrk), ";m_{MV} [GeV]", 100, 0., 100.)
    mergedMassDict_dist_drWeight[ntrk] = r.TH1D("mergedMass_dist_drWeight_{}".format(ntrk), ";m_{MV} [GeV]", 100, 0., 100.)
    mergedMassDict_dist_weight[ntrk] = r.TH1D("mergedMass_dist_weight_{}".format(ntrk), ";m_{MV} [GeV]", 100, 0., 100.)
    # Chi2 cut
    sigSameDict_chi2[ntrk] = r.TH1D("sigSame_chi2_{}".format(ntrk), ";Significance", 100, 0., 1000.)
    sigMixedDict_chi2[ntrk] = r.TH1D("sigMixed_chi2_{}".format(ntrk), ";Significance", 100, 0., 1000.)
    dRSameDict_chi2[ntrk] = r.TH1D("dRSame_chi2_{}".format(ntrk), ";dR(jet,DV_{2})", 100, 0., 10.)
    dRMixedDict_chi2[ntrk] = r.TH1D("dRMixed_chi2_{}".format(ntrk), ";dR(jet,DV_{2})", 100, 0., 10.)
    mergedMassDict_chi2[ntrk] = r.TH1D("mergedMass_chi2_{}".format(ntrk), ";m_{MV} [GeV]", 100, 0., 100.)
    mergedMassDict_chi2_sigWeight[ntrk] = r.TH1D("mergedMass_chi2_sigWeight_{}".format(ntrk), ";m_{MV} [GeV]", 100, 0., 100.)
    mergedMassDict_chi2_drWeight[ntrk] = r.TH1D("mergedMass_chi2_drWeight_{}".format(ntrk), ";m_{MV} [GeV]", 100, 0., 100.)
    mergedMassDict_chi2_weight[ntrk] = r.TH1D("mergedMass_chi2_weight_{}".format(ntrk), ";m_{MV} [GeV]", 100, 0., 100.)
    # matVeto
    sigSameDict_matVeto[ntrk] = r.TH1D("sigSame_matVeto_{}".format(ntrk), ";Significance", 100, 0., 1000.)
    sigMixedDict_matVeto[ntrk] = r.TH1D("sigMixed_matVeto_{}".format(ntrk), ";Significance", 100, 0., 1000.)
    dRSameDict_matVeto[ntrk] = r.TH1D("dRSame_matVeto_{}".format(ntrk), ";dR(jet,DV_{2})", 100, 0., 10.)
    dRMixedDict_matVeto[ntrk] = r.TH1D("dRMixed_matVeto_{}".format(ntrk), ";dR(jet,DV_{2})", 100, 0., 10.)
    mergedMassDict_matVeto[ntrk] = r.TH1D("mergedMass_matVeto_{}".format(ntrk), ";m_{MV} [GeV]", 100, 0., 100.)
    mergedMassDict_matVeto_sigWeight[ntrk] = r.TH1D("mergedMass_matVeto_sigWeight_{}".format(ntrk), ";m_{MV} [GeV]", 100, 0., 100.)
    mergedMassDict_matVeto_drWeight[ntrk] = r.TH1D("mergedMass_matVeto_drWeight_{}".format(ntrk), ";m_{MV} [GeV]", 100, 0., 100.)
    mergedMassDict_matVeto_weight[ntrk] = r.TH1D("mergedMass_matVeto_weight_{}".format(ntrk), ";m_{MV} [GeV]", 100, 0., 100.)
    # DV selection
    sigSameDict_DVsel[ntrk] = r.TH1D("sigSame_DVsel_{}".format(ntrk), ";Significance", 100, 0., 1000.)
    sigMixedDict_DVsel[ntrk] = r.TH1D("sigMixed_DVsel_{}".format(ntrk), ";Significance", 100, 0., 1000.)
    dRSameDict_DVsel[ntrk] = r.TH1D("dRSame_DVsel_{}".format(ntrk), ";dR(jet,DV_{2})", 100, 0., 10.)
    dRMixedDict_DVsel[ntrk] = r.TH1D("dRMixed_DVsel_{}".format(ntrk), ";dR(jet,DV_{2})", 100, 0., 10.)
    mergedMassDict_DVsel[ntrk] = r.TH1D("mergedMass_DVsel_{}".format(ntrk), ";m_{MV} [GeV]", 100, 0., 100.)
    mergedMassDict_DVsel_sigWeight[ntrk] = r.TH1D("mergedMass_DVsel_sigWeight_{}".format(ntrk), ";m_{MV} [GeV]", 100, 0., 100.)
    mergedMassDict_DVsel_drWeight[ntrk] = r.TH1D("mergedMass_DVsel_drWeight_{}".format(ntrk), ";m_{MV} [GeV]", 100, 0., 100.)
    mergedMassDict_DVsel_weight[ntrk] = r.TH1D("mergedMass_DVsel_weight_{}".format(ntrk), ";m_{MV} [GeV]", 100, 0., 100.)
    """

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
    
    ntrkBin = determineNtrkBin(ntrk)
    if (isSame):
        sigSameDict[ntrkBin].Fill(sig)
        dRSameDict[ntrkBin].Fill(dR)
        """
        dzSameDict[ntrkBin].Fill(dz)
        sig_vs_dz_sameDict[ntrkBin].Fill(sig, dz)
        """
        """
        if (passFiducial):
            sigSameDict_fiducial[ntrkBin].Fill(sig)
            dRSameDict_fiducial[ntrkBin].Fill(dR)
        if (passDist):
            sigSameDict_dist[ntrkBin].Fill(sig)
            dRSameDict_dist[ntrkBin].Fill(dR)
        if (passChi2):
            sigSameDict_chi2[ntrkBin].Fill(sig)
            dRSameDict_chi2[ntrkBin].Fill(dR)
        if (passMatVeto):
            sigSameDict_matVeto[ntrkBin].Fill(sig)
            dRSameDict_matVeto[ntrkBin].Fill(dR)
        if (passFiducial and passDist and passChi2 and passMatVeto):
            sigSameDict_DVsel[ntrkBin].Fill(sig)
            dRSameDict_DVsel[ntrkBin].Fill(dR)
        """
    else:
        sigMixedDict[ntrkBin].Fill(sig)
        dRMixedDict[ntrkBin].Fill(dR)
        """
        dzMixedDict[ntrkBin].Fill(dz)
        sig_vs_dz_mixedDict[ntrkBin].Fill(sig, dz)
        """
        """
        if (passFiducial):
            sigMixedDict_fiducial[ntrkBin].Fill(sig)
            dRMixedDict_fiducial[ntrkBin].Fill(dR)
        if (passDist):
            sigMixedDict_dist[ntrkBin].Fill(sig)
            dRMixedDict_dist[ntrkBin].Fill(dR)
        if (passChi2):
            sigMixedDict_chi2[ntrkBin].Fill(sig)
            dRMixedDict_chi2[ntrkBin].Fill(dR)
        if (passMatVeto):
            sigMixedDict_matVeto[ntrkBin].Fill(sig)
            dRMixedDict_matVeto[ntrkBin].Fill(dR)
        if (passFiducial and passDist and passChi2 and passMatVeto):
            sigMixedDict_DVsel[ntrkBin].Fill(sig)
            dRMixedDict_DVsel[ntrkBin].Fill(dR)
        """
    
# Prepare Latex
sampleLabel = r.TLatex()
sampleLabel.SetNDC()
sampleLabel.SetTextFont(42)
sampleLabel.SetTextAlign(13)
sampleLabel.SetTextSize(0.03)
dataLabel = dataSet

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
    """
    dzSameHist = dzSameDict[ntrkBin]
    dzMixedHist = dzMixedDict[ntrkBin]
    sig_vs_dz_sameHist = sig_vs_dz_sameDict[ntrkBin]
    sig_vs_dz_mixedHist = sig_vs_dz_mixedDict[ntrkBin]
    """
    """
    # Fiducial cut
    sigSameHist_fiducial = sigSameDict_fiducial[ntrkBin]
    sigMixedHist_fiducial = sigMixedDict_fiducial[ntrkBin]
    dRSameHist_fiducial = dRSameDict_fiducial[ntrkBin]
    dRMixedHist_fiducial = dRMixedDict_fiducial[ntrkBin]
    # Dist cut
    sigSameHist_dist = sigSameDict_dist[ntrkBin]
    sigMixedHist_dist = sigMixedDict_dist[ntrkBin]
    dRSameHist_dist = dRSameDict_dist[ntrkBin]
    dRMixedHist_dist = dRMixedDict_dist[ntrkBin]
    # Chi2 cut
    sigSameHist_chi2 = sigSameDict_chi2[ntrkBin]
    sigMixedHist_chi2 = sigMixedDict_chi2[ntrkBin]
    dRSameHist_chi2 = dRSameDict_chi2[ntrkBin]
    dRMixedHist_chi2 = dRMixedDict_chi2[ntrkBin]
    # matVeto
    sigSameHist_matVeto = sigSameDict_matVeto[ntrkBin]
    sigMixedHist_matVeto = sigMixedDict_matVeto[ntrkBin]
    dRSameHist_matVeto = dRSameDict_matVeto[ntrkBin]
    dRMixedHist_matVeto = dRMixedDict_matVeto[ntrkBin]
    # DV selection
    sigSameHist_DVsel = sigSameDict_DVsel[ntrkBin]
    sigMixedHist_DVsel = sigMixedDict_DVsel[ntrkBin]
    dRSameHist_DVsel = dRSameDict_DVsel[ntrkBin]
    dRMixedHist_DVsel = dRMixedDict_DVsel[ntrkBin]
    """

    # Ratio
    ratio = plotSigRatio(sigSameHist, sigMixedHist, "", ntrkBin, c, directory, dataLabel, label, leg)
    sigRatioDict[ntrkBin] = ratio
    """
    ratio_fiducial = plotSigRatio(sigSameHist_fiducial, sigMixedHist_fiducial, "fiducial", ntrkBin, c, directory, dataLabel, label, leg)
    sigRatioDict_fiducial[ntrkBin] = ratio_fiducial
    ratio_dist = plotSigRatio(sigSameHist_dist, sigMixedHist_dist, "dist", ntrkBin, c, directory, dataLabel, label, leg)
    sigRatioDict_dist[ntrkBin] = ratio_dist
    ratio_chi2 = plotSigRatio(sigSameHist_chi2, sigMixedHist_chi2, "chi2", ntrkBin, c, directory, dataLabel, label, leg)
    sigRatioDict_chi2[ntrkBin] = ratio_chi2
    ratio_matVeto = plotSigRatio(sigSameHist_matVeto, sigMixedHist_matVeto, "matVeto", ntrkBin, c, directory, dataLabel, label, leg)
    sigRatioDict_matVeto[ntrkBin] = ratio_matVeto
    ratio_DVsel = plotSigRatio(sigSameHist_DVsel, sigMixedHist_DVsel, "DVsel", ntrkBin, c, directory, dataLabel, label, leg)
    sigRatioDict_DVsel[ntrkBin] = ratio_DVsel
    """

    # dR
    c.SetLogy(0)
    drRatio = plotdRRatio(dRSameHist, dRMixedHist, "", ntrkBin, c, dataLabel, label, leg)
    dRRatioDict[ntrkBin] = drRatio
    """
    drRatio_fiducial = plotdRRatio(dRSameHist_fiducial, dRMixedHist_fiducial, "fiducial", ntrkBin, c, dataLabel, label, leg)
    dRRatioDict_fiducial[ntrkBin] = drRatio_fiducial
    drRatio_dist = plotdRRatio(dRSameHist_dist, dRMixedHist_dist, "dist", ntrkBin, c, dataLabel, label, leg)
    dRRatioDict_dist[ntrkBin] = drRatio_dist
    drRatio_chi2 = plotdRRatio(dRSameHist_chi2, dRMixedHist_chi2, "chi2", ntrkBin, c, dataLabel, label, leg)
    dRRatioDict_chi2[ntrkBin] = drRatio_chi2
    drRatio_matVeto = plotdRRatio(dRSameHist_matVeto, dRMixedHist_matVeto, "matVeto", ntrkBin, c, dataLabel, label, leg)
    dRRatioDict_matVeto[ntrkBin] = drRatio_matVeto
    drRatio_DVsel = plotdRRatio(dRSameHist_DVsel, dRMixedHist_DVsel, "DVsel", ntrkBin, c, dataLabel, label, leg)
    dRRatioDict_DVsel[ntrkBin] = drRatio_DVsel
    """

    """
    # dZ
    dzMixedHist.SetLineColor(r.kRed)
    dzMixedHist.SetMarkerColor(r.kRed)
    dzSameHist.Sumw2()
    dzMixedHist.Sumw2()
    dzSameHist.Scale(1./(dzSameHist.Integral()+1))
    dzMixedHist.Scale(1./(dzMixedHist.Integral()+1))
    ratio_dZ = r.TRatioPlot(dzSameHist, dzMixedHist)
    decorateRatioPlot(ratio_dZ)
    leg.Draw()
    sampleLabel.DrawLatex(0.65, 0.80, dataLabel)
    sampleLabel.DrawLatex(0.65, 0.75, "Event preselection")
    sampleLabel.DrawLatex(0.65, 0.70, getNtrkLabel(ntrkBin))
    ATLASLabel(0.20, 0.955, label)
    c.Print("{}/{}.pdf".format(directory, "dZ_ratio_"+ntrkBin))

    c.SetLogz(1)
    sig_vs_dz_sameHist.Draw("colz")
    ATLASLabel(0.20, 0.955, label)
    c.Print("{}/{}.pdf".format(directory, "sig_vs_dz_same_"+ntrkBin))

    sig_vs_dz_mixedHist.Draw("colz")
    ATLASLabel(0.20, 0.955, label)
    c.Print("{}/{}.pdf".format(directory, "sig_vs_dz_mixed_"+ntrkBin))
    c.SetLogz(0)
    """
    

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

    ntrkBin = determineNtrkBin(ntrk)
    sigBin = sigRatioDict[ntrkBin].FindBin(sig)
    drBin = dRRatioDict[ntrkBin].FindBin(dR)
    
    sigWeight = 1. - sigRatioDict[ntrkBin].GetBinContent(sigBin)
    """
    #if (passFiducial):
    sigWeight_fiducial = 1. - sigRatioDict_fiducial[ntrkBin].GetBinContent(sigBin)
    drWeight_fiducial = dRRatioDict_fiducial[ntrkBin].GetBinContent(drBin)
    #if (passDist):
    sigWeight_dist = 1. - sigRatioDict_dist[ntrkBin].GetBinContent(sigBin)
    drWeight_dist = dRRatioDict_dist[ntrkBin].GetBinContent(drBin)
    #if (passChi2):
    sigWeight_chi2 = 1. - sigRatioDict_chi2[ntrkBin].GetBinContent(sigBin)
    drWeight_chi2 = dRRatioDict_chi2[ntrkBin].GetBinContent(drBin)
    #if (passMatVeto):
    sigWeight_matVeto = 1. - sigRatioDict_matVeto[ntrkBin].GetBinContent(sigBin)
    drWeight_matVeto = dRRatioDict_matVeto[ntrkBin].GetBinContent(drBin)
    #if (passFiducial and passDist and passChi2 and passMatVeto):
    sigWeight_DVsel = 1. - sigRatioDict_DVsel[ntrkBin].GetBinContent(sigBin)
    drWeight_DVsel = dRRatioDict_DVsel[ntrkBin].GetBinContent(drBin)
    """
        
    if (sigWeight < 0.):
        sigWeight = 0
    """
    if (sigWeight_fiducial < 0.):
        sigWeight_fiducial = 0
    if (sigWeight_dist < 0.):
        sigWeight_dist = 0
    if (sigWeight_chi2 < 0.):
        sigWeight_chi2 = 0
    if (sigWeight_matVeto < 0.):
        sigWeight_matVeto = 0
    if (sigWeight_DVsel < 0.):
        sigWeight_DVsel = 0
    """
        
    drWeight = dRRatioDict[ntrkBin].GetBinContent(drBin)
    weight = sigWeight * drWeight
    """
    weight_fiducial = sigWeight_fiducial * drWeight_fiducial
    weight_dist = sigWeight_dist * drWeight_dist
    weight_chi2 = sigWeight_chi2 * drWeight_chi2
    weight_matVeto = sigWeight_matVeto * drWeight_matVeto
    weight_DVsel = sigWeight_DVsel * drWeight_DVsel
    """
   
    if (not isSame):
        if (sig < 100.):
            mergedMassDict[ntrkBin].Fill(dvMass)
            mergedMassDict_sigWeight[ntrkBin].Fill(dvMass, sigWeight)
            mergedMassDict_drWeight[ntrkBin].Fill(dvMass, drWeight)
            mergedMassDict_weight[ntrkBin].Fill(dvMass, weight)
            """
            if (passFiducial):
                mergedMassDict_fiducial[ntrkBin].Fill(dvMass)
                mergedMassDict_fiducial_sigWeight[ntrkBin].Fill(dvMass, sigWeight_fiducial)
                mergedMassDict_fiducial_drWeight[ntrkBin].Fill(dvMass, drWeight_fiducial)
                mergedMassDict_fiducial_weight[ntrkBin].Fill(dvMass, weight_fiducial)
            if (passDist):
                mergedMassDict_dist[ntrkBin].Fill(dvMass)
                mergedMassDict_dist_sigWeight[ntrkBin].Fill(dvMass, sigWeight_dist)
                mergedMassDict_dist_drWeight[ntrkBin].Fill(dvMass, drWeight_dist)
                mergedMassDict_dist_weight[ntrkBin].Fill(dvMass, weight_dist)
            if (passChi2):
                mergedMassDict_chi2[ntrkBin].Fill(dvMass)
                mergedMassDict_chi2_sigWeight[ntrkBin].Fill(dvMass, sigWeight_chi2)
                mergedMassDict_chi2_drWeight[ntrkBin].Fill(dvMass, drWeight_chi2)
                mergedMassDict_chi2_weight[ntrkBin].Fill(dvMass, weight_chi2)
            if (passMatVeto):
                mergedMassDict_matVeto[ntrkBin].Fill(dvMass)
                mergedMassDict_matVeto_sigWeight[ntrkBin].Fill(dvMass, sigWeight_matVeto)
                mergedMassDict_matVeto_drWeight[ntrkBin].Fill(dvMass, drWeight_matVeto)
                mergedMassDict_matVeto_weight[ntrkBin].Fill(dvMass, weight_matVeto)
            if (passFiducial and passDist and passChi2 and passMatVeto):
                mergedMassDict_DVsel[ntrkBin].Fill(dvMass)
                mergedMassDict_DVsel_sigWeight[ntrkBin].Fill(dvMass, sigWeight_DVsel)
                mergedMassDict_DVsel_drWeight[ntrkBin].Fill(dvMass, drWeight_DVsel)
                mergedMassDict_DVsel_weight[ntrkBin].Fill(dvMass, weight_DVsel)
            """

for ntrkBin in ntrkList:
    mergedMassHist = mergedMassDict[ntrkBin]
    mergedMassHist_sigWeight = mergedMassDict_sigWeight[ntrkBin]
    mergedMassHist_drWeight = mergedMassDict_drWeight[ntrkBin]
    mergedMassHist_weight = mergedMassDict_weight[ntrkBin]
    """
    mergedMassHist_fiducial = mergedMassDict_fiducial[ntrkBin]
    mergedMassHist_fiducial_sigWeight = mergedMassDict_fiducial_sigWeight[ntrkBin]
    mergedMassHist_fiducial_drWeight = mergedMassDict_fiducial_drWeight[ntrkBin]
    mergedMassHist_fiducial_weight = mergedMassDict_fiducial_weight[ntrkBin]
    mergedMassHist_dist = mergedMassDict_dist[ntrkBin]
    mergedMassHist_dist_sigWeight = mergedMassDict_dist_sigWeight[ntrkBin]
    mergedMassHist_dist_drWeight = mergedMassDict_dist_drWeight[ntrkBin]
    mergedMassHist_dist_weight = mergedMassDict_dist_weight[ntrkBin]
    mergedMassHist_chi2 = mergedMassDict_chi2[ntrkBin]
    mergedMassHist_chi2_sigWeight = mergedMassDict_chi2_sigWeight[ntrkBin]
    mergedMassHist_chi2_drWeight = mergedMassDict_chi2_drWeight[ntrkBin]
    mergedMassHist_chi2_weight = mergedMassDict_chi2_weight[ntrkBin]
    mergedMassHist_matVeto = mergedMassDict_matVeto[ntrkBin]
    mergedMassHist_matVeto_sigWeight = mergedMassDict_matVeto_sigWeight[ntrkBin]
    mergedMassHist_matVeto_drWeight = mergedMassDict_matVeto_drWeight[ntrkBin]
    mergedMassHist_matVeto_weight = mergedMassDict_matVeto_weight[ntrkBin]
    mergedMassHist_DVsel = mergedMassDict_DVsel[ntrkBin]
    mergedMassHist_DVsel_sigWeight = mergedMassDict_DVsel_sigWeight[ntrkBin]
    mergedMassHist_DVsel_drWeight = mergedMassDict_DVsel_drWeight[ntrkBin]
    mergedMassHist_DVsel_weight = mergedMassDict_DVsel_weight[ntrkBin]
    """


    plotMassHist(mergedMassHist, "", "", ntrkBin, c, sampleLabel, dataLabel, label)
    plotMassHist(mergedMassHist_sigWeight, "", "sigWeight", ntrkBin, c, sampleLabel, dataLabel, label)
    plotMassHist(mergedMassHist_drWeight, "", "drWeight", ntrkBin, c, sampleLabel, dataLabel, label)
    plotMassHist(mergedMassHist_weight, "", "weight", ntrkBin, c, sampleLabel, dataLabel, label)
    """
    plotMassHist(mergedMassHist_fiducial, "fiducial", "", ntrkBin, c, sampleLabel, dataLabel, label)
    plotMassHist(mergedMassHist_fiducial_sigWeight, "fiducial", "sigWeight", ntrkBin, c, sampleLabel, dataLabel, label)
    plotMassHist(mergedMassHist_fiducial_drWeight, "fiducial", "drWeight", ntrkBin, c, sampleLabel, dataLabel, label)
    plotMassHist(mergedMassHist_fiducial_weight, "fiducial", "weight", ntrkBin, c, sampleLabel, dataLabel, label)
    plotMassHist(mergedMassHist_dist, "dist", "", ntrkBin, c, sampleLabel, dataLabel, label)
    plotMassHist(mergedMassHist_dist_sigWeight, "dist", "sigWeight", ntrkBin, c, sampleLabel, dataLabel, label)
    plotMassHist(mergedMassHist_dist_drWeight, "dist", "drWeight", ntrkBin, c, sampleLabel, dataLabel, label)
    plotMassHist(mergedMassHist_dist_weight, "dist", "weight", ntrkBin, c, sampleLabel, dataLabel, label)
    plotMassHist(mergedMassHist_chi2, "chi2", "", ntrkBin, c, sampleLabel, dataLabel, label)
    plotMassHist(mergedMassHist_chi2_sigWeight, "chi2", "sigWeight", ntrkBin, c, sampleLabel, dataLabel, label)
    plotMassHist(mergedMassHist_chi2_drWeight, "chi2", "drWeight", ntrkBin, c, sampleLabel, dataLabel, label)
    plotMassHist(mergedMassHist_chi2_weight, "chi2", "weight", ntrkBin, c, sampleLabel, dataLabel, label)
    plotMassHist(mergedMassHist_matVeto, "matVeto", "", ntrkBin, c, sampleLabel, dataLabel, label)
    plotMassHist(mergedMassHist_matVeto_sigWeight, "matVeto", "sigWeight", ntrkBin, c, sampleLabel, dataLabel, label)
    plotMassHist(mergedMassHist_matVeto_drWeight, "matVeto", "drWeight", ntrkBin, c, sampleLabel, dataLabel, label)
    plotMassHist(mergedMassHist_matVeto_weight, "matVeto", "weight", ntrkBin, c, sampleLabel, dataLabel, label)
    plotMassHist(mergedMassHist_DVsel, "DVsel", "", ntrkBin, c, sampleLabel, dataLabel, label)
    plotMassHist(mergedMassHist_DVsel_sigWeight, "DVsel", "sigWeight", ntrkBin, c, sampleLabel, dataLabel, label)
    plotMassHist(mergedMassHist_DVsel_drWeight, "DVsel", "drWeight", ntrkBin, c, sampleLabel, dataLabel, label)
    plotMassHist(mergedMassHist_DVsel_weight, "DVsel", "weight", ntrkBin, c, sampleLabel, dataLabel, label)
    """
    

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
