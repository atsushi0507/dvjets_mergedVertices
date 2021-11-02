import ROOT as r

#SR = "highPtSR"
SR = "tracklessSR"

inputFile = r.TFile("rootfiles/sigAndMass_{}.root".format(SR), "READ")
outputFile = r.TFile("rootfiles/mvTemplate_{}.root".format(SR), "RECREATE")

ntrkList = ["Ntrk4", "Ntrk5", "Ntrk6", "Ntrk>6"]

massDict = {}
massDict_sig = {}
massDict_weight = {}
baseName = "mergedMass"
for ntrk in ntrkList:
    massDict[ntrk] = {}
    massDict_sig[ntrk] = {}
    massDict_weight[ntrk] = {}

    massDict[ntrk] = inputFile.Get(baseName + "_" + ntrk)
    massDict_sig[ntrk] = inputFile.Get(baseName + "_sigWeight_" + ntrk)
    massDict_weight[ntrk] = inputFile.Get(baseName + "_weight_" + ntrk)

for ntrk in ntrkList:
    h_mass = massDict[ntrk]
    h_mass_sig = massDict_sig[ntrk]
    h_mass_weight = massDict_weight[ntrk]
    
    h_mass.SetLineColor(r.kBlack)
    h_mass.SetMarkerColor(r.kBlack)

    h_mass_sig.SetLineColor(r.kBlack)
    h_mass_sig.SetMarkerColor(r.kBlack)
    h_mass_weight.SetLineColor(r.kBlack)
    h_mass_weight.SetMarkerColor(r.kBlack)
    
    h_mass.Write()
    #h_mass_sig.Write()
    #h_mass_weight.Write()
    
outputFile.Write()
outputFile.Close()
