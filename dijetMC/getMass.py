import ROOT as r
from glob import glob
import sys, os
sys.path.append("/Users/amizukam/DVJets/atlasstyle")
from AtlasStyle import *
from AtlasLabel import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-sr", "--SR", required=True, help="Signal region, 'HighPtSR' or 'TracklessSR'")
parser.add_argument("-tag", required=True, help="The campaign tag, 'a', 'd', or 'e'")
parser.add_argument("-n", "--nEvents", default=-1, help="Set maximum number of events to process")
args = parser.parse_args()

r.gROOT.SetBatch()
SetAtlasStyle()
label = "Internal"

SR = args.SR

outputTag = "mc16{}".format(args.tag)
evtMax = int(args.nEvents)

# xs = xs * genFilterEff * kFactor(=1)
if (outputTag == "mc16a"):
    dataDir = "user.gripelli.mc16_13TeV.361024.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ4W.210630_dijetMC16a_trees.root/"
    lumi = 32988.1 + 3218.56
    xs = 254630.0 * 5.3137e-4 * 1
    sumOfWeights = 990000 # sum of weights: 25110544.1279
elif (outputTag == "mc16d"):
    dataDir = "user.gripelli.mc16_13TeV.361024.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ4W.210618_dijetMC16d_trees.root/"
    lumi = 44307.4
    xs = 254630.0 * 5.3137e-4 * 1
    sumOfWeights = 1000000 # sum of weights: 25326409.913
elif (outputTag == "mc16e"):
    dataDir = "user.gripelli.mc16_13TeV.364704.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ4WithSW.210618_dijetMC16e_trees.root/"
    lumi = 58450.1
    xs = 254610.0 * 1.3366e-2 * 1
    sumOfWeights = 2.89897496062 # raw count: 13000200

if (not os.path.isdir("outputFiles")):
    os.makedirs("outputFiles")

dataPath = "/Volumes/LaCie/DVJets/mc/dijets/"
dataSet = dataPath + dataDir
fileNames = glob(dataSet + "*.root")

tree = r.TChain("trees_SRDV_")
for fileName in fileNames:
    tree.Add(fileName)

outputFile = r.TFile("outputFiles/dvMass_{}.root".format(outputTag+"_" + SR), "RECREATE")

evtTotal = tree.GetEntries()
if (evtMax == -1):
    evtMax = evtTotal

lumiWeight = (lumi * xs) / sumOfWeights

ntrkList = ["Ntrk2", "Ntrk3", "Ntrk4", "Ntrk5", "Ntrk6", "Ntrk>6"]
# Output histograms
dvMassDict = {}
dvMassDict_DVSel = {}
dvMassDict_fullSel = {}
dvMassDict_tc = {}
dvMassDict_selectedCut = {}
dvMassDict_DVSel_selectedCut = {}
dvMassDict_fullSel_selectedCut = {}
dvMassDict_tc_selectedCut = {}
dvMassDict_fullSelection = {}
dvMassDict_DVSel_fullSelection = {}
dvMassDict_fullSel_fullSelection = {}
dvMassDict_tc_fullSelection = {}
mvtrack_pt_total = {}
mvtrack_pt = {}
mvtrack_pt_selected_total = {}
mvtrack_pt_selected = {}
mvtrack_pt_attached_total = {}
mvtrack_pt_attached = {}
mvtrack_d0Selected_total = {}
mvtrack_d0Selected = {}
mvtrack_d0_total = {}
mvtrack_d0 = {}
dvMassDict_selected = {}
dvMassDict_selected_tc = {}
for ntrk in ntrkList:
    dvMassDict[ntrk] = r.TH1D("dvMass_noSelection_"+ntrk, ";m_{DV} [GeV]", 1000, 0., 100.)
    dvMassDict_DVSel[ntrk] = r.TH1D("dvMass_DVSel_"+ntrk, ";m_{DV} [GeV]", 1000, 0., 100.)
    dvMassDict_fullSel[ntrk] = r.TH1D("dvMass_fullSel_"+ntrk, ";m_{DV} [GeV]", 1000, 0., 100.)
    dvMassDict_tc[ntrk] = r.TH1D("dvMass_tc_"+ntrk, ";m_{DV} [GeV]", 1000, 0., 100.)
    dvMassDict_selectedCut[ntrk] = r.TH1D("dvMass_noSelection_selectedCut_"+ntrk, ";m_{DV} [GeV]", 1000, 0., 100.)
    dvMassDict_DVSel_selectedCut[ntrk] = r.TH1D("dvMass_DVSelection_selectedCut_"+ntrk, ";m_{DV} [GeV]", 1000, 0., 100.)
    dvMassDict_fullSel_selectedCut[ntrk] = r.TH1D("dvMass_fullSelection_selectedCut_"+ntrk, ";m_{DV} [GeV]", 1000, 0., 100.)
    dvMassDict_tc_selectedCut[ntrk] = r.TH1D("dvMass_tc_selectedCut_"+ntrk, ";m_{DV} [GeV]", 1000, 0., 100.)
    dvMassDict_fullSelection[ntrk] = r.TH1D("dvMass_noSelection_fullSelection_"+ntrk, ";m_{DV} [GeV]", 1000, 0., 100.)
    dvMassDict_DVSel_fullSelection[ntrk] = r.TH1D("dvMass_DVSel_fullSelection_"+ntrk, ";m_{DV} [GeV]", 1000, 0., 100.)
    dvMassDict_fullSel_fullSelection[ntrk] = r.TH1D("dvMass_fullSel_fullSelection_"+ntrk, ";m_{DV} [GeV]", 1000, 0., 100.)
    dvMassDict_tc_fullSelection[ntrk] = r.TH1D("dvMass_tc_fullSelection_"+ntrk, ";m_{DV} [GeV]", 1000, 0., 100.)
    mvtrack_pt[ntrk] = r.TH1D("mvtrack_pt_"+ntrk, ";p_{T} [GeV]", 250, 0., 25.)
    mvtrack_pt_selected[ntrk] = r.TH1D("mvtrack_pt_selected_"+ntrk, ";p_{T} [GeV]", 250, 0., 25.)
    mvtrack_pt_attached[ntrk] = r.TH1D("mvtrack_pt_attached_"+ntrk, ";p_{T} [GeV]", 250, 0., 25.)
    mvtrack_d0Selected[ntrk] = r.TH1D("mvtrack_d0Selected_"+ntrk, ";d0-significance", 100, 0., 100.)
    mvtrack_d0[ntrk] = r.TH1D("mvtrack_d0_"+ntrk, ";d0 [mm]", 250, 0., 25.)
    mvtrack_pt_total[ntrk] = r.TH1D("mvtrack_pt_total_"+ntrk, ";p_{T} [GeV]", 250, 0., 25.)
    mvtrack_pt_selected_total[ntrk] = r.TH1D("mvtrack_pt_selected_total_"+ntrk, ";p_{T} [GeV]", 250, 0., 25.)
    mvtrack_pt_attached_total[ntrk] = r.TH1D("mvtrack_pt_attached_total_"+ntrk, ";p_{T} [GeV]", 250, 0., 25.)
    mvtrack_d0Selected_total[ntrk] = r.TH1D("mvtrack_d0Selected_total_"+ntrk, ";d0-significance", 100, 0., 100.)
    mvtrack_d0_total[ntrk] = r.TH1D("mvtrack_d0_total_"+ntrk, ";d0 [mm]", 250, 0., 25.)
    dvMassDict_selected[ntrk] = r.TH1D("dvMass_selected_"+ntrk, ";m_{DV} [GeV]", 1000, 0., 100.)
    dvMassDict_selected_tc[ntrk] = r.TH1D("dvMass_selected_tc_"+ntrk, ";m_{DV} [GeV]", 1000, 0., 100.)

def getNtrkBin(ntrk):
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

events = []
evtCounter = 0
for t in tree:
    evtCounter += 1
    if (evtCounter > evtMax):
        break
    if (evtCounter % 10000 == 0):
        print("Processed {}/{}".format(evtCounter, evtMax))

    if (not ord(t.DRAW_pass_triggerFlags)):
        continue
    if (not ord(t.DRAW_pass_DVJETS)):
        continue
    if (SR == "HighPtSR"):
        if (not ord(t.BaselineSel_HighPtSR)):
            continue
    if (SR == "TrackessSR"):
        if (not ord(t.BaselineSel_TracklessSR)):
            continue

    weight = lumiWeight * t.mcEventWeight

    for idv in range(len(t.DV_index)):
        tracks_noDVSel = r.TLorentzVector()
        tracks_selected = r.TLorentzVector()
        nTracks_noDVSel = 0
        nSelected_noDVSel = 0
        nLargeD0_noDVSel = 0
        nAttached_noDVSel = 0
        for itrack in range(len(t.dvtrack_DVIndex)):
            if (t.DV_index[idv] != t.dvtrack_DVIndex[itrack]):
                continue
            if (t.DV_index[idv] != t.dvtrack_DVIndex[itrack]):
                continue
            track = r.TLorentzVector()
            track.SetPtEtaPhiM(t.dvtrack_ptWrtDV[itrack],
                               t.dvtrack_etaWrtDV[itrack],
                               t.dvtrack_phiWrtDV[itrack],
                               t.dvtrack_m[itrack]
                               )
            nTracks_noDVSel += 1
            tracks_noDVSel += track
            if (not t.dvtrack_isAssociated[itrack]):
                nSelected_noDVSel += 1
                tracks_selected += track
                if (r.TMath.Abs(t.dvtrack_d0[itrack]) > 2.):
                    nLargeD0_noDVSel += 1
            else:
                nAttached_noDVSel += 1
    for idv in range(len(t.DV_index)):
        
        tracks_DVSel = r.TLorentzVector()
        tracks_fullSel = r.TLorentzVector()
        tracks_tc = r.TLorentzVector()
        tracks_selected_tc = r.TLorentzVector()
        
        nTracks_DVSel = 0
        nTracks_fullSel = 0
        nTracks_tc = 0
        nSelected_DVSel = 0
        nSelected_fullSel = 0
        nSelected_tc = 0
        nLargeD0_DVSel = 0
        nLargeD0_fullSel = 0
        nLargeD0_tc = 0
        nAttached_tc = 0

        for itrack in range(len(t.dvtrack_DVIndex)):
            if (t.DV_index[idv] != t.dvtrack_DVIndex[itrack]):
                continue
            track = r.TLorentzVector()
            track.SetPtEtaPhiM(t.dvtrack_ptWrtDV[itrack],
                               t.dvtrack_etaWrtDV[itrack],
                               t.dvtrack_phiWrtDV[itrack],
                               t.dvtrack_m[itrack]
                               )
            if (ord(t.dvtrack_PassTrackCleaning[itrack])):
                nTracks_tc += 1
                tracks_tc += track
                if (not t.dvtrack_isAssociated[itrack]):
                    nSelected_tc += 1
                    tracks_selected_tc += track
                    if (r.TMath.Abs(t.dvtrack_d0[itrack]) > 2.):
                        nLargeD0_tc += 1
                else:
                    nAttached_tc += 1
        
        if (not t.DV_passFiducialCut[idv]):
            continue
        if (not t.DV_passDistCut[idv]):
            continue
        if (not t.DV_passChiSqCut[idv]):
            continue
        if (not t.DV_passMaterialVeto[idv]):
            continue
        if (not t.DV_passMaterialVeto_strict[idv]):
            continue
        
        for itrack in range(len(t.dvtrack_DVIndex)):
            if (t.DV_index[idv] != t.dvtrack_DVIndex[itrack]):
                continue
            track = r.TLorentzVector()
            track.SetPtEtaPhiM(t.dvtrack_ptWrtDV[itrack],
                               t.dvtrack_etaWrtDV[itrack],
                               t.dvtrack_phiWrtDV[itrack],
                               t.dvtrack_m[itrack]
                               )
            nTracks_DVSel += 1
            tracks_DVSel += track
            if (not t.dvtrack_isAssociated[itrack]):
                nSelected_DVSel += 1
                if (r.TMath.Abs(t.dvtrack_d0[itrack]) > 2.):
                    nLargeD0_DVSel += 1
            if (ord(t.dvtrack_PassTrackCleaning[itrack])):
                tracks_fullSel += track
                nTracks_fullSel += 1
                if (not t.dvtrack_isAssociated[itrack]):
                    nSelected_fullSel += 1
                    if (r.TMath.Abs(t.dvtrack_d0[itrack]) > 2.):
                        nLargeD0_fullSel += 1
        for itrack in range(len(t.dvtrack_DVIndex)):
            if (t.DV_index[idv] != t.dvtrack_DVIndex[itrack]):
                continue
            nTrk_noDVSel = getNtrkBin(nTracks_noDVSel)
            nSel = getNtrkBin(nSelected_noDVSel)
            mvtrack_pt_total[nTrk_noDVSel].Fill(t.dvtrack_ptWrtDV[itrack], weight)
            mvtrack_pt[nSel].Fill(t.dvtrack_ptWrtDV[itrack], weight)
            d0sig = r.TMath.Abs(t.dvtrack_d0[itrack]/t.dvtrack_errd0[itrack])
            if (t.dvtrack_isAssociated[itrack]):
                mvtrack_pt_attached_total[nTrk_noDVSel].Fill(t.dvtrack_ptWrtDV[itrack], weight)
                mvtrack_pt_attached[nSel].Fill(t.dvtrack_ptWrtDV[itrack], weight)
            else:
                mvtrack_pt_selected_total[nTrk_noDVSel].Fill(t.dvtrack_ptWrtDV[itrack], weight)
                mvtrack_pt_selected[nSel].Fill(t.dvtrack_ptWrtDV[itrack], weight)
                mvtrack_d0Selected_total[nTrk_noDVSel].Fill(d0sig, weight)
                mvtrack_d0Selected[nSel].Fill(d0sig, weight)
                mvtrack_d0_total[nTrk_noDVSel].Fill(r.TMath.Abs(t.dvtrack_d0[itrack]), weight)
                mvtrack_d0[nSel].Fill(r.TMath.Abs(t.dvtrack_d0[itrack]), weight)

    if nTracks_noDVSel > 1:
        nTrk_noDVSel = getNtrkBin(nTracks_noDVSel)
        dvMassDict[nTrk_noDVSel].Fill(tracks_noDVSel.M(), weight)
        if (nSelected_noDVSel >= 4):
            dvMassDict_selectedCut[nTrk_noDVSel].Fill(tracks_noDVSel.M(), weight)
            if (nLargeD0_noDVSel >= 2):
                dvMassDict_fullSelection[nTrk_noDVSel].Fill(tracks_noDVSel.M(), weight)
    if nTracks_DVSel > 1:
        nTrk_DVSel = getNtrkBin(nTracks_DVSel)
        dvMassDict_DVSel[nTrk_DVSel].Fill(tracks_DVSel.M(), weight)
        if (nSelected_DVSel >= 4):
            dvMassDict_DVSel_selectedCut[nTrk_DVSel].Fill(tracks_DVSel.M(), weight)
            if (nLargeD0_DVSel >= 2):
                dvMassDict_DVSel_fullSelection[nTrk_DVSel].Fill(tracks_DVSel.M(), weight)
    if nTracks_fullSel > 1:
        nTrk_fullSel = getNtrkBin(nTracks_fullSel)
        dvMassDict_fullSel[nTrk_fullSel].Fill(tracks_fullSel.M(), weight)
        if (nSelected_fullSel >= 4):
            dvMassDict_fullSel_selectedCut[nTrk_fullSel].Fill(tracks_fullSel.M(), weight)
            if (nLargeD0_fullSel >= 2):
                dvMassDict_fullSel_fullSelection[nTrk_fullSel].Fill(tracks_fullSel.M(), weight)
    if nTracks_tc > 1:
        nTrk_tc = getNtrkBin(nTracks_tc)
        dvMassDict_tc[nTrk_tc].Fill(tracks_tc.M(), weight)
        if (nSelected_tc >= 4):
            dvMassDict_tc_selectedCut[nTrk_tc].Fill(tracks_tc.M(), weight)
            if (nLargeD0_tc >= 2):
                dvMassDict_tc_fullSelection[nTrk_tc].Fill(tracks_tc.M(), weight)
    if (nSelected_noDVSel > 1 and nAttached_noDVSel == 0):
        nSel = getNtrkBin(nSelected_noDVSel)
        dvMassDict_selected[nSel].Fill(tracks_selected.M(), weight)
    if (nSelected_tc > 1 and nAttached_tc == 0):
        nSel_tc = getNtrkBin(nSelected_tc)
        dvMassDict_selected_tc[nSel_tc].Fill(tracks_selected_tc.M(), weight)

outputFile.Write()
outputFile.Close()
