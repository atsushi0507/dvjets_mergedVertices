import ROOT as r
import sys, os
sys.path.append("/Users/amizukam/DVJets/atlasstyle")
from AtlasStyle import *
from AtlasLabel import *
from utils import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-tag", required=True, help="The campaign tag, 'a', 'd', or 'e'")
parser.add_argument("-sr", "--SR", required=True, help="Signal region, 'HighPtSR' or 'TracklessSR'")
parser.add_argument("-doHI", "--doHIrejection", action="store_true", default=False, help="Reject HI from MV")
parser.add_argument("-tc", "--trackCleaning", action="store_true", default=False, help="Read trackCleaning file")
args = parser.parse_args()

r.gROOT.SetBatch()
SetAtlasStyle()
label = "Internal"

doHIrejection = args.doHIrejection
isTrackCleaning = args.trackCleaning
tag = args.tag
SR = args.SR
dataSet = "mc16{}_trackCleaning_{}".format(tag, SR) if isTrackCleaning else "mc16{}_{}".format(tag, SR)


plotType = "mass"
if (doHIrejection):
    directory = "pdfs/" + plotType + "/" + dataSet + "_HIrejection"#"_newSample"
else:
    directory = "pdfs/" + plotType + "/" + dataSet #+ "_newSample"
if (not os.path.isdir(directory)):
    os.makedirs(directory)
if (not os.path.isdir("rootfiles")):
    os.makedirs("rootfiles")
    
inputFile = r.TFile("../outputFiles/mergedVerticesTreeMC_{}.root".format(dataSet), "READ")
tree = inputFile.Get("trees_SRDV_")

if (doHIrejection):
    outputFile = r.TFile("rootfiles/{}_{}.root".format(plotType, dataSet+"_HIrejection"), "RECREATE")
else:
    outputFile = r.TFile("rootfiles/{}_{}.root".format(plotType, dataSet), "RECREATE")

colors = [r.kGreen, r.kRed, r.kBlue, r.kOrange, r.kMagenta, r.kCyan, r.kViolet]

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

def determineTypeBin(dvType):
    dvTypeBin = ""
    if dvType == 1:
        dvTypeBin = "type1"
    if dvType == 2:
        dvTypeBin = "type2"
    if dvType == 3:
        dvTypeBin = "type3"
    if dvType == 4:
        dvTypeBin = "type4"
    if dvType == 5:
        dvTypeBin = "type5"
    if dvType == 6:
        dvTypeBin = "type6"
    if dvType == 7:
        dvTypeBin = "type7"
    return dvTypeBin

def getDVTypeLabel(dvTypeBin):
    dvTypeLabel = ""
    if dvTypeBin == "type1":
        dvTypeLabel = "G4 DV"
    if dvTypeBin == "type2":
        dvTypeLabel = "G4 + PU DV"
    if dvTypeBin == "type3":
        dvTypeLabel = "G4 + Gen DV"
    if dvTypeBin == "type4":
        dvTypeLabel = "PU DV"
    if dvTypeBin == "type5":
        dvTypeLabel = "PU + Gen DV"
    if dvTypeBin == "type6":
        dvTypeLabel = "Gen DV"
    if dvTypeBin == "type7":
        dvTypeLabel = "Combination DV"
    return dvTypeLabel

dvTypeList = ["type1", "type2", "type3", "type4", "type5", "type6", "type7"]
# Define histograms
massDict = {}
massDict_1parent = {}
massDict_multiParent = {}
massDict_multiParent_hasUnrelatedTracks = {}
massDict_multiParent_noUnrelatedTracks = {}
massDict_MVcand = {}
massDict_MVcand_noDVsel = {}
massDict_MVcand_noDVsel_type = {}
rxyDict_MVcand = {}
rxyDict_MVcand_noDVsel = {}
rxyDict_MVcand_type = {}
rxyDict_MVcand_noDVsel_type = {}
for ntrk in ntrkList:
    massDict[ntrk] = {}
    massDict_1parent[ntrk] = {}
    massDict_multiParent[ntrk] = {}
    massDict_multiParent_hasUnrelatedTracks[ntrk] = {}
    massDict_multiParent_noUnrelatedTracks[ntrk] = {}
    massDict_MVcand[ntrk] = r.TH1D("mass_MVcand_{}".format(ntrk), ";m_{MV} [GeV]", 100, 0., 100.)
    massDict_MVcand_noDVsel[ntrk] = r.TH1D("mass_MVcand_noDVsel_{}".format(ntrk), ";m_{MV} [GeV]", 100, 0., 100.)
    massDict_MVcand_noDVsel_type[ntrk] = {}
    rxyDict_MVcand[ntrk] = r.TH1D("rxy_MVcand_"+ntrk, ";r_{xy} [mm]", 500, 0., 500.)
    rxyDict_MVcand_noDVsel[ntrk] = r.TH1D("rxy_MVcand_noDVsel_"+ntrk, ";r_{xy} [mm]", 500, 0., 500.)
    rxyDict_MVcand_type[ntrk] = {}
    rxyDict_MVcand_noDVsel_type[ntrk] = {}
    for dvType in dvTypeList:
        massDict[ntrk][dvType] = r.TH1D("mass_{}_{}".format(ntrk, dvType), ";m_{MV} [GeV]", 100, 0., 100.)
        massDict_1parent[ntrk][dvType] = r.TH1D("mass_1parent_{}_{}".format(ntrk, dvType), ";m_{MV} [GeV]", 100, 0., 100.)
        massDict_multiParent[ntrk][dvType] = r.TH1D("mass_multiParent_{}_{}".format(ntrk, dvType), ";m_{MV} [GeV]", 100, 0., 100.)
        massDict_multiParent_hasUnrelatedTracks[ntrk][dvType] = r.TH1D("mass_multiParent_hasUnrelatedTracks_{}_{}".format(ntrk, dvType), ";m_{MV} [GeV]", 100, 0., 100.)
        massDict_multiParent_noUnrelatedTracks[ntrk][dvType] = r.TH1D("mass_multiParent_noUnrelatedTracks_{}_{}".format(ntrk, dvType), ";m_{MV} [GeV]", 100, 0., 100.)
        massDict_MVcand_noDVsel_type[ntrk][dvType] = r.TH1D("mass_MVcand_noDVsel_type_{}_{}".format(ntrk, dvType), ";m_{MV} [GeV]", 100, 0., 100.)
        rxyDict_MVcand_type[ntrk][dvType] = r.TH1D("rxy_MVcand_{}_{}".format(ntrk, dvType), ";r_{xy} [mm]", 500, 0., 500.)
        rxyDict_MVcand_noDVsel_type[ntrk][dvType] = r.TH1D("rxy_MVcand_noDVsel_{}_{}".format(ntrk, dvType), ";r_{xy} [mm]", 500, 0., 500.)

dvCounter = 0
#sumWeight = inputFile.Get("sumOfWeights").GetBinContent(1)
#sumWeight = inputFile.Get("nEvt").GetBinContent(1)
sumWeight = 1
for dv in tree:
    dvCounter += 1
    if (dvCounter % 10000 == 0):
        print("Processed {} DVs".format(dvCounter))
    dvPassFiducial = dv.dv_PassFiducialCut
    dvPassDist     = dv.dv_PassDistCut
    dvPassChi2     = dv.dv_PassChi2Cut
    dvIsInMaterial = dv.dv_isInMaterial

    dvType = dv.dv_type
    dvNtrk = dv.dv_ntrk
    dvMass = dv.dv_mass
    dv_rxy = dv.dv_rxy
    nParents = dv.nParents
    hasUnrelatedTracks = dv.hasUnrelatedTracks
    maxInterTruthParticleDist = dv.dv_maxInterTruthParticleDist
    hasHIParents = dv.hasHIParents

    if dvNtrk < 2:
        continue
    ntrkBin = determineNtrkBin(dvNtrk)
    dvTypeBin = determineTypeBin(dvType)

    if (nParents > 1 and not hasUnrelatedTracks and maxInterTruthParticleDist > 0.15 and not dvType == 1):
        if (doHIrejection):
            if (hasHIParents):
                continue
            massDict_MVcand_noDVsel[ntrkBin].Fill(dvMass)
            massDict_MVcand_noDVsel_type[ntrkBin][dvTypeBin].Fill(dvMass)
            rxyDict_MVcand_noDVsel[ntrkBin].Fill(dv_rxy)
            rxyDict_MVcand_noDVsel_type[ntrkBin][dvTypeBin].Fill(dv_rxy)
        else:
            massDict_MVcand_noDVsel[ntrkBin].Fill(dvMass)
            massDict_MVcand_noDVsel_type[ntrkBin][dvTypeBin].Fill(dvMass)
            rxyDict_MVcand_noDVsel[ntrkBin].Fill(dv_rxy)
            rxyDict_MVcand_noDVsel_type[ntrkBin][dvTypeBin].Fill(dv_rxy)

    #if not(dvPassFiducial and dvPassDist and dvPassChi2 and not dvIsInMaterial):
    #continue
    if (not dvPassFiducial):
        continue
    if (not dvPassDist):
        continue
    if (not dvPassChi2):
        continue
    if (dvIsInMaterial):
        continue
    
    massDict[ntrkBin][dvTypeBin].Fill(dvMass)

    if (nParents == 1):
        massDict_1parent[ntrkBin][dvTypeBin].Fill(dvMass)
    else:
        massDict_multiParent[ntrkBin][dvTypeBin].Fill(dvMass)
        if (hasUnrelatedTracks):
            massDict_multiParent_hasUnrelatedTracks[ntrkBin][dvTypeBin].Fill(dvMass)
        else:
            if (maxInterTruthParticleDist > 0.15 and not dvType == 1):
                if (doHIrejection):
                    if (hasHIParents):
                        continue
                    massDict_multiParent_noUnrelatedTracks[ntrkBin][dvTypeBin].Fill(dvMass)
                    massDict_MVcand[ntrkBin].Fill(dvMass)
                    rxyDict_MVcand[ntrkBin].Fill(dv_rxy)
                    rxyDict_MVcand_type[ntrkBin][dvTypeBin].Fill(dv_rxy)
                else:
                    massDict_multiParent_noUnrelatedTracks[ntrkBin][dvTypeBin].Fill(dvMass)
                    massDict_MVcand[ntrkBin].Fill(dvMass)
                    rxyDict_MVcand[ntrkBin].Fill(dv_rxy)
                    rxyDict_MVcand_type[ntrkBin][dvTypeBin].Fill(dv_rxy)
    

c1 = r.TCanvas("c1", "c1", 800, 700)
c1.cd()

leg = r.TLegend(0.65, 0.65, 0.80, 0.90)
leg.SetFillStyle(0)
leg.SetBorderSize(0)
leg.SetLineStyle(0)
leg.SetTextSize(0.035)
leg.SetTextFont(42)

for dvTypeBin in dvTypeList:
    massHists = massDict["Ntrk2"][dvTypeBin]
    dvTypeLabel = getDVTypeLabel(dvTypeBin)
    leg.AddEntry(massHists, dvTypeLabel, "l")

sampleLabel = r.TLatex()
sampleLabel.SetNDC()
sampleLabel.SetTextFont(42)
sampleLabel.SetTextAlign(13)
sampleLabel.SetTextSize(0.03)

dataLabel = dataSet + ", di-jet"

c1.SetLogy(1)
for ntrkBin in ntrkList:
    counter = 0
    maximum = 0
    for dvTypeBin in dvTypeList:
        massHists = massDict[ntrkBin][dvTypeBin]
        tmpMax = massHists.GetMaximum()
        if (tmpMax > maximum):
            maximum = tmpMax
        massDict[ntrkBin]["type1"].SetMaximum(maximum * 1.1)
        if (ntrkBin == "Ntrk2"):
            if (dvTypeBin == "type1"):
                counter = 0
                massHists.SetLineColor(colors[counter])
                massHists.Draw("histo")
            else:
                massHists.SetLineColor(colors[counter])
                massHists.Draw("histo same")
            counter += 1
        if (ntrkBin == "Ntrk3"):
            if (dvTypeBin == "type1"):
                counter = 0
                massHists.SetLineColor(colors[counter])
                massHists.Draw("histo")
            else:
                massHists.SetLineColor(colors[counter])
                massHists.Draw("histo same")
            counter += 1
        if (ntrkBin == "Ntrk4"):
            if (dvTypeBin == "type1"):
                counter = 0
                massHists.SetLineColor(colors[counter])
                massHists.Draw("histo")
            else:
                massHists.SetLineColor(colors[counter])
                massHists.Draw("histo same")
            counter += 1
        if (ntrkBin == "Ntrk5"):
            if (dvTypeBin == "type1"):
                counter = 0
                massHists.SetLineColor(colors[counter])
                massHists.Draw("histo")
            else:
                massHists.SetLineColor(colors[counter])
                massHists.Draw("histo same")
            counter += 1
        if (ntrkBin == "Ntrk6"):
            if (dvTypeBin == "type1"):
                counter = 0
                massHists.SetLineColor(colors[counter])
                massHists.Draw("histo")
            else:
                massHists.SetLineColor(colors[counter])
                massHists.Draw("histo same")
            counter += 1
        if (ntrkBin == "Ntrk>6"):
            if (dvTypeBin == "type1"):
                counter = 0
                massHists.SetLineColor(colors[counter])
                massHists.Draw("histo")
            else:
                massHists.SetLineColor(colors[counter])
                massHists.Draw("histo same")
            counter += 1
    leg.Draw()
    sampleLabel.DrawLatex(0.65, 0.60, dataLabel)
    sampleLabel.DrawLatex(0.65, 0.55, "Event and DV preselection")
    sampleLabel.DrawLatex(0.65, 0.50, getNtrkLabel(ntrkBin))
    ATLASLabel(0.20, 0.955, label)

    c1.Print("{}/{}.pdf".format(directory, "mass_{}".format(ntrkBin)))


for ntrkBin in ntrkList:
    counter = 0
    maximum = 0
    for dvTypeBin in dvTypeList:
        massHists_1parent = massDict_1parent[ntrkBin][dvTypeBin]
        tmpMax = massHists_1parent.GetMaximum()
        if (tmpMax > maximum):
            maximum = tmpMax
        massDict_1parent[ntrkBin]["type1"].SetMaximum(maximum * 1.1)
        if (ntrkBin == "Ntrk2"):
            if (dvTypeBin == "type1"):
                counter = 0
                massHists_1parent.SetLineColor(colors[counter])
                massHists_1parent.Draw("histo")
            else:
                massHists_1parent.SetLineColor(colors[counter])
                massHists_1parent.Draw("histo same")
            counter += 1
        if (ntrkBin == "Ntrk3"):
            if (dvTypeBin == "type1"):
                counter = 0
                massHists_1parent.SetLineColor(colors[counter])
                massHists_1parent.Draw("histo")
            else:
                massHists_1parent.SetLineColor(colors[counter])
                massHists_1parent.Draw("histo same")
            counter += 1
        if (ntrkBin == "Ntrk4"):
            if (dvTypeBin == "type1"):
                counter = 0
                massHists_1parent.SetLineColor(colors[counter])
                massHists_1parent.Draw("histo")
            else:
                massHists_1parent.SetLineColor(colors[counter])
                massHists_1parent.Draw("histo same")
            counter += 1
        if (ntrkBin == "Ntrk5"):
            if (dvTypeBin == "type1"):
                counter = 0
                massHists_1parent.SetLineColor(colors[counter])
                massHists_1parent.Draw("histo")
            else:
                massHists_1parent.SetLineColor(colors[counter])
                massHists_1parent.Draw("histo same")
            counter += 1
        if (ntrkBin == "Ntrk6"):
            if (dvTypeBin == "type1"):
                counter = 0
                massHists_1parent.SetLineColor(colors[counter])
                massHists_1parent.Draw("histo")
            else:
                massHists_1parent.SetLineColor(colors[counter])
                massHists_1parent.Draw("histo same")
            counter += 1
        if (ntrkBin == "Ntrk>6"):
            if (dvTypeBin == "type1"):
                counter = 0
                massHists_1parent.SetLineColor(colors[counter])
                massHists_1parent.Draw("histo")
            else:
                massHists_1parent.SetLineColor(colors[counter])
                massHists_1parent.Draw("histo same")
            counter += 1
    leg.Draw()
    sampleLabel.DrawLatex(0.65, 0.60, dataLabel)
    sampleLabel.DrawLatex(0.65, 0.55, "Event and DV preselection")
    sampleLabel.DrawLatex(0.65, 0.50, "DV has 1 parent")
    sampleLabel.DrawLatex(0.65, 0.45, getNtrkLabel(ntrkBin))
    ATLASLabel(0.20, 0.955, label)

    c1.Print("{}/{}.pdf".format(directory, "mass_1parent_{}".format(ntrkBin)))

for ntrkBin in ntrkList:
    counter = 0
    maximum = 0
    for dvTypeBin in dvTypeList:
        massHists_multiParent = massDict_multiParent[ntrkBin][dvTypeBin]
        tmpMax = massHists_multiParent.GetMaximum()
        if (tmpMax > maximum):
            maximum = tmpMax
        massDict_multiParent[ntrkBin]["type1"].SetMaximum(maximum * 1.1)
        if (ntrkBin == "Ntrk2"):
            if (dvTypeBin == "type1"):
                counter = 0
                massHists_multiParent.SetLineColor(colors[counter])
                massHists_multiParent.Draw("histo")
            else:
                massHists_multiParent.SetLineColor(colors[counter])
                massHists_multiParent.Draw("histo same")
            counter += 1
        if (ntrkBin == "Ntrk3"):
            if (dvTypeBin == "type1"):
                counter = 0
                massHists_multiParent.SetLineColor(colors[counter])
                massHists_multiParent.Draw("histo")
            else:
                massHists_multiParent.SetLineColor(colors[counter])
                massHists_multiParent.Draw("histo same")
            counter += 1
        if (ntrkBin == "Ntrk4"):
            if (dvTypeBin == "type1"):
                counter = 0
                massHists_multiParent.SetLineColor(colors[counter])
                massHists_multiParent.Draw("histo")
            else:
                massHists_multiParent.SetLineColor(colors[counter])
                massHists_multiParent.Draw("histo same")
            counter += 1
        if (ntrkBin == "Ntrk5"):
            if (dvTypeBin == "type1"):
                counter = 0
                massHists_multiParent.SetLineColor(colors[counter])
                massHists_multiParent.Draw("histo")
            else:
                massHists_multiParent.SetLineColor(colors[counter])
                massHists_multiParent.Draw("histo same")
            counter += 1
        if (ntrkBin == "Ntrk6"):
            if (dvTypeBin == "type1"):
                counter = 0
                massHists_multiParent.SetLineColor(colors[counter])
                massHists_multiParent.Draw("histo")
            else:
                massHists_multiParent.SetLineColor(colors[counter])
                massHists_multiParent.Draw("histo same")
            counter += 1
        if (ntrkBin == "Ntrk>6"):
            if (dvTypeBin == "type1"):
                counter = 0
                massHists_multiParent.SetLineColor(colors[counter])
                massHists_multiParent.Draw("histo")
            else:
                massHists_multiParent.SetLineColor(colors[counter])
                massHists_multiParent.Draw("histo same")
            counter += 1
    leg.Draw()
    sampleLabel.DrawLatex(0.65, 0.60, dataLabel)
    sampleLabel.DrawLatex(0.65, 0.55, "Event and DV preselection")
    sampleLabel.DrawLatex(0.65, 0.50, "DV has multiple parent")
    sampleLabel.DrawLatex(0.65, 0.45, getNtrkLabel(ntrkBin))
    ATLASLabel(0.20, 0.955, label)

    c1.Print("{}/{}.pdf".format(directory, "mass_multiParent_{}".format(ntrkBin)))

for ntrkBin in ntrkList:
    counter = 0
    maximum = 0
    for dvTypeBin in dvTypeList:
        massHists_multiParent_hasUnrelatedTracks = massDict_multiParent_hasUnrelatedTracks[ntrkBin][dvTypeBin]
        tmpMax = massHists_multiParent_hasUnrelatedTracks.GetMaximum()
        if (tmpMax > maximum):
            maximum = tmpMax
        massDict_multiParent_hasUnrelatedTracks[ntrkBin]["type1"].SetMaximum(maximum * 1.1)
        if (ntrkBin == "Ntrk2"):
            if (dvTypeBin == "type1"):
                counter = 0
                massHists_multiParent_hasUnrelatedTracks.SetLineColor(colors[counter])
                massHists_multiParent_hasUnrelatedTracks.Draw("histo")
            else:
                massHists_multiParent_hasUnrelatedTracks.SetLineColor(colors[counter])
                massHists_multiParent_hasUnrelatedTracks.Draw("histo same")
            counter += 1
        if (ntrkBin == "Ntrk3"):
            if (dvTypeBin == "type1"):
                counter = 0
                massHists_multiParent_hasUnrelatedTracks.SetLineColor(colors[counter])
                massHists_multiParent_hasUnrelatedTracks.Draw("histo")
            else:
                massHists_multiParent_hasUnrelatedTracks.SetLineColor(colors[counter])
                massHists_multiParent_hasUnrelatedTracks.Draw("histo same")
            counter += 1
        if (ntrkBin == "Ntrk4"):
            if (dvTypeBin == "type1"):
                counter = 0
                massHists_multiParent_hasUnrelatedTracks.SetLineColor(colors[counter])
                massHists_multiParent_hasUnrelatedTracks.Draw("histo")
            else:
                massHists_multiParent_hasUnrelatedTracks.SetLineColor(colors[counter])
                massHists_multiParent_hasUnrelatedTracks.Draw("histo same")
            counter += 1
        if (ntrkBin == "Ntrk5"):
            if (dvTypeBin == "type1"):
                counter = 0
                massHists_multiParent_hasUnrelatedTracks.SetLineColor(colors[counter])
                massHists_multiParent_hasUnrelatedTracks.Draw("histo")
            else:
                massHists_multiParent_hasUnrelatedTracks.SetLineColor(colors[counter])
                massHists_multiParent_hasUnrelatedTracks.Draw("histo same")
            counter += 1
        if (ntrkBin == "Ntrk6"):
            if (dvTypeBin == "type1"):
                counter = 0
                massHists_multiParent_hasUnrelatedTracks.SetLineColor(colors[counter])
                massHists_multiParent_hasUnrelatedTracks.Draw("histo")
            else:
                massHists_multiParent_hasUnrelatedTracks.SetLineColor(colors[counter])
                massHists_multiParent_hasUnrelatedTracks.Draw("histo same")
            counter += 1
        if (ntrkBin == "Ntrk>6"):
            if (dvTypeBin == "type1"):
                counter = 0
                massHists_multiParent_hasUnrelatedTracks.SetLineColor(colors[counter])
                massHists_multiParent_hasUnrelatedTracks.Draw("histo")
            else:
                massHists_multiParent_hasUnrelatedTracks.SetLineColor(colors[counter])
                massHists_multiParent_hasUnrelatedTracks.Draw("histo same")
            counter += 1
    leg.Draw()
    sampleLabel.DrawLatex(0.65, 0.60, dataLabel)
    sampleLabel.DrawLatex(0.65, 0.55, "Event and DV preselection")
    sampleLabel.DrawLatex(0.65, 0.50, "DV has multiple parents with AX")
    sampleLabel.DrawLatex(0.65, 0.45, getNtrkLabel(ntrkBin))
    ATLASLabel(0.20, 0.955, label)

    c1.Print("{}/{}.pdf".format(directory, "mass_multiParent_hasUnrelatedTracks_{}".format(ntrkBin)))

c1.SetLogy(0)
for ntrkBin in ntrkList:
    counter = 0
    maximum = -1e10
    for dvTypeBin in dvTypeList:
        massHists_multiParent_noUnrelatedTracks = massDict_multiParent_noUnrelatedTracks[ntrkBin][dvTypeBin]
        tmpMax = massHists_multiParent_noUnrelatedTracks.GetMaximum()
        if (tmpMax > maximum):
            maximum = tmpMax
        massDict_multiParent_noUnrelatedTracks[ntrkBin]["type1"].SetMaximum(maximum * 1.1)
        
        if (ntrkBin == "Ntrk2"):
            if (dvTypeBin == "type1"):
                counter = 0
                massHists_multiParent_noUnrelatedTracks.SetLineColor(colors[counter])
                massHists_multiParent_noUnrelatedTracks.Draw("histo")
            else:
                massHists_multiParent_noUnrelatedTracks.SetLineColor(colors[counter])
                massHists_multiParent_noUnrelatedTracks.Draw("histo same")
            counter += 1
        if (ntrkBin == "Ntrk3"):
            if (dvTypeBin == "type1"):
                counter = 0
                massHists_multiParent_noUnrelatedTracks.SetLineColor(colors[counter])
                massHists_multiParent_noUnrelatedTracks.Draw("histo")
            else:
                massHists_multiParent_noUnrelatedTracks.SetLineColor(colors[counter])
                massHists_multiParent_noUnrelatedTracks.Draw("histo same")
            counter += 1
        if (ntrkBin == "Ntrk4"):
            if (dvTypeBin == "type1"):
                counter = 0
                massHists_multiParent_noUnrelatedTracks.SetLineColor(colors[counter])
                massHists_multiParent_noUnrelatedTracks.Draw("histo")
            else:
                massHists_multiParent_noUnrelatedTracks.SetLineColor(colors[counter])
                massHists_multiParent_noUnrelatedTracks.Draw("histo same")
            counter += 1
        if (ntrkBin == "Ntrk5"):
            if (dvTypeBin == "type1"):
                counter = 0
                massHists_multiParent_noUnrelatedTracks.SetLineColor(colors[counter])
                massHists_multiParent_noUnrelatedTracks.Draw("histo")
            else:
                massHists_multiParent_noUnrelatedTracks.SetLineColor(colors[counter])
                massHists_multiParent_noUnrelatedTracks.Draw("histo same")
            counter += 1
        if (ntrkBin == "Ntrk6"):
            if (dvTypeBin == "type1"):
                counter = 0
                massHists_multiParent_noUnrelatedTracks.SetLineColor(colors[counter])
                massHists_multiParent_noUnrelatedTracks.Draw("histo")
            else:
                massHists_multiParent_noUnrelatedTracks.SetLineColor(colors[counter])
                massHists_multiParent_noUnrelatedTracks.Draw("histo same")
            counter += 1
        if (ntrkBin == "Ntrk>6"):
            if (dvTypeBin == "type1"):
                counter = 0
                massHists_multiParent_noUnrelatedTracks.SetLineColor(colors[counter])
                massHists_multiParent_noUnrelatedTracks.Draw("histo")
            else:
                massHists_multiParent_noUnrelatedTracks.SetLineColor(colors[counter])
                massHists_multiParent_noUnrelatedTracks.Draw("histo same")
            counter += 1
    leg.Draw()
    sampleLabel.DrawLatex(0.65, 0.60, dataLabel)
    sampleLabel.DrawLatex(0.65, 0.55, "Event and DV preselection")
    sampleLabel.DrawLatex(0.65, 0.50, "DV has multiple parent, without AX")
    sampleLabel.DrawLatex(0.65, 0.45, getNtrkLabel(ntrkBin))
    ATLASLabel(0.20, 0.955, label)

    c1.Print("{}/{}.pdf".format(directory, "mass_multiParent_noUnrelatedTracks_{}".format(ntrkBin)))
    
c1.SetLogy(1)
for ntrkBin in ntrkList:
    counter = 0
    maximum = -1e10
    for dvTypeBin in dvTypeList:
        massHists_multiParent_noUnrelatedTracks = massDict_multiParent_noUnrelatedTracks[ntrkBin][dvTypeBin]
        tmpMax = massHists_multiParent_noUnrelatedTracks.GetMaximum()
        if (tmpMax > maximum):
            maximum = tmpMax
        massDict_multiParent_noUnrelatedTracks[ntrkBin]["type1"].SetMaximum(maximum * 1.1)
        if (ntrkBin == "Ntrk2"):
            if (dvTypeBin == "type1"):
                counter = 0
                massHists_multiParent_noUnrelatedTracks.SetLineColor(colors[counter])
                massHists_multiParent_noUnrelatedTracks.Draw("histo")
            else:
                massHists_multiParent_noUnrelatedTracks.SetLineColor(colors[counter])
                massHists_multiParent_noUnrelatedTracks.Draw("histo same")
            counter += 1
        if (ntrkBin == "Ntrk3"):
            if (dvTypeBin == "type1"):
                counter = 0
                massHists_multiParent_noUnrelatedTracks.SetLineColor(colors[counter])
                massHists_multiParent_noUnrelatedTracks.Draw("histo")
            else:
                massHists_multiParent_noUnrelatedTracks.SetLineColor(colors[counter])
                massHists_multiParent_noUnrelatedTracks.Draw("histo same")
            counter += 1
        if (ntrkBin == "Ntrk4"):
            if (dvTypeBin == "type1"):
                counter = 0
                massHists_multiParent_noUnrelatedTracks.SetLineColor(colors[counter])
                massHists_multiParent_noUnrelatedTracks.Draw("histo")
            else:
                massHists_multiParent_noUnrelatedTracks.SetLineColor(colors[counter])
                massHists_multiParent_noUnrelatedTracks.Draw("histo same")
            counter += 1
        if (ntrkBin == "Ntrk5"):
            if (dvTypeBin == "type1"):
                counter = 0
                massHists_multiParent_noUnrelatedTracks.SetLineColor(colors[counter])
                massHists_multiParent_noUnrelatedTracks.Draw("histo")
            else:
                massHists_multiParent_noUnrelatedTracks.SetLineColor(colors[counter])
                massHists_multiParent_noUnrelatedTracks.Draw("histo same")
            counter += 1
        if (ntrkBin == "Ntrk6"):
            if (dvTypeBin == "type1"):
                counter = 0
                massHists_multiParent_noUnrelatedTracks.SetLineColor(colors[counter])
                massHists_multiParent_noUnrelatedTracks.Draw("histo")
            else:
                massHists_multiParent_noUnrelatedTracks.SetLineColor(colors[counter])
                massHists_multiParent_noUnrelatedTracks.Draw("histo same")
            counter += 1
        if (ntrkBin == "Ntrk>6"):
            if (dvTypeBin == "type1"):
                counter = 0
                massHists_multiParent_noUnrelatedTracks.SetLineColor(colors[counter])
                massHists_multiParent_noUnrelatedTracks.Draw("histo")
            else:
                massHists_multiParent_noUnrelatedTracks.SetLineColor(colors[counter])
                massHists_multiParent_noUnrelatedTracks.Draw("histo same")
            counter += 1
    leg.Draw()
    sampleLabel.DrawLatex(0.65, 0.60, dataLabel)
    sampleLabel.DrawLatex(0.65, 0.55, "Event and DV preselection")
    sampleLabel.DrawLatex(0.65, 0.50, "DV has multiple parent, without AX")
    sampleLabel.DrawLatex(0.65, 0.45, getNtrkLabel(ntrkBin))
    ATLASLabel(0.20, 0.955, label)

    c1.Print("{}/{}.pdf".format(directory, "mass_multiParent_noUnrelatedTracks_{}_logy".format(ntrkBin)))

c1.SetLogy(0)
for ntrkBin in ntrkList:
    counter = 0        
    massHists_MVcand = massDict_MVcand[ntrkBin]
    
    massHists_MVcand.Draw("histo")
    sampleLabel.DrawLatex(0.55, 0.60, dataLabel)
    sampleLabel.DrawLatex(0.55, 0.55, "Event and DV preselection")
    sampleLabel.DrawLatex(0.55, 0.50, "DV has multiple parent, without AX")
    sampleLabel.DrawLatex(0.55, 0.45, getNtrkLabel(ntrkBin))
    ATLASLabel(0.20, 0.955, label)

    c1.Print("{}/{}.pdf".format(directory, "mass_MVcand_{}".format(ntrkBin)))

c1.SetLogy(1)
for ntrkBin in ntrkList:
    counter = 0        
    massHists_MVcand = massDict_MVcand[ntrkBin]
    
    massHists_MVcand.Draw("histo")
    sampleLabel.DrawLatex(0.55, 0.60, dataLabel)
    sampleLabel.DrawLatex(0.55, 0.55, "Event and DV preselection")
    sampleLabel.DrawLatex(0.55, 0.50, "DV has multiple parent, without AX")
    sampleLabel.DrawLatex(0.55, 0.45, getNtrkLabel(ntrkBin))
    ATLASLabel(0.20, 0.955, label)

    c1.Print("{}/{}.pdf".format(directory, "mass_MVcand_{}_logy".format(ntrkBin)))

c1.SetLogy(1)
for ntrkBin in ntrkList:
    counter = 0        
    massHists_MVcand_noDVsel = massDict_MVcand_noDVsel[ntrkBin]
    
    massHists_MVcand_noDVsel.Draw("histo")
    sampleLabel.DrawLatex(0.55, 0.60, dataLabel)
    sampleLabel.DrawLatex(0.55, 0.55, "Event preselection")
    sampleLabel.DrawLatex(0.55, 0.50, "DV has multiple parent, without AX")
    sampleLabel.DrawLatex(0.55, 0.45, getNtrkLabel(ntrkBin))
    ATLASLabel(0.20, 0.955, label)

    c1.Print("{}/{}.pdf".format(directory, "mass_MVcand_noDVsel_{}_logy".format(ntrkBin)))

c1.SetLogy(0)
for ntrkBin in ntrkList:
    counter = 0        
    massHists_MVcand_noDVsel = massDict_MVcand_noDVsel[ntrkBin]
    
    massHists_MVcand_noDVsel.Draw("histo")
    sampleLabel.DrawLatex(0.55, 0.60, dataLabel)
    sampleLabel.DrawLatex(0.55, 0.55, "Event preselection")
    sampleLabel.DrawLatex(0.55, 0.50, "DV has multiple parent, without AX")
    sampleLabel.DrawLatex(0.55, 0.45, getNtrkLabel(ntrkBin))
    ATLASLabel(0.20, 0.955, label)

    c1.Print("{}/{}.pdf".format(directory, "mass_MVcand_noDVsel_{}".format(ntrkBin)))

c1.SetLogy(1)
for ntrkBin in ntrkList:
    counter = 0        
    massHists_MVcand_noDVsel = massDict_MVcand_noDVsel[ntrkBin]
    
    massHists_MVcand_noDVsel.Draw("histo")
    sampleLabel.DrawLatex(0.55, 0.60, dataLabel)
    sampleLabel.DrawLatex(0.55, 0.55, "Event preselection")
    sampleLabel.DrawLatex(0.55, 0.50, "DV has multiple parent, without AX")
    sampleLabel.DrawLatex(0.55, 0.45, getNtrkLabel(ntrkBin))
    ATLASLabel(0.20, 0.955, label)

    c1.Print("{}/{}.pdf".format(directory, "mass_MVcand_noDVsel_{}_logy".format(ntrkBin)))

c1.SetLogy(1)
leg_type = r.TLegend(0.65, 0.53, 0.80, 0.73)
decorateLeg(leg_type)
leg_type.AddEntry(massDict_MVcand_noDVsel_type["Ntrk4"]["type2"], "G4+PU DV", "l")
leg_type.AddEntry(massDict_MVcand_noDVsel_type["Ntrk4"]["type3"], "G4+Gen DV", "l")
leg_type.AddEntry(massDict_MVcand_noDVsel_type["Ntrk4"]["type4"], "PU DV", "l")
leg_type.AddEntry(massDict_MVcand_noDVsel_type["Ntrk4"]["type5"], "PU+Gen DV", "l")
leg_type.AddEntry(massDict_MVcand_noDVsel_type["Ntrk4"]["type6"], "Gen DV", "l")
leg_type.AddEntry(massDict_MVcand_noDVsel_type["Ntrk4"]["type7"], "Combination DV", "l")
for ntrkBin in ntrkList:
    counter = 0
    maximum = -1e10
    for dvTypeBin in dvTypeList:
        massHists_MVcand_noDVsel_type = massDict_MVcand_noDVsel_type[ntrkBin][dvTypeBin]
        tmpMax = massHists_MVcand_noDVsel_type.GetMaximum()
        if (tmpMax > maximum):
            maximum = tmpMax
        massDict_MVcand_noDVsel_type[ntrkBin]["type1"].SetMaximum(maximum*2.0)
        if (ntrkBin == "Ntrk2"):
            if (dvTypeBin == "type1"):
                counter = 0
                massHists_MVcand_noDVsel_type.SetLineColor(colors[counter])
                massHists_MVcand_noDVsel_type.Draw("histo")
            else:
                massHists_MVcand_noDVsel_type.SetLineColor(colors[counter])
                massHists_MVcand_noDVsel_type.Draw("histo same")
            counter += 1
        if (ntrkBin == "Ntrk3"):
            if (dvTypeBin == "type1"):
                counter = 0
                massHists_MVcand_noDVsel_type.SetLineColor(colors[counter])
                massHists_MVcand_noDVsel_type.Draw("histo")
            else:
                massHists_MVcand_noDVsel_type.SetLineColor(colors[counter])
                massHists_MVcand_noDVsel_type.Draw("histo same")
            counter += 1
        if (ntrkBin == "Ntrk4"):
            if (dvTypeBin == "type1"):
                counter = 0
                massHists_MVcand_noDVsel_type.SetLineColor(colors[counter])
                massHists_MVcand_noDVsel_type.Draw("histo")
            else:
                massHists_MVcand_noDVsel_type.SetLineColor(colors[counter])
                massHists_MVcand_noDVsel_type.Draw("histo same")
            counter += 1
        if (ntrkBin == "Ntrk5"):
            if (dvTypeBin == "type1"):
                counter = 0
                massHists_MVcand_noDVsel_type.SetLineColor(colors[counter])
                massHists_MVcand_noDVsel_type.Draw("histo")
            else:
                massHists_MVcand_noDVsel_type.SetLineColor(colors[counter])
                massHists_MVcand_noDVsel_type.Draw("histo same")
            counter += 1
        if (ntrkBin == "Ntrk6"):
            if (dvTypeBin == "type1"):
                counter = 0
                massHists_MVcand_noDVsel_type.SetLineColor(colors[counter])
                massHists_MVcand_noDVsel_type.Draw("histo")
            else:
                massHists_MVcand_noDVsel_type.SetLineColor(colors[counter])
                massHists_MVcand_noDVsel_type.Draw("histo same")
            counter += 1
        if (ntrkBin == "Ntrk>6"):
            if (dvTypeBin == "type1"):
                counter = 0
                massHists_MVcand_noDVsel_type.SetLineColor(colors[counter])
                massHists_MVcand_noDVsel_type.Draw("histo")
            else:
                massHists_MVcand_noDVsel_type.SetLineColor(colors[counter])
                massHists_MVcand_noDVsel_type.Draw("histo same")
            counter += 1
    leg_type.Draw()
    sampleLabel.DrawLatex(0.65, 0.93, dataLabel)
    sampleLabel.DrawLatex(0.65, 0.88, "Event preselection")
    sampleLabel.DrawLatex(0.65, 0.83, "Merged vertices candidate")
    sampleLabel.DrawLatex(0.65, 0.78, getNtrkLabel(ntrkBin))
    ATLASLabel(0.20, 0.955, label)

    c1.Print("{}/{}.pdf".format(directory, "mass_MVcand_noDVsel_type_{}_logy".format(ntrkBin)))

c1.SetLogy(0)
for ntrkBin in ntrkList:
    counter = 0
    maximum = -1e10
    for dvTypeBin in dvTypeList:
        massHists_MVcand_noDVsel_type = massDict_MVcand_noDVsel_type[ntrkBin][dvTypeBin]
        tmpMax = massHists_MVcand_noDVsel_type.GetMaximum()
        if (tmpMax > maximum and not dvTypeBin == "type1"):
            maximum = tmpMax
        print(dvTypeBin, maximum)
        massDict_MVcand_noDVsel_type[ntrkBin]["type1"].SetMaximum(maximum*1.1)
        if (ntrkBin == "Ntrk2"):
            if (dvTypeBin == "type1"):
                counter = 0
                massHists_MVcand_noDVsel_type.SetLineColor(colors[counter])
                massHists_MVcand_noDVsel_type.Draw("histo")
            else:
                massHists_MVcand_noDVsel_type.SetLineColor(colors[counter])
                massHists_MVcand_noDVsel_type.Draw("histo same")
            counter += 1
        if (ntrkBin == "Ntrk3"):
            if (dvTypeBin == "type1"):
                counter = 0
                massHists_MVcand_noDVsel_type.SetLineColor(colors[counter])
                massHists_MVcand_noDVsel_type.Draw("histo")
            else:
                massHists_MVcand_noDVsel_type.SetLineColor(colors[counter])
                massHists_MVcand_noDVsel_type.Draw("histo same")
            counter += 1
        if (ntrkBin == "Ntrk4"):
            if (dvTypeBin == "type1"):
                counter = 0
                massHists_MVcand_noDVsel_type.SetLineColor(colors[counter])
                massHists_MVcand_noDVsel_type.Draw("histo")
            else:
                massHists_MVcand_noDVsel_type.SetLineColor(colors[counter])
                massHists_MVcand_noDVsel_type.Draw("histo same")
            counter += 1
        if (ntrkBin == "Ntrk5"):
            if (dvTypeBin == "type1"):
                counter = 0
                massHists_MVcand_noDVsel_type.SetLineColor(colors[counter])
                massHists_MVcand_noDVsel_type.Draw("histo")
            else:
                massHists_MVcand_noDVsel_type.SetLineColor(colors[counter])
                massHists_MVcand_noDVsel_type.Draw("histo same")
            counter += 1
        if (ntrkBin == "Ntrk6"):
            if (dvTypeBin == "type1"):
                counter = 0
                massHists_MVcand_noDVsel_type.SetLineColor(colors[counter])
                massHists_MVcand_noDVsel_type.Draw("histo")
            else:
                massHists_MVcand_noDVsel_type.SetLineColor(colors[counter])
                massHists_MVcand_noDVsel_type.Draw("histo same")
            counter += 1
        if (ntrkBin == "Ntrk>6"):
            if (dvTypeBin == "type1"):
                counter = 0
                massHists_MVcand_noDVsel_type.SetLineColor(colors[counter])
                massHists_MVcand_noDVsel_type.Draw("histo")
            else:
                massHists_MVcand_noDVsel_type.SetLineColor(colors[counter])
                massHists_MVcand_noDVsel_type.Draw("histo same")
            counter += 1
    leg_type.Draw()
    sampleLabel.DrawLatex(0.65, 0.93, dataLabel)
    sampleLabel.DrawLatex(0.65, 0.88, "Event preselection")
    sampleLabel.DrawLatex(0.65, 0.83, "Merged vertices candidate")
    sampleLabel.DrawLatex(0.65, 0.78, getNtrkLabel(ntrkBin))
    ATLASLabel(0.20, 0.955, label)

    c1.Print("{}/{}.pdf".format(directory, "mass_MVcand_noDVsel_type_{}".format(ntrkBin)))

for ntrkBin in ntrkList:
    c1.SetLogy(0)
    rxyDict_MVcand[ntrkBin].Draw("hist")
    sampleLabel.DrawLatex(0.65, 0.75, dataLabel)
    sampleLabel.DrawLatex(0.65, 0.70, "Event and DV preselection")
    sampleLabel.DrawLatex(0.65, 0.65, "MV candidate")
    sampleLabel.DrawLatex(0.65, 0.60, getNtrkLabel(ntrkBin))
    ATLASLabel(0.20, 0.955, label)
    c1.Print("{}/{}.pdf".format(directory, "rxy_MVcand_"+ntrkBin))

    rxyDict_MVcand_noDVsel[ntrkBin].Draw("hist")
    sampleLabel.DrawLatex(0.65, 0.75, dataLabel)
    sampleLabel.DrawLatex(0.65, 0.70, "Event preselection")
    sampleLabel.DrawLatex(0.65, 0.65, "MV candidate")
    sampleLabel.DrawLatex(0.65, 0.60, getNtrkLabel(ntrkBin))
    ATLASLabel(0.20, 0.955, label)
    c1.Print("{}/{}.pdf".format(directory, "rxy_MVcand_noDVsel_"+ntrkBin))

for ntrkBin in ntrkList:
    counter = 0
    maximum = -1e10
    for dvTypeBin in dvTypeList:
        rxyHist_MVcand_noDVsel_type = rxyDict_MVcand_noDVsel_type[ntrkBin][dvTypeBin]
        tmpMax = rxyHist_MVcand_noDVsel_type.GetMaximum()
        if (tmpMax > maximum):
            maximum = tmpMax
        rxyDict_MVcand_noDVsel_type[ntrkBin]["type1"].SetMaximum(maximum*1.5)
        if (ntrkBin == "Ntrk2"):
            if (dvTypeBin == "type1"):
                counter = 0
                rxyHist_MVcand_noDVsel_type.SetLineColor(colors[counter])
                rxyHist_MVcand_noDVsel_type.Draw("hist")
            else:
                rxyHist_MVcand_noDVsel_type.SetLineColor(colors[counter])
                rxyHist_MVcand_noDVsel_type.Draw("hist same")
            counter += 1
        if (ntrkBin == "Ntrk3"):
            if (dvTypeBin == "type1"):
                counter = 0
                rxyHist_MVcand_noDVsel_type.SetLineColor(colors[counter])
                rxyHist_MVcand_noDVsel_type.Draw("hist")
            else:
                rxyHist_MVcand_noDVsel_type.SetLineColor(colors[counter])
                rxyHist_MVcand_noDVsel_type.Draw("hist same")
            counter += 1
        if (ntrkBin == "Ntrk4"):
            if (dvTypeBin == "type1"):
                counter = 0
                rxyHist_MVcand_noDVsel_type.SetLineColor(colors[counter])
                rxyHist_MVcand_noDVsel_type.Draw("hist")
            else:
                rxyHist_MVcand_noDVsel_type.SetLineColor(colors[counter])
                rxyHist_MVcand_noDVsel_type.Draw("hist same")
            counter += 1
        if (ntrkBin == "Ntrk5"):
            if (dvTypeBin == "type1"):
                counter = 0
                rxyHist_MVcand_noDVsel_type.SetLineColor(colors[counter])
                rxyHist_MVcand_noDVsel_type.Draw("hist")
            else:
                rxyHist_MVcand_noDVsel_type.SetLineColor(colors[counter])
                rxyHist_MVcand_noDVsel_type.Draw("hist same")
            counter += 1
        if (ntrkBin == "Ntrk6"):
            if (dvTypeBin == "type1"):
                counter = 0
                rxyHist_MVcand_noDVsel_type.SetLineColor(colors[counter])
                rxyHist_MVcand_noDVsel_type.Draw("hist")
            else:
                rxyHist_MVcand_noDVsel_type.SetLineColor(colors[counter])
                rxyHist_MVcand_noDVsel_type.Draw("hist same")
            counter += 1
        if (ntrkBin == "Ntrk>6"):
            if (dvTypeBin == "type1"):
                counter = 0
                rxyHist_MVcand_noDVsel_type.SetLineColor(colors[counter])
                rxyHist_MVcand_noDVsel_type.Draw("hist")
            else:
                rxyHist_MVcand_noDVsel_type.SetLineColor(colors[counter])
                rxyHist_MVcand_noDVsel_type.Draw("hist same")
            counter += 1
    sampleLabel.DrawLatex(0.65, 0.63, dataLabel)
    sampleLabel.DrawLatex(0.65, 0.58, "Event preselection")
    sampleLabel.DrawLatex(0.65, 0.53, "MV candidate")
    sampleLabel.DrawLatex(0.65, 0.48, getNtrkLabel(ntrkBin))
    leg.Draw()
    ATLASLabel(0.20, 0.955, label)
    c1.Print("{}/{}.pdf".format(directory, "type_rxy_MVcand_noDVsel_{}".format(ntrkBin)))

# DV sel
for ntrkBin in ntrkList:
    counter = 0
    maximum = -1e10
    for dvTypeBin in dvTypeList:
        rxyHist_MVcand_type = rxyDict_MVcand_type[ntrkBin][dvTypeBin]
        tmpMax = rxyHist_MVcand_type.GetMaximum()
        if (tmpMax > maximum):
            maximum = tmpMax
        rxyDict_MVcand_type[ntrkBin]["type1"].SetMaximum(maximum*1.5)
        if (ntrkBin == "Ntrk2"):
            if (dvTypeBin == "type1"):
                counter = 0
                rxyHist_MVcand_type.SetLineColor(colors[counter])
                rxyHist_MVcand_type.Draw("hist")
            else:
                rxyHist_MVcand_type.SetLineColor(colors[counter])
                rxyHist_MVcand_type.Draw("hist same")
            counter += 1
        if (ntrkBin == "Ntrk3"):
            if (dvTypeBin == "type1"):
                counter = 0
                rxyHist_MVcand_type.SetLineColor(colors[counter])
                rxyHist_MVcand_type.Draw("hist")
            else:
                rxyHist_MVcand_type.SetLineColor(colors[counter])
                rxyHist_MVcand_type.Draw("hist same")
            counter += 1
        if (ntrkBin == "Ntrk4"):
            if (dvTypeBin == "type1"):
                counter = 0
                rxyHist_MVcand_type.SetLineColor(colors[counter])
                rxyHist_MVcand_type.Draw("hist")
            else:
                rxyHist_MVcand_type.SetLineColor(colors[counter])
                rxyHist_MVcand_type.Draw("hist same")
            counter += 1
        if (ntrkBin == "Ntrk5"):
            if (dvTypeBin == "type1"):
                counter = 0
                rxyHist_MVcand_type.SetLineColor(colors[counter])
                rxyHist_MVcand_type.Draw("hist")
            else:
                rxyHist_MVcand_type.SetLineColor(colors[counter])
                rxyHist_MVcand_type.Draw("hist same")
            counter += 1
        if (ntrkBin == "Ntrk6"):
            if (dvTypeBin == "type1"):
                counter = 0
                rxyHist_MVcand_type.SetLineColor(colors[counter])
                rxyHist_MVcand_type.Draw("hist")
            else:
                rxyHist_MVcand_type.SetLineColor(colors[counter])
                rxyHist_MVcand_type.Draw("hist same")
            counter += 1
        if (ntrkBin == "Ntrk>6"):
            if (dvTypeBin == "type1"):
                counter = 0
                rxyHist_MVcand_type.SetLineColor(colors[counter])
                rxyHist_MVcand_type.Draw("hist")
            else:
                rxyHist_MVcand_type.SetLineColor(colors[counter])
                rxyHist_MVcand_type.Draw("hist same")
            counter += 1
    sampleLabel.DrawLatex(0.65, 0.63, dataLabel)
    sampleLabel.DrawLatex(0.65, 0.58, "Event preselection")
    sampleLabel.DrawLatex(0.65, 0.53, "MV candidate")
    sampleLabel.DrawLatex(0.65, 0.48, getNtrkLabel(ntrkBin))
    ATLASLabel(0.20, 0.955, label)
    leg.Draw()
    c1.Print("{}/{}.pdf".format(directory, "type_rxy_MVcand_{}".format(ntrkBin)))


outputFile.Write()
outputFile.Close()
