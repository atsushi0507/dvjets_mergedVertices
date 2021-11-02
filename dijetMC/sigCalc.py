import ROOT as r
from glob import glob
import sys, os
from utils import *
import random
from array import array
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-sr", "--SR", required=True, help="the signal region, 'HighPtSR', or 'TracklessSR'")
parser.add_argument("-tag", required=True, help="The campaign tag, 'a', 'd', or 'e'")
parser.add_argument("-n", "--nEvents", default=-1, help="Number of events to process")
parser.add_argument("-t", "--trackCleaning", action="store_true", help="Apply track cleaning")
parser.add_argument("-m", "--materialVeto", action="store_true", help="Apply materialVeto (strict)")
parser.add_argument("-d", "--DVSel", action="store_true", help="Apply DV selection")
parser.add_argument("-s", "--skimmed", action="store_true", help="Use skimmed files")
args = parser.parse_args()

outputTag = "mc16{}".format(args.tag)
evtMax = int(args.nEvents)
SR = args.SR
doTrackCleaning = args.trackCleaning
useSkimmed = args.skimmed
useMaterialVeto = args.materialVeto
doDVSel = args.DVSel

if (outputTag == "mc16a"):
    dataDir = "user.gripelli.mc16_13TeV.361024.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ4W.210618_dijetMC16a_trees.root/"
if (outputTag == "mc16d"):
    dataDir = "user.gripelli.mc16_13TeV.361024.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ4W.210618_dijetMC16d_trees.root/"
elif (outputTag == "mc16e"):
    dataDir = "user.gripelli.mc16_13TeV.364704.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ4WithSW.210618_dijetMC16e_trees.root/"
    if (useSkimmed):
        dataDir = "skimmed/mc16e/"

if (not os.path.isdir("outputFiles")):
    os.makedirs("outputFiles")

dataPath = "/Volumes/LaCie/DVJets/mc/dijets/"
dataSet = dataPath + dataDir
fileNames = glob(dataSet + "*.root")

tree = r.TChain("trees_SRDV_")
for fileName in fileNames:
    tree.Add(fileName)

lastSuffix = ""
if useMaterialVeto:
    lastSuffix += "_matVeto"
if doDVSel:
    lastSuffix += "_DVSel"
if doTrackCleaning:
    lastSuffix += "_trackCleaning"

outputFile = r.TFile("outputFiles/significance_{}_{}{}.root".format(outputTag, SR, lastSuffix), "RECREATE")

evtTotal = tree.GetEntries()
if (evtMax == -1):
    evtMax = evtTotal

ntrkList = ["Ntrk4", "Ntrk5", "Ntrk6", "Ntrk>6"]
# Output histograms
sigSameDict = {}
sigMixedDict = {}
distSameDict = {}
distMixedDict = {}
mvMassDict_same = {}
mvMassDict_mixed = {}
nSelectedDict_same = {}
nSelectedDict_mixed = {}
dzSameDict = {}
dzMixedDict = {}
dvdv_sameDict = {}
dvdv_mixedDict = {}
dv1Jet_sameDict = {}
dv1Jet_mixedDict = {}
dv2Jet_sameDict = {}
dv2Jet_mixedDict = {}
sigSameDict_type = {}
sigMixedDict_type = {}
distSameDict_type = {}
distMixedDict_type = {}

# Near: < 30 mm, far: > 30 mm
mvRxyDict = {}
mvZDict = {}
mvRxyDict_type = {}
mvZDict_type = {}
mvRxyDict_near = {}
mvRxyDict_far = {}
mvZDict_near = {}
mvZDict_far = {}
mvRxyDict_type_near = {}
mvRxyDict_type_far = {}
mvZDict_type_near = {}
mvZDict_type_far = {}

sigSameDict_tight = {}
sigMixedDict_tight = {}
distSameDict_tight = {}
distMixedDict_tight = {}
mvMassDict_same_tight = {}
mvMassDict_mixed_tight = {}
for ntrkBin in ntrkList:
    sigSameDict[ntrkBin] = r.TH1D("sigSame_"+ntrkBin, ";Significance", 100, 0., 1000.)
    sigMixedDict[ntrkBin] = r.TH1D("sigMixed_"+ntrkBin, ";Significance", 100, 0., 1000.)
    distSameDict[ntrkBin] = r.TH1D("distSame_"+ntrkBin, ";Distance [mm]", 3000, 0., 300.)
    distMixedDict[ntrkBin] = r.TH1D("distMixed_"+ntrkBin, ";Distance [mm]", 3000, 0., 300.)
    mvMassDict_same[ntrkBin] = r.TH1D("mvMass_same_"+ntrkBin, ";m_{DV} [GeV]", 1000, 0., 100.)
    mvMassDict_mixed[ntrkBin] = r.TH1D("mvMass_mixed_"+ntrkBin, ";m_{DV} [GeV]", 1000, 0., 100.)
    nSelectedDict_same[ntrkBin] = r.TH1I("nSelected_same_"+ntrkBin, ";nSelected", 6, 0, 6)
    nSelectedDict_mixed[ntrkBin] = r.TH1I("nSelected_mixed_"+ntrkBin, ";nSelected", 6, 0, 6)
    dzSameDict[ntrkBin] = r.TH1D("deltaZ_same_"+ntrkBin, ";#Deltaz [mm]", 300, -150., 150.)
    dzMixedDict[ntrkBin] = r.TH1D("deltaZ_mixed_"+ntrkBin, ";#Deltaz [mm]", 300, -150., 150.)
    dvdv_sameDict[ntrkBin] = r.TH1D("dvdv_same_"+ntrkBin, ";#DeltaR(DV_{1}, DV_{2})", 100, 0., 10.)
    dvdv_mixedDict[ntrkBin] = r.TH1D("dvdv_mixed_"+ntrkBin, ";#DeltaR(DV_{1}, DV_{2})", 100, 0., 10.)
    dv1Jet_sameDict[ntrkBin] = r.TH1D("dv1Jet_same_"+ntrkBin, ";#DeltaR(DV_{1}, Jet)", 100, 0., 10.)
    dv1Jet_mixedDict[ntrkBin] = r.TH1D("dv1Jet_mixed_"+ntrkBin, ";#DeltaR(DV_{1}, Jet)", 100, 0., 10.)
    dv2Jet_sameDict[ntrkBin] = r.TH1D("dv2Jet_same_"+ntrkBin, ";#DeltaR(DV_{2}, Jet)", 100, 0., 10.)
    dv2Jet_mixedDict[ntrkBin] = r.TH1D("dv2Jet_mixed_"+ntrkBin, ";#DeltaR(DV_{2}, Jet)", 100, 0., 10.)
    sigSameDict_tight[ntrkBin] = r.TH1D("sigSame_tight_"+ntrkBin, ";Significance", 100, 0., 1000.)
    sigMixedDict_tight[ntrkBin] = r.TH1D("sigMixed_tight_"+ntrkBin, ";Significance", 100, 0., 1000.)
    distSameDict_tight[ntrkBin] = r.TH1D("distSame_tight_"+ntrkBin, ";Distance [mm]", 3000, 0., 300.)
    distMixedDict_tight[ntrkBin] = r.TH1D("distMixed_tight_"+ntrkBin, ";Distance [mm]", 3000, 0., 300.)
    mvMassDict_same_tight[ntrkBin] = r.TH1D("mvMass_same_tight_"+ntrkBin, ";m_{DV} [GeV]", 1000, 0., 100.)
    mvMassDict_mixed_tight[ntrkBin] = r.TH1D("mvMass_mixed_tight_"+ntrkBin, ";m_{DV} [GeV]", 1000, 0., 100.)

    mvRxyDict[ntrkBin] = r.TH1D("mvRxy_"+ntrkBin, ";R_{xy} [mm]", 3000, 0., 300.)
    mvZDict[ntrkBin] = r.TH1D("mvZ_"+ntrkBin, "z [mm]", 600, -300., 300.)
    mvRxyDict_near[ntrkBin] = r.TH1D("mvRxy_near_"+ntrkBin, ";R_{xy} [mm]", 3000, 0., 300.)
    mvRxyDict_far[ntrkBin] = r.TH1D("mvRxy_far_"+ntrkBin, ";R_{xy} [mm]", 3000, 0., 300.)
    mvZDict_near[ntrkBin] = r.TH1D("mvZ_near_"+ntrkBin, ";z [mm]", 600, -300., 300.)
    mvZDict_far[ntrkBin] = r.TH1D("mvZ_far_"+ntrkBin, ";z [mm]", 600, -300., 300.)
    
    sigSameDict_type[ntrkBin] = {}
    sigMixedDict_type[ntrkBin] = {}
    distSameDict_type[ntrkBin] = {}
    distMixedDict_type[ntrkBin] = {}
    mvRxyDict_type[ntrkBin] = {}
    mvZDict_type[ntrkBin] = {}
    mvRxyDict_type_near[ntrkBin] = {}
    mvRxyDict_type_far[ntrkBin] = {}
    mvZDict_type_near[ntrkBin] = {}
    mvZDict_type_far[ntrkBin] = {}
    for dvType in range(1, 8):
        sigSameDict_type[ntrkBin][dvType] = r.TH1D("sigSame_{}_{}".format(ntrkBin, dvType), ";Significance", 100, 0., 1000.)
        sigMixedDict_type[ntrkBin][dvType] = r.TH1D("sigMixed_{}_{}".format(ntrkBin, dvType), ";Significance", 100, 0., 1000.)
        distSameDict_type[ntrkBin][dvType] = r.TH1D("distSame_{}_{}".format(ntrkBin, dvType), ";Distance [mm]", 3000, 0., 300.)
        distMixedDict_type[ntrkBin][dvType] = r.TH1D("distMixed_{}_{}".format(ntrkBin, dvType), ";Distance [mm]", 3000, 0., 300.)
        mvRxyDict_type[ntrkBin][dvType] = r.TH1D("mvRxy_{}_{}".format(ntrkBin, dvType), ";R_{xy} [mm]", 3000, 0., 300.)
        mvZDict_type[ntrkBin][dvType] = r.TH1D("mvZ_{}_{}".format(ntrkBin, dvType), ";z [mm]", 600, -300., 300.)
        mvRxyDict_type_near[ntrkBin][dvType] = r.TH1D("mvRxy_near_{}_{}".format(ntrkBin, dvType), ";R_{xy} [mm]", 3000, 0., 300.)
        mvRxyDict_type_far[ntrkBin][dvType] = r.TH1D("mvRxy_far_{}_{}".format(ntrkBin, dvType), ";R_{xy} [mm]", 3000, 0., 300.)
        mvZDict_type_near[ntrkBin][dvType] = r.TH1D("mvZ_near_{}_{}".format(ntrkBin, dvType), ";z [mm]", 3000, 0., 300.)
        mvZDict_type_far[ntrkBin][dvType] = r.TH1D("mvZ_far_{}_{}".format(ntrkBin, dvType), ";z [mm]", 3000, 0., 300.)

    sigSameDict[ntrkBin].Sumw2()
    distSameDict[ntrkBin].Sumw2()
    sigSameDict_tight[ntrkBin].Sumw2()
    distSameDict_tight[ntrkBin].Sumw2()
    dzSameDict[ntrkBin].Sumw2()
    dzMixedDict[ntrkBin].Sumw2()
    
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

def getType(type1, type2):
    # dvType1: G4 DV
    # dvType2: G4 +PU DV
    # dvType3: G4 + Gen DV
    # dvType4: PU DV
    # dvType5: Gen + PU DV
    # dvType6: Gen DV
    # dvType7: G4 + Gen + PU DV
    dvType = -1
    if (type1 == 1 and type2 == 1):
        dvType = 1
    elif ((type1 == 1 and type2 == 4) or (type1 == 4 and type1 == 1)):
        dvType = 2
    elif ((type1 == 1 and type2 == 6) or (type1 == 6 and type2 == 1)):
        dvType = 3
    elif ((type1 == 4 and type2 == 4)):
        dvType = 4
    elif ((type1 == 4 and type2 == 6) or (type1 == 6 and type2 == 4)):
        dvType = 5
    elif (type1 == 6 and type2 == 6):
        dvType = 6
    else:
        dvType = 7
    return dvType
    
events = []
evtCounter = 0
print("Will process {}/{}".format(evtMax, evtTotal))
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

    # Apply event selection
    if (not ord(t.DRAW_pass_triggerFlags)):
        continue
    if (not ord(t.DRAW_pass_DVJETS)):
        continue
    if (SR == "HighPtSR"):
        if (not ord(t.BaselineSel_HighPtSR)):
            continue
    if (SR == "TracklessSR"):
        if (not ord(t.BaselineSel_TracklessSR)):
            continue
        
    for ijet in range(len(t.calibJet_Pt)):
        jets.append([t.calibJet_Pt[ijet],
                     t.calibJet_Eta[ijet],
                     t.calibJet_Phi[ijet],
                     t.calibJet_M[ijet]*0.001
                     ])

    for idv in range(len(t.DV_m)):
        if (useMaterialVeto and not t.DV_passMaterialVeto_strict[idv]):
            continue
        if (doDVSel):
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
                           t.DV_covariance5[idv],
                           ])
        track = []
        for itrack in range(len(t.dvtrack_DVIndex)):
            if (t.DV_index[idv] != t.dvtrack_DVIndex[itrack]):
                continue
            if (t.dvtrack_failedExtrapolation[itrack]):
                continue
            #if (doTrackCleaning and not ord(t.dvtrack_PassTrackCleaning[itrack])):
            if (doTrackCleaning and not t.dvtrack_PassTrackCleaning[itrack]):
                continue

            # To simplify the method, only using selected track
            if (t.dvtrack_isAssociated[itrack]):
                continue
                      
            truthMatchTrack = t.dvtrack_hasValidTruthLink[itrack] and t.dvtrack_truthMatchProb[itrack] > 0.5

            G4Track = False
            GenTrack = False
            PUTrack = False
            if (not truthMatchTrack):
                PUTrack = True
            else:
                if t.dvtrack_truthBarcode[itrack] > 200000:
                    G4Track = True
                else:
                    GenTrack = True

            track.append([t.dvtrack_ptWrtDV[itrack],
                          t.dvtrack_etaWrtDV[itrack],
                          t.dvtrack_phiWrtDV[itrack],
                          t.dvtrack_m[itrack],
                          t.dvtrack_isAssociated[itrack],
                          t.dvtrack_d0[itrack],
                          t.dvtrack_truthPdgId[itrack],
                          t.dvtrack_truthBarcode[itrack],
                          t.dvtrack_truthParentPdgId[itrack],
                          t.dvtrack_truthParentBarcode[itrack],
                          t.dvtrack_hasValidTruthLink[itrack],
                          t.dvtrack_truthMatchProb[itrack],
                          GenTrack,
                          G4Track,
                          PUTrack
                          ])
        tracks.append(track)
    if (len(dv) == 0):
        continue
    events.append([dv, tracks, covariance, jets])

print("Looping for same-event")
for iEvent in range(len(events)):
    dvs = events[iEvent][0]
    if (len(dvs) < 2):
        continue
    dvtracks = events[iEvent][1]
    cov = events[iEvent][2]
    jets = events[iEvent][3]
    nDV_4track = 0
    nDV_5track = 0
    nDV_6track = 0
    nDV_7track = 0
    for idv in range(len(dvs)-1):
        for jdv in range(idv+1, len(dvs)):
            nSelected1 = 0
            nSelected2 = 0
            nAttached1 = 0
            nAttached2 = 0
            for dvtrack in dvtracks[idv]:
                if (dvtrack[4] == 1): # Attached track?
                    nAttached1 += 1
                else:
                    nSelected1 += 1
            if (nSelected1 < 2):
                continue
            nTracks1 = nAttached1 + nSelected1
            for dvtrack in dvtracks[jdv]:
                if (dvtrack[4] == 1): # Attached track?
                    nAttached2 += 1
                else:
                    nSelected2 += 1
            if (nSelected2 < 2):
                continue
            nTracks2 = nAttached2 + nSelected2

            nTracks = nTracks1 + nTracks2
            nSelected = nSelected1 + nSelected2
            if (nSelected < 4):
                continue
            if (nSelected == 4):
                nDV_4track += 1
            if (nSelected == 5):
                nDV_5track += 1
            if (nSelected == 6):
                nDV_6track += 1
            if (nSelected > 6):
                nDV_7track += 1
    weight = {"Ntrk4": nDV_4track,
              "Ntrk5": nDV_5track,
              "Ntrk6": nDV_6track,
              "Ntrk>6": nDV_7track
              }
    
    for idv in range(len(dvs)-1):
        for jdv in range(idv+1, len(dvs)):
            dv1, dv2 = getDVMatrix(dvs[idv]), getDVMatrix(dvs[jdv])
            cov1, cov2 = getCovarianceMatrix(cov[idv]), getCovarianceMatrix(cov[jdv])

            tracks1 = r.TLorentzVector()
            tracks2 = r.TLorentzVector()
            nSelected1 = 0
            nSelected2 = 0
            nAttached1 = 0
            nAttached2 = 0
            nLargeD0_1 = 0
            nLargeD0_2 = 0
            hasG4Track = False
            hasGenTrack = False
            hasPUTrack = False
            dvType_1 = -1
            for dvtrack in dvtracks[idv]:
                track = r.TLorentzVector()
                track.SetPtEtaPhiM(dvtrack[0],
                                   dvtrack[1],
                                   dvtrack[2],
                                   dvtrack[3]
                                   )
                tracks1 += track
                if (dvtrack[4]):
                    nAttached1 += 1
                else:
                    nSelected1 += 1
                    if (r.TMath.Abs(dvtrack[5]) > 2.):
                        nLargeD0_1 += 1
                hasGenTrack = dvtrack[12]
                hasG4Track = dvtrack[13]
                hasPUTrack = dvtrack[14]
            if (hasG4Track and not hasGenTrack and not hasPUTrack):
                dvType_1 = 1
            elif (hasG4Track and hasPUTrack and not hasGenTrack):
                dvType_1 = 2
            elif (hasG4Track and hasGenTrack and not hasPUTrack):
                dvType_1 = 3
            elif (hasPUTrack and not hasG4Track and not hasGenTrack):
                dvType_1 = 4
            elif (hasPUTrack and hasGenTrack and not hasG4Track):
                dvType_1 = 5
            elif (hasGenTrack and not hasG4Track and not hasPUTrack):
                dvType_1 = 6
            elif (not hasG4Track and not hasGenTrack and not hasPUTrack):
                dvType_1 = 7
                    
            if (nSelected1 < 2):
                continue
            if (dvType_1 == 7 or dvType_1 == -1):
                print(dvType_1, ", 1st DV:", nSelected1)
                print(hasGenTrack, hasG4Track, hasPUTrack)

            hasG4Track = False
            hasGenTrack = False
            hasPUTrack = False
            dvType_2 = -1
            for dvtrack in dvtracks[jdv]:
                track = r.TLorentzVector()
                track.SetPtEtaPhiM(dvtrack[0],
                                   dvtrack[1],
                                   dvtrack[2],
                                   dvtrack[3]
                                   )
                tracks2 += track
                if (dvtrack[4]):
                    nAttached2 += 1
                else:
                    nSelected2 += 1
                    if (r.TMath.Abs(dvtrack[5]) > 2.):
                        nLargeD0_2 += 1
                hasGenTrack = dvtrack[12]
                hasG4Track = dvtrack[13]
                hasPUTrack = dvtrack[14]
            if (hasG4Track and not hasGenTrack and not hasPUTrack):
                dvType_2 = 1
            elif (hasG4Track and hasPUTrack and not hasGenTrack):
                dvType_2 = 2
            elif (hasG4Track and hasGenTrack and not hasPUTrack):
                dvType_2 = 3
            elif (hasPUTrack and not hasG4Track and not hasGenTrack):
                dvType_2 = 4
            elif (hasPUTrack and hasGenTrack and not hasG4Track):
                dvType_2 = 5
            elif (hasGenTrack and not hasG4Track and not hasPUTrack):
                dvType_2 = 6
            elif (not hasG4Track and not hasGenTrack and not hasPUTrack):
                dvType_2 = 7
                
            if (nSelected2 < 2):
                continue
            if (dvType_2 == 7 or dvType_2 == -1):
                print(dvType_2, ", 2nd DV", nSelected2)
                print(hasGenTrack, hasG4Track, hasPUTrack)
            nTracks1 = nSelected1 + nAttached1
            nTracks2 = nSelected2 + nAttached2
            nTracks = nTracks1 + nTracks2
            
            mv = tracks1 + tracks2

            cJet = getClosestJet(dvs[idv], jets)
            dR_jetDV1 = cJet.DeltaR(tracks1)
            dR_jetDV2 = cJet.DeltaR(tracks2)
            dR_dvdv = tracks1.DeltaR(tracks2)

            sig = getSignificance(dv1, dv2, cov1, cov2)
            dist = getDistance(dv1, dv2)
            deltaZ = dvs[idv][2] - dvs[jdv][2]

            nSelected = nSelected1 + nSelected2
            if (nSelected < 4):
                continue
            if (nTracks < 4):
                continue
            dvType = getType(dvType_1, dvType_2)
            ntrkBin = getNtrkBin(nTracks)
            ntrkSelBin = getNtrkBin(nSelected)
            sigSameDict[ntrkBin].Fill(sig, 1./weight[ntrkBin])
            mvMassDict_same[ntrkBin].Fill(mv.M())
            nSelectedDict_same[ntrkBin].Fill(nSelected)
            dvdv_sameDict[ntrkBin].Fill(dR_dvdv)
            dv1Jet_sameDict[ntrkBin].Fill(dR_jetDV1)
            dv2Jet_sameDict[ntrkBin].Fill(dR_jetDV2)
            #sigSameDict_type[ntrkBin][dvType_1][dvType_2].Fill(sig, 1./weight[ntrkBin])
            sigSameDict_type[ntrkBin][dvType].Fill(sig, 1./weight[ntrkBin])
            if (sig < 100.):
                distSameDict[ntrkBin].Fill(dist)
                dzSameDict[ntrkBin].Fill(deltaZ)
                distSameDict_type[ntrkBin][dvType].Fill(dist)
            if ((nLargeD0_1 + nLargeD0_2) < 2):
                continue
            sigSameDict_tight[ntrkBin].Fill(sig, 1./weight[ntrkBin])
            mvMassDict_same_tight[ntrkBin].Fill(mv.M())
            if (sig < 100.):
                distSameDict_tight[ntrkBin].Fill(dist)

print("Looping for mixed-event")
for iEvent in range(len(events)-1):
    if (len(events) < 3):
        continue
    if (iEvent % 1000 == 0):
        print("Processed {}/{}".format(iEvent, len(events)))
    dvs1 = events[iEvent][0]
    dvtracks1 = events[iEvent][1]
    covs1 = events[iEvent][2]

    dvs2 = events[iEvent+1][0]
    dvtracks2 = events[iEvent+1][1]
    covs2 = events[iEvent+1][2]

    eventList = [i for i in range(len(events))]
    isSame = True
    i = -1
    while isSame:
        i = random.choice(eventList)
        if (i != iEvent and i != iEvent+1):
            isSame = False
    jets = events[i][3]

    for idv in range(len(dvs1)):
        for jdv in range(len(dvs2)):
            dv1, dv2 = getDVMatrix(dvs1[idv]), getDVMatrix(dvs2[jdv])
            cov1, cov2 = getCovarianceMatrix(covs1[idv]), getCovarianceMatrix(covs2[jdv])
            
            sig = getSignificance(dv1, dv2, cov1, cov2)
            dist = getDistance(dv1, dv2)
            deltaZ = dvs1[idv][2] - dvs2[jdv][2]

            tracks1 = r.TLorentzVector()
            tracks2 = r.TLorentzVector()
            nSelected1 = 0
            nSelected2 = 0
            nAttached1 = 0
            nAttached2 = 0
            nLargeD0_1 = 0
            nLargeD0_2 = 0
            hasG4Track = False
            hasGenTrack = False
            hasPUTrack = False
            dvType_1 = 7
            for dvtrack in dvtracks1[idv]:
                track = r.TLorentzVector()
                track.SetPtEtaPhiM(dvtrack[0],
                                   dvtrack[1],
                                   dvtrack[2],
                                   dvtrack[3]
                                   )
                tracks1 += track
                if (dvtrack[4]):
                    nAttached1 += 1
                else:
                    nSelected1 += 1
                    if (r.TMath.Abs(dvtrack[5]) > 2.):
                        nLargeD0_1 += 1
                hasGenTrack = dvtrack[12]
                hasG4Track = dvtrack[13]
                hasPUTrack = dvtrack[14]
                if (hasG4Track and not hasGenTrack and not hasPUTrack):
                    dvType_1 = 1
                elif (hasG4Track and hasPUTrack and not hasGenTrack):
                    dvType_1 = 2
                elif (hasG4Track and hasGenTrack and not hasPUTrack):
                    dvType_1 = 3
                elif (hasPUTrack and not hasG4Track and not hasGenTrack):
                    dvType_1 = 4
                elif (hasPUTrack and hasGenTrack and not hasG4Track):
                    dvType_1 = 5
                elif (hasGenTrack and not hasG4Track and not hasPUTrack):
                    dvType_1 = 6
                elif (not hasG4Track and not hasG4Track and not hasPUTrack):
                    dvType_1 = 7
                
            if (nSelected1 < 2):
                continue

            hasG4Track = False
            hasGenTrack = False
            hasPUTrack = False
            dvType_2 = 7
            for dvtrack in dvtracks2[jdv]:
                track = r.TLorentzVector()
                track.SetPtEtaPhiM(dvtrack[0],
                                   dvtrack[1],
                                   dvtrack[2],
                                   dvtrack[3]
                                   )
                tracks2 += track
                if (dvtrack[4]):
                    nAttached2 += 1
                else:
                    nSelected2 += 1
                    if (r.TMath.Abs(dvtrack[5]) > 2.):
                        nLargeD0_2 += 1
                hasGenTrack = dvtrack[12]
                hasG4Track = dvtrack[13]
                hasPUTrack = dvtrack[14]
                if (hasG4Track and not hasGenTrack and not hasPUTrack):
                    dvType_2 = 1
                elif (hasG4Track and hasPUTrack and not hasGenTrack):
                    dvType_2 = 2
                elif (hasG4Track and hasGenTrack and not hasPUTrack):
                    dvType_2 = 3
                elif (hasPUTrack and not hasG4Track and not hasGenTrack):
                    dvType_2 = 4
                elif (hasPUTrack and hasGenTrack and not hasG4Track):
                    dvType_2 = 5
                elif (hasGenTrack and not hasG4Track and not hasPUTrack):
                    dvType_2 = 6
                elif (not hasG4Track and not hasG4Track and not hasPUTrack):
                    dvType_2 = 7
                
            if (nSelected2 < 2):
                continue
            nTracks1 = nSelected1 + nAttached1
            nTracks2 = nSelected2 + nAttached2
            nTracks = nTracks1 + nTracks2
            
            nTracks = nTracks1 + nTracks2

            mv = tracks1 + tracks2
            mv_x = (tracks1.M()*dvs1[idv][0] + tracks2.M()*dvs2[jdv][0]) / mv.M()
            mv_y = (tracks1.M()*dvs1[idv][1] + tracks2.M()*dvs2[jdv][1]) / mv.M()
            mv_z = (tracks1.M()*dvs1[idv][2] + tracks2.M()*dvs2[jdv][2]) / mv.M()
            mvRxy = r.TMath.Sqrt(mv_x*mv_x + mv_y*mv_y)

            dx = dvs1[idv][0] - dvs2[jdv][0]
            dy = dvs1[idv][1] - dvs2[jdv][1]
            dz = dvs1[idv][2] - dvs2[jdv][2]
            mvDist = r.TMath.Sqrt(dx*dx + dy*dy + dz*dz)

            cJet = getClosestJet(dvs1[idv], jets)
            dR_jetDV2 = cJet.DeltaR(tracks2)
            dR_jetDV1 = cJet.DeltaR(tracks1)
            dR_dvdv = tracks1.DeltaR(tracks2)

            nSelected = nSelected1 + nSelected2
            if (nSelected < 4):
                continue
            if (nTracks < 4):
                continue
            dvType = getType(dvType_1, dvType_2)
            ntrkBin = getNtrkBin(nTracks)
            ntrkSelBin = getNtrkBin(nSelected)
            sigMixedDict[ntrkBin].Fill(sig)
            mvMassDict_mixed[ntrkBin].Fill(mv.M())
            nSelectedDict_mixed[ntrkBin].Fill(nSelected)
            dvdv_mixedDict[ntrkBin].Fill(dR_dvdv)
            dv1Jet_mixedDict[ntrkBin].Fill(dR_jetDV1)
            dv2Jet_mixedDict[ntrkBin].Fill(dR_jetDV2)
            #sigMixedDict_type[ntrkBin][dvType_1][dvType_2].Fill(sig)
            sigMixedDict_type[ntrkBin][dvType].Fill(sig)
            if (sig < 100.):
                distMixedDict[ntrkBin].Fill(dist)
                dzMixedDict[ntrkBin].Fill(deltaZ)
                distMixedDict_type[ntrkBin][dvType].Fill(dist)
                mvRxyDict[ntrkBin].Fill(mvRxy)
                mvZDict[ntrkBin].Fill(mv_z)
                mvRxyDict_type[ntrkBin][dvType].Fill(mvRxy)
                mvZDict_type[ntrkBin][dvType].Fill(mv_z)
                if (mvDist < 30.):
                    mvRxyDict_near[ntrkBin].Fill(mvRxy)
                    mvZDict_near[ntrkBin].Fill(mv_z)
                    mvRxyDict_type_near[ntrkBin][dvType].Fill(mvRxy)
                    mvZDict_type_near[ntrkBin][dvType].Fill(mv_z)
                else:
                    mvRxyDict_far[ntrkBin].Fill(mvRxy)
                    mvZDict_far[ntrkBin].Fill(mv_z)
                    mvRxyDict_type_far[ntrkBin][dvType].Fill(mvRxy)
                    mvZDict_type_far[ntrkBin][dvType].Fill(mv_z)
                    
            if ((nLargeD0_1 + nLargeD0_2) < 2):
                continue
            sigMixedDict_tight[ntrkBin].Fill(sig)
            mvMassDict_mixed_tight[ntrkBin].Fill(mv.M())
            if (sig < 100.):
                distMixedDict_tight[ntrkBin].Fill(dist)
            
outputFile.Write()
outputFile.Close()
