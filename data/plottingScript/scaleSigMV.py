import ROOT as r
from scipy.special import comb
import sys, os
sys.path.append("/Users/amizukam/DVJets/atlasstyle")
from AtlasStyle import *
from AtlasLabel import *

r.gROOT.SetBatch()
SetAtlasStyle()
label = "Internal"

evtMax = -1

plotType = "sigScale"
directory = "pdfs/" + plotType
if (not os.path.isdir(directory)):
    os.makedirs(directory)
    
inputFile = r.TFile("/Volumes/LaCie/DVJets/data/fullData.root", "READ")
tree = inputFile.Get("trees_SRDV_")

ntrkList = ["Ntrk2", "Ntrk3", "Ntrk4", "Ntrk>4"]

def getNtrkBin(ntrk):
    ntrkBin = ""
    if ntrk == 2:
        ntrkBin = "Ntrk2"
    if ntrk == 3:
        ntrkBin = "Ntrk3"
    if ntrk == 4:
        ntrkBin = "Ntrk4"
    if ntrk > 4:
        ntrkBin = "Ntrk>4"
    return ntrkBin

def getNtrkLabel(ntrkBin):
    ntrkLabel = ""
    if (ntrkBin == "Ntrk2"):
        ntrkLabel = "N_{trk} = 2"
    if (ntrkBin == "Ntrk3"):
        ntrkLabel = "N_{trk} = 3"
    if (ntrkBin == "Ntrk4"):
        ntrkLabel = "N_{trk} = 4"
    if (ntrkBin == "Ntrk>4"):
        ntrkLabel = "N_{trk} > 4"
    return ntrkLabel
    
nDVHistDict = {}
totalDict = {}
aveNDVDict = {}
aveCombDict = {}
nDVDict = {}
for ntrk in ntrkList:
    nDVHistDict[ntrk] = r.TH1I("nDV_"+ntrk, ";nDV", 22, 0, 22)
    totalDict[ntrk] = 0
    aveNDVDict[ntrk] = 0.
    aveCombDict[ntrk] = 0.
    nDVDict[ntrk] = {}
    for ndv in range(22):
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

    ndv = dv.DV_n
    for idv in range(len(dv.DV_m)):
        nTracks = 0
        for itrack in range(len(dv.dvtrack_m)):
            if (dv.DV_index[idv] != dv.dvtrack_DVIndex[itrack]):
                continue
            if (dv.dvtrack_failedExtrapolation[itrack]):
                continue
            if (dv.dvtrack_isBackwardsTrack[itrack]):
                continue
            nTracks += 1
        #print(evtCounter, idv, ndv, nTracks)
        if nTracks < 2:
            continue
        ntrkBin = getNtrkBin(nTracks)
        nDVHistDict[ntrkBin].Fill(ndv)
        nDVDict[ntrkBin][ndv] += 1

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

sampleText = "Data"
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
