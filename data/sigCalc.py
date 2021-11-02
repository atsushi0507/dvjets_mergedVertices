import ROOT as r
from glob import glob
import sys, os
from utils import *
import random
from array import array
import numpy as np

outputTag = "08"
evtMax = -1
#m_pion = 139.56 * 0.001
doTrackCleaning = False

if (not os.path.isdir("outputFiles")):
    os.makedirs("outputFiles")

fileList = open("inputList/inputList_{:0>2}.txt".format(outputTag), "r")
fileNames = []
while True:
    line = fileList.readline().strip()
    if line:
        fileNames.append(line)
    else:
        break

tree = r.TChain("trees_SRDV_")
for fileName in fileNames:
    tree.Add(fileName)

if doTrackCleaning:
    outputFile = r.TFile("outputFiles/significance_{:0>2}_trackCleaning.root".format(outputTag), "RECREATE")
else:
    outputFile = r.TFile("outputFiles/significance_{:0>2}.root".format(outputTag), "RECREATE")
outTree = r.TTree("trees_SRDV_", "trees_SRDV_")

evtTotal = tree.GetEntries()
if (evtMax == -1):
    evtMax = evtTotal

significance = array("f", [0.])
dR = array("f", [0.])
mass = array("f", [0.])
ntrk = array("i", [0])
rxy1 = array("f", [0.])
rxy2 = array("f", [0.])
sameEvent = array("i", [0])
deltaZ = array("f", [0.])
det = array("f", [0.])

outTree.Branch("significance", significance, "significance/F")
outTree.Branch("dR", dR, "dR/F")
outTree.Branch("mass", mass, "mass/F")
outTree.Branch("ntrk", ntrk, "ntrk/I")
outTree.Branch("rxy1", rxy1, "rxy1/F")
outTree.Branch("rxy2", rxy2, "rxy2/F")
outTree.Branch("sameEvent", sameEvent, "sameEvent/I")
outTree.Branch("deltaZ", deltaZ, "deltaZ/F")
outTree.Branch("det", det, "det/F")

# Branches to transfer
dvPassFiducialCut = array("i", [0])
dvPassDistCut = array("i", [0])
dvPassChi2Cut = array("i", [0])
dvPassMaterialVeto = array("i", [0])

outTree.Branch("dvPassFiducialCut", dvPassFiducialCut, "dvPassFiducialCut/I")
outTree.Branch("dvPassDistCut", dvPassDistCut, "dvPassDistCut/I")
outTree.Branch("dvPassChi2Cut", dvPassChi2Cut, "dvPassChi2Cut/I")
outTree.Branch("dvPassMaterialVeto", dvPassMaterialVeto, "dvPassMaterialVeto/I")

ntrkList = ["Ntrk4", "Ntrk5", "Ntrk6", "Ntrk>6"]
# Output histograms
sigSameDict = {}
dzSameDict = {}
sigMixedDict = {}
dzMixedDict = {}
sigRatioDict = {}
dzRatioDict = {}
for ntrkBin in ntrkList:
    sigSameDict[ntrkBin] = r.TH1D("sigSame_"+ntrkBin, ";Significance", 100, 0., 1000.)
    dzSameDict[ntrkBin] = r.TH1D("dzSame_"+ntrkBin, ";#Deltaz[mm]", 300, 0., 1500.)
    sigMixedDict[ntrkBin] = r.TH1D("sigMixed_"+ntrkBin, ";Significance", 100, 0., 1000.)
    dzMixedDict[ntrkBin] = r.TH1D("dzMixed_"+ntrkBin, ";#Deltaz[mm]", 300, 0., 1500.)

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
    """
    if (not ord(t.DRAW_pass_triggerFlags)):
        continue
    if (not ord(t.DRAW_pass_DVJETS)):
        continue
    if (not ord(t.BaselineSel_pass)):
        continue
    """
    for ijet in range(len(t.calibJet_pt)):
        jets.append([t.calibJet_pt[ijet],
                     t.calibJet_eta[ijet],
                     t.calibJet_phi[ijet],
                     t.calibJet_m[ijet]*0.001
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
                           t.DV_covariance5[idv],
                           ])
        track = []
        for itrack in range(len(t.dvtrack_DVIndex)):
            if (t.DV_index[idv] != t.dvtrack_DVIndex[itrack]):
                continue
            if (t.dvtrack_failedExtrapolation[itrack]):
                continue
            if (doTrackCleaning):
                if (not t.dvtrack_PassTrackCleaning[itrack]):
                    continue
            
            track.append([t.dvtrack_ptWrtDV[itrack],
                          t.dvtrack_etaWrtDV[itrack],
                          t.dvtrack_phiWrtDV[itrack],
                          t.dvtrack_m[itrack]
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
    for idv in range(len(dvs)-1):
        for jdv in range(idv+1, len(dvs)):
            dv1, dv2 = getDVMatrix(dvs[idv]), getDVMatrix(dvs[jdv])
            cov1, cov2 = getCovarianceMatrix(cov[idv]), getCovarianceMatrix(cov[jdv])
            tracks1, nTracks1 = getDVTracks(dvtracks[idv])
            tracks2, nTracks2 = getDVTracks(dvtracks[jdv])

            if (nTracks1 < 2 or nTracks2 < 2):
                continue
            nTracks = nTracks1 + nTracks2
            
            deltaZ[0] = dvs[idv][2] - dvs[jdv][2]
            sumCov = cov1 + cov2
            det[0] = np.linalg.det(sumCov)
            rxy1[0] = dvs[idv][4]
            rxy2[0] = dvs[jdv][4]
            

            mv = tracks1 + tracks2

            cJet = getClosestJet(dvs[idv], jets)
            dR_jetDV2 = cJet.DeltaR(tracks2)

            sig = getSignificance(dv1, dv2, cov1, cov2)
            dist = getDistance(dv1, dv2)

            significance[0] = sig
            dR[0] = dR_jetDV2
            mass[0] = mv.M()
            sameEvent[0] = 1
            ntrk[0] = nTracks

            dvPassFiducialCut[0] = dvs[idv][5] and dvs[jdv][5]
            dvPassDistCut[0] = dvs[idv][6] and dvs[jdv][6]
            dvPassChi2Cut[0] = dvs[idv][7] and dvs[jdv][7]
            dvPassMaterialVeto[0] = dvs[idv][8] and dvs[jdv][8]

            outTree.Fill()

            if (nTracks < 4):
                continue
            ntrkBin = getNtrkBin(nTracks)
            sigSameDict[ntrkBin].Fill(sig)
            dzSameDict[ntrkBin].Fill(dvs[idv][2] - dvs[jdv][2])


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

            tracks1, nTracks1 = getDVTracks(dvtracks1[idv])
            tracks2, nTracks2 = getDVTracks(dvtracks2[jdv])
            
            if (nTracks1 < 2 or nTracks2 < 2):
                continue
            
            deltaZ[0] = dvs1[idv][2] - dvs2[jdv][2]
            sumCov = cov1 + cov2
            det[0] = np.linalg.det(sumCov)
            rxy1[0] = dvs1[idv][4]
            rxy2[0] = dvs2[jdv][4]
            
            nTracks = nTracks1 + nTracks2

            mv = tracks1 + tracks2

            cJet = getClosestJet(dvs1[idv], jets)
            dR_jetDV2 = cJet.DeltaR(tracks2)

            significance[0] = sig
            dR[0] = dR_jetDV2
            mass[0] = mv.M()
            sameEvent[0] = 0
            ntrk[0] = nTracks

            dvPassFiducialCut[0] = dvs1[idv][5] and dvs2[jdv][5]
            dvPassDistCut[0] = dvs1[idv][6] and dvs2[jdv][6]
            dvPassChi2Cut[0] = dvs1[idv][7] and dvs2[jdv][7]
            dvPassMaterialVeto[0] = dvs1[idv][8] and dvs2[jdv][8]
            
            outTree.Fill()

            if (nTracks < 4):
                continue
            ntrkBin = getNtrkBin(nTracks)
            sigMixedDict[ntrkBin].Fill(sig)
            dzMixedDict[ntrkBin].Fill(dvs1[idv][2] - dvs2[jdv][2])

# Get ratio histograms
sigDivideDict = {}
dzDivideDict = {}
for ntrkBin in ntrkList:
    sigRatioDict[ntrkBin] = sigSameDict[ntrkBin].Clone("sigRatio_"+ntrkBin)
    dzRatioDict[ntrkBin] = dzSameDict[ntrkBin].Clone("dzRatio_"+ntrkBin)
    sigDivideDict[ntrkBin] = sigMixedDict[ntrkBin].Clone("sigDivide_"+ntrkBin)
    dzDivideDict[ntrkBin] = dzMixedDict[ntrkBin].Clone("dzDivide_"+ntrkBin)
    
    sigRatioDict[ntrkBin].Sumw2()
    sigDivideDict[ntrkBin].Sumw2()
    sigRatioDict[ntrkBin].Scale(1./sigRatioDict[ntrkBin].Integral())
    sigDivideDict[ntrkBin].Scale(1./sigDivideDict[ntrkBin].Integral())
    sigRatioDict[ntrkBin].Divide(sigDivideDict[ntrkBin])

    dzRatioDict[ntrkBin].Sumw2()
    dzDivideDict[ntrkBin].Sumw2()
    dzRatioDict[ntrkBin].Scale(1./dzRatioDict[ntrkBin].Integral())
    dzDivideDict[ntrkBin].Scale(1./dzDivideDict[ntrkBin].Integral())
    dzRatioDict[ntrkBin].Divide(dzDivideDict[ntrkBin])
        
            
outputFile.Write()
outputFile.Close()
