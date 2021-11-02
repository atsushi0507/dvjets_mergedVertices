import ROOT as r
import datetime
from helper import *
import sys, os
sys.path.append("/Users/amizukam/DVJets/atlasstyle")
from AtlasStyle import *
from AtlasLabel import *

r.gROOT.SetBatch()
SetAtlasStyle()
label = "Internal"

dataSet = "mc16e"
#dataSet = "mc16e_trackCleaning"


plotType = "properties"
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
binLabel = ["G4", "G4+PU", "G4+Gen", "PU", "PU+Gen", "Gen", "Combination"]

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
dvType_total = {}
dvType_MVcand = {}
dvType_passDVsel = {}
dvType_oneParent = {}
dvType_multiParent = {}
dvType_hasUnrelatedTrack = {}
dvType_noUnrelatedTrack = {}
for ntrkBin in ntrkList:
    dvType_total[ntrkBin] = r.TH1D("dvType_total_" + ntrkBin, ";DV type", 7, 1, 8)
    dvType_total[ntrkBin].SetLabelSize(0.03)
    dvType_MVcand[ntrkBin] = r.TH1D("dvType_MVcand_" + ntrkBin, ";DV_type", 7, 1, 8)
    dvType_MVcand[ntrkBin].SetLabelSize(0.03)
    dvType_passDVsel[ntrkBin] = r.TH1D("dvType_passDVsel_" + ntrkBin, ";DV type", 7, 1, 8)
    dvType_passDVsel[ntrkBin].SetLabelSize(0.03)
    dvType_oneParent[ntrkBin] = r.TH1D("dvType_oneParent_" + ntrkBin, ";DV type", 7, 1, 8)   
    dvType_oneParent[ntrkBin].SetLabelSize(0.03)
    dvType_multiParent[ntrkBin] = r.TH1D("dvType_multiParent_" + ntrkBin, ";DV type", 7, 1, 8)
    dvType_multiParent[ntrkBin].SetLabelSize(0.03)
    dvType_hasUnrelatedTrack[ntrkBin] = r.TH1D("dvType_hasUnrelatedTrack_" + ntrkBin, ";DV type", 7, 1, 8)
    dvType_hasUnrelatedTrack[ntrkBin].SetLabelSize(0.03)
    dvType_noUnrelatedTrack[ntrkBin] = r.TH1D("dvType_noUnrelatedTrack_" + ntrkBin, ";DV type", 7, 1, 8)
    dvType_noUnrelatedTrack[ntrkBin].SetLabelSize(0.03)
    for nbin in range(1, dvType_total[ntrkBin].GetNbinsX()+1):
        dvType_total[ntrkBin].GetXaxis().SetBinLabel(nbin, binLabel[nbin-1])
        dvType_MVcand[ntrkBin].GetXaxis().SetBinLabel(nbin, binLabel[nbin-1])
        dvType_passDVsel[ntrkBin].GetXaxis().SetBinLabel(nbin, binLabel[nbin-1])
        dvType_oneParent[ntrkBin].GetXaxis().SetBinLabel(nbin, binLabel[nbin-1])
        dvType_multiParent[ntrkBin].GetXaxis().SetBinLabel(nbin, binLabel[nbin-1])
        dvType_hasUnrelatedTrack[ntrkBin].GetXaxis().SetBinLabel(nbin, binLabel[nbin-1])
        dvType_noUnrelatedTrack[ntrkBin].GetXaxis().SetBinLabel(nbin, binLabel[nbin-1])

dvCounter = 0
for dv in tree:
    dvType = dv.dv_type
    dvNtrk = dv.dv_ntrk
    if (dvNtrk < 2):
        continue

    eventWeight = dv.mcEventWeight
    ntrkBin = determineNtrkBin(dvNtrk)
    dvType_total[ntrkBin].Fill(dvType)
    
    dvPassFiducial = dv.dv_PassFiducialCut
    dvPassDist = dv.dv_PassDistCut
    dvPassChi2 = dv.dv_PassChi2Cut
    dvIsInMaterial = dv.dv_isInMaterial
    dvHasDefinedPdgId = dv.dv_hasDefinedPdgId

    nParents = dv.nParents
    hasUnrelatedTracks = dv.hasUnrelatedTracks
    dvProperties = {}
    dvProperties["dist"] = dv.dv_maxTruthParticleDist
    dvProperties["distSig"] = dv.dv_maxTruthParticleDistSig
    dvProperties["interDist"] = dv.dv_maxInterTruthParticleDist
    maxInterTruthParticleDist = dv.dv_maxInterTruthParticleDist

    if (nParents > 1 and not hasUnrelatedTracks and maxInterTruthParticleDist > 0.15):
        dvType_MVcand[ntrkBin].Fill(dvType)

    if (not dvPassFiducial):
        continue
    if (not dvPassDist):
        continue
    if (not dvPassChi2):
        continue
    if (dvIsInMaterial):
        continue
    dvType_passDVsel[ntrkBin].Fill(dvType)

    if (nParents == 1):
        dvType_oneParent[ntrkBin].Fill(dvType)
    else:
        dvType_multiParent[ntrkBin].Fill(dvType)
        if (maxInterTruthParticleDist < 0.15):
            continue
        if (hasUnrelatedTracks):
            dvType_hasUnrelatedTrack[ntrkBin].Fill(dvType)
        else:
            dvType_noUnrelatedTrack[ntrkBin].Fill(dvType)

    dvCounter += 1

sampleLabel = r.TLatex()
sampleLabel.SetNDC()
sampleLabel.SetTextFont(42)
sampleLabel.SetTextAlign(13)
sampleLabel.SetTextSize(0.03)

sampleText1 = dataSet + ", di-jet"

c = r.TCanvas("c", "c", 800, 700)
c.cd()

for ntrkBin in ntrkList:
    totalHist = dvType_total[ntrkBin]
    mvCandHist = dvType_MVcand[ntrkBin]
    dvSelHist = dvType_passDVsel[ntrkBin]
    oneParentHist = dvType_oneParent[ntrkBin]
    multiParentHist = dvType_multiParent[ntrkBin]
    hasUnrelatedTrackHist = dvType_hasUnrelatedTrack[ntrkBin]
    noUnrelatedTrackHist = dvType_noUnrelatedTrack[ntrkBin]

    c.SetLogy(0)
    totalHist.Draw("histo")
    ATLASLabel(0.2, 0.955, label)
    sampleLabel.DrawLatex(0.75, 0.85, sampleText1)
    sampleLabel.DrawLatex(0.75,0.8, "Event preselection")
    sampleLabel.DrawLatex(0.75, 0.75, getNtrkLabel(ntrkBin))
    c.Print("{}/{}.pdf".format(directory, "dvType_total_"+ntrkBin))

    c.SetLogy(1)
    totalHist.Draw("histo")
    ATLASLabel(0.2, 0.955, label)
    sampleLabel.DrawLatex(0.75, 0.85, sampleText1)
    sampleLabel.DrawLatex(0.75,0.8, "Event preselection")
    sampleLabel.DrawLatex(0.75, 0.75, getNtrkLabel(ntrkBin))
    c.Print("{}/{}.pdf".format(directory, "dvType_total_"+ntrkBin+"_logy"))

    c.SetLogy(0)
    mvCandHist.Draw("histo")
    ATLASLabel(0.2, 0.955, label)
    sampleLabel.DrawLatex(0.70, 0.85, sampleText1)
    sampleLabel.DrawLatex(0.70,0.8, "Event preselection")
    sampleLabel.DrawLatex(0.70, 0.75, "MV candidates")
    sampleLabel.DrawLatex(0.70, 0.70, getNtrkLabel(ntrkBin))
    c.Print("{}/{}.pdf".format(directory, "dvType_mvCand_"+ntrkBin))

    c.SetLogy(1)
    mvCandHist.Draw("histo")
    ATLASLabel(0.2, 0.955, label)
    sampleLabel.DrawLatex(0.75, 0.85, sampleText1)
    sampleLabel.DrawLatex(0.75,0.8, "Event preselection")
    sampleLabel.DrawLatex(0.75, 0.75, "MV candidates")
    sampleLabel.DrawLatex(0.75, 0.70, getNtrkLabel(ntrkBin))
    c.Print("{}/{}.pdf".format(directory, "dvType_mvCand_"+ntrkBin+"_logy"))

    c.SetLogy(0)
    dvSelHist.Draw("histo")
    ATLASLabel(0.2, 0.955, label)
    sampleLabel.DrawLatex(0.75, 0.85, sampleText1)
    sampleLabel.DrawLatex(0.75, 0.80, "Event and DV preselection")
    sampleLabel.DrawLatex(0.75, 0.75, getNtrkLabel(ntrkBin))
    c.Print("{}/{}.pdf".format(directory, "dvType_passDVsel_"+ntrkBin))

    c.SetLogy(1)
    dvSelHist.Draw("histo")
    ATLASLabel(0.2, 0.955, label)
    sampleLabel.DrawLatex(0.75, 0.85, sampleText1)
    sampleLabel.DrawLatex(0.75, 0.80, "Event and DV preselection")
    sampleLabel.DrawLatex(0.75, 0.75, getNtrkLabel(ntrkBin))
    c.Print("{}/{}.pdf".format(directory, "dvType_passDVsel_"+ntrkBin+"_logy"))

    c.SetLogy(0)
    oneParentHist.Draw("histo")
    ATLASLabel(0.2, 0.955, label)
    sampleLabel.DrawLatex(0.75, 0.85, sampleText1)
    sampleLabel.DrawLatex(0.75, 0.80, "Event and DV preselection")
    sampleLabel.DrawLatex(0.75, 0.75, "DV has one parent")
    sampleLabel.DrawLatex(0.75, 0.70, getNtrkLabel(ntrkBin))
    c.Print("{}/{}.pdf".format(directory, "dvType_oneParent_"+ntrkBin))

    c.SetLogy(1)
    oneParentHist.Draw("histo")
    ATLASLabel(0.2, 0.955, label)
    sampleLabel.DrawLatex(0.75, 0.85, sampleText1)
    sampleLabel.DrawLatex(0.75, 0.80, "Event and DV preselection")
    sampleLabel.DrawLatex(0.75, 0.75, "DV has one parent")
    sampleLabel.DrawLatex(0.75, 0.70, getNtrkLabel(ntrkBin))
    c.Print("{}/{}.pdf".format(directory, "dvType_oneParent_"+ntrkBin+"_logy"))

    c.SetLogy(0)
    multiParentHist.Draw("histo")
    ATLASLabel(0.2, 0.955, label)
    sampleLabel.DrawLatex(0.75, 0.85, sampleText1)
    sampleLabel.DrawLatex(0.75, 0.80, "Event and DV preselection")
    sampleLabel.DrawLatex(0.75, 0.75, "DV has multiple parent")
    sampleLabel.DrawLatex(0.75, 0.70, getNtrkLabel(ntrkBin))
    c.Print("{}/{}.pdf".format(directory, "dvType_multiParent_"+ntrkBin))

    c.SetLogy(1)
    multiParentHist.Draw("histo")
    ATLASLabel(0.2, 0.955, label)
    sampleLabel.DrawLatex(0.75, 0.85, sampleText1)
    sampleLabel.DrawLatex(0.75, 0.80, "Event and DV preselection")
    sampleLabel.DrawLatex(0.75, 0.75, "DV has multiple parent")
    sampleLabel.DrawLatex(0.75, 0.70, getNtrkLabel(ntrkBin))
    c.Print("{}/{}.pdf".format(directory, "dvType_multiParent_"+ntrkBin+"_logy"))

    c.SetLogy(0)
    hasUnrelatedTrackHist.Draw("histo")
    ATLASLabel(0.2, 0.955, label)
    sampleLabel.DrawLatex(0.55, 0.85, sampleText1)
    sampleLabel.DrawLatex(0.55, 0.80, "Event and DV preselection")
    sampleLabel.DrawLatex(0.55, 0.75, "DV has multiple parent, with AX")
    sampleLabel.DrawLatex(0.55, 0.70, getNtrkLabel(ntrkBin))
    c.Print("{}/{}.pdf".format(directory, "dvType_hasUnrelatedTrack_"+ntrkBin))

    c.SetLogy(1)
    hasUnrelatedTrackHist.Draw("histo")
    ATLASLabel(0.2, 0.955, label)
    sampleLabel.DrawLatex(0.55, 0.85, sampleText1)
    sampleLabel.DrawLatex(0.55, 0.80, "Event and DV preselection")
    sampleLabel.DrawLatex(0.55, 0.75, "DV has multiple parent, with AX")
    sampleLabel.DrawLatex(0.55, 0.70, getNtrkLabel(ntrkBin))
    c.Print("{}/{}.pdf".format(directory, "dvType_hasUnrelatedTrack_"+ntrkBin+"_logy"))

    c.SetLogy(0)
    noUnrelatedTrackHist.Draw("histo")
    ATLASLabel(0.2, 0.955, label)
    sampleLabel.DrawLatex(0.55, 0.85, sampleText1)
    sampleLabel.DrawLatex(0.55, 0.80, "Event and DV preselection")
    sampleLabel.DrawLatex(0.55, 0.75, "DV has multiple parent, without AX")
    sampleLabel.DrawLatex(0.55, 0.70, getNtrkLabel(ntrkBin))
    c.Print("{}/{}.pdf".format(directory, "dvType_noUnrelatedTrack_"+ntrkBin))

    c.SetLogy(1)
    noUnrelatedTrackHist.Draw("histo")
    ATLASLabel(0.2, 0.955, label)
    sampleLabel.DrawLatex(0.55, 0.85, sampleText1)
    sampleLabel.DrawLatex(0.55, 0.80, "Event and DV preselection")
    sampleLabel.DrawLatex(0.55, 0.75, "DV has multiple parent, without AX")
    sampleLabel.DrawLatex(0.55, 0.70, getNtrkLabel(ntrkBin))
    c.Print("{}/{}.pdf".format(directory, "dvType_noUnrelatedTrack_"+ntrkBin+"_logy"))


outputFile.Write()
outputFile.Close()
