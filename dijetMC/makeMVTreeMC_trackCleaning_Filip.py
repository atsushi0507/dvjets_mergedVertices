import ROOT
from glob import glob
import math
import os
from array import array
from collections import Counter

outputTag = "mc16e"
#outputTag = "mc16e_parentInfo"

evtMax = -1
useMCMap = True #Turn on the use of the MC material map instead of the default data material map flag from the FT ntuple
doJetSel = False #With this setting, only events where leading and subleading jet pT are between 550 and 750 GeV are saved. This is used to compare distributions between data and MC.

m_pion = 139.57 * 0.001

### Prepare input files ###
if (outputTag == "mc16a"):
    #dataDir = "user.gripelli.mc16_13TeV.361024.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ4W.HadInt20210409_mc16a_trees.root/"
    dataDir = "user.gripelli.mc16_13TeV.361024.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ4W.210618_dijetMC16a_trees.root"
elif (outputTag == "mc16d"):
    #dataDir = "user.gripelli.mc16_13TeV.361024.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ4W.HadInt20210409_mc16d_trees.root/"
    dataDir = "user.gripelli.mc16_13TeV.361024.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ4W.210618_dijetMC16d_trees.root"
elif (outputTag == "mc16e"):
    #dataDir = "user.cohm.mc16_13TeV.364704.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ4WithSW.210426_test_trees.root/"
    dataDir = "user.gripelli.mc16_13TeV.364704.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ4WithSW.210618_dijetMC16e_trees.root"

if (not os.path.isdir("outputFiles")):
    os.makedirs("outputFiles")
if (not os.path.isdir("textFiles")):
    os.makedirs("textFiles")

dataPath = "/Volumes/LaCie/DVJets/mc/dijets/"
dataSet = dataPath + dataDir
fileNames = glob(dataSet+"/*.root")
print(fileNames)

### Prepare input tree ###
treeIn = ROOT.TChain("trees_SRDV_")
for fileName in fileNames:
    treeIn.Add(fileName)

### Prepare output files ###
fileOut=ROOT.TFile("outputFiles/mergedVerticesTreeMC_%s_trackCleaning_Filip_newSamples.root"%(outputTag),"RECREATE")

### Prepare histogram to save number of events ###
nEvtHisto = ROOT.TH1D("nEvt","nEvt",1,0,1)

### Prepare output tree ###
treeOut=ROOT.TTree("trees_SRDV_","trees_SRDV_")

### Prepare branches for output tree ###
# New branches
nDV = array('i',[0])
dvNtrk = array('i',[0])
dvMass = array('f',[0.])
dvDeltaRMax = array('f',[0.])
dvType = array('i',[0])
dvPdgId = array('i',[0])
dvHasDefinedPdgId = array('i',[0])
dvMaxTruthParticleDist = array('f',[0.])
dvAvgTruthParticleDist = array('f',[0.])
dvMaxTruthParticleDistSig = array('f',[0.])
dvAvgTruthParticleDistSig = array('f',[0.])
dvMaxInterTruthParticleDist = array('f',[0.])
dvMaxInterTruthParticleDistSig = array('f',[0.])
dvIsInMaterial = array('i',[0])
nParents = array('i', [0])
hasUnrelatedTracks = array('i', [0])
axDV = array("i", [0])
hasHIParents = array("i", [0])

treeOut.Branch('nDV', nDV, 'nDV/I')
treeOut.Branch('dv_ntrk', dvNtrk, 'dv_ntrk/I')
treeOut.Branch('dv_mass', dvMass, 'dv_mass/F')
treeOut.Branch('dv_dRmax', dvDeltaRMax, 'dv_dRmax/F')
treeOut.Branch('dv_type', dvType, 'dv_type/I')
treeOut.Branch('dv_pdgId', dvPdgId, 'dv_pdgId/I')
treeOut.Branch('dv_hasDefinedPdgId', dvHasDefinedPdgId, 'dv_hasDefinedPdgId/I')
treeOut.Branch('dv_maxTruthParticleDist', dvMaxTruthParticleDist, 'dv_maxTruthParticleDist/F')
treeOut.Branch('dv_avgTruthParticleDist', dvAvgTruthParticleDist, 'dv_avgTruthParticleDist/F')
treeOut.Branch('dv_maxTruthParticleDistSig', dvMaxTruthParticleDistSig, 'dv_maxTruthParticleDistSig/F')
treeOut.Branch('dv_avgTruthParticleDistSig', dvAvgTruthParticleDistSig, 'dv_avgTruthParticleDistSig/F')
treeOut.Branch('dv_maxInterTruthParticleDist', dvMaxInterTruthParticleDist, 'dv_maxInterTruthParticleDist/F')
treeOut.Branch('dv_maxInterTruthParticleDistSig', dvMaxInterTruthParticleDistSig, 'dv_maxInterTruthParticleDistSig/F')
treeOut.Branch('dv_isInMaterial', dvIsInMaterial, 'dv_isInMaterial/I')
treeOut.Branch("nParents", nParents, "nParents/I")
treeOut.Branch("hasUnrelatedTracks", hasUnrelatedTracks, "hasUnrelatedTracks/I")
treeOut.Branch("axDV", axDV, "axDV/I")
treeOut.Branch("hasHIParents", hasHIParents, "hasHIParents/I")

# Branches to transfer
mcEventWeight = array('f',[0.])
nPV = array('i',[0])
dvRadius = array('f',[0.])
dvPassFiducialCut = array('i',[0])
dvPassDistCut = array('i',[0])
dvPassChi2Cut = array('i',[0])

treeOut.Branch('mcEventWeight', mcEventWeight, 'mcEventWeight/F')
treeOut.Branch('nPV', nPV, 'nPV/I')
treeOut.Branch('dv_rxy', dvRadius, 'dv_rxy/F')
treeOut.Branch('dv_PassFiducialCut', dvPassFiducialCut, 'dv_PassFiducialCut/I')
treeOut.Branch('dv_PassDistCut', dvPassDistCut, 'dv_PassDistCut/I')
treeOut.Branch('dv_PassChi2Cut', dvPassChi2Cut, 'dv_PassChi2Cut/I')

def get_PVDV(pv, dv):
    PV_DV = dv - pv
    return PV_DV

### Branches that should be activated for the input tree ###
# List of branches
branches=[
    'mcEventWeight',
    'NPV',
    'DRAW_pass_triggerFlags',
    'DRAW_pass_DVJETS',
    #'BaselineSel_pass',
    'BaselineSel_HighPtSR',
    'calibJet_Pt',
    'NPV',
    'DV_index',
    'DV_rxy',
    'DV_x',
    'DV_y',
    'DV_z',
    'DV_covariance0',
    'DV_covariance2',
    'DV_covariance5',
    'DV_passMaterialVeto',
    'dvtrack_DVIndex',
    'dvtrack_etaWrtDV',
    'dvtrack_phiWrtDV',
    'dvtrack_m',
    'dvtrack_ptWrtDV',
    'dvtrack_pt',
    'dvtrack_isBackwardsTrack',
    # 'dvtrack_hasd0InSpike',
    'dvtrack_failedExtrapolation',
    'dvtrack_hasValidTruthLink',
    'dvtrack_hasValidTruthParentInfo',
    ### Add for track cleaning study
    'dvtrack_d0',
    'dvtrack_errd0',
    'dvtrack_isAssociated',
    'dvtrack_passpatternCheck',
    'dvtrack_RadFirstHit',
    'PV_x',
    'PV_y',
    'PV_z',
    ### End 
    'dvtrack_truthMatchProb',
    'dvtrack_truthParentBarcode',
    'dvtrack_truthParentPdgId',
    'dvtrack_truthBarcode',
    'dvtrack_truthPdgId',
    'dvtrack_truthVtxX',
    'dvtrack_truthVtxY',
    'dvtrack_truthVtxZ',
    'DV_passFiducialCut',
    'DV_passDistCut',
    'DV_passChiSqCut'
]

treeIn.SetBranchStatus('*',0)
for branch in branches:
    treeIn.SetBranchStatus(branch, 1)

### Read in MC material map ###
if useMCMap:
    print ("Importing material map for MC")
    print ("Reading in map")
    #matMapFile = ROOT.TFile("materialMapMCRebinned.root")
    matMapFile = ROOT.TFile("/Users/amizukam/DVJets/materialMap/materialMapMCRebinned.root", "READ")
    matMap = matMapFile.Get("RZphiIntLen_i")
    print ("Done importing material map")

multiParentFile = open("textFiles/multiParent_{}_trackCleaning.txt".format(outputTag), "w")
multiParentFile_G4 = open("textFiles/multiParent_G4_{}_trackCleaning.txt".format(outputTag), "w")
axFile = open("textFiles/axCandidate_{}.txt".format(outputTag), "w")

### Start loop over events ###
evtTot = treeIn.GetEntries()
if evtMax == -1: evtMax = evtTot

baselineSelectionPass = 0 # Counter for events that pass the baseline selection
baselineSelectionPassWeighted = 0
dvPass = 0 # Counter for events that contain DVs after track cleaning has been applied
totDVs = 0 # Counter for total number of DVs that will be saved to the TTree

print ("Will process",evtMax,"events out of",evtTot)

evtCounter = 0
for event in treeIn:
    evtCounter += 1
    if (evtCounter > evtMax):
        break
    if evtCounter%10000==0:
        print ("Processed ",evtCounter," events out of ",evtTot)

    # Apply basic event selection
    #if not (ord(event.DRAW_pass_triggerFlags) and ord(event.DRAW_pass_DVJETS) and ord(event.BaselineSel_pass)):
    if not (ord(event.DRAW_pass_triggerFlags) and ord(event.DRAW_pass_DVJETS) and ord(event.BaselineSel_HighPtSR)):
        continue

    #Determine which jet is leading
    sortedJetPt=sorted(event.calibJet_Pt,reverse=True)
    leadingJetPt = sortedJetPt[0]
    subleadingJetPt = sortedJetPt[1]

    if doJetSel and not (len(event.calibJet_Pt)>1 and 550<leadingJetPt<750 and 550<subleadingJetPt<750):
        continue

    baselineSelectionPass += 1
    
    eventHasDVs = False

    # Create dictionaries that will hold the properties of all the Dvs in the event
    dvNtrkDict = {}
    dvMassDict = {}
    dvRadiusDict = {}
    
    dvPassFiducialCutDict = {}
    dvPassDistCutDict = {}
    dvPassChi2CutDict = {}
    
    dvDeltaRMaxDict = {}
    dvFourVectorDict = {}
    dvIsInMaterialDict = {}
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

    dvParentDict = {}
    dvtrack_d0sigDict = {}
    dvtrack_isAssociatedDict = {}
    
    mcEventWeight[0] = event.mcEventWeight 
    nPV[0] = event.NPV

    baselineSelectionPassWeighted += event.mcEventWeight 

    # Loop over DVs and create keys in the dictionaries corresponding to the indices of the DVs
    for dvIndex in event.DV_index:
        dvNtrkDict[dvIndex] = 0
        dvRadiusDict[dvIndex] = event.DV_rxy[dvIndex]

        dvPassFiducialCutDict[dvIndex] = event.DV_passFiducialCut[dvIndex]
        dvPassDistCutDict[dvIndex] = event.DV_passDistCut[dvIndex]
        dvPassChi2CutDict[dvIndex] = event.DV_passChiSqCut[dvIndex]

        dvFourVectorDict[dvIndex] = ROOT.TLorentzVector()
        dvFourVectorDict[dvIndex].SetPtEtaPhiM(0,0,0,0)
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

        dvXDict[dvIndex] = event.DV_x[dvIndex]
        dvYDict[dvIndex] = event.DV_y[dvIndex]
        dvZDict[dvIndex] = event.DV_z[dvIndex]
        dvVarXDict[dvIndex] = event.DV_covariance0[dvIndex]
        dvVarYDict[dvIndex] = event.DV_covariance2[dvIndex]
        dvVarZDict[dvIndex] = event.DV_covariance5[dvIndex]

        dvParentDict[dvIndex] = []
        
    # Loop over tracks and add them to the correct key in the dictionary based on their DV index
    trkCounter = 0
    for trkdvIndex in event.dvtrack_DVIndex:
        trkEta = event.dvtrack_etaWrtDV[trkCounter]
        trkPhi = event.dvtrack_phiWrtDV[trkCounter]
        trkM = event.dvtrack_m[trkCounter]
        trkPtWrtDV = event.dvtrack_ptWrtDV[trkCounter]
        trkPt = event.dvtrack_pt[trkCounter]
        trkIsBackward = event.dvtrack_isBackwardsTrack[trkCounter]
        trkFailedExtrapolation = event.dvtrack_failedExtrapolation[trkCounter]

        trk_d0sig = ROOT.TMath.Abs(event.dvtrack_d0[trkCounter]/event.dvtrack_errd0[trkCounter])
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

        trkTruthDist = math.sqrt((trkTruthX-trkdvX)*(trkTruthX-trkdvX)+(trkTruthY-trkdvY)*(trkTruthY-trkdvY)+(trkTruthZ-trkdvZ)*(trkTruthZ-trkdvZ))
        trkTruthDistSig = math.sqrt((trkTruthX-trkdvX)*(trkTruthX-trkdvX)/trkdvVarX+(trkTruthY-trkdvY)*(trkTruthY-trkdvY)/trkdvVarY+(trkTruthZ-trkdvZ)*(trkTruthZ-trkdvZ)/trkdvVarZ)

	# If the track passes the track cleaning, add it to the dictionaries
	# if not (trkIsBackward or trkInDOSpike or trkFailedExtrapolation):
        #if not (trkIsBackward or trkFailedExtrapolation or (not trkHasParentInfo)):
        if not (trkIsBackward or trkFailedExtrapolation):
            # Filip's track cleaning
            if (radFirstHit < dvRadiusDict[trkdvIndex]):
                continue
            # pT selection
            if (trkPtWrtDV < 2.): # All track pT < 2. GeV is vetoed
                continue
            if (assoTrk):
                if (dvRadiusDict[trkdvIndex] > 25. and trkPtWrtDV < 3.):
                    continue # Require pT > 3 GeV for attached tracks outside BP
                if (dvRadiusDict[trkdvIndex] > 145 and trkPtWrtDV < 4.):
                    continue # Require pT > 4 GeV for attached tracks outside last pixel
            # d0-significance selection
            if (dvRadiusDict[trkdvIndex] < 25. and trk_d0sig < 10.):
                continue # d0sig > 10 for all tracks inside BP
            if (dvRadiusDict[trkdvIndex] < 145. and trk_d0sig < 15. and assoTrk):
                continue # d0sig > 15 for attached tracks inside last pixel
            if (dvRadiusDict[trkdvIndex] > 145. and trk_d0sig < 10. and not assoTrk):
                continue # d0sig > 10 for selected tracks outside last pixel

            # angular selection
            p4_track = ROOT.TLorentzVector()
            p4_track.SetPtEtaPhiM(trkPtWrtDV,
                                  trkEta,
                                  trkPhi,
                                  trkM)
            dv = ROOT.TVector3(event.DV_x[trkdvIndex], event.DV_y[trkdvIndex], event.DV_z[trkdvIndex])
            pv = ROOT.TVector3(event.PV_x, event.PV_y, event.PV_z)
            if (assoTrk and p4_track.Angle(get_PVDV(pv, dv)) > ROOT.TMath.Pi()/2.):
                continue
            if (dvRadiusDict[trkdvIndex] > 25. and p4_track.Angle(get_PVDV(pv, dv)) < 0.2 and trkPtWrtDV < 4.):
                continue
            
            
            dvTrkParentBarcodeDict[trkdvIndex].append(trkParentBarcode)
            dvTrkParentPdgIdDict[trkdvIndex].append(trkParentPdgId)
            dvTrkBarcodeDict[trkdvIndex].append(trkBarcode)
            dvTrkPdgIdDict[trkdvIndex].append(trkPdgId)
            dvTrkTMDict[trkdvIndex].append(trkIsTM)
            dvNtrkDict[trkdvIndex] += 1
            trkFourVector = ROOT.TLorentzVector()
            trkFourVector.SetPtEtaPhiM(trkPtWrtDV,trkEta,trkPhi,trkM)
            dvFourVectorDict[trkdvIndex] += trkFourVector
            dvTrkFourVectorDict[trkdvIndex].append(trkFourVector)
            dvTrkTruthDistDict[trkdvIndex].append(trkTruthDist)
            dvTrkTruthDistSigDict[trkdvIndex].append(trkTruthDistSig)
            
            dvTrkTruthXDict[trkdvIndex].append(trkTruthX)
            dvTrkTruthYDict[trkdvIndex].append(trkTruthY)
            dvTrkTruthZDict[trkdvIndex].append(trkTruthZ)
            dvParentDict[trkdvIndex].append((trkParentPdgId, trkParentBarcode))
            dvTrkParentInfoDict[trkdvIndex].append(trkHasParentInfo)
            
        trkCounter += 1

    # Compute number of DVs in the event
    nDVs = 0
    for dvIndex in event.DV_index:
        if dvNtrkDict[dvIndex]>1:
            nDVs += 1
    nDV[0] = nDVs
    
    # Compute DV variables
    for dvIndex in event.DV_index:
        if dvNtrkDict[dvIndex]<2:
            continue
        eventHasDVs = True
        totDVs += 1
        
        # New DV mass after track cleaning
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
                hasHIParents[0] = True if (trkParentPdgId in [211, 2212, -211, -2212]) else False
                if (dvPdgIdDict[dvIndex] != trkParentPdgId or dvBarcodeDict[dvIndex] != trkParentBarcode) and (dvPdgIdDict[dvIndex]!=0 and dvBarcodeDict[dvIndex] !=0):
                    dvPdgIdIsNotDefinedDict[dvIndex] = True
                dvPdgIdDict[dvIndex] = trkParentPdgId
                dvBarcodeDict[dvIndex] = trkParentBarcode
                    
            trkCounter += 1

        # DV types: 1=g4, 2=g4Wpileup, 3=g4Wgenerator, 4=pileup, 5=pileupWgenerator, 6=generator, 7=unknown
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

        # Determine if the DV is in material
        if useMCMap:
            phi = ROOT.TMath.ATan2(dvYDict[dvIndex],dvXDict[dvIndex])
            z = dvZDict[dvIndex]
            r = dvRadiusDict[dvIndex]
            matMapBin = matMap.FindBin(r,phi,z)
            
            matMapBinContent = matMap.GetBinContent(matMapBin)
            if matMapBinContent == 0:
                dvIsInMaterial[0] = 0
            elif matMapBinContent > 0:
                dvIsInMaterial[0] = 1
            isInMaterial = True if matMapBinContent > 0 else False

        else:
            dvIsInMaterial[0]=(int(not event.DV_passMaterialVeto[dvIndex]))

        # Figure out the truth particle distances from DV
        varX = abs(dvVarXDict[dvIndex])
        varY = abs(dvVarYDict[dvIndex])
        varZ = abs(dvVarZDict[dvIndex])
        dvInterTruthParticleDist = []
        dvInterTruthParticleDistSig = []
        hasUnrelatedTrack = any(ntrk[1] == 1 for ntrk in parentCounter.most_common())
        nChildren = [ntrk[1] for ntrk in parentCounter.most_common()]
        childCounter = Counter(nChildren)
        #print(nChildren, childCounter, len(childCounter))
        isAX = True if (len(childCounter) > 1 and nChildren.count(1) == 1) else False
        """
        if (isAX):
            print(nChildren, childCounter, len(childCounter), dvTypeDict[dvIndex])
        """
        for track1 in range(0,len(dvTrkTruthXDict[dvIndex])):
            for track2 in range(0,len(dvTrkTruthXDict[dvIndex])):
                dx = dvTrkTruthXDict[dvIndex][track1]-dvTrkTruthXDict[dvIndex][track2]
                dy = dvTrkTruthYDict[dvIndex][track1]-dvTrkTruthYDict[dvIndex][track2]
                dz = dvTrkTruthZDict[dvIndex][track1]-dvTrkTruthZDict[dvIndex][track2]
                dist = math.sqrt(dx*dx+dy*dy+dz*dz)
                distSig = math.sqrt(dx*dx/varX+dy*dy/varY+dz*dz/varZ)
                dvInterTruthParticleDist.append(dist)
                dvInterTruthParticleDistSig.append(distSig)

        
        if (nParent > 1 and not isInMaterial):
            if (not hasUnrelatedTrack):
                if (dvTypeDict[dvIndex] != 1):
                    multiParentFile.write("{}, {}, {}, {}, {}, {} \n".format(nParent, nTracks, parentList, isInMaterial, dvTypeDict[dvIndex], dvTrkParentInfoDict[dvIndex]))
                    multiParentFile.write("{}\n".format(parentCounter))
                    multiParentFile.write("{}, {}\n\n".format(dvTrkPdgIdDict[dvIndex], max(dvInterTruthParticleDist)))
                else:
                    multiParentFile_G4.write("{}, {}, {}, {}, {} \n".format(nParent, nTracks, parentList, isInMaterial, dvTypeDict[dvIndex]))
                    multiParentFile_G4.write("{}\n".format(parentCounter))
                    multiParentFile_G4.write("{}, {}\n\n".format(dvTrkPdgIdDict[dvIndex], max(dvInterTruthParticleDist)))
        if (nParent > 1 and isAX):
            axFile.write("{}, {}, {}, {}, {} \n".format(nParent, nTracks, parentList, isInMaterial, dvTypeDict[dvIndex]))
            axFile.write("{}\n".format(parentCounter))
            axFile.write("{}, {}\n\n".format(dvTrkPdgIdDict[dvIndex], max(dvInterTruthParticleDist)))


        # Fill all branches in the tree
        dvNtrk[0] = (dvNtrkDict[dvIndex])
        dvMass[0] = (dvMassDict[dvIndex])
        dvRadius[0] = (dvRadiusDict[dvIndex])
        dvPassFiducialCut[0] = dvPassFiducialCutDict[dvIndex]
        dvPassDistCut[0] = dvPassDistCutDict[dvIndex]
        dvPassChi2Cut[0] = dvPassChi2CutDict[dvIndex]

        dvDeltaRMax[0] = (dvDeltaRMaxDict[dvIndex])
        dvType[0] = (dvTypeDict[dvIndex])
        dvPdgId[0] = (dvPdgIdDict[dvIndex])
        dvHasDefinedPdgId[0] = (int(not dvPdgIdIsNotDefinedDict[dvIndex]))
        dvMaxTruthParticleDist[0] = (max(dvTrkTruthDistDict[dvIndex]))
        dvAvgTruthParticleDist[0] = ((sum(dvTrkTruthDistDict[dvIndex])-dvMaxTruthParticleDist[0])/(len(dvTrkTruthDistDict[dvIndex])-1))
        dvMaxTruthParticleDistSig[0] = (max(dvTrkTruthDistSigDict[dvIndex]))
        dvAvgTruthParticleDistSig[0] = ((sum(dvTrkTruthDistSigDict[dvIndex])-dvMaxTruthParticleDistSig[0])/(len(dvTrkTruthDistSigDict[dvIndex])-1))

        dvMaxInterTruthParticleDist[0] = max(dvInterTruthParticleDist)
        dvMaxInterTruthParticleDistSig[0] = max(dvInterTruthParticleDistSig)

        nParents[0] = nParent
        hasUnrelatedTracks[0] = hasUnrelatedTrack
        axDV[0] = isAX
        
        treeOut.Fill()

    if eventHasDVs:
        dvPass += 1

print ("Processed",evtMax,"events,",baselineSelectionPass,"passed baseline selection and",dvPass,"contained DVs")

print ("A total of",totDVs,"DVs are saved in the tree")
print ("Total number of saved weighted events:",baselineSelectionPassWeighted)

nEvtHisto.SetBinContent(1,baselineSelectionPassWeighted)

print ("Writing tree to file")
fileOut.cd()	
treeOut.Write()
nEvtHisto.Write()
fileOut.Close()

print ("Bye!")
