import ROOT as r
from glob import glob
import sys, os
sys.path.append("/Users/amizukam/DVJets/mvStudy")
sys.path.append("/Users/amizukam/DVJets/atlasstyle")
from utils import *
from AtlasStyle import *

r.gROOT.SetBatch()
SetAtlasStyle()

evtMax = -1

dataDir = "user.cohm.mc16_13TeV.364704.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ4WithSW.210426_test_trees.root/"

directory = "pdfs/check"
if (not os.path.isdir(directory)):
    os.makedirs(directory)

dataPath = "/Volumes/LaCie/DVJets/mc/"
dataSet = dataPath + dataDir
fileNames = glob(dataSet + "*.root")
tree = r.TChain("trees_SRDV_")
for fileName in fileNames:
    tree.Add(fileName)

outputFile = r.TFile("outputFiles/check.root", "RECREATE")

evtTotal = tree.GetEntries()
if (evtMax == -1):
    evtMax = evtTotal

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

ntrkList = ["Ntrk4", "Ntrk5", "Ntrk6", "Ntrk>6"]
# Output histograms
rxy1SameDict = {}
rxy2SameDict = {}
rxy1MixedDict = {}
rxy2MixedDict = {}
for ntrk in ntrkList:
    rxy1SameDict[ntrk] = r.TH1D("rxy1_same_"+ntrk, ";rxy [mm]", 300, 0., 300.)
    rxy2SameDict[ntrk] = r.TH1D("rxy2_same_"+ntrk, ";rxy [mm]", 300, 0., 300.)
    rxy1MixedDict[ntrk] = r.TH1D("rxy1_mixed_"+ntrk, ";rxy [mm]", 300, 0., 300.)
    rxy2MixedDict[ntrk] = r.TH1D("rxy2_mixed_"+ntrk, ";rxy [mm]", 300, 0., 300.)


events = []
evtCounter = 0
for t in tree:
    evtCounter += 1
    if (evtCounter > evtMax):
        break
    if (evtCounter % 10000 == 0):
        print("Processed {}/{}".format(evtCounter, evtMax))

    dv = []
    tracks = []
    covariance = []
    jets = []

    if (not ord(t.DRAW_pass_triggerFlags)):
        continue
    if (not ord(t.DRAW_pass_DVJETS)):
        continue
    if (not ord(t.BaselineSel_pass)):
        continue

    for ijet in range(len(t.calibJet_Pt)):
        jets.append([t.calibJet_Pt[ijet],
                     t.calibJet_Eta[ijet],
                     t.calibJet_Phi[ijet],
                     t.calibJet_M[ijet]*0.001
                     ])

    for idv in range(len(t.DV_m)):
        dv.append([t.DV_x[idv],
                   t.DV_y[idv],
                   t.DV_z[idv],
                   t.DV_m[idv],
                   t.DV_rxy[idv],
                   t.DV_passFiducialCut[idv],
                   t.DV_passDistCut[idv],
                   t.DV_passChiSqCut[idv],
                   t.DV_passMaterialVeto[idv]
                   ])
        covariance.append([t.DV_covariance0[idv],
                           t.DV_covariance1[idv],
                           t.DV_covariance2[idv],
                           t.DV_covariance3[idv],
                           t.DV_covariance4[idv],
                           t.DV_covariance5[idv]
                           ])

        track = []
        for itrack in range(len(t.dvtrack_DVIndex)):
            if (t.DV_index[idv] != t.dvtrack_DVIndex[itrack]):
                continue
            if (t.dvtrack_failedExtrapolation[itrack]):
                continue
            track.append([t.dvtrack_ptWrtDV[itrack],
                          t.dvtrack_etaWrtDV[itrack],
                          t.dvtrack_phiWrtDV[itrack],
                          t.dvtrack_m[itrack],
                          ])
        tracks.append(track)
    if (len(dv) == 0):
        continue
    events.append([dv, tracks, covariance, jets])

print("Looping for same event")
for event in events:
    dvs = event[0]
    tracks = event[1]
    covs = event[2]
    jets = event[3]
    nDV = len(dvs)
    if (nDV < 2):
        continue
    for idv in range(0, nDV-1):
        nTracks1 = len(tracks[idv])
        for jdv in range(idv+1, nDV):
            nTracks2 = len(tracks[jdv])
            if (nTracks1 < 2 or nTracks2 < 2):
                continue
            nTracks = nTracks1 + nTracks2
            ntrkBin = getNtrkBin(nTracks)

            rxy1 = dvs[idv][4]
            rxy2 = dvs[jdv][4]
            """
            print(len(dvs))
            print(idv, jdv, ntrkBin, rxy1, rxy2)
            """

            rxy1SameDict[ntrkBin].Fill(rxy1)
            rxy2SameDict[ntrkBin].Fill(rxy2)

print("Looping for mixed-event")
for iEvent in range(len(events)-1):
    if (len(events) < 3):
        continue
    if (iEvent % 1000 == 0):
        print("Processed {}/{}".format(iEvent, len(events)))
    dvs1 = events[iEvent][0]
    tracks1 = events[iEvent][1]

    dvs2 = events[iEvent+1][0]
    tracks2 = events[iEvent+1][1]
    for idv in range(len(dvs1)):
        nTracks1 = len(tracks1[idv])
        for jdv in range(len(dvs2)):
            nTracks2 = len(tracks2[jdv])
            if (nTracks1 < 2 or nTracks2 < 2):
                continue
            nTracks = nTracks1 + nTracks2
            ntrkBin = getNtrkBin(nTracks)

            rxy1 = dvs1[idv][4]
            rxy2 = dvs2[jdv][4]
            """
            print(len(dvs1), len(dvs2))
            print(iEvent, idv, jdv, ntrkBin, rxy1, rxy2)
            """

            rxy1MixedDict[ntrkBin].Fill(rxy1)
            rxy2MixedDict[ntrkBin].Fill(rxy2)

c = r.TCanvas("c", "c", 800, 700)
c.cd()
for ntrk in ntrkList:
    rxy1SameHist = rxy1SameDict[ntrk]
    rxy2SameHist = rxy2SameDict[ntrk]
    rxy1MixedHist = rxy1MixedDict[ntrk]
    rxy2MixedHist = rxy2MixedDict[ntrk]

    rxy1SameHist.SetLineColor(r.kBlack)
    rxy2SameHist.SetLineColor(r.kRed)
    rxy1MixedHist.SetLineColor(r.kBlack)
    rxy2MixedHist.SetLineColor(r.kRed)

    nbins = rxy1SameHist.GetNbinsX()
    rxy1SameHist.SetBinContent(nbins, rxy1SameHist.GetBinContent(nbins)+rxy1SameHist.GetBinContent(nbins+1))
    rxy2SameHist.SetBinContent(nbins, rxy2SameHist.GetBinContent(nbins)+rxy2SameHist.GetBinContent(nbins+1))
    rxy1MixedHist.SetBinContent(nbins, rxy1MixedHist.GetBinContent(nbins)+rxy1MixedHist.GetBinContent(nbins+1))
    rxy2MixedHist.SetBinContent(nbins, rxy2MixedHist.GetBinContent(nbins)+rxy2MixedHist.GetBinContent(nbins+1))

    leg = r.TLegend(0.75, 0.75, 0.85, 0.85)
    leg.SetFillStyle(0)
    leg.SetBorderSize(0)
    leg.SetTextSize(0.03)

    leg.AddEntry(rxy1SameDict["Ntrk4"], "DV1", "l")
    leg.AddEntry(rxy2SameDict["Ntrk4"], "DV2", "l")

    c.SetLogy(1)

    if (rxy1SameHist.GetMaximum() > rxy2SameHist.GetMaximum()):
        maximum = rxy1SameHist.GetMaximum()
    else:
        maximum = rxy2SameHist.GetMaximum()
        
    rxy1SameHist.SetMaximum(maximum * 1.2)
    rxy1SameHist.Draw("hist")
    rxy2SameHist.Draw("hist same")
    leg.Draw()
    c.Print("{}/{}.pdf".format(directory, "same_"+ntrk))

    if (rxy1MixedHist.GetMaximum() > rxy2MixedHist.GetMaximum()):
        maximum = rxy1MixedHist.GetMaximum()
    else:
        maximum = rxy2MixedHist.GetMaximum()

    rxy1MixedHist.SetMaximum(maximum * 1.2)
    rxy1MixedHist.Draw("hist")
    rxy2MixedHist.Draw("hist same")
    leg.Draw()
    c.Print("{}/{}.pdf".format(directory, "mixed_"+ntrk))
