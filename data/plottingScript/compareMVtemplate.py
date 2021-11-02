import ROOT as r
import sys, os
sys.path.append("/Users/amizukam/DVJets/atlasstyle")
from AtlasStyle import *
from AtlasLabel import *
from utils import *

r.gROOT.SetBatch()
SetAtlasStyle()
label = "Internal"

#SR = "highPtSR"
SR = "tracklessSR"

plotType = "mvTemplateCompare"
directory = "pdfs/" + plotType + "/" + SR
if (not os.path.isdir(directory)):
    os.makedirs(directory)

inputFile = r.TFile("rootfiles/sigAndMass_{}.root".format(SR), "READ")
dijetFile = r.TFile("/Users/amizukam/dvjets_mergedVertices/dijetMC/plottingScript/rootfiles/sigAndMass_mc16e_{}.root".format(SR), "READ")

ntrkList = ["Ntrk4", "Ntrk5", "Ntrk6", "Ntrk>6"]

noWeightMass = {}
sigWeightMass = {}
drWeightMass = {}
weightMass = {}
dijetMVMass = {}
dijetSigWeight = {}
dijetdrWeight = {}
dijetWeight = {}
for ntrk in ntrkList:
    noWeightMass[ntrk] = inputFile.Get("mergedMass_"+ntrk)
    sigWeightMass[ntrk] = inputFile.Get("mergedMass_sigWeight_"+ntrk)
    drWeightMass[ntrk] = inputFile.Get("mergedMass_drWeight_"+ntrk)
    weightMass[ntrk] = inputFile.Get("mergedMass_weight_"+ntrk)
    dijetMVMass[ntrk] = dijetFile.Get("mergedMass_"+ntrk)
    dijetSigWeight[ntrk] = dijetFile.Get("mergedMass_sigWeight_"+ntrk)
    dijetdrWeight[ntrk] = dijetFile.Get("mergedMass_drWeight_"+ntrk)
    dijetWeight[ntrk] = dijetFile.Get("mergedMass_weight_"+ntrk)

c = r.TCanvas("c", "c", 800, 700)
c.cd()
c.SetLogy(1)

sampleLabel = prepareLatex()
for ntrk in ntrkList:
    h_nominal = noWeightMass[ntrk]
    h_sigWeight = sigWeightMass[ntrk]
    h_drWeight = drWeightMass[ntrk]
    h_weight = weightMass[ntrk]
    h_dijet = dijetMVMass[ntrk]
    h_dijetSigWeight = dijetSigWeight[ntrk]
    h_dijetdrWeight = dijetdrWeight[ntrk]
    h_dijetWeight = dijetWeight[ntrk]

    h_sigWeight.SetLineColor(r.kRed)
    h_sigWeight.SetMarkerColor(r.kRed)
    h_drWeight.SetLineColor(r.kBlue)
    h_drWeight.SetMarkerColor(r.kBlue)
    h_weight.SetLineColor(r.kGreen)
    h_weight.SetMarkerColor(r.kGreen)
    h_dijet.SetLineColor(r.kRed)
    h_dijet.SetMarkerColor(r.kRed)
    h_dijetSigWeight.SetLineColor(r.kRed)
    h_dijetSigWeight.SetMarkerColor(r.kRed)
    h_dijetdrWeight.SetLineColor(r.kBlue)
    h_dijetdrWeight.SetMarkerColor(r.kBlue)
    h_dijetWeight.SetLineColor(r.kGreen)
    h_dijetWeight.SetMarkerColor(r.kGreen)

    h_nominal.Sumw2()
    h_dijet.Sumw2()

    leg = r.TLegend(0.60, 0.55, 0.72, 0.80)
    decorateLeg(leg)
    leg.AddEntry(h_nominal, "S < 100", "l")
    leg.AddEntry(h_sigWeight, "Significance weight", "l")
    leg.AddEntry(h_drWeight, "dR weight", "l")
    leg.AddEntry(h_weight, "Weight = sig #times dR", "l")

    h_nominal.DrawNormalized("hist e0")
    h_sigWeight.DrawNormalized("hist e0 same")
    h_drWeight.DrawNormalized("hist e0 same")
    h_weight.DrawNormalized("hist e0 same")
    ATLASLabel(0.20, 0.955, label)
    sampleLabel.DrawLatex(0.62, 0.90, "Dijet-MC")
    sampleLabel.DrawLatex(0.62, 0.84, getNtrkLabel(ntrk))
    leg.Draw()

    c.Print("{}/{}.pdf".format(directory, "mvTemplate_"+ntrk))
    
    leg_mcData = r.TLegend(0.60, 0.65, 0.72, 0.78)
    decorateLeg(leg_mcData)
    leg_mcData.AddEntry(h_dijet, "Dijet MC", "l")
    leg_mcData.AddEntry(h_nominal, "Data", "l")
    h_dijet.DrawNormalized("hist e0")
    h_nominal.DrawNormalized("hist e0 same")
    ATLASLabel(0.20, 0.955, label)
    leg_mcData.Draw()
    sampleLabel.DrawLatex(0.62, 0.88, SR)
    sampleLabel.DrawLatex(0.62, 0.83, getNtrkLabel(ntrk))
    c.Print("{}/{}.pdf".format(directory, "mcData_"+ntrk))


    h_dijet.SetLineColor(r.kBlack)
    h_dijet.SetMarkerColor(r.kBlack)
    h_dijet.DrawNormalized("hist e0")
    h_dijetSigWeight.DrawNormalized("hist e0 same")
    h_dijetdrWeight.DrawNormalized("hist e0 same")
    h_dijetWeight.DrawNormalized("hist e0 same")
    ATLASLabel(0.20, 0.955, label)
    leg.Draw()
    sampleLabel.DrawLatex(0.62, 0.90, "Data, {}".format(SR))
    sampleLabel.DrawLatex(0.62, 0.84, getNtrkLabel(ntrk))
    c.Print("{}/{}.pdf".format(directory, "data_"+ntrk))
