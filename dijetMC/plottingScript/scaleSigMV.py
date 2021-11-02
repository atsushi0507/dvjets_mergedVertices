import ROOT as r
from scipy.special import comb
from glob import glob
import sys, os
sys.path.append("/Users/amizukam/DVJets/atlasstyle")
from AtlasStyle import *
from AtlasLabel import *

r.gROOT.SetBatch()
SetAtlasStyle()
label = "Internal"

evtMax = -1
dataSet = "mc16e"

plotType = "sigScale"
directory = "pdfs/" + plotType + "/" + dataSet
if (not os.path.isdir(directory)):
    os.makedirs(directory)

if (dataSet == "mc16e"):
    dataDir = "/Volumes/LaCie/DVJets/mc/user.cohm.mc16_13TeV.364704.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ4WithSW.210426_test_trees.root/"
#inputFile = r.TFile("/Volumes/LaCie/DVJets/data/fullData.root", "READ")
fileNames = glob(dataDir + "*.root")
tree = r.TChain("trees_SRDV_")
for fileName in fileNames:
    tree.Add(fileName)

ntrkList = ["Ntrk4", "Ntrk5", "Ntrk6", "Ntrk>6"]

def getNtrkBin(ntrk):
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
    if (ntrkBin == "Ntrk4"):
        ntrkLabel = "N_{trk} = 4"
    if (ntrkBin == "Ntrk5"):
        ntrkLabel = "N_{trk} = 5"
    if (ntrkBin == "Ntrk6"):
        ntrkLabel = "N_{trk} = 6"
    if (ntrkBin == "Ntrk>6"):
        ntrkLabel = "N_{trk} > 6"
    return ntrkLabel
    
nDVHistDict = {}
totalDict = {}
aveNDVDict = {}
aveCombDict = {}
nDVDict = {}
for ntrk in ntrkList:
    nDVHistDict[ntrk] = r.TH1I("nDV_"+ntrk, ";nDV", 25, 0, 25)
    totalDict[ntrk] = 0
    aveNDVDict[ntrk] = 0.
    aveCombDict[ntrk] = 0.
    nDVDict[ntrk] = {}
    for ndv in range(25):
        nDVDict[ntrk][ndv] = 0
    
evtTotal = tree.GetEntries()
if (evtMax == -1):
    evtMax = evtTotal
    
evtCounter = 0
for dv in tree:
    evtCounter += 1
    if (evtCounter % 10000 == 0):
        print("Processed {}/{}".format(evtCounter, tree.GetEntries()))
    if (evtCounter > evtMax):
        break

    if (not ord(dv.DRAW_pass_triggerFlags)):
        continue
    if (not ord(dv.DRAW_pass_DVJETS)):
        continue
    if (not ord(dv.BaselineSel_pass)):
        continue

    ndv = dv.DV_n
    if (ndv < 2):
        continue
    for idv in range(0, len(dv.DV_m)-1):
        nTracks_1 = 0
        for itrack in range(len(dv.dvtrack_m)):
            if (dv.DV_index[idv] != dv.dvtrack_DVIndex[itrack]):
                continue
            if (dv.dvtrack_failedExtrapolation[itrack]):
                continue
            if (dv.dvtrack_isBackwardsTrack[itrack]):
                continue
            nTracks_1 += 1
        for jdv in range(idv+1, len(dv.DV_m)):
            nTracks_2 = 0
            for jtrack in range(len(dv.dvtrack_m)):
                if (dv.DV_index[jdv] != dv.dvtrack_DVIndex[jtrack]):
                    continue
                if (dv.dvtrack_failedExtrapolation[jtrack]):
                    continue
                if (dv.dvtrack_isBackwardsTrack[jtrack]):
                    continue
                nTracks_2 += 1
            nTracks = nTracks_1 + nTracks_2
                
            #print(evtCounter, idv, ndv, nTracks)
            if nTracks < 4:
                continue
            ntrkBin = getNtrkBin(nTracks)
            nDVHistDict[ntrkBin].Fill(ndv)
            nDVDict[ntrkBin][ndv] += 1
            #print(evtCounter, idv, jdv, nTracks, nTracks_1, nTracks_2)
            
totalDVDict = {}
ave_nDVDict = {}
ave_combDict = {}
for ntrk in ntrkList:
    totalDVDict[ntrk] = 0
    ave_nDVDict[ntrk] = 0.
    ave_combDict[ntrk] = 0.
for ntrk, ndv_dict in nDVDict.items():
    for ndv, num in ndv_dict.items():
        nComb = comb(ndv, 2)
        totalDVDict[ntrk] += num
        ave_nDVDict[ntrk] += ndv * num
        ave_combDict[ntrk] += nComb * num
             
c = r.TCanvas("c", "c", 800, 700)
c.cd()
c.SetLogy(1)

sampleLabel = r.TLatex()
sampleLabel.SetNDC()
sampleLabel.SetTextFont(42)
sampleLabel.SetTextAlign(13)
sampleLabel.SetTextSize(0.03)

sampleText = dataSet + ", di-jet"
for ntrk in ntrkList:
    nDVHist = nDVHistDict[ntrk]
    nDVHist.SetMaximum(nDVHist.GetMaximum()*2.5)
    nDVHist.SetMinimum(1)
    nDVHist.Draw("hist")
    ATLASLabel(0.20, 0.955, label)
    sampleLabel.DrawLatex(0.65, 0.90, sampleText)
    sampleLabel.DrawLatex(0.65, 0.85, "Event preselection")
    sampleLabel.DrawLatex(0.65, 0.80, getNtrkLabel(ntrk))
    sampleLabel.DrawLatex(0.65, 0.75, "Total {} DV: {}".format(ntrk, totalDVDict[ntrk]))
    sampleLabel.DrawLatex(0.65, 0.70, "Ave. nDV: {:.3f}".format(ave_nDVDict[ntrk]/totalDVDict[ntrk]))
    sampleLabel.DrawLatex(0.65, 0.65, "Ave. comb.: {:.3f}".format(ave_combDict[ntrk]/totalDVDict[ntrk]))
    c.Print("{}/{}.pdf".format(directory, "nDV_"+ntrk))
