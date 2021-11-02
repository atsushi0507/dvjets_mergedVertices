import ROOT as r
import math
from glob import glob
import os
from collections import Counter
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-sr", "--SR", required=True, help="Signal region, 'HighPtSR' or 'TracklessSR'")
parser.add_argument("-tag", required=True, help="The campaign tag, 'a', 'd', or 'e'")
parser.add_argument("-n", "--nEvents", default=-1, help="Set maximum number of events to process")
parser.add_argument("-sf", "--suffix", default="", help="File suffix if needed")
parser.add_argument("-s", "--slimmed", action="store_true", help="Use skimmed files")
parser.add_argument("-w", "--weight", action="store_true", help="Apply event weight")
parser.add_argument("-na", "--noAttached", action="store_true", help="Not use attached track")
parser.add_argument("--noEvtSel", action="store_true", help="Not apply event selection")
args = parser.parse_args()

outputTag = "mc16{}".format(args.tag)
SR = args.SR
evtMax = int(args.nEvents)
suffix = args.suffix
useSkimmed = args.slimmed
doWeight = args.weight
noEvtSel = args.noEvtSel
noAttached = args.noAttached

if (noEvtSel or doWeight):
    useSkimmed = False

if not (suffix == "" or suffix == "selectedCut" or suffix == "fullSelection"):
    print(">> suffix only allow 'selectedCut' or 'fullSelection', or blank")
    print(">> Exit...")
    exit()

if (outputTag == "mc16a"):
    dataDir = "user.gripelli.mc16_13TeV.361024.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ4W.210618_dijetMC16a_trees.root"
    lumi = 32988.1 + 3218.56
    xs = 254630.0 * 5.3137e-4 * 1
    sumOfWeights = 990000 # Sum of weights: 25110544.1279
elif (outputTag == "mc16d"):
    dataDir = "user.gripelli.mc16_13TeV.361024.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ4W.210618_dijetMC16d_trees.root"
    lumi = 44307.4
    xs = 254630.0 * 5.3137e-4 * 1
    sumOfWeights = 1000000 # Sum of weights: 25326409.913
    if (useSkimmed):
        dataDir = "skimmed/mc16d/"
elif (outputTag == "mc16e"):
    dataDir = "user.gripelli.mc16_13TeV.364704.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ4WithSW.210618_dijetMC16e_trees.root"
    lumi = 58450.1
    xs = 254610.0 * 1.3366e-2 * 1
    sumOfWeights = 2.89897496062 # Raw count: 13000200
    if (useSkimmed):
        dataDir = "skimmed/mc16e/"

dataPath = "/Volumes/LaCie/DVJets/mc/dijets/"
dataSet = dataPath + dataDir
fileNames = glob(dataSet + "/*.root")

tree = r.TChain("trees_SRDV_")
for fileName in fileNames:
    tree.Add(fileName)

evtTotal = tree.GetEntries()
if evtMax == -1:
    evtMax = evtTotal

lumiWeight = (lumi * xs) / sumOfWeights

mergedVertices = []
print("Will process {} events out of {}".format(evtMax, evtTotal))
evtCounter = 0
for event in tree:
    evtCounter += 1
    if (evtCounter > evtMax):
        break
    if evtCounter % 10000 == 0:
        print("Processed {}/{}".format(evtCounter, evtMax))

    if not (noEvtSel):
        if (not ord(event.DRAW_pass_triggerFlags)):
            continue
        if (not ord(event.DRAW_pass_DVJETS)):
            continue
        if (SR == "HighPtSR"):
            if (not ord(event.BaselineSel_HighPtSR)):
                continue
        if (SR == "TracklessSR"):
            if (not ord(event.BaselineSel_TracklessSR)):
                continue

    # Create dictionaries that will hold the properties of all the DVs in the event
    eventWeightDict = {}
    
    dvNtrkDict = {}
    dvMassDict = {}
    dvRadiusDict = {}

    dvPassFiducialCutDict = {}
    dvPassDistCutDict = {}
    dvPassChi2CutDict = {}
    dvPassMaterialVetoDict = {}
    dvPassMaterialVeto_strictDict = {}

    dvDeltaRMaxDict = {}
    dvFourVectorDict = {}
    dvTypeDict = {}
    dvTrkPtDict = {}
    dvTrkFourVectorDict = {}
    dvTrkPdgIdDict = {}
    dvTrkBarcodeDict = {}
    dvTrkTMDict = {}
    dvBarcodeDict = {}
    dvPdgIdDict = {}
    dvPdgIdIsNotDefinedDict = {}
    dvTrkParentBarcodeDict = {}
    dvTrkParentPdgIdDict = {}
    dvTrkTruthDistDict = {}
    dvTrkTruthDistSigDict = {}
    dvXDict = {}
    dvYDict = {}
    dvZDict = {}
    dvVarXDict = {}
    dvVarYDict = {}
    dvVarZDict = {}
    dvTrkTruthXDict = {}
    dvTrkTruthYDict = {}
    dvTrkTruthZDict = {}
    dvTrkParentInfoDict = {}
    # For MV reduction factor
    dvTrkHasHIParentDict = {}
    dvTrkPtWrtDVDict = {}
    dvTrkEtaWrtDVDict = {}
    dvTrkPhiWrtDVDict = {}
    dvTrkMDict = {}
    dvTrkIsAssoDict = {}
    dvTrkRadFirstHitDict = {}
    dvTrk_pvdvVectorAngleDict = {}
    dvTrk_passTCDict = {}

    dvParentDict = {}
    dvtrack_d0sigDict = {}
    dvtrack_d0Dict = {}
    dvtrack_isAssociatedDict = {}

    # DV properties
    dvChiSqDict = {}

    for dvIndex in event.DV_index:
        if (doWeight):
            eventWeightDict[dvIndex] = lumiWeight * event.mcEventWeight
        else:
            eventWeightDict[dvIndex] = 1
        
        dvNtrkDict[dvIndex] = 0
        dvRadiusDict[dvIndex] = event.DV_rxy[dvIndex]

        dvPassFiducialCutDict[dvIndex] = event.DV_passFiducialCut[dvIndex]
        dvPassDistCutDict[dvIndex] = event.DV_passDistCut[dvIndex]
        dvPassChi2CutDict[dvIndex] = event.DV_passChiSqCut[dvIndex]
        dvPassMaterialVetoDict[dvIndex] = event.DV_passMaterialVeto[dvIndex]
        dvPassMaterialVeto_strictDict[dvIndex] = event.DV_passMaterialVeto_strict[dvIndex]

        dvChiSqDict[dvIndex] = event.DV_chisqPerDoF[dvIndex]

        dvFourVectorDict[dvIndex] = r.TLorentzVector()
        dvFourVectorDict[dvIndex].SetPtEtaPhiM(0, 0, 0, 0)
        dvTrkFourVectorDict[dvIndex] = []
        dvTrkPdgIdDict[dvIndex] = []
        dvTrkBarcodeDict[dvIndex] = []
        dvTrkTMDict[dvIndex] = []
        dvDeltaRMaxDict[dvIndex] = 0
        dvBarcodeDict[dvIndex] = 0
        dvPdgIdDict[dvIndex] = 0
        dvPdgIdIsNotDefinedDict[dvIndex] = False
        dvTrkParentBarcodeDict[dvIndex] = []
        dvTrkParentPdgIdDict[dvIndex] = []
        dvTrkTruthDistDict[dvIndex] = []
        dvTrkTruthDistSigDict[dvIndex] = []
        dvTrkTruthXDict[dvIndex] = []
        dvTrkTruthYDict[dvIndex] = []
        dvTrkTruthZDict[dvIndex] = []
        dvTrkParentInfoDict[dvIndex] = []
        dvTrkHasHIParentDict[dvIndex] = []
        dvTrkPtWrtDVDict[dvIndex] = []
        dvTrkEtaWrtDVDict[dvIndex] = []
        dvTrkPhiWrtDVDict[dvIndex] = []
        dvTrkMDict[dvIndex] = []
        dvTrkIsAssoDict[dvIndex] = []
        dvTrkRadFirstHitDict[dvIndex] = []
        dvTrk_pvdvVectorAngleDict[dvIndex] = []
        dvTrk_passTCDict[dvIndex] = []

        dvXDict[dvIndex]= event.DV_x[dvIndex]
        dvYDict[dvIndex]= event.DV_y[dvIndex]
        dvZDict[dvIndex]= event.DV_z[dvIndex]
        dvVarXDict[dvIndex] = event.DV_covariance0[dvIndex]
        dvVarYDict[dvIndex] = event.DV_covariance2[dvIndex]
        dvVarZDict[dvIndex] = event.DV_covariance5[dvIndex]

        dvParentDict[dvIndex] = []
        dvtrack_d0sigDict[dvIndex] = []
        dvtrack_d0Dict[dvIndex] = []

    # Loop over tracks and add them to the correct key in the dictionary based on their DV index
    trkCounter = 0
    for trkdvIndex in event.dvtrack_DVIndex:
        trkEta = event.dvtrack_etaWrtDV[trkCounter]
        trkPhi = event.dvtrack_phiWrtDV[trkCounter]
        trkM = event.dvtrack_m[trkCounter]
        trkPtWrtDV = event.dvtrack_ptWrtDV[trkCounter]
        #trkPt = event.dvtrack_pt[trkCounter]
        trkIsBackward = event.dvtrack_isBackwardsTrack[trkCounter]
        trkFailedExtrapolation = event.dvtrack_failedExtrapolation[trkCounter]
        passTrackCleaning = event.dvtrack_PassTrackCleaning[trkCounter]

        trk_d0 = r.TMath.Abs(event.dvtrack_d0[trkCounter])
        trk_d0sig = r.TMath.Abs(event.dvtrack_d0[trkCounter] / event.dvtrack_errd0[trkCounter])
        assoTrk = event.dvtrack_isAssociated[trkCounter]
        passPatternCheck = event.dvtrack_passpatternCheck[trkCounter]
        radFirstHit = event.dvtrack_RadFirstHit[trkCounter]
        trkIsTM = (event.dvtrack_hasValidTruthLink[trkCounter] and event.dvtrack_truthMatchProb[trkCounter] > 0.5)
        trkParentBarcode = event.dvtrack_truthParentBarcode[trkCounter]
        trkParentPdgId = event.dvtrack_truthParentPdgId[trkCounter]
        trkBarcode = event.dvtrack_truthBarcode[trkCounter]
        trkPdgId = event.dvtrack_truthPdgId[trkCounter]
        trkHasParentInfo = event.dvtrack_hasValidTruthParentInfo[trkCounter]

        trkdvX = dvXDict[trkdvIndex]
        trkdvY = dvYDict[trkdvIndex]
        trkdvZ = dvZDict[trkdvIndex]

        trkdvVarX = abs(dvVarXDict[trkdvIndex])
        trkdvVarY = abs(dvVarYDict[trkdvIndex])
        trkdvVarZ = abs(dvVarZDict[trkdvIndex])

        trkTruthX = event.dvtrack_truthVtxX[trkCounter]
        trkTruthY = event.dvtrack_truthVtxY[trkCounter]
        trkTruthZ = event.dvtrack_truthVtxZ[trkCounter]

        deltaX = trkTruthX - trkdvX
        deltaY = trkTruthY - trkdvY
        deltaZ = trkTruthZ - trkdvZ
        trkTruthDist = math.sqrt(deltaX**2 + deltaY**2 + deltaZ**2)
        trkTruthDistSig = math.sqrt(deltaX**2/trkdvVarX + deltaY**2/trkdvVarY + deltaZ**2/trkdvVarZ)

        if not (trkIsBackward or trkFailedExtrapolation):
            p4_track = r.TLorentzVector()
            p4_track.SetPtEtaPhiM(trkPtWrtDV,
                                  trkEta,
                                  trkPhi,
                                  trkM)
            dv = r.TVector3(event.DV_x[trkdvIndex], event.DV_y[trkdvIndex], event.DV_z[trkdvIndex])
            pv = r.TVector3(event.PV_x, event.PV_y, event.PV_z)
            dvTrk_pvdvVectorAngle = p4_track.Angle((dv-pv))

            dvTrkParentBarcodeDict[trkdvIndex].append(trkParentBarcode)
            dvTrkParentPdgIdDict[trkdvIndex].append(trkParentPdgId)
            dvTrkBarcodeDict[trkdvIndex].append(trkBarcode)
            dvTrkPdgIdDict[trkdvIndex].append(trkPdgId)
            dvTrkTMDict[trkdvIndex].append(trkIsTM)
            dvNtrkDict[trkdvIndex] += 1
            trkFourVector = r.TLorentzVector()
            trkFourVector.SetPtEtaPhiM(trkPtWrtDV, trkEta, trkPhi, trkM)
            dvFourVectorDict[trkdvIndex] += trkFourVector
            dvTrkFourVectorDict[trkdvIndex].append(trkFourVector)
            dvTrkTruthDistDict[trkdvIndex].append(trkTruthDist)
            dvTrkTruthDistSigDict[trkdvIndex].append(trkTruthDistSig)
            # MV study
            dvTrkPtWrtDVDict[trkdvIndex].append(trkPtWrtDV)
            dvTrkEtaWrtDVDict[trkdvIndex].append(trkEta)
            dvTrkPhiWrtDVDict[trkdvIndex].append(trkPhi)
            dvTrkMDict[trkdvIndex].append(trkM)
            dvTrkIsAssoDict[trkdvIndex].append(assoTrk)
            dvTrkRadFirstHitDict[trkdvIndex].append(radFirstHit)
            dvTrk_pvdvVectorAngleDict[trkdvIndex].append(dvTrk_pvdvVectorAngle)
            dvTrk_passTCDict[trkdvIndex].append(passTrackCleaning)
            
            dvTrkTruthXDict[trkdvIndex].append(trkTruthX)
            dvTrkTruthYDict[trkdvIndex].append(trkTruthY)
            dvTrkTruthZDict[trkdvIndex].append(trkTruthZ)
            dvParentDict[trkdvIndex].append((trkParentPdgId, trkParentBarcode))
            dvTrkParentInfoDict[trkdvIndex].append(trkHasParentInfo)
            dvtrack_d0sigDict[trkdvIndex].append(trk_d0sig)
            dvtrack_d0Dict[trkdvIndex].append(trk_d0)

        trkCounter += 1

    # Compute number of DVs in the event
    nDVs = 0
    for dvIndex in event.DV_index:
        if dvNtrkDict[dvIndex] > 1:
            nDVs += 1

    # Compute DV variables
    for dvIndex in event.DV_index:
        if dvNtrkDict[dvIndex] < 2:
            continue
        
        dvMassDict[dvIndex] = dvFourVectorDict[dvIndex].M()

        # For MV
        parentCounter = Counter(dvParentDict[dvIndex])
        parentList = set(dvParentDict[dvIndex])
        nParent = len(parentList)
        nTracks = dvNtrkDict[dvIndex]

        dvContainsG4Tracks = False
        dvContainsPileupTracks = False
        dvContainsGeneratorTracks = False

        # Figure out deltaRmax and truth matching
        trkCounter = 0
        for trkFourVector in dvTrkFourVectorDict[dvIndex]:
            dvFourVectorWithoutTrack = dvFourVectorDict[dvIndex] - trkFourVector
            deltaR = dvFourVectorWithoutTrack.DeltaR(trkFourVector)

            if deltaR > dvDeltaRMaxDict[dvIndex]:
                dvDeltaRMaxDict[dvIndex] = deltaR
            if not dvTrkTMDict[dvIndex][trkCounter]:
                dvContainsPileupTracks = True
                dvPdgIdIsNotDefinedDict[dvIndex] = True
            else:
                if dvTrkBarcodeDict[dvIndex][trkCounter] > 200000:
                    dvContainsG4Tracks = True
                else:
                    dvContainsGeneratorTracks = True
                trkParentPdgId = dvTrkParentPdgIdDict[dvIndex][trkCounter]
                trkParentBarcode = dvTrkParentBarcodeDict[dvIndex][trkCounter]            

                if (dvPdgIdDict[dvIndex] != trkParentPdgId or dvBarcodeDict[dvIndex] != trkParentBarcode) and (dvPdgIdDict[dvIndex] != 0 and dvBarcodeDict[dvIndex] != 0):
                    dvPdgIdIsNotDefinedDict[dvIndex] = True
                dvPdgIdDict[dvIndex] = trkParentPdgId
                dvBarcodeDict[dvIndex] = trkParentBarcode
            hasHIParent = True if (trkParentPdgId in [211, 2212, -211, -2212]) else False
            dvTrkHasHIParentDict[dvIndex].append(hasHIParent)
            trkCounter += 1

        # DV types: 1=G4, 2=G4withPU, 3=G4withGen , 4=PU, 5=PUwithGen, 6=Gen, 7=Unknown
        dvTypeDict[dvIndex] = 7
        if (dvContainsG4Tracks and not dvContainsPileupTracks and not dvContainsGeneratorTracks):
            dvTypeDict[dvIndex] = 1
        elif (dvContainsG4Tracks and dvContainsPileupTracks and not dvContainsGeneratorTracks):
            dvTypeDict[dvIndex] = 2
        elif (dvContainsG4Tracks and not dvContainsPileupTracks and dvContainsGeneratorTracks):
            dvTypeDict[dvIndex] = 3
        elif (dvContainsPileupTracks and not dvContainsG4Tracks and not dvContainsGeneratorTracks):
            dvTypeDict[dvIndex] = 4
        elif (dvContainsPileupTracks and not dvContainsG4Tracks and dvContainsGeneratorTracks):
            dvTypeDict[dvIndex] = 5
        elif (dvContainsGeneratorTracks and not dvContainsG4Tracks and not dvContainsPileupTracks):
            dvTypeDict[dvIndex] = 6
                

        # Figure out the truth particle distance from DV
        varX = abs(dvVarXDict[dvIndex])
        varY = abs(dvVarYDict[dvIndex])
        varZ = abs(dvVarZDict[dvIndex])
        dvInterTruthParticleDist = []
        dvInterTruthParticleDistSig = []
        hasUnrelatedTrack = any(ntrk[1] == 1 for ntrk in parentCounter.most_common())
        nChildren = [ntrk[1] for ntrk in parentCounter.most_common()]
        childCounter = Counter(nChildren)

        for track1 in range(len(dvTrkTruthXDict[dvIndex])):
            for track2 in range(len(dvTrkTruthXDict[dvIndex])):
                dx = dvTrkTruthXDict[dvIndex][track1] - dvTrkTruthXDict[dvIndex][track2]
                dy = dvTrkTruthYDict[dvIndex][track1] - dvTrkTruthYDict[dvIndex][track2]
                dz = dvTrkTruthZDict[dvIndex][track1] - dvTrkTruthZDict[dvIndex][track2]
                dist = math.sqrt(dx**2 + dy**2 + dz**2)
                distSig = math.sqrt(dx**2/varX + dy**2/varY + dz**2/varZ)
                dvInterTruthParticleDist.append(dist)
                dvInterTruthParticleDistSig.append(distSig)

        if (nParent > 1 or (dvTypeDict[dvIndex] == 4 and nParent > 0)):
        #if (nParent > 1):
            if (not hasUnrelatedTrack):
                trk = []
                for itrack in range(dvNtrkDict[dvIndex]):
                    hasHI = True if any(dvTrkHasHIParentDict[dvIndex]) else False
                    trk.append([dvTrkPtWrtDVDict[dvIndex][itrack],
                                dvTrkEtaWrtDVDict[dvIndex][itrack],
                                dvTrkPhiWrtDVDict[dvIndex][itrack],
                                dvTrkMDict[dvIndex][itrack],
                                dvTrkIsAssoDict[dvIndex][itrack],
                                dvTrkRadFirstHitDict[dvIndex][itrack],
                                dvTrk_pvdvVectorAngleDict[dvIndex][itrack],
                                dvtrack_d0sigDict[dvIndex][itrack],
                                dvTrk_passTCDict[dvIndex][itrack],
                                dvTrkParentPdgIdDict[dvIndex][itrack],
                                dvTrkParentBarcodeDict[dvIndex][itrack],
                                dvtrack_d0Dict[dvIndex][itrack]
                                ])
                mergedVertices.append([nParent,
                                       nTracks,
                                       dvMassDict[dvIndex],
                                       dvTypeDict[dvIndex],
                                       dvPassFiducialCutDict[dvIndex],
                                       dvPassDistCutDict[dvIndex],
                                       dvPassChi2CutDict[dvIndex],
                                       dvPassMaterialVetoDict[dvIndex],
                                       dvPassMaterialVeto_strictDict[dvIndex],
                                       dvRadiusDict[dvIndex],
                                       trk,
                                       hasHI,
                                       eventWeightDict[dvIndex],
                                       dvChiSqDict[dvIndex],
                                       dvXDict[dvIndex],
                                       dvYDict[dvIndex],
                                       dvZDict[dvIndex]
                                       ])

outputName = "extractFactor_{}_{}_{}".format(outputTag, SR, suffix) if (suffix != "") else "extractFactor_{}_{}".format(outputTag, SR)
if (noEvtSel):
    outputName += "_noEvtSel"
if (noAttached):
    outputName += "_noAttached"
if (doWeight):
    outputName += "_weighted.root"
else:
    outputName += ".root"
outputFile = r.TFile("outputFiles/"+outputName, "RECREATE")
ntrkList = ["Ntrk4", "Ntrk5", "Ntrk6", "Ntrk>6"]
h_mvMassDict = {}
h_mvMassDict_DVSel = {}
h_mvMassDict_passFiducial = {}
h_mvMassDict_passDist = {}
h_mvMassDict_passChiSq = {}
h_mvMassDict_passMaterial = {}
h_mvMassDict_passMaterial_strict = {}
h_mvMassDict_upstream = {}
h_mvMassDict_allPtSel = {}
h_mvMassDict_ptOutsideBP = {}
h_mvMassDict_ptOutsidePixel = {}
h_mvMassDict_d0InsideBP = {}
h_mvMassDict_d0InsidePixel = {}
h_mvMassDict_d0Selected = {}
h_mvMassDict_angle = {}
h_mvMassDict_lowPtForward = {}
h_mvMassDict_passTC = {}
h_mvMassDict_fullSel = {}
h_mvMassDict_ptSel = {}
h_mvMassDict_d0Sel = {}
h_mvMassDict_angleForward = {}
h_mvMassDict_attachedPt = {}
h_mvMassDict_exceptAllPt = {}
h_mvMassDict_trackCleaning = {}
h_mvMassDict_allPtSelAndPtOutsideBP = {}
h_mvMassDict_allPtSel_1p2GeV = {}
h_mvMassDict_allPtSel_1p4GeV = {}
h_mvMassDict_allPtSel_1p6GeV = {}
h_mvMassDict_allPtSel_1p8GeV = {}
h_mvMassDict_orig = {}
h_mvMassDict_DVSel_orig = {}
h_mvMassDict_upstream_orig = {}
h_mvMassDict_allPtSel_orig = {}
h_mvMassDict_ptOutsideBP_orig = {}
h_mvMassDict_ptOutsidePixel_orig = {}
h_mvMassDict_d0InsideBP_orig = {}
h_mvMassDict_d0InsidePixel_orig = {}
h_mvMassDict_d0Selected_orig = {}
h_mvMassDict_angle_orig = {}
h_mvMassDict_lowPtForward_orig = {}
h_mvMassDict_passTC_orig = {}
h_mvMassDict_fullSel_orig = {}
h_mvMassDict_ptSel_orig = {}
h_mvMassDict_d0Sel_orig = {}
h_mvMassDict_angleForward_orig = {}
h_mvMassDict_attachedPt_orig = {}
h_mvMassDict_exceptAllPt_orig = {}
h_mvMassDict_trackCleaning_orig = {}
h_mvMassDict_allPtSelAndPtOutsideBP_orig = {}
h_mvMassDict_allPtSel_1p2GeV_orig = {}
h_mvMassDict_allPtSel_1p4GeV_orig = {}
h_mvMassDict_allPtSel_1p6GeV_orig = {}
h_mvMassDict_allPtSel_1p8GeV_orig = {}
h_mvMassDict_passFiducial_orig = {}
h_mvMassDict_passDist_orig = {}
h_mvMassDict_passChiSq_orig = {}
h_mvMassDict_passMaterial_orig = {}
h_mvMassDict_passMaterial_strict_orig = {}

for ntrk in ntrkList:
    h_mvMassDict[ntrk] = r.TH1D("mvMass_"+ntrk, ";m_{DV} [GeV]", 1000, 0., 100.)
    h_mvMassDict_DVSel[ntrk] = r.TH1D("mvMass_DVSel_"+ntrk, ";m_{DV} [GeV]", 1000, 0., 100.)
    h_mvMassDict_upstream[ntrk] = r.TH1D("mvMass_upstreamHitVeto_"+ntrk, ";m_{DV} [GeV]", 1000, 0., 100.)
    h_mvMassDict_allPtSel[ntrk] = r.TH1D("mvMass_allPtSel_"+ntrk, ";m_{DV} [GeV]", 1000, 0., 100.)
    h_mvMassDict_ptOutsideBP[ntrk] = r.TH1D("mvMass_ptOutsideBP_"+ntrk, ";m_{DV} [GeV]", 1000, 0., 100.)
    h_mvMassDict_ptOutsidePixel[ntrk] = r.TH1D("mvMass_ptOutsidePixel_"+ntrk, ";m_{DV} [GeV]", 1000, 0., 100.)
    h_mvMassDict_d0InsideBP[ntrk] = r.TH1D("mvMass_d0InsideBP_"+ntrk, ";m_{DV} [GeV]", 1000, 0., 100.)
    h_mvMassDict_d0InsidePixel[ntrk] = r.TH1D("mvMass_d0InsidePixel_"+ntrk, ";m_{DV} [GeV]", 1000, 0., 100.)
    h_mvMassDict_d0Selected[ntrk] = r.TH1D("mvMass_d0Selected_"+ntrk, ";m_{DV} [GeV]", 1000, 0., 100.)
    h_mvMassDict_angle[ntrk] = r.TH1D("mvMass_angle_"+ntrk, ";m_{DV} [GeV]", 1000, 0., 100.)
    h_mvMassDict_lowPtForward[ntrk] = r.TH1D("mvMass_lowPtForward_"+ntrk, ";m_{DV} [GeV]", 1000, 0., 100.)
    h_mvMassDict_passTC[ntrk] = r.TH1D("mvMass_passTC_"+ntrk, ";m_{DV} [GeV]", 1000, 0., 100.)
    h_mvMassDict_fullSel[ntrk] = r.TH1D("mvMass_fullSel_"+ntrk, ";m_{DV} [GeV]", 1000, 0., 100.)
    h_mvMassDict_ptSel[ntrk] = r.TH1D("mvMass_ptSel_"+ntrk, ";m_{DV} [GeV]", 1000, 0., 100.)
    h_mvMassDict_d0Sel[ntrk] = r.TH1D("mvMass_d0Sel_"+ntrk, ";m_{DV} [GeV]", 1000, 0., 100.)
    h_mvMassDict_angleForward[ntrk] = r.TH1D("mvMass_angleForward_"+ntrk, ";m_{DV} [GeV]", 1000, 0., 100.)
    h_mvMassDict_attachedPt[ntrk] = r.TH1D("mvMass_attachedPt_"+ntrk, ";m_{DV} [GeV]", 1000, 0., 100.)
    h_mvMassDict_exceptAllPt[ntrk] = r.TH1D("mvMass_exceptAllPt_"+ntrk, ";m_{DV} [GeV]", 1000, 0., 100.)
    h_mvMassDict_trackCleaning[ntrk] = r.TH1D("mvMass_trackCleaning_"+ntrk, ";m_{DV} [GeV]", 1000, 0., 100.)
    h_mvMassDict_allPtSelAndPtOutsideBP[ntrk] = r.TH1D("mvMass_allPtSelAndPtOutsideBP_"+ntrk, ";m_{DV} [GeV]", 1000, 0., 100.)
    h_mvMassDict_allPtSel_1p2GeV[ntrk] = r.TH1D("mvMass_allPtSel_1p2GeV_"+ntrk, ";m_{DV} [GeV]", 1000, 0., 100.)
    h_mvMassDict_allPtSel_1p4GeV[ntrk] = r.TH1D("mvMass_allPtSel_1p4GeV_"+ntrk, ";m_{DV} [GeV]", 1000, 0., 100.)
    h_mvMassDict_allPtSel_1p6GeV[ntrk] = r.TH1D("mvMass_allPtSel_1p6GeV_"+ntrk, ";m_{DV} [GeV]", 1000, 0., 100.)
    h_mvMassDict_allPtSel_1p8GeV[ntrk] = r.TH1D("mvMass_allPtSel_1p8GeV_"+ntrk, ";m_{DV} [GeV]", 1000, 0., 100.)
    h_mvMassDict_passFiducial[ntrk] = r.TH1D("mvMass_passFiducial_"+ntrk, ";m_{DV} [GeV]", 1000, 0., 100.)
    h_mvMassDict_passDist[ntrk] = r.TH1D("mvMass_passDist_"+ntrk, ";m_{DV} [GeV]", 1000, 0., 100.)
    h_mvMassDict_passChiSq[ntrk] = r.TH1D("mvMass_passChiSq_"+ntrk, ";m_{DV} [GeV]", 1000, 0., 100.)
    h_mvMassDict_passMaterial[ntrk] = r.TH1D("mvMass_passMaterial_"+ntrk, ";m_{DV} [GeV]", 1000, 0., 100.)
    h_mvMassDict_passMaterial_strict[ntrk] = r.TH1D("mvMass_passMaterial_strict_"+ntrk, ";m_{DV} [GeV]", 1000, 0., 100.)
   
    h_mvMassDict_orig[ntrk] = r.TH1D("mvMass_orig_"+ntrk, ";m_{DV} [GeV]", 1000, 0., 100.)
    h_mvMassDict_DVSel_orig[ntrk] = r.TH1D("mvMass_DVSel_orig_"+ntrk, ";m_{DV} [GeV]", 1000, 0., 100.)
    h_mvMassDict_upstream_orig[ntrk] = r.TH1D("mvMass_upstreamHitVeto_orig_"+ntrk, ";m_{DV} [GeV]", 1000, 0., 100.)
    h_mvMassDict_allPtSel_orig[ntrk] = r.TH1D("mvMass_allPtSel_orig_"+ntrk, ";m_{DV} [GeV]", 1000, 0., 100.)
    h_mvMassDict_ptOutsideBP_orig[ntrk] = r.TH1D("mvMass_ptOutsideBP_orig_"+ntrk, ";m_{DV} [GeV]", 1000, 0., 100.)
    h_mvMassDict_ptOutsidePixel_orig[ntrk] = r.TH1D("mvMass_ptOutsidePixel_orig_"+ntrk, ";m_{DV} [GeV]", 1000, 0., 100.)
    h_mvMassDict_d0InsideBP_orig[ntrk] = r.TH1D("mvMass_d0InsideBP_orig_"+ntrk, ";m_{DV} [GeV]", 1000, 0., 100.)
    h_mvMassDict_d0InsidePixel_orig[ntrk] = r.TH1D("mvMass_d0InsidePixel_orig_"+ntrk, ";m_{DV} [GeV]", 1000, 0., 100.)
    h_mvMassDict_d0Selected_orig[ntrk] = r.TH1D("mvMass_d0Selected_orig_"+ntrk, ";m_{DV} [GeV]", 1000, 0., 100.)
    h_mvMassDict_angle_orig[ntrk] = r.TH1D("mvMass_angle_orig_"+ntrk, ";m_{DV} [GeV]", 1000, 0., 100.)
    h_mvMassDict_lowPtForward_orig[ntrk] = r.TH1D("mvMass_lowPtForward_orig_"+ntrk, ";m_{DV} [GeV]", 1000, 0., 100.)
    h_mvMassDict_passTC_orig[ntrk] = r.TH1D("mvMass_passTC_orig_"+ntrk, ";m_{DV} [GeV]", 1000, 0., 100.)
    h_mvMassDict_fullSel_orig[ntrk] = r.TH1D("mvMass_fullSel_orig_"+ntrk, ";m_{DV} [GeV]", 1000, 0., 100.)
    h_mvMassDict_ptSel_orig[ntrk] = r.TH1D("mvMass_ptSel_orig_"+ntrk, ";m_{DV} [GeV]", 1000, 0., 100.)
    h_mvMassDict_d0Sel_orig[ntrk] = r.TH1D("mvMass_d0Sel_orig_"+ntrk, ";m_{DV} [GeV]", 1000, 0., 100.)
    h_mvMassDict_angleForward_orig[ntrk] = r.TH1D("mvMass_angleForward_orig_"+ntrk, ";m_{DV} [GeV]", 1000, 0., 100.)
    h_mvMassDict_attachedPt_orig[ntrk] = r.TH1D("mvMass_attachedPt_orig_"+ntrk, ";m_{DV} [GeV]", 1000, 0., 100.)
    h_mvMassDict_exceptAllPt_orig[ntrk] = r.TH1D("mvMass_exceptAllPt_orig_"+ntrk, ";m_{DV} [GeV]", 1000, 0., 100.)
    h_mvMassDict_trackCleaning_orig[ntrk] = r.TH1D("mvMass_trackCleaning_orig_"+ntrk, ";m_{DV} [GeV]", 1000, 0., 100.)
    h_mvMassDict_allPtSelAndPtOutsideBP_orig[ntrk] = r.TH1D("mvMass_allPtSelAndPtOutsideBP_orig_"+ntrk, ";m_{DV} [GeV]", 1000, 0., 100.)
    h_mvMassDict_allPtSel_1p2GeV_orig[ntrk] = r.TH1D("mvMass_allPtSel_1p2GeV_orig_"+ntrk, ";m_{DV} [GeV]", 1000, 0., 100.)
    h_mvMassDict_allPtSel_1p4GeV_orig[ntrk] = r.TH1D("mvMass_allPtSel_1p4GeV_orig_"+ntrk, ";m_{DV} [GeV]", 1000, 0., 100.)
    h_mvMassDict_allPtSel_1p6GeV_orig[ntrk] = r.TH1D("mvMass_allPtSel_1p6GeV_orig_"+ntrk, ";m_{DV} [GeV]", 1000, 0., 100.)
    h_mvMassDict_allPtSel_1p8GeV_orig[ntrk] = r.TH1D("mvMass_allPtSel_1p8GeV_orig_"+ntrk, ";m_{DV} [GeV]", 1000, 0., 100.)
    h_mvMassDict_passFiducial_orig[ntrk] = r.TH1D("mvMass_passFiducial_orig_"+ntrk, ";m_{DV} [GeV]", 1000, 0., 100.)
    h_mvMassDict_passDist_orig[ntrk] = r.TH1D("mvMass_passDist_orig_"+ntrk, ";m_{DV} [GeV]", 1000, 0., 100.)
    h_mvMassDict_passChiSq_orig[ntrk] = r.TH1D("mvMass_passChiSq_orig_"+ntrk, ";m_{DV} [GeV]", 1000, 0., 100.)
    h_mvMassDict_passMaterial_orig[ntrk] = r.TH1D("mvMass_passMaterial_orig_"+ntrk, ";m_{DV} [GeV]", 1000, 0., 100.)
    h_mvMassDict_passMaterial_strict_orig[ntrk] = r.TH1D("mvMass_passMaterial_strict_orig_"+ntrk, ";m_{DV} [GeV]", 1000, 0., 100.)

def getNtrkBin(nTracks):
    ntrkBin = ""
    if nTracks == 4:
        ntrkBin = "Ntrk4"
    elif nTracks == 5:
        ntrkBin = "Ntrk5"
    elif nTracks == 6:
        ntrkBin = "Ntrk6"
    elif nTracks > 6:
        ntrkBin = "Ntrk>6"
    return ntrkBin

def cleaning(mergedVertices, selection, hist, hist_orig):
    ntrkList = ["Ntrk4", "Ntrk5", "Ntrk6", "Ntrk>6"]
    typeList = [1, 2, 3, 4, 5, 6, 7]
    h_mvtrack_nAttached = {}
    h_mvtrack_allPtSel ={}
    h_mvtrack_ptOutsideBP = {}
    h_mvtrack_ptOutsidePixel = {}
    h_mvtrack_d0InsideBP = {}
    h_mvtrack_d0InsidePixel = {}
    h_mvtrack_d0Selected = {}
    h_mvtrack_angle = {}
    h_mvtrack_lowPtForward = {}
    h_nAttached_vs_dvType = {}
    h_mvtrack_d0_selected = {}
    h_mvtrack_d0_attached = {}
    h_mvtrack_d0_all = {}
    h_mvtrack_d0sig = {}
    h_mvMass_dvType = {}
    h_mvChiSq_dvType = {}
    h_mvRxy_dvType = {}
    h_mvZ_dvType = {}
    for ntrk in ntrkList:
        h_mvtrack_nAttached[ntrk] = r.TH1I("mvtrack_nAttached_"+ntrk+"_"+selection, ";nAttached", 6, 0, 6)
        h_mvtrack_allPtSel[ntrk] = r.TH1D("mvtrack_allPtSel_"+ntrk+"_"+selection, ";p_{T} [GeV]", 250, 0., 25.)
        h_mvtrack_ptOutsideBP[ntrk] = r.TH1D("mvtrack_ptOutsideBP_"+ntrk+"_"+selection, ";p_{T} [GeV]", 250, 0., 25.)
        h_mvtrack_ptOutsidePixel[ntrk] = r.TH1D("mvtrack_ptOutsidePixel_"+ntrk+"_"+selection, ";p_{T} [GeV]", 250, 0., 25.)
        h_mvtrack_d0InsideBP[ntrk] = r.TH1D("mvtrack_d0InsideBP_"+ntrk+"_"+selection, ";d0-significance", 100, 0., 100.)
        h_mvtrack_d0InsidePixel[ntrk] = r.TH1D("mvtrack_d0InsidePixel_"+ntrk+"_"+selection, ";d0-significance", 100, 0., 100.)
        h_mvtrack_d0Selected[ntrk] = r.TH1D("mvtrack_d0Selected_"+ntrk+"_"+selection, ";d0-significance", 100, 0., 100.)
        h_mvtrack_angle[ntrk] = r.TH1D("mvtrack_angle_"+ntrk+"_"+selection, ";angle", 320, 0., 3.2)
        h_mvtrack_lowPtForward[ntrk] = r.TH1D("mvtrack_lowPtForward_"+ntrk+"_"+selection, ";p_{T} [GeV]", 250, 0., 25.)
        h_nAttached_vs_dvType[ntrk] = r.TH2D("nAttached_vs_dvType_"+ntrk+"_"+selection, ";nAttached;dvType", 6, 0, 6, 6, 1, 7)
        h_mvtrack_d0_selected[ntrk] = r.TH1D("mvtrack_d0_selected_"+ntrk+"_"+selection, ";d0 [mm]", 250, 0., 25.)
        h_mvtrack_d0_attached[ntrk] = r.TH1D("mvtrack_d0_attached_"+ntrk+"_"+selection, ";d0 [mm]", 250, 0., 25.)
        h_mvtrack_d0_all[ntrk] = r.TH1D("mvtrack_d0_all_"+ntrk+"_"+selection, ";d0 [mm]", 250, 0., 250.)
        h_mvtrack_d0sig[ntrk] = r.TH1D("mvtrack_d0sig_"+ntrk+"_"+selection, ";d0-sig", 100, 0., 100.)
        h_mvMass_dvType[ntrk] = {}
        h_mvChiSq_dvType[ntrk] = {}
        h_mvRxy_dvType[ntrk] = {}
        h_mvZ_dvType[ntrk] = {}
        for dvtype in typeList:
            h_mvMass_dvType[ntrk][dvtype] = r.TH1D("mvMass_dvType{}_{}_{}".format(dvtype, ntrk, selection), ";m_{DV} [GeV]", 1000, 0., 100.)
            h_mvChiSq_dvType[ntrk][dvtype] = r.TH1D("mvChiSq_dvType{}_{}_{}".format(dvtype, ntrk, selection), ";#chi^{2}/n_{DoF}", 1000, 0., 100.)
            h_mvRxy_dvType[ntrk][dvtype] = r.TH1D("mvRxy_dvType{}_{}_{}".format(dvtype, ntrk, selection), ";R_{xy} [mm]", 3000, 0., 300.)
            h_mvZ_dvType[ntrk][dvtype] = r.TH1D("mvZ_dvType{}_{}_{}".format(dvtype, ntrk, selection), ";z [mm]", 600, -300., 300.)
        
    for mv in mergedVertices:
        nParent = mv[0]
        nTracks = mv[1]
        dvMass = mv[2]
        dvType = mv[3]
        DV_passFiducialCut = mv[4]
        DV_passDistCut = mv[5]
        DV_passChiSqCut = mv[6]
        DV_passMaterialVeto = mv[7]
        DV_passMaterialVeto_strict = mv[8]
        DV_rxy = mv[9]
        dvtracks = mv[10]
        hasHI = mv[11]
        weight = mv[12]
        chisq = mv[13]
        x = mv[14]
        y = mv[15]
        z = mv[16]
        rxy = r.TMath.Sqrt(x*x + y*y)
        passDVSel = True if (DV_passFiducialCut and DV_passDistCut and DV_passChiSqCut and DV_passMaterialVeto and DV_passMaterialVeto_strict) else False

        if (selection == ("DVSel" or "fullSel") and not passDVSel):
            continue
        if (selection == "passFiducial" and not DV_passFiducialCut):
            continue
        if (selection == "passDist" and not DV_passDistCut):
            continue
        if (selection == "passChiSq" and not DV_passChiSqCut):
            continue
        if (selection == "passMaterial" and not DV_passMaterialVeto):
            continue
        if (selection == "passMaterial_strict" and not DV_passMaterialVeto_strict):
            continue
        nSelected = 0
        nSelected_larged0 = 0
        nAttached = 0
        for dvtrack in dvtracks:
            isAssociated = dvtrack[4]
            d0sig = dvtrack[7]
            d0 = dvtrack[11]
            if (noAttached and isAssociated):
                continue
            if (not isAssociated):
                nSelected += 1
                if (d0 > 2.):
                    nSelected_larged0 += 1
            else:
                nAttached += 1
        nTrks = nSelected + nAttached

        if (suffix == "selectedCut" or suffix == "fullSelection"):
            if (nSelected < 4):
                continue
            if (suffix == "fullSelection" and nSelected_larged0 < 2):
                continue
                
        merged = r.TLorentzVector()
        nTrks_orig = 0
        #nTrks = 0
        nAttached = 0
        for dvtrack in dvtracks:
            dvtrack_pt = dvtrack[0]
            dvtrack_eta = dvtrack[1]
            dvtrack_phi = dvtrack[2]
            dvtrack_m = dvtrack[3]
            isAssociated = dvtrack[4]
            firstHit = dvtrack[5]
            angle = dvtrack[6]
            d0sig = dvtrack[7]
            passTC = dvtrack[8]
            parentPdgId = dvtrack[9]
            parentBarcode = dvtrack[10]
            d0 = dvtrack[11]

            if (noAttached and isAssociated):
                continue

            selList = {"noSel": "",
                       "DVSel": not passDVSel,
                       "passFiducial": not DV_passFiducialCut,
                       "passDist": not DV_passDistCut,
                       "passChiSq": not DV_passChiSqCut,
                       "passMaterial": not DV_passMaterialVeto,
                       "passMaterial_strict": not DV_passMaterialVeto_strict,
                       "upstreamHitVeto": firstHit < DV_rxy,
                       "allPtSel": dvtrack_pt < 2.,
                       "ptOutsideBP": DV_rxy > 25 and isAssociated and dvtrack_pt < 3.,
                       "ptOutsidePixel": DV_rxy > 145 and isAssociated and dvtrack_pt < 4.,
                       "d0InsideBP": DV_rxy < 25 and d0sig < 10.,
                       "d0InsidePixel": DV_rxy < 145 and isAssociated and d0sig < 15.,
                       "d0Selected": DV_rxy > 145 and not isAssociated and d0sig < 10.,
                       "angle": isAssociated and angle > r.TMath.Pi()/2.,
                       "lowPtForward": DV_rxy > 25 and angle < 0.2 and dvtrack_pt < 4.,
                       "passTC": not passTC,
                       "fullSel": not (passDVSel and passTC),
                       "1p2": dvtrack_pt < 1.2,
                       "1p4": dvtrack_pt < 1.4,
                       "1p6": dvtrack_pt < 1.6,
                       "1p8": dvtrack_pt < 1.8
                       }
            selList["ptSel"] = (selList["allPtSel"] or selList["ptOutsideBP"] or selList["ptOutsidePixel"])
            selList["d0Sel"] = (selList["d0InsideBP"] or selList["d0InsidePixel"] or selList["d0Selected"])
            selList["angleForward"] = (selList["angle"] or selList["lowPtForward"])
            selList["attachedPt"] = (selList["ptOutsideBP"] or selList["ptOutsidePixel"])
            selList["exceptAllPt"] = (selList["d0Sel"] or selList["angleForward"] or selList["upstreamHitVeto"])
            selList["allPtSelAndPtOutsideBP"] = (selList["allPtSel"] or selList["ptOutsideBP"])
            selList["trackCleaning"] = (selList["upstreamHitVeto"] or selList["allPtSel"] or selList["ptOutsideBP"] or selList["ptOutsidePixel"]
                                        or selList["d0InsideBP"] or selList["d0InsidePixel"] or selList["d0Selected"] or selList["angle"] or selList["lowPtForward"])
            nTrks_orig += 1
            if (selection != "noSel" and selList[selection]):
                continue
           
            track = r.TLorentzVector()
            track.SetPtEtaPhiM(dvtrack_pt,
                               dvtrack_eta,
                               dvtrack_phi,
                               dvtrack_m
                               )
            merged += track
            #nTrks += 1
            if (isAssociated):
                nAttached += 1
            h_mvtrack_nAttached[getNtrkBin(nTrks)].Fill(nAttached)
            h_nAttached_vs_dvType[getNtrkBin(nTrks)].Fill(nAttached, dvType)

            h_mvtrack_d0_all[getNtrkBin(nTrks)].Fill(d0)
            if (isAssociated):
                h_mvtrack_d0_attached[getNtrkBin(nTrks)].Fill(d0)
            else:
                h_mvtrack_d0_selected[getNtrkBin(nTrks)].Fill(d0)
            
            h_mvtrack_allPtSel[getNtrkBin(nTrks)].Fill(dvtrack_pt)
            h_mvtrack_d0sig[getNtrkBin(nTrks)].Fill(d0sig)
            if (isAssociated and DV_rxy > 25.):
                h_mvtrack_ptOutsideBP[getNtrkBin(nTrks)].Fill(dvtrack_pt)
            if (isAssociated and DV_rxy > 145.):
                h_mvtrack_ptOutsidePixel[getNtrkBin(nTrks)].Fill(dvtrack_pt)
            if (DV_rxy < 25.):
                h_mvtrack_d0InsideBP[getNtrkBin(nTrks)].Fill(d0sig)
            if (isAssociated and DV_rxy < 145.):
                h_mvtrack_d0InsidePixel[getNtrkBin(nTrks)].Fill(d0sig)
            if (not isAssociated and DV_rxy > 145.):
                h_mvtrack_d0Selected[getNtrkBin(nTrks)].Fill(d0sig)
            if (isAssociated):
                h_mvtrack_angle[getNtrkBin(nTrks)].Fill(angle)
            if (DV_rxy > 25. and angle < 0.2):
                h_mvtrack_lowPtForward[getNtrkBin(nTrks)].Fill(dvtrack_pt)
        if (nTrks >= 4):
            ntrkBin = getNtrkBin(nTrks)
            if (merged.M() < 0.5):
                continue
            if (dvType == 4):
                continue
            hist[ntrkBin].Fill(merged.M(), weight)
            h_mvMass_dvType[ntrkBin][dvType].Fill(merged.M(), weight)
            h_mvChiSq_dvType[ntrkBin][dvType].Fill(chisq, weight)
            h_mvRxy_dvType[ntrkBin][dvType].Fill(rxy, weight)
            h_mvZ_dvType[ntrkBin][dvType].Fill(z, weight)

            if (nTrks == nTrks_orig):
                ntrkBin = getNtrkBin(nTrks)
                if (merged.M() < 0.5):
                    continue
                hist_orig[ntrkBin].Fill(merged.M(), weight)

    return [h_mvtrack_allPtSel, h_mvtrack_ptOutsideBP, h_mvtrack_ptOutsidePixel, h_mvtrack_d0InsideBP, h_mvtrack_d0InsidePixel, h_mvtrack_d0Selected, h_mvtrack_angle, h_mvtrack_lowPtForward, h_mvtrack_nAttached, h_nAttached_vs_dvType, h_mvtrack_d0_all, h_mvtrack_d0_selected, h_mvtrack_d0_attached, h_mvtrack_d0sig, h_mvMass_dvType, h_mvChiSq_dvType, h_mvRxy_dvType, h_mvZ_dvType]

noSelHists = cleaning(mergedVertices, "noSel", h_mvMassDict, h_mvMassDict_orig)
DVSelHists = cleaning(mergedVertices, "DVSel", h_mvMassDict_DVSel, h_mvMassDict_DVSel_orig)
upstreamHists = cleaning(mergedVertices, "upstreamHitVeto", h_mvMassDict_upstream, h_mvMassDict_upstream_orig)
allptSelHists = cleaning(mergedVertices, "allPtSel", h_mvMassDict_allPtSel, h_mvMassDict_allPtSel_orig)
ptOutsideBPHists = cleaning(mergedVertices, "ptOutsideBP", h_mvMassDict_ptOutsideBP, h_mvMassDict_ptOutsideBP_orig)
ptOutsidePixelHists = cleaning(mergedVertices, "ptOutsidePixel", h_mvMassDict_ptOutsidePixel, h_mvMassDict_ptOutsidePixel_orig)
d0InsideBPHists = cleaning(mergedVertices, "d0InsideBP", h_mvMassDict_d0InsideBP, h_mvMassDict_d0InsideBP_orig)
d0InsidePixelHists = cleaning(mergedVertices, "d0InsidePixel", h_mvMassDict_d0InsidePixel, h_mvMassDict_d0InsidePixel_orig)
d0SelectedHists = cleaning(mergedVertices, "d0Selected", h_mvMassDict_d0Selected, h_mvMassDict_d0Selected_orig)
angleHists = cleaning(mergedVertices, "angle", h_mvMassDict_angle, h_mvMassDict_angle_orig)
lowPtForwardHists = cleaning(mergedVertices, "lowPtForward", h_mvMassDict_lowPtForward, h_mvMassDict_lowPtForward_orig)
passTCHists = cleaning(mergedVertices, "passTC", h_mvMassDict_passTC, h_mvMassDict_passTC_orig)
fullSelHists = cleaning(mergedVertices, "fullSel", h_mvMassDict_fullSel, h_mvMassDict_fullSel_orig)
ptSelHists = cleaning(mergedVertices, "ptSel", h_mvMassDict_ptSel, h_mvMassDict_ptSel_orig)
d0SelHists = cleaning(mergedVertices, "d0Sel", h_mvMassDict_d0Sel, h_mvMassDict_d0Sel_orig)
angleForwardHists = cleaning(mergedVertices, "angleForward", h_mvMassDict_angleForward, h_mvMassDict_angleForward_orig)
attachedPtHists = cleaning(mergedVertices, "attachedPt", h_mvMassDict_attachedPt, h_mvMassDict_attachedPt_orig)
exceptAllPtHists = cleaning(mergedVertices, "exceptAllPt", h_mvMassDict_exceptAllPt, h_mvMassDict_exceptAllPt_orig)
trackCleaningHists = cleaning(mergedVertices, "trackCleaning", h_mvMassDict_trackCleaning, h_mvMassDict_trackCleaning_orig)
allPtSelAndPtOutsideBP = cleaning(mergedVertices, "allPtSelAndPtOutsideBP", h_mvMassDict_allPtSelAndPtOutsideBP, h_mvMassDict_allPtSelAndPtOutsideBP_orig)
allPtSel_1p2GeV = cleaning(mergedVertices, "1p2", h_mvMassDict_allPtSel_1p2GeV, h_mvMassDict_allPtSel_1p2GeV_orig)
allPtSel_1p4GeV = cleaning(mergedVertices, "1p4", h_mvMassDict_allPtSel_1p4GeV, h_mvMassDict_allPtSel_1p4GeV_orig)
allPtSel_1p6GeV = cleaning(mergedVertices, "1p6", h_mvMassDict_allPtSel_1p6GeV, h_mvMassDict_allPtSel_1p6GeV_orig)
allPtSel_1p8GeV = cleaning(mergedVertices, "1p8", h_mvMassDict_allPtSel_1p8GeV, h_mvMassDict_allPtSel_1p8GeV_orig)
passFiducial = cleaning(mergedVertices, "passFiducial", h_mvMassDict_passFiducial, h_mvMassDict_passFiducial_orig)
passDist = cleaning(mergedVertices, "passDist", h_mvMassDict_passDist, h_mvMassDict_passDist_orig)
passChiSq = cleaning(mergedVertices, "passChiSq", h_mvMassDict_passChiSq, h_mvMassDict_passChiSq_orig)
passMaterial = cleaning(mergedVertices, "passMaterial", h_mvMassDict_passMaterial, h_mvMassDict_passMaterial_orig)
passMaterial_strict = cleaning(mergedVertices, "passMaterial_strict", h_mvMassDict_passMaterial_strict, h_mvMassDict_passMaterial_strict_orig)

outputFile.Write()
outputFile.Close()
