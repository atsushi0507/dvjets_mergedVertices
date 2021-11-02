import ROOT as r
import sys, os
sys.path.append("/Users/amizukam/DVJets/atlasstyle")
from AtlasStyle import *
from AtlasLabel import *

r.gROOT.SetBatch()
SetAtlasStyle()
label = "Internal"

dataSet = "mc16e"
#dataSet = "mc16e_trackCleaning"

plotType = "cutflow"
directory = "pdfs/" + plotType + "/" + dataSet + "_newSamples/"
if (not os.path.isdir(directory)):
    os.makedirs(directory)
if (not os.path.isdir("rootfiles")):
    os.makedirs("rootfiles")

inputFile = r.TFile("../outputFiles/mergedVerticesTreeMC_{}_newSamples.root".format(dataSet), "READ")
tree = inputFile.Get("trees_SRDV_")

outputFile = r.TFile("rootfiles/{}_{}.root".format(plotType, dataSet), "RECREATE")

colors = [r.kGreen-3, r.kRed-3, r.kBlue-3, r.kOrange-3, r.kMagenta-3, r.kCyan-3]

ntrkList = ["Ntrk2", "Ntrk3", "Ntrk4", "Ntrk5", "Ntrk6", "Ntrk>6"]

def determineNtrkBin(ntrk):
    ntrkBin = ""
    if ntrk == 2:
        ntrkBin = "Ntrk2"
    if ntrk == 3:
        ntrkBin = "Ntrk3"
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
    if ntrkBin == "Ntrk2":
        ntrkLabel = "N_{trk} = 2"
    if ntrkBin == "Ntrk3":
        ntrkLabel = "N_{trk} = 3"
    if ntrkBin == "Ntrk4":
        ntrkLabel = "N_{trk} = 4"
    if ntrkBin == "Ntrk5":
        ntrkLabel = "N_{trk} = 5"
    if ntrkBin == "Ntrk6":
        ntrkLabel = "N_{trk} = 6"
    if ntrkBin == "Ntrk>6":
        ntrkLabel = "N_{trk} > 6"
    return ntrkLabel

# Define histograms
cutflow_inclusive = {}
cutflow_dvType1 = {}
cutflow_dvType2 = {}
cutflow_dvType3 = {}
cutflow_dvType4 = {}
cutflow_dvType5 = {}
cutflow_dvType6 = {}
cutflow_dvType7 = {}
cutflow_label = ["Total", "Fiducial cut", "PV-DV dist > 4mm", "#chi^{2}/n_{DoF} cut", "Material veto", "nParent > 1", "has multi-track", "dX_{max}>0.15mm"]
cutflow_inclusive_noDVsel = {}
cutflow_dvType1_noDVsel = {}
cutflow_dvType2_noDVsel = {}
cutflow_dvType3_noDVsel = {}
cutflow_dvType4_noDVsel = {}
cutflow_dvType5_noDVsel = {}
cutflow_dvType6_noDVsel = {}
cutflow_dvType7_noDVsel = {}
cutflow_label2 = ["Total", "nParent > 1", "has multi-track", "dX_{max}>0.15mm"]
for ntrkBin in ntrkList:
    cutflow_inclusive[ntrkBin] = r.TH1D("cutflow_inclusive_"+ntrkBin, ";cutflow", 8, 0, 8)
    cutflow_dvType1[ntrkBin] = r.TH1D("cutflow_dvType1_"+ntrkBin, ";cutflow", 8, 0, 8)
    cutflow_dvType2[ntrkBin] = r.TH1D("cutflow_dvType2_"+ntrkBin, ";cutflow", 8, 0, 8)
    cutflow_dvType3[ntrkBin] = r.TH1D("cutflow_dvType3_"+ntrkBin, ";cutflow", 8, 0, 8)
    cutflow_dvType4[ntrkBin] = r.TH1D("cutflow_dvType4_"+ntrkBin, ";cutflow", 8, 0, 8)
    cutflow_dvType5[ntrkBin] = r.TH1D("cutflow_dvType5_"+ntrkBin, ";cutflow", 8, 0, 8)
    cutflow_dvType6[ntrkBin] = r.TH1D("cutflow_dvType6_"+ntrkBin, ";cutflow", 8, 0, 8)
    cutflow_dvType7[ntrkBin] = r.TH1D("cutflow_dvType7_"+ntrkBin, ";cutflow", 8, 0, 8)

    cutflow_inclusive_noDVsel[ntrkBin] = r.TH1D("cutflow_inclusive_noDVsel_"+ntrkBin, ";cutflow", 4, 0, 4)
    cutflow_dvType1_noDVsel[ntrkBin] = r.TH1D("cutflow_dvType1_noDVsel_"+ntrkBin, ";cutflow", 4, 0, 4)
    cutflow_dvType2_noDVsel[ntrkBin] = r.TH1D("cutflow_dvType2_noDVsel_"+ntrkBin, ";cutflow", 4, 0, 4)
    cutflow_dvType3_noDVsel[ntrkBin] = r.TH1D("cutflow_dvType3_noDVsel_"+ntrkBin, ";cutflow", 4, 0, 4)
    cutflow_dvType4_noDVsel[ntrkBin] = r.TH1D("cutflow_dvType4_noDVsel_"+ntrkBin, ";cutflow", 4, 0, 4)
    cutflow_dvType5_noDVsel[ntrkBin] = r.TH1D("cutflow_dvType5_noDVsel_"+ntrkBin, ";cutflow", 4, 0, 4)
    cutflow_dvType6_noDVsel[ntrkBin] = r.TH1D("cutflow_dvType6_noDVsel_"+ntrkBin, ";cutflow", 4, 0, 4)
    cutflow_dvType7_noDVsel[ntrkBin] = r.TH1D("cutflow_dvType7_noDVsel_"+ntrkBin, ";cutflow", 4, 0, 4)
    for nbin in range(cutflow_inclusive[ntrkBin].GetNbinsX()):
        cutflow_inclusive[ntrkBin].GetXaxis().SetBinLabel(nbin+1, cutflow_label[nbin])
        cutflow_dvType1[ntrkBin].GetXaxis().SetBinLabel(nbin+1, cutflow_label[nbin])
        cutflow_dvType2[ntrkBin].GetXaxis().SetBinLabel(nbin+1, cutflow_label[nbin])
        cutflow_dvType3[ntrkBin].GetXaxis().SetBinLabel(nbin+1, cutflow_label[nbin])
        cutflow_dvType4[ntrkBin].GetXaxis().SetBinLabel(nbin+1, cutflow_label[nbin])
        cutflow_dvType5[ntrkBin].GetXaxis().SetBinLabel(nbin+1, cutflow_label[nbin])
        cutflow_dvType6[ntrkBin].GetXaxis().SetBinLabel(nbin+1, cutflow_label[nbin])
        cutflow_dvType7[ntrkBin].GetXaxis().SetBinLabel(nbin+1, cutflow_label[nbin])
    for nbin in range(cutflow_inclusive_noDVsel[ntrkBin].GetNbinsX()):
        cutflow_inclusive_noDVsel[ntrkBin].GetXaxis().SetBinLabel(nbin+1, cutflow_label2[nbin])
        cutflow_dvType1_noDVsel[ntrkBin].GetXaxis().SetBinLabel(nbin+1, cutflow_label2[nbin])
        cutflow_dvType2_noDVsel[ntrkBin].GetXaxis().SetBinLabel(nbin+1, cutflow_label2[nbin])
        cutflow_dvType3_noDVsel[ntrkBin].GetXaxis().SetBinLabel(nbin+1, cutflow_label2[nbin])
        cutflow_dvType4_noDVsel[ntrkBin].GetXaxis().SetBinLabel(nbin+1, cutflow_label2[nbin])
        cutflow_dvType5_noDVsel[ntrkBin].GetXaxis().SetBinLabel(nbin+1, cutflow_label2[nbin])
        cutflow_dvType6_noDVsel[ntrkBin].GetXaxis().SetBinLabel(nbin+1, cutflow_label2[nbin])
        cutflow_dvType7_noDVsel[ntrkBin].GetXaxis().SetBinLabel(nbin+1, cutflow_label2[nbin])

print("Looping with DV selections")
for dv in tree:
    dvNtrk = dv.dv_ntrk
    if (dvNtrk < 2):
        continue
    ntrkBin = determineNtrkBin(dvNtrk)
    dvType = dv.dv_type

    cutflow_inclusive[ntrkBin].AddBinContent(1)
    if (dvType == 1):
        cutflow_dvType1[ntrkBin].AddBinContent(1)
    elif (dvType == 2):
        cutflow_dvType2[ntrkBin].AddBinContent(1)
    elif (dvType == 3):
        cutflow_dvType3[ntrkBin].AddBinContent(1)
    elif (dvType == 4):
        cutflow_dvType4[ntrkBin].AddBinContent(1)
    elif (dvType == 5):
        cutflow_dvType5[ntrkBin].AddBinContent(1)
    elif (dvType == 6):
        cutflow_dvType6[ntrkBin].AddBinContent(1)
    elif (dvType == 7):
        cutflow_dvType7[ntrkBin].AddBinContent(1)

    if (not dv.dv_PassFiducialCut):
        continue
    cutflow_inclusive[ntrkBin].AddBinContent(2)
    if (dvType == 1):
        cutflow_dvType1[ntrkBin].AddBinContent(2)
    elif (dvType == 2):
        cutflow_dvType2[ntrkBin].AddBinContent(2)
    elif (dvType == 3):
        cutflow_dvType3[ntrkBin].AddBinContent(2)
    elif (dvType == 4):
        cutflow_dvType4[ntrkBin].AddBinContent(2)
    elif (dvType == 5):
        cutflow_dvType5[ntrkBin].AddBinContent(2)
    elif (dvType == 6):
        cutflow_dvType6[ntrkBin].AddBinContent(2)
    elif (dvType == 7):
        cutflow_dvType7[ntrkBin].AddBinContent(2)

    if (not dv.dv_PassDistCut):
        continue
    cutflow_inclusive[ntrkBin].AddBinContent(3)
    if (dvType == 1):
        cutflow_dvType1[ntrkBin].AddBinContent(3)
    elif (dvType == 2):
        cutflow_dvType2[ntrkBin].AddBinContent(3)
    elif (dvType == 3):
        cutflow_dvType3[ntrkBin].AddBinContent(3)
    elif (dvType == 4):
        cutflow_dvType4[ntrkBin].AddBinContent(3)
    elif (dvType == 5):
        cutflow_dvType5[ntrkBin].AddBinContent(3)
    elif (dvType == 6):
        cutflow_dvType6[ntrkBin].AddBinContent(3)
    elif (dvType == 7):
        cutflow_dvType7[ntrkBin].AddBinContent(3)

    if (not dv.dv_PassChi2Cut):
        continue
    cutflow_inclusive[ntrkBin].AddBinContent(4)
    if (dvType == 1):
        cutflow_dvType1[ntrkBin].AddBinContent(4)
    elif (dvType == 2):
        cutflow_dvType2[ntrkBin].AddBinContent(4)
    elif (dvType == 3):
        cutflow_dvType3[ntrkBin].AddBinContent(4)
    elif (dvType == 4):
        cutflow_dvType4[ntrkBin].AddBinContent(4)
    elif (dvType == 5):
        cutflow_dvType5[ntrkBin].AddBinContent(4)
    elif (dvType == 6):
        cutflow_dvType6[ntrkBin].AddBinContent(4)
    elif (dvType == 7):
        cutflow_dvType7[ntrkBin].AddBinContent(4)

    if (dv.dv_isInMaterial):
        continue
    cutflow_inclusive[ntrkBin].AddBinContent(5)
    if (dvType == 1):
        cutflow_dvType1[ntrkBin].AddBinContent(5)
    elif (dvType == 2):
        cutflow_dvType2[ntrkBin].AddBinContent(5)
    elif (dvType == 3):
        cutflow_dvType3[ntrkBin].AddBinContent(5)
    elif (dvType == 4):
        cutflow_dvType4[ntrkBin].AddBinContent(5)
    elif (dvType == 5):
        cutflow_dvType5[ntrkBin].AddBinContent(5)
    elif (dvType == 6):
        cutflow_dvType6[ntrkBin].AddBinContent(5)
    elif (dvType == 7):
        cutflow_dvType7[ntrkBin].AddBinContent(5)

    if (dv.nParents < 2):
        continue
    cutflow_inclusive[ntrkBin].AddBinContent(6)
    if (dvType == 1):
        cutflow_dvType1[ntrkBin].AddBinContent(6)
    elif (dvType == 2):
        cutflow_dvType2[ntrkBin].AddBinContent(6)
    elif (dvType == 3):
        cutflow_dvType3[ntrkBin].AddBinContent(6)
    elif (dvType == 4):
        cutflow_dvType4[ntrkBin].AddBinContent(6)
    elif (dvType == 5):
        cutflow_dvType5[ntrkBin].AddBinContent(6)
    elif (dvType == 6):
        cutflow_dvType6[ntrkBin].AddBinContent(6)
    elif (dvType == 7):
        cutflow_dvType7[ntrkBin].AddBinContent(6)

    if (dv.hasUnrelatedTracks):
        continue
    cutflow_inclusive[ntrkBin].AddBinContent(7)
    if (dvType == 1):
        cutflow_dvType1[ntrkBin].AddBinContent(7)
    elif (dvType == 2):
        cutflow_dvType2[ntrkBin].AddBinContent(7)
    elif (dvType == 3):
        cutflow_dvType3[ntrkBin].AddBinContent(7)
    elif (dvType == 4):
        cutflow_dvType4[ntrkBin].AddBinContent(7)
    elif (dvType == 5):
        cutflow_dvType5[ntrkBin].AddBinContent(7)
    elif (dvType == 6):
        cutflow_dvType6[ntrkBin].AddBinContent(7)
    elif (dvType == 7):
        cutflow_dvType7[ntrkBin].AddBinContent(7)

    if (dv.dv_maxInterTruthParticleDist < 0.15):
        continue
    cutflow_inclusive[ntrkBin].AddBinContent(8)
    if (dvType == 1):
        cutflow_dvType1[ntrkBin].AddBinContent(8)
    if (dvType == 2):
        cutflow_dvType2[ntrkBin].AddBinContent(8)
    if (dvType == 3):
        cutflow_dvType3[ntrkBin].AddBinContent(8)
    if (dvType == 4):
        cutflow_dvType4[ntrkBin].AddBinContent(8)
    if (dvType == 5):
        cutflow_dvType5[ntrkBin].AddBinContent(8)
    if (dvType == 6):
        cutflow_dvType6[ntrkBin].AddBinContent(8)
    if (dvType == 7):
        cutflow_dvType7[ntrkBin].AddBinContent(8)

print("Looping without DV selections")
for dv in tree:
    dvNtrk = dv.dv_ntrk
    if (dvNtrk < 2):
        continue
    ntrkBin = determineNtrkBin(dvNtrk)
    dvType = dv.dv_type

    cutflow_inclusive_noDVsel[ntrkBin].AddBinContent(1)
    if (dvType == 1):
        cutflow_dvType1_noDVsel[ntrkBin].AddBinContent(1)
    elif (dvType == 2):
        cutflow_dvType2_noDVsel[ntrkBin].AddBinContent(1)
    elif (dvType == 3):
        cutflow_dvType3_noDVsel[ntrkBin].AddBinContent(1)
    elif (dvType == 4):
        cutflow_dvType4_noDVsel[ntrkBin].AddBinContent(1)
    elif (dvType == 5):
        cutflow_dvType5_noDVsel[ntrkBin].AddBinContent(1)
    elif (dvType == 6):
        cutflow_dvType6_noDVsel[ntrkBin].AddBinContent(1)
    elif (dvType == 7):
        cutflow_dvType7_noDVsel[ntrkBin].AddBinContent(1)

    if (dv.nParents < 2):
        continue
    cutflow_inclusive_noDVsel[ntrkBin].AddBinContent(2)
    if (dvType == 1):
        cutflow_dvType1_noDVsel[ntrkBin].AddBinContent(2)
    elif (dvType == 2):
        cutflow_dvType2_noDVsel[ntrkBin].AddBinContent(2)
    elif (dvType == 3):
        cutflow_dvType3_noDVsel[ntrkBin].AddBinContent(2)
    elif (dvType == 4):
        cutflow_dvType4_noDVsel[ntrkBin].AddBinContent(2)
    elif (dvType == 5):
        cutflow_dvType5_noDVsel[ntrkBin].AddBinContent(2)
    elif (dvType == 6):
        cutflow_dvType6_noDVsel[ntrkBin].AddBinContent(2)
    elif (dvType == 7):
        cutflow_dvType7_noDVsel[ntrkBin].AddBinContent(2)

    if (dv.hasUnrelatedTracks):
        continue
    cutflow_inclusive_noDVsel[ntrkBin].AddBinContent(3)
    if (dvType == 1):
        cutflow_dvType1_noDVsel[ntrkBin].AddBinContent(3)
    elif (dvType == 2):
        cutflow_dvType2_noDVsel[ntrkBin].AddBinContent(3)
    elif (dvType == 3):
        cutflow_dvType3_noDVsel[ntrkBin].AddBinContent(3)
    elif (dvType == 4):
        cutflow_dvType4_noDVsel[ntrkBin].AddBinContent(3)
    elif (dvType == 5):
        cutflow_dvType5_noDVsel[ntrkBin].AddBinContent(3)
    elif (dvType == 6):
        cutflow_dvType6_noDVsel[ntrkBin].AddBinContent(3)
    elif (dvType == 7):
        cutflow_dvType7_noDVsel[ntrkBin].AddBinContent(3)

    if (dv.dv_maxInterTruthParticleDist < 0.15):
        continue
    cutflow_inclusive_noDVsel[ntrkBin].AddBinContent(4)
    if (dvType == 1):
        cutflow_dvType1_noDVsel[ntrkBin].AddBinContent(4)
    if (dvType == 2):
        cutflow_dvType2_noDVsel[ntrkBin].AddBinContent(4)
    if (dvType == 3):
        cutflow_dvType3_noDVsel[ntrkBin].AddBinContent(4)
    if (dvType == 4):
        cutflow_dvType4_noDVsel[ntrkBin].AddBinContent(4)
    if (dvType == 5):
        cutflow_dvType5_noDVsel[ntrkBin].AddBinContent(4)
    if (dvType == 6):
        cutflow_dvType6_noDVsel[ntrkBin].AddBinContent(4)
    if (dvType == 7):
        cutflow_dvType7_noDVsel[ntrkBin].AddBinContent(4)


c = r.TCanvas("c", "c", 800, 700)
c.SetLeftMargin(0.14)
c.SetRightMargin(0.08)
c.cd()

sampleLabel = r.TLatex()
sampleLabel.SetNDC()
sampleLabel.SetTextFont(42)
sampleLabel.SetTextAlign(13)
sampleLabel.SetTextSize(0.03)
dataLabel = dataSet + ", di-jet"
for ntrkBin in ntrkList:
    inclusiveHist = cutflow_inclusive[ntrkBin]
    dvType1Hist = cutflow_dvType1[ntrkBin]
    dvType2Hist = cutflow_dvType2[ntrkBin]
    dvType3Hist = cutflow_dvType3[ntrkBin]
    dvType4Hist = cutflow_dvType4[ntrkBin]
    dvType5Hist = cutflow_dvType5[ntrkBin]
    dvType6Hist = cutflow_dvType6[ntrkBin]
    dvType7Hist = cutflow_dvType7[ntrkBin]

    inclusiveHist_noDVsel = cutflow_inclusive_noDVsel[ntrkBin]
    dvType1Hist_noDVsel = cutflow_dvType1_noDVsel[ntrkBin]
    dvType2Hist_noDVsel = cutflow_dvType2_noDVsel[ntrkBin]
    dvType3Hist_noDVsel = cutflow_dvType3_noDVsel[ntrkBin]
    dvType4Hist_noDVsel = cutflow_dvType4_noDVsel[ntrkBin]
    dvType5Hist_noDVsel = cutflow_dvType5_noDVsel[ntrkBin]
    dvType6Hist_noDVsel = cutflow_dvType6_noDVsel[ntrkBin]
    dvType7Hist_noDVsel = cutflow_dvType7_noDVsel[ntrkBin]

    inclusiveHist.SetMinimum(0)
    dvType1Hist.SetMinimum(0)
    dvType2Hist.SetMinimum(0)
    dvType3Hist.SetMinimum(0)
    dvType4Hist.SetMinimum(0)
    dvType5Hist.SetMinimum(0)
    dvType6Hist.SetMinimum(0)
    dvType7Hist.SetMinimum(0)

    inclusiveHist_noDVsel.SetMinimum(0)
    dvType1Hist_noDVsel.SetMinimum(0)
    dvType2Hist_noDVsel.SetMinimum(0)
    dvType3Hist_noDVsel.SetMinimum(0)
    dvType4Hist_noDVsel.SetMinimum(0)
    dvType5Hist_noDVsel.SetMinimum(0)
    dvType6Hist_noDVsel.SetMinimum(0)
    dvType7Hist_noDVsel.SetMinimum(0)
    
    c.SetLogy(0)
    inclusiveHist.Draw("histo")
    ATLASLabel(0.15, 0.955, label)
    sampleLabel.DrawLatex(0.65, 0.88, dataLabel)
    sampleLabel.DrawLatex(0.65, 0.83, "Event preselection")
    c.Print("{}/{}.pdf".format(directory, "cutflow_inclusive_"+ntrkBin))

    inclusiveHist_noDVsel.Draw("histo")
    ATLASLabel(0.15, 0.955, label)
    sampleLabel.DrawLatex(0.65, 0.88, dataLabel)
    sampleLabel.DrawLatex(0.65, 0.83, "Event preselection")
    c.Print("{}/{}.pdf".format(directory, "cutflow_inclusive_noDVsel_"+ntrkBin))

    dvType1Hist.Draw("histo")
    ATLASLabel(0.15, 0.955, label)
    sampleLabel.DrawLatex(0.65, 0.88, dataLabel)
    sampleLabel.DrawLatex(0.65, 0.83, "Event preselection")
    sampleLabel.DrawLatex(0.65, 0.78, "G4 DV")
    c.Print("{}/{}.pdf".format(directory, "cutflow_dvType1_"+ntrkBin))

    dvType1Hist_noDVsel.Draw("histo")
    ATLASLabel(0.15, 0.955, label)
    sampleLabel.DrawLatex(0.65, 0.88, dataLabel)
    sampleLabel.DrawLatex(0.65, 0.83, "Event preselection")
    sampleLabel.DrawLatex(0.65, 0.78, "G4 DV")
    c.Print("{}/{}.pdf".format(directory, "cutflow_dvType1_noDVsel_"+ntrkBin))

    dvType2Hist.Draw("histo")
    ATLASLabel(0.15, 0.955, label)
    sampleLabel.DrawLatex(0.65, 0.88, dataLabel)
    sampleLabel.DrawLatex(0.65, 0.83, "Event preselection")
    sampleLabel.DrawLatex(0.65, 0.78, "G4+PU DV")
    c.Print("{}/{}.pdf".format(directory, "cutflow_dvType2_"+ntrkBin))

    dvType2Hist_noDVsel.Draw("histo")
    ATLASLabel(0.15, 0.955, label)
    sampleLabel.DrawLatex(0.65, 0.88, dataLabel)
    sampleLabel.DrawLatex(0.65, 0.83, "Event preselection")
    sampleLabel.DrawLatex(0.65, 0.78, "G4+PU DV")
    c.Print("{}/{}.pdf".format(directory, "cutflow_dvType2_noDVsel_"+ntrkBin))

    dvType3Hist.Draw("histo")
    ATLASLabel(0.15, 0.955, label)
    sampleLabel.DrawLatex(0.65, 0.88, dataLabel)
    sampleLabel.DrawLatex(0.65, 0.83, "Event preselection")
    sampleLabel.DrawLatex(0.65, 0.78, "G4+Gen DV")
    c.Print("{}/{}.pdf".format(directory, "cutflow_dvType3_"+ntrkBin))

    dvType3Hist_noDVsel.Draw("histo")
    ATLASLabel(0.15, 0.955, label)
    sampleLabel.DrawLatex(0.65, 0.88, dataLabel)
    sampleLabel.DrawLatex(0.65, 0.83, "Event preselection")
    sampleLabel.DrawLatex(0.65, 0.78, "G4+Gen DV")
    c.Print("{}/{}.pdf".format(directory, "cutflow_dvType3_noDVsel_"+ntrkBin))

    dvType4Hist.Draw("histo")
    ATLASLabel(0.15, 0.955, label)
    sampleLabel.DrawLatex(0.65, 0.88, dataLabel)
    sampleLabel.DrawLatex(0.65, 0.83, "Event preselection")
    sampleLabel.DrawLatex(0.65, 0.78, "PU DV")
    c.Print("{}/{}.pdf".format(directory, "cutflow_dvType4_"+ntrkBin))

    dvType4Hist_noDVsel.Draw("histo")
    ATLASLabel(0.15, 0.955, label)
    sampleLabel.DrawLatex(0.65, 0.88, dataLabel)
    sampleLabel.DrawLatex(0.65, 0.83, "Event preselection")
    sampleLabel.DrawLatex(0.65, 0.78, "PU DV")
    c.Print("{}/{}.pdf".format(directory, "cutflow_dvType4_noDVsel_"+ntrkBin))

    dvType5Hist.Draw("histo")
    ATLASLabel(0.15, 0.955, label)
    sampleLabel.DrawLatex(0.65, 0.88, dataLabel)
    sampleLabel.DrawLatex(0.65, 0.83, "Event preselection")
    sampleLabel.DrawLatex(0.65, 0.78, "PU+Gen DV")
    c.Print("{}/{}.pdf".format(directory, "cutflow_dvType5_"+ntrkBin))

    dvType5Hist_noDVsel.Draw("histo")
    ATLASLabel(0.15, 0.955, label)
    sampleLabel.DrawLatex(0.65, 0.88, dataLabel)
    sampleLabel.DrawLatex(0.65, 0.83, "Event preselection")
    sampleLabel.DrawLatex(0.65, 0.78, "PU+Gen DV")
    c.Print("{}/{}.pdf".format(directory, "cutflow_dvType5_noDVsel_"+ntrkBin))

    dvType6Hist.Draw("histo")
    ATLASLabel(0.15, 0.955, label)
    sampleLabel.DrawLatex(0.65, 0.88, dataLabel)
    sampleLabel.DrawLatex(0.65, 0.83, "Event preselection")
    sampleLabel.DrawLatex(0.65, 0.78, "Gen DV")
    c.Print("{}/{}.pdf".format(directory, "cutflow_dvType6_"+ntrkBin))

    dvType6Hist_noDVsel.Draw("histo")
    ATLASLabel(0.15, 0.955, label)
    sampleLabel.DrawLatex(0.65, 0.88, dataLabel)
    sampleLabel.DrawLatex(0.65, 0.83, "Event preselection")
    sampleLabel.DrawLatex(0.65, 0.78, "Gen DV")
    c.Print("{}/{}.pdf".format(directory, "cutflow_dvType6_noDVsel_"+ntrkBin))

    dvType7Hist.Draw("histo")
    ATLASLabel(0.15, 0.955, label)
    sampleLabel.DrawLatex(0.65, 0.88, dataLabel)
    sampleLabel.DrawLatex(0.65, 0.83, "Event preselection")
    sampleLabel.DrawLatex(0.65, 0.78, "Combination DV")
    c.Print("{}/{}.pdf".format(directory, "cutflow_dvType7_"+ntrkBin))

    dvType7Hist_noDVsel.Draw("histo")
    ATLASLabel(0.15, 0.955, label)
    sampleLabel.DrawLatex(0.65, 0.88, dataLabel)
    sampleLabel.DrawLatex(0.65, 0.83, "Event preselection")
    sampleLabel.DrawLatex(0.65, 0.78, "Combination DV")
    c.Print("{}/{}.pdf".format(directory, "cutflow_dvType7_noDVsel_"+ntrkBin))


outputFile.Write()
outputFile.Close()
