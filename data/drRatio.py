import ROOT as r
from glob import glob
import sys, os
sys.path.append("/Users/amizukam/DVJets/mvStudy/")
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
    outputFile = r.TFile("outputFiles/drPlots_{:0>2}_trackCleaning.root".format(outputTag), "RECREATE")
else:
    outputFile = r.TFile("outputFiles/drPlots_{:0>2}.root".format(outputTag), "RECREATE")

evtTotal = tree.GetEntries()
if (evtMax == -1):
    evtMax = evtTotal

ntrkList = ["Ntrk4", "Ntrk5", "Ntrk6", "Ntrk>6"]
# Output histograms
dr1SameDict = {}
dr2SameDict = {}
dr1MixedDict = {}
dr2MixedDict = {}
for ntrkBin in ntrkList:
    dr1SameDict[ntrkBin] = r.TH1D("dr1Same_"+ntrkBin, ";dR(jet,DV1)", 640, 0., 6.4)
    dr2SameDict[ntrkBin] = r.TH1D("dr2Same_"+ntrkBin, ";#Deltaz[mm]", 640, 0., 6.4)
    dr1MixedDict[ntrkBin] = r.TH1D("dr1Mixed_"+ntrkBin, ";Significance", 640, 0., 6.4)
    dr2MixedDict[ntrkBin] = r.TH1D("dr2Mixed_"+ntrkBin, ";#Deltaz[mm]", 640, 0., 6.4)

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
            
            mv = tracks1 + tracks2

            cJet = getClosestJet(dvs[idv], jets)
            dR_jetDV2 = cJet.DeltaR(tracks2)
            dR_jetDV1 = cJet.DeltaR(tracks1)

            sig = getSignificance(dv1, dv2, cov1, cov2)
            dist = getDistance(dv1, dv2)

            if (nTracks < 4):
                continue
            ntrkBin = getNtrkBin(nTracks)
            dr1SameDict[ntrkBin].Fill(dR_jetDV1)
            dr2SameDict[ntrkBin].Fill(dR_jetDV2)


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
            
            nTracks = nTracks1 + nTracks2

            mv = tracks1 + tracks2

            cJet = getClosestJet(dvs1[idv], jets)
            dR_jetDV2 = cJet.DeltaR(tracks2)
            dR_jetDV1 = cJet.DeltaR(tracks1)

            if (nTracks < 4):
                continue
            ntrkBin = getNtrkBin(nTracks)

            dr1MixedDict[ntrkBin].Fill(dR_jetDV1)
            dr2MixedDict[ntrkBin].Fill(dR_jetDV2)


            
outputFile.Write()
outputFile.Close()
