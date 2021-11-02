import ROOT as r
import sys, os
sys.path.append("/Users/amizukam/DVJets/atlasstyle")
from AtlasStyle import *
from AtlasLabel import *

r.gROOT.SetBatch()
SetAtlasStyle()
label = "Internal"

#dataSet = "mc16e"
#dataSet = "mc16e_new"
#dataSet = "mc16e_trackCleaning"
dataSet = "mc16e_parentInfo"

plotType = "truthAXMass"
directory = "pdfs/" + plotType + "/" + dataSet
if (not os.path.isdir(directory)):
    os.makedirs(directory)
if (not os.path.isdir("rootfiles")):
    os.makedirs("rootfiles")

inputFile = r.TFile("../outputFiles/mergedVerticesTreeMC_{}.root".format(dataSet), "READ")
tree = inputFile.Get("trees_SRDV_")

outputFile = r.TFile("rootfiles/{}_{}.root".format(plotType, dataSet), "RECREATE")

colors = [r.kGreen, r.kRed, r.kBlue, r.kOrange, r.kMagenta, r.kCyan]

ntrkList = ["Ntrk2", "Ntrk3", "Ntrk4", "Ntrk5", "Ntrk6", "Ntrk>6"]

def determineNtrkBin(ntrk):
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

def getNtrkLabel(ntrkBin):
    ntrkLabel = ""
    if ntrkBin == "Ntrk2":
        ntrkLabel = "N_{trk} = 2"
    if ntrkBin == "Ntrk3":
        ntrkLabel = "N_{trk} = 3"
    if ntrkBin == "Ntrk4":
        ntrkLabel = "N_{trk} = 4"
    if ntrkBin == "Ntrk5":
        ntrkLabel = "N_{trk} = 5"
    if ntrkBin == "Ntrk6":
        ntrkLabel = "N_{trk} = 6"
    if ntrkBin == "Ntrk>6":
        ntrkLabel = "N_{trk} > 6"
    return ntrkLabel

def decorateRatioPlot(rp):
    rp.SetH2DrawOpt("histo")
    rp.Draw()
    rp.GetLowerRefGraph().SetMaximum(2.0)
    rp.GetLowerRefGraph().SetMinimum(0.0)
    rp.GetLowYaxis().SetNdivisions(4)
    rp.SetSeparationMargin(0.02)
    rp.SetLeftMargin(0.1575)
    rp.SetLowBottomMargin(0.50)

def decorateLeg(leg):
    leg.SetFillStyle(0)
    leg.SetBorderSize(0)
    leg.SetLineStyle(0)
    leg.SetTextSize(0.035)
    leg.SetTextFont(42)


# Main body
massDict = {}
massDict_passFiducialCut = {}
massDict_passDistCut = {}
massDict_passChi2Cut = {}
massDict_matVeto = {}
massDict_passDVsel = {}
for ntrk in ntrkList:
    massDict[ntrk] = r.TH1D("ax_"+ntrk, ";m_{AX} [GeV]", 100, 0., 100.)
    massDict_passFiducialCut[ntrk] = r.TH1D("ax_passFiducialCut"+ntrk, ";m_{AX} [GeV]", 100, 0., 100.)
    massDict_passDistCut[ntrk] = r.TH1D("ax_passDistCut"+ntrk, ";m_{AX} [GeV]", 100, 0., 100.)
    massDict_passChi2Cut[ntrk] = r.TH1D("ax_passChi2Cut"+ntrk, ";m_{AX} [GeV]", 100, 0., 100.)
    massDict_matVeto[ntrk] = r.TH1D("ax_matVeto"+ntrk, ";m_{AX} [GeV]", 100, 0., 100.)
    massDict_passDVsel[ntrk] = r.TH1D("ax_passDVsel"+ntrk, ";m_{AX} [GeV]", 100, 0., 100.)

for dv in tree:
    dvPassFiducial = dv.dv_PassFiducialCut
    dvPassDist     = dv.dv_PassDistCut
    dvPassChi2     = dv.dv_PassChi2Cut
    dvIsInMaterial = dv.dv_isInMaterial

    dvType = dv.dv_type
    ntrk = dv.dv_ntrk
    dvMass = dv.dv_mass
    nParents = dv.nParents
    hasUnrelatedTracks = dv.hasUnrelatedTracks
    maxInterTruthParticleDist = dv.dv_maxInterTruthParticleDist
    axDV = dv.axDV

    if ntrk < 2:
        continue

    ntrkBin = determineNtrkBin(ntrk)
    
    # Is the DV satisfy AX definition?
    if (nParents < 2):
        continue
    if (not axDV):
        continue
    if (maxInterTruthParticleDist < 0.15):
        continue
    if (dvType == 1):
        continue
    
    massDict[ntrkBin].Fill(dvMass)

    if (dvPassFiducial):
        massDict_passFiducialCut[ntrkBin].Fill(dvMass)
    if (dvPassDist):
        massDict_passDistCut[ntrkBin].Fill(dvMass)
    if (dvPassChi2):
        massDict_passChi2Cut[ntrkBin].Fill(dvMass)
    if (not dvIsInMaterial):
        massDict_matVeto[ntrkBin].Fill(dvMass)
    if (dvPassFiducial and dvPassDist and dvPassChi2 and not dvIsInMaterial):
        massDict_passDVsel[ntrkBin].Fill(dvMass)

# Draw histograms
c = r.TCanvas("c", "c", 800, 700)
c.cd()

sampleLabel = r.TLatex()
sampleLabel.SetNDC()
sampleLabel.SetTextFont(42)
sampleLabel.SetTextAlign(13)
sampleLabel.SetTextSize(0.03)

dataLabel = dataSet + ", di-jet"

def drawSampleLabel(sampleLabel, ntrkBin, text):
    sampleLabel.DrawLatex(0.65, 0.80, dataLabel)
    sampleLabel.DrawLatex(0.65, 0.75, "Event preselection")
    sampleLabel.DrawLatex(0.65, 0.70, getNtrkLabel(ntrkBin))
    if not (text == ""):
        sampleLabel.DrawLatex(0.65, 0.65, text)

c.SetLogy(1)
for ntrkBin in ntrkList:
    massHist = massDict[ntrkBin]
    massHist_passFiducial = massDict_passFiducialCut[ntrkBin]
    massHist_passDist = massDict_passDistCut[ntrkBin]
    massHist_passChi2 = massDict_passChi2Cut[ntrkBin]
    massHist_matVeto = massDict_matVeto[ntrkBin]
    massHist_passDVsel = massDict_passDVsel[ntrkBin]

    massHist.Draw("histo")
    drawSampleLabel(sampleLabel, ntrkBin, "No DV preselection")
    ATLASLabel(0.20, 0.955, label)
    c.Print("{}/{}.pdf".format(directory, "axMass_noDVsel_"+ntrkBin))

    massHist_passFiducial.Draw("histo")
    drawSampleLabel(sampleLabel, ntrkBin, "Pass fiducial cut")
    ATLASLabel(0.20, 0.955, label)
    c.Print("{}/{}.pdf".format(directory, "axMass_passFiducial_"+ntrkBin))

    massHist_passDist.Draw("histo")
    drawSampleLabel(sampleLabel, ntrkBin, "Pass PV-DV distance cut")
    ATLASLabel(0.20, 0.955, label)
    c.Print("{}/{}.pdf".format(directory, "axMass_passDist_"+ntrkBin))

    massHist_passChi2.Draw("histo")
    drawSampleLabel(sampleLabel, ntrkBin, "#chi^{2}/n_{DoF} cut")
    ATLASLabel(0.20, 0.955, label)
    c.Print("{}/{}.pdf".format(directory, "axMass_passChi2_"+ntrkBin))

    massHist_matVeto.Draw("histo")
    drawSampleLabel(sampleLabel, ntrkBin, "Pass material veto")
    ATLASLabel(0.20, 0.955, label)
    c.Print("{}/{}.pdf".format(directory, "axMass_matVeto_"+ntrkBin))

    massHist_passDVsel.Draw("histo")
    drawSampleLabel(sampleLabel, ntrkBin, "Pass DV preselection")
    ATLASLabel(0.20, 0.955, label)
    c.Print("{}/{}.pdf".format(directory, "axMass_passDVsel_"+ntrkBin))

    massHist.SetLineColor(colors[0])
    massHist_passFiducial.SetLineColor(colors[1])
    massHist_passDist.SetLineColor(colors[2])
    massHist_passChi2.SetLineColor(colors[3])
    massHist_matVeto.SetLineColor(colors[4])
    massHist_passDVsel.SetLineColor(colors[5])

    leg = r.TLegend(0.65, 0.45, 0.80, 0.65)
    decorateLeg(leg)
    
    leg.AddEntry(massDict[ntrkList[0]], "No DV selection", "l")
    leg.AddEntry(massDict_passFiducialCut[ntrkList[0]], "Pass fiducial cut", "l")
    leg.AddEntry(massDict_passDistCut[ntrkList[0]], "Pass distance cut", "l")
    leg.AddEntry(massDict_passChi2Cut[ntrkList[0]], "Pass #chi^{2}/n_{DoF} cut", "l")
    leg.AddEntry(massDict_matVeto[ntrkList[0]], "Pass material veto", "l")
    leg.AddEntry(massDict_passDVsel[ntrkList[0]], "Pass DV preselection", "l")

    massHist.Draw("histo")
    massHist_passFiducial.Draw("histo same")
    massHist_passDist.Draw("histo same")
    massHist_passChi2.Draw("histo same")
    massHist_matVeto.Draw("histo same")
    massHist_passDVsel.Draw("histo same")
    drawSampleLabel(sampleLabel, ntrkBin, "")
    ATLASLabel(0.20, 0.955, label)
    leg.Draw()
    c.Print("{}/{}.pdf".format(directory, "axMass_allCategory_"+ntrkBin))

    leg_passFid = r.TLegend(0.62, 0.50, 0.78, 0.68)
    decorateLeg(leg_passFid)
    leg_passFid.AddEntry(massDict[ntrkList[0]], "No DV selection", "l")
    leg_passFid.AddEntry(massDict_passFiducialCut[ntrkList[0]], "Pass fiducial cut", "l")

    ratio_fiducial = r.TRatioPlot(massHist_passFiducial, massHist)
    decorateRatioPlot(ratio_fiducial)
    leg_passFid.Draw()
    drawSampleLabel(sampleLabel, ntrkBin, "")
    ATLASLabel(0.15, 0.945, label)
    c.Print("{}/{}.pdf".format(directory, "ratioPlot_passFiducial_"+ntrkBin))
    

    leg_passDist = r.TLegend(0.62, 0.50, 0.78, 0.68)
    decorateLeg(leg_passDist)
    leg_passDist.AddEntry(massDict[ntrkList[0]], "No DV selection", "l")
    leg_passDist.AddEntry(massDict_passDistCut[ntrkList[0]], "Pass distance cut", "l")

    ratio_dist = r.TRatioPlot(massHist_passDist, massHist)
    decorateRatioPlot(ratio_dist)
    leg_passDist.Draw()
    drawSampleLabel(sampleLabel, ntrkBin, "")
    ATLASLabel(0.15, 0.945, label)
    c.Print("{}/{}.pdf".format(directory, "ratioPlot_passDist_"+ntrkBin))

    
    leg_passChi2 = r.TLegend(0.62, 0.50, 0.78, 0.68)
    decorateLeg(leg_passChi2)
    leg_passChi2.AddEntry(massDict[ntrkList[0]], "No DV selection", "l")
    leg_passChi2.AddEntry(massDict_passChi2Cut[ntrkList[0]], "Pass #chi^{2}/n_{DoF} cut", "l")

    ratio_chi2 = r.TRatioPlot(massHist_passChi2, massHist)
    decorateRatioPlot(ratio_chi2)
    leg_passChi2.Draw()
    drawSampleLabel(sampleLabel, ntrkBin, "")
    ATLASLabel(0.15, 0.945, label)
    c.Print("{}/{}.pdf".format(directory, "ratioPlot_passChi2_"+ntrkBin))


    leg_matVeto = r.TLegend(0.62, 0.50, 0.78, 0.68)
    decorateLeg(leg_matVeto)
    leg_matVeto.AddEntry(massDict[ntrkList[0]], "No DV selection", "l")
    leg_matVeto.AddEntry(massDict_matVeto[ntrkList[0]], "Pass material veto", "l")

    ratio_matVeto = r.TRatioPlot(massHist_matVeto, massHist)
    decorateRatioPlot(ratio_matVeto)
    leg_matVeto.Draw()
    drawSampleLabel(sampleLabel, ntrkBin, "")
    ATLASLabel(0.15, 0.945, label)
    c.Print("{}/{}.pdf".format(directory, "ratioPlot_matVeto_"+ntrkBin))


    leg_passDVsel = r.TLegend(0.62, 0.50, 0.78, 0.68)
    decorateLeg(leg_passDVsel)
    leg_passDVsel.AddEntry(massDict[ntrkList[0]], "No DV selection", "l")
    leg_passDVsel.AddEntry(massDict_passDVsel[ntrkList[0]], "Pass DV selection", "l")

    ratio_DVsel = r.TRatioPlot(massHist_passDVsel, massHist)
    decorateRatioPlot(ratio_DVsel)
    leg_passDVsel.Draw()
    drawSampleLabel(sampleLabel, ntrkBin, "")
    ATLASLabel(0.15, 0.945, label)
    c.Print("{}/{}.pdf".format(directory, "ratioPlot_passDVsel_"+ntrkBin))
    

outputFile.Write()
outputFile.Close()
