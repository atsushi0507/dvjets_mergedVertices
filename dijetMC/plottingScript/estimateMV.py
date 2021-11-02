import ROOT as r
import sys, os
sys.path.append("/Users/amizukam/DVJets/atlasstyle")
from AtlasStyle import *
from AtlasLabel import *
from ctypes import c_double as double
from utils import *
import argparse

r.gROOT.SetBatch()
SetAtlasStyle()

parser = argparse.ArgumentParser()
parser.add_argument("-sr", "--SR", required=True, help="Signal region")
parser.add_argument("-tag", required=True, help="The campaign tag")
parser.add_argument("-sf", "--suffix", default="", help="File suffix if needed")
parser.add_argument("-label", default="Internal", help="Label for ATLASLabel")
parser.add_argument("-n", "--nbins", type=int, default=1, help="Rebin")
parser.add_argument("-logy", action="store_true", help="Use logy?")
args = parser.parse_args()

tag = "mc16{}".format(args.tag)
SR = args.SR
suffix = args.suffix
label = args.label
logy = args.logy
nbins = args.nbins

dataSet = "{}_{}".format(tag, SR)
if (suffix != ""):
    dataSet += "_" + suffix

if (args.tag == "a"):
    year = 1516
if (args.tag == "d"):
    year = 17
if (args.tag == "e"):
    year = 18

bgFile = r.TFile("../outputFiles/dvMass_{}_{}.root".format(tag, SR), "READ")
mvFile = r.TFile("../outputFiles/extractFactor_{}.root".format(dataSet), "READ")
weightFile = r.TFile("../outputFiles/extractFactor_{}_weighted.root".format(dataSet), "READ")
dataFile = r.TFile("/Users/amizukam/DVJets/trackCleaning/rootfiles/data{}_DV_mass_{}.root".format(year, SR), "READ")
sigFile = r.TFile("../outputFiles/significance_{}_{}.root".format(tag, SR), "READ")
if (not bgFile.IsOpen or not mvFile.IsOpen() or not weightFile.IsOpen() or not dataFile.IsOpen() or not sigFile.IsOpen()):
    print(">> File not found. Stop processing...")
    exit()

plotType = "estimateMV"
directory = "pdfs/" + plotType + "/" + dataSet
if (not os.path.isdir(directory)):
    os.makedirs(directory)

ntrkList = ["Ntrk4", "Ntrk5", "Ntrk6"]
typeList = ["dvType1", "dvType2", "dvType3", "dvType5", "dvType6"]
legLabel = {"dvType1": "G4 DV",
            "dvType2": "G4 + PU DV",
            "dvType3": "G4 + Gen DV",
            "dvType4": "PU DV",
            "dvType5": "Gen + PU DV",
            "dvType6": "Gen DV",
            "dvType7": "Combination DV"
            }
colors = [r.kBlack, r.kRed, r.kBlue, r.kGreen, r.kOrange, r.kCyan, r.kViolet]
h_bg_noSel = {}
h_bg_DVSel = {}
h_bg_fullSel = {}
h_bg_tc = {}
h_mv_noSel = {}
h_mv_DVSel = {}
h_mv_fullSel = {}
h_mv_tc = {}
h_data_noSel = {}
h_data_DVSel = {}
h_data_fullSel = {}
h_data_tc = {}
h_mvMass_type_noSel = {}
h_mvMass_type_DVSel = {}
h_mvMass_type_fullSel = {}
h_mvMass_type_tc = {}
h_sigMass = {}
h_weightMass_noSel = {}
h_weightMass_DVSel = {}
h_weightMass_fullSel = {}
h_weightMass_tc = {}
h_mvMass_type2_noSel = {}
h_mvMass_type_passFiducial = {}
h_mvMass_type_passDist = {}
h_mvMass_type_passChiSq = {}
h_mvMass_type_passMaterial = {}
h_dvMass_selected = {}
h_dvMass_selected_tc = {}
h_dvtrack_pt_selected = {}
h_mvtrack_pt_selected = {}
h_dvtrack_d0Selected = {}
h_mvtrack_d0Selected = {}
h_dvtrack_d0 = {}
h_mvtrack_d0 = {}
for ntrk in ntrkList:
    h_bg_noSel[ntrk] = bgFile.Get("dvMass_noSelection_{}".format(ntrk)).Rebin(nbins)
    h_bg_DVSel[ntrk] = bgFile.Get("dvMass_DVSel_{}".format(ntrk)).Rebin(nbins)
    h_bg_fullSel[ntrk] = bgFile.Get("dvMass_fullSel_{}".format(ntrk)).Rebin(5)
    h_bg_tc[ntrk] = bgFile.Get("dvMass_tc_{}".format(ntrk)).Rebin(nbins)
    h_mv_noSel[ntrk] = mvFile.Get("mvMass_"+ntrk).Rebin(nbins)
    h_mv_DVSel[ntrk] = mvFile.Get("mvMass_DVSel_"+ntrk).Rebin(nbins)
    h_mv_fullSel[ntrk] = mvFile.Get("mvMass_fullSel_"+ntrk).Rebin(5)
    h_mv_tc[ntrk] = mvFile.Get("mvMass_trackCleaning_"+ntrk).Rebin(nbins)
    h_data_noSel[ntrk] = dataFile.Get("mDV_"+ntrk).Rebin(nbins)
    h_data_DVSel[ntrk] = dataFile.Get("mDV_DVSel_"+ntrk).Rebin(nbins)
    h_data_fullSel[ntrk] = dataFile.Get("mDV_fullSel_"+ntrk).Rebin(5)
    h_data_tc[ntrk] = dataFile.Get("mDV_tc_"+ntrk).Rebin(5)
    h_sigMass[ntrk] = sigFile.Get("mvMass_mixed_"+ntrk).Rebin(nbins)
    h_weightMass_noSel[ntrk] = weightFile.Get("mvMass_"+ntrk).Rebin(nbins)
    h_weightMass_DVSel[ntrk] = weightFile.Get("mvMass_DVSel_"+ntrk).Rebin(nbins)
    h_weightMass_fullSel[ntrk] = weightFile.Get("mvMass_fullSel_"+ntrk).Rebin(5)
    h_weightMass_tc[ntrk] = weightFile.Get("mvMass_trackCleaning_"+ntrk).Rebin(nbins)
    h_mvMass_type2_noSel[ntrk] = mvFile.Get("mvMass_dvType2_"+ntrk+"_noSel").Rebin(nbins)
    h_mvMass_type_passFiducial[ntrk] = mvFile.Get("mvMass_dvType2_"+ntrk+"_passFiducial").Rebin(nbins)
    h_mvMass_type_passDist[ntrk] = mvFile.Get("mvMass_dvType2_"+ntrk+"_passDist").Rebin(nbins)
    h_mvMass_type_passChiSq[ntrk] = mvFile.Get("mvMass_dvType2_"+ntrk+"_passChiSq").Rebin(nbins)
    h_mvMass_type_passMaterial[ntrk] = mvFile.Get("mvMass_dvType2_"+ntrk+"_passMaterial_strict").Rebin(nbins)
    h_dvMass_selected[ntrk] = bgFile.Get("dvMass_selected_"+ntrk).Rebin(nbins)
    h_dvMass_selected_tc[ntrk] = bgFile.Get("dvMass_selected_tc_"+ntrk).Rebin(nbins)

    h_dvtrack_pt_selected[ntrk] = bgFile.Get("mvtrack_pt_selected_"+ntrk).Rebin(10)
    h_mvtrack_pt_selected[ntrk] = mvFile.Get("mvtrack_allPtSel_"+ntrk+"_noSel").Rebin(10)
    h_dvtrack_d0Selected[ntrk] = bgFile.Get("mvtrack_d0Selected_"+ntrk).Rebin(2)
    h_mvtrack_d0Selected[ntrk] = mvFile.Get("mvtrack_d0sig_"+ntrk+"_noSel").Rebin(2)
    h_dvtrack_d0[ntrk] = bgFile.Get("mvtrack_d0_"+ntrk).Rebin(10)
    h_mvtrack_d0[ntrk] = mvFile.Get("mvtrack_d0_selected_"+ntrk+"_noSel")
    
    h_mvMass_type_noSel[ntrk] = {}
    h_mvMass_type_DVSel[ntrk] = {}
    h_mvMass_type_fullSel[ntrk] = {}
    h_mvMass_type_tc[ntrk] = {}
    for dvtype in typeList:
        h_mvMass_type_noSel[ntrk][dvtype] = weightFile.Get("mvMass_{}_{}_{}".format(dvtype, ntrk, "noSel")).Rebin(nbins)
        h_mvMass_type_DVSel[ntrk][dvtype] = weightFile.Get("mvMass_{}_{}_{}".format(dvtype, ntrk, "DVSel")).Rebin(nbins)
        h_mvMass_type_fullSel[ntrk][dvtype] = weightFile.Get("mvMass_{}_{}_{}".format(dvtype, ntrk, "fullSel")).Rebin(nbins)
        h_mvMass_type_tc[ntrk][dvtype] = weightFile.Get("mvMass_{}_{}_{}".format(dvtype, ntrk, "trackCleaning")).Rebin(nbins)

outputFile = r.TFile("rootfiles/mvMassTemplate_{}.root".format(SR), "RECREATE")

c = r.TCanvas("c", "c", 800, 700)
c.cd()
sampleLabel = prepareLatex()
if (logy):
    c.SetLogy(True)
for ntrk in ntrkList:
    bg_noSel = h_bg_noSel[ntrk]
    bg_DVSel = h_bg_DVSel[ntrk]
    bg_fullSel = h_bg_fullSel[ntrk]
    bg_tc = h_bg_tc[ntrk]
    mv_noSel = h_mv_noSel[ntrk]
    mv_DVSel = h_mv_DVSel[ntrk]
    mv_fullSel = h_mv_fullSel[ntrk]
    mv_tc = h_mv_tc[ntrk]
    data_noSel = h_data_noSel[ntrk]
    data_DVSel = h_data_DVSel[ntrk]
    data_fullSel = h_data_fullSel[ntrk]
    data_tc = h_data_tc[ntrk]
    sigMass = h_sigMass[ntrk]
    weightMass_noSel = h_weightMass_noSel[ntrk]
    weightMass_DVSel = h_weightMass_DVSel[ntrk]
    weightMass_fullSel = h_weightMass_fullSel[ntrk]
    weightMass_tc = h_weightMass_tc[ntrk]
    mv_noSel_type = h_mvMass_type_noSel[ntrk]["dvType2"]
    mv_DVSel_type = h_mvMass_type_DVSel[ntrk]["dvType2"]
    mv_fullSel_type = h_mvMass_type_fullSel[ntrk]["dvType2"]
    mv_tc_type = h_mvMass_type_tc[ntrk]["dvType2"]
    mvMass_type_noSel = h_mvMass_type2_noSel[ntrk]
    mvMass_type_passFiducial = h_mvMass_type_passFiducial[ntrk]
    mvMass_type_passDist = h_mvMass_type_passDist[ntrk]
    mvMass_type_passChiSq = h_mvMass_type_passChiSq[ntrk]
    mvMass_type_passMaterial = h_mvMass_type_passMaterial[ntrk]
    dvMass_selected = h_dvMass_selected[ntrk]
    dvMass_selected_tc = h_dvMass_selected_tc[ntrk]
    dvtrack_pt_selected = h_dvtrack_pt_selected[ntrk]
    mvtrack_pt_selected = h_mvtrack_pt_selected[ntrk]
    dvtrack_d0Selected = h_dvtrack_d0Selected[ntrk]
    mvtrack_d0Selected = h_mvtrack_d0Selected[ntrk]
    dvtrack_d0 = h_dvtrack_d0[ntrk]
    mvtrack_d0 = h_mvtrack_d0[ntrk]

    setHistColor(mv_noSel, r.kRed)
    setHistColor(mv_DVSel, r.kRed)
    setHistColor(mv_fullSel, r.kRed)
    setHistColor(mv_tc, r.kRed)
    setHistColor(bg_noSel, r.kBlue)
    setHistColor(bg_DVSel, r.kBlue)
    setHistColor(bg_fullSel, r.kBlue)
    setHistColor(bg_tc, r.kBlue)
    setHistColor(weightMass_noSel, r.kRed)
    setHistColor(weightMass_DVSel, r.kRed)
    setHistColor(weightMass_fullSel, r.kRed)
    setHistColor(weightMass_tc, r.kRed)
    setHistColor(sigMass, r.kGreen)
    setHistColor(mv_noSel_type, r.kViolet)
    setHistColor(mv_DVSel_type, r.kViolet)
    setHistColor(mv_fullSel_type, r.kViolet)
    setHistColor(dvtrack_pt_selected, r.kRed)
    setHistColor(dvtrack_d0Selected, r.kRed)
    setHistColor(dvtrack_d0, r.kRed)

    bg_noSel.SetMinimum(0.5)
    bg_DVSel.SetMinimum(0.05)
    bg_fullSel.SetMinimum(0.005)
    bg_tc.SetMinimum(0.05)
    bg_noSel.SetMaximum(bg_noSel.GetMaximum()*3.0)
    bg_DVSel.SetMaximum(bg_DVSel.GetMaximum()*10.0)
    bg_fullSel.SetMaximum(bg_fullSel.GetMaximum()*3.0)
    bg_fullSel.GetXaxis().SetRange(1, bg_fullSel.FindBin(20.))

    leg = r.TLegend(0.60, 0.48, 0.85, 0.63)
    decorateLeg(leg)

    leg.AddEntry(data_noSel, "Data", "pe")
    leg.AddEntry(bg_noSel, tag, "l")
    leg.AddEntry(weightMass_noSel, "Merged Vertices", "l")
    leg.AddEntry(sigMass, "Data-driven template", "l")

    firstBin =1
    lastBin = bg_noSel.GetNbinsX() + 1

    # Event selection only
    errDV = double(0.)
    errMV = double(0.)
    errMV_g4pu = double(0.)
    nDV = bg_noSel.IntegralAndError(firstBin, lastBin, errDV)
    nMV = weightMass_noSel.IntegralAndError(firstBin, lastBin, errMV)
    nMV_g4pu = mv_noSel_type.IntegralAndError(firstBin, lastBin, errMV_g4pu)
    sigMass.Sumw2()
    sigLastBin = sigMass.GetNbinsX() + 1
    bin10 = sigMass.FindBin(10.)
    sf = nMV_g4pu / sigMass.Integral(1, sigLastBin)
    sigMass.Scale(sf)
    errSRMV = double(0.)
    nSRMV = sigMass.IntegralAndError(bin10, sigLastBin, errSRMV)
    errSig = double(0.)
    sigMV = sigMass.IntegralAndError(firstBin, sigLastBin, errSig)
    bg_noSel.Draw("hist e0")
    data_noSel.Draw("e0 same")
    weightMass_noSel.Draw("hist e0 same")
    sigMass.Draw("hist e0 same")
    ATLASLabel(0.20, 0.955, label)
    sampleLabel.DrawLatex(0.615, 0.93, "{}, {}".format(tag, SR))
    sampleLabel.DrawLatex(0.615, 0.88, getNtrkLabel(ntrk)+", event selection")
    sampleLabel.DrawLatex(0.615, 0.83, "BG: {:.2f} #pm {:.2f}".format(nDV, errDV.value))
    sampleLabel.DrawLatex(0.615, 0.78, "MV: {:.2f} #pm {:.2f}".format(nMV, errMV.value))
    sampleLabel.DrawLatex(0.615, 0.73, "G4 + PU: {:.2f} #pm {:.2f}".format(sigMV, errSig.value))
    sampleLabel.DrawLatex(0.615, 0.68, "m_{DV} > 10 GeV:"+" {:.2f} #pm {:.2f}".format(nSRMV, errSRMV.value))
    leg.Draw()
    c.Print("{}/{}.pdf".format(directory, "mass_noSel_"+ntrk))
    bin20 = sigMass.FindBin(20.)
    errmv20 = double(0.)
    mv20 = sigMass.IntegralAndError(bin20, sigLastBin, errmv20)
    if (ntrk == "Ntrk4"):
        print(ntrk)
        print("m > 20 GeV: {:.2f} +- {:.2f}".format(mv20, errmv20.value))
    else:
        print(ntrk)
        print("m > 10 GeV: {:.2f} +- {:.2f}".format(sigMV, errSig.value))

    sigMass_DVSel = sigMass.Clone("sigMass_DVSel")
    sigMass_fullSel = sigMass.Clone("sigMass_fullSel_"+ntrk)
    sigMass_tc = sigMass.Clone("sigMass_tc")

    # DV selection
    errNoSel = double(0.)
    errPassFiducial = double(0.)
    errPassDist = double(0.)
    errPassChiSq = double(0.)
    errPassMaterial = double(0.)
    nMV_noSel = mvMass_type_noSel.IntegralAndError(firstBin, lastBin, errNoSel)
    nMV_passFiducial = mvMass_type_passFiducial.IntegralAndError(firstBin, lastBin, errPassFiducial)
    nMV_passDist= mvMass_type_passDist.IntegralAndError(firstBin, lastBin, errPassDist)
    nMV_passChiSq = mvMass_type_passChiSq.IntegralAndError(firstBin, lastBin, errPassChiSq)
    nMV_passMaterial = mvMass_type_passMaterial.IntegralAndError(firstBin, lastBin, errPassMaterial)

    passFiducialRate, errRate_passFiducial = divideError(nMV_passFiducial, nMV_noSel, errPassFiducial.value, errNoSel.value)
    passDistRate, errRate_passDist = divideError(nMV_passDist, nMV_noSel, errPassDist.value, errNoSel.value)
    passChiSqRate, errRate_passChiSq = divideError(nMV_passChiSq, nMV_noSel, errPassChiSq.value, errNoSel.value)
    passMaterialRate, errRate_passMaterial = divideError(nMV_passMaterial, nMV_noSel, errPassMaterial.value, errNoSel.value)
    dvSelRate = passFiducialRate * passDistRate * passChiSqRate * passMaterialRate
    print(dvSelRate)
    print(passFiducialRate, passDistRate, passChiSqRate, passMaterialRate)

    #sigMass_DVSel.Sumw2()
    sigMass_DVSel.Scale(dvSelRate)

    errDV_DVSel = double(0.)
    errMV_DVSel = double(0.)
    errMV_DVSel_g4pu = double(0.)
    errSig_DVSel = double(0.)
    errSRMV_DVSel = double(0.)
    nDV_DVSel = bg_DVSel.IntegralAndError(firstBin, lastBin, errDV_DVSel)
    nMV_DVSel = weightMass_DVSel.IntegralAndError(firstBin, lastBin, errMV_DVSel)
    nMV_DVSel_g4pu = mv_DVSel_type.IntegralAndError(firstBin, lastBin, errMV_DVSel_g4pu)
    sigMV_DVSel = sigMass_DVSel.IntegralAndError(firstBin, sigLastBin, errSig_DVSel)
    nSRMV_DVSel = sigMass_DVSel.IntegralAndError(bin10, sigLastBin, errSRMV_DVSel)

    bg_DVSel.Draw("hist e0")
    data_DVSel.Draw("e0 same")
    weightMass_DVSel.Draw("hist e0 same")
    sigMass_DVSel.Draw("hist e0 same")
    ATLASLabel(0.20, 0.955, label)
    sampleLabel.DrawLatex(0.615, 0.93, "{}, {}".format(tag, SR))
    sampleLabel.DrawLatex(0.615, 0.88, getNtrkLabel(ntrk)+", DV selection")
    sampleLabel.DrawLatex(0.615, 0.83, "BG: {:.2f} #pm {:.2f}".format(nDV_DVSel, errDV_DVSel.value))
    sampleLabel.DrawLatex(0.615, 0.78, "MV: {:.2f} #pm {:.2f}".format(nMV_DVSel, errMV_DVSel.value))
    sampleLabel.DrawLatex(0.615, 0.73, "G4 + PU: {:.2f} #pm {:.3f}".format(sigMV_DVSel, errSig_DVSel.value))
    sampleLabel.DrawLatex(0.615, 0.68, "m_{DV} > 10 GeV: :" + " {:.2f} #pm {:.3f}".format(nSRMV_DVSel, errSRMV_DVSel.value))
    leg.Draw()
    c.Print("{}/{}.pdf".format(directory, "mass_DVSel_"+ntrk))

    # Track cleaning
    errNoSel = double(0.)
    errTC = double(0.)
    bin5 = dvMass_selected.FindBin(5.)
    nNoSel = dvMass_selected.IntegralAndError(bin5, lastBin, errNoSel)
    nTC = dvMass_selected_tc.IntegralAndError(bin5, lastBin, errTC)
    rateTC, errRateTC = divideError(nTC, nNoSel, errTC.value, errNoSel.value)
    print(nTC, nNoSel)
    print(rateTC, errRateTC)

    #sigMass_tc.Sumw2()
    sigMass_tc.Scale(rateTC)

    errDV_tc = double(0.)
    errMV_tc = double(0.)
    errMV_tc_g4pu = double(0.)
    errSig_tc = double(0.)
    errSRMV_tc = double(0.)
    nDV_tc = bg_tc.IntegralAndError(firstBin, lastBin, errDV_tc)
    nMV_tc = weightMass_tc.IntegralAndError(firstBin, lastBin, errMV_tc)
    nMV_tc_g4pu = mv_tc_type.IntegralAndError(firstBin, lastBin, errMV_tc_g4pu)
    sigMV_tc = sigMass_tc.IntegralAndError(firstBin, sigLastBin, errSig_tc)
    nSRMV_tc = sigMass_tc.IntegralAndError(bin10, sigLastBin, errSRMV_tc)
    
    bg_tc.Draw("hist e0")
    data_tc.Draw("e0 same")
    weightMass_tc.Draw("hist e0 same")
    sigMass_tc.Draw("hist e0 same")
    ATLASLabel(0.20, 0.955, label)
    sampleLabel.DrawLatex(0.615, 0.93, "{}, {}".format(tag, SR))
    sampleLabel.DrawLatex(0.615, 0.88, getNtrkLabel(ntrk)+", Track cleaning")
    sampleLabel.DrawLatex(0.615, 0.83, "BG: {:.2f} #pm {:.2f}".format(nDV_tc, errDV_tc.value))
    sampleLabel.DrawLatex(0.615, 0.78, "MV: {:.2f} #pm {:.2f}".format(nMV_tc, errMV_tc.value))
    sampleLabel.DrawLatex(0.615, 0.73, "G4 + PU: {:.2f} #pm {:.3f}".format(sigMV_tc, errSig_tc.value))
    sampleLabel.DrawLatex(0.615, 0.68, "m_{DV} > 10 GeV: :" + " {:.2f} #pm {:.3f}".format(nSRMV_tc, errSRMV_tc.value))
    leg.Draw()
    c.Print("{}/{}.pdf".format(directory, "mass_tc_"+ntrk))

    # Full selection
    #sigMass_fullSel.Sumw2()
    sigMass_fullSel.Scale(dvSelRate * rateTC)

    errDV_fullSel = double(0.)
    errMV_fullSel = double(0.)
    errMV_fullSel_g4pu = double(0.)
    errSig_fullSel = double(0.)
    errSRMV_fullSel = double(0.)
    nDV_fullSel = bg_fullSel.IntegralAndError(firstBin, lastBin, errDV_fullSel)
    nMV_fullSel = weightMass_fullSel.IntegralAndError(firstBin, lastBin, errMV_fullSel)
    nMV_fullSel_g4pu = mv_fullSel_type.IntegralAndError(firstBin, lastBin, errMV_fullSel_g4pu)
    sigMV_fullSel = sigMass_fullSel.IntegralAndError(firstBin, sigLastBin, errSig_fullSel)
    nSRMV_fullSel = sigMass_fullSel.IntegralAndError(bin10, sigLastBin, errSRMV_fullSel)
    
    bg_fullSel.Draw("hist e0")
    data_fullSel.Draw("e0 same")
    weightMass_fullSel.Draw("hist e0 same")
    sigMass_fullSel.Draw("hist e0 same")
    ATLASLabel(0.20, 0.955, label)
    sampleLabel.DrawLatex(0.615, 0.93, "{}, {}".format(tag, SR))
    sampleLabel.DrawLatex(0.615, 0.88, getNtrkLabel(ntrk)+", Full selection")
    sampleLabel.DrawLatex(0.615, 0.83, "BG: {:.2f} #pm {:.2f}".format(nDV_fullSel, errDV_fullSel.value))
    sampleLabel.DrawLatex(0.615, 0.78, "MV: {:.2f} #pm {:.2f}".format(nMV_fullSel, errMV_fullSel.value))
    sampleLabel.DrawLatex(0.615, 0.73, "G4 + PU: {:.2f} #pm {:.3f}".format(sigMV_fullSel, errSig_fullSel.value))
    sampleLabel.DrawLatex(0.615, 0.68, "m_{DV} > 10 GeV: :" + " {:.2f} #pm {:.3f}".format(nSRMV_fullSel, errSRMV_fullSel.value))
    leg.Draw()
    c.Print("{}/{}.pdf".format(directory, "mass_fullSel_"+ntrk))

    sigMass_fullSel.Write()

    # Track properties
    leg_track = r.TLegend(0.60, 0.65, 0.85, 0.80)
    decorateLeg(leg_track)

    leg_track.AddEntry(mvtrack_pt_selected, "MV track", "l")
    leg_track.AddEntry(dvtrack_pt_selected, "DV track", "l")

    # Pt
    dvtrack_pt_selected.Sumw2()
    lastBin = dvtrack_pt_selected.GetNbinsX() + 1
    sf = mvtrack_pt_selected.Integral(1, lastBin) / dvtrack_pt_selected.Integral(1, lastBin)
    dvtrack_pt_selected.Scale(sf)

    mvtrack_pt_selected.Draw("hist e0")
    dvtrack_pt_selected.Draw("hist e0 same")
    ATLASLabel(0.20, 0.955, label)
    sampleLabel.DrawLatex(0.615, 0.90, "{}, {}".format(tag, SR))
    sampleLabel.DrawLatex(0.615, 0.85, getNtrkLabel(ntrk))
    leg_track.Draw()
    c.Print("{}/{}.pdf".format(directory, "mvtrack_pt_selected_"+ntrk))

    # d0 significance
    dvtrack_d0Selected.Sumw2()
    lastBin = dvtrack_d0Selected.GetNbinsX() + 1
    sf = mvtrack_d0Selected.Integral(1, lastBin) / dvtrack_d0Selected.Integral(1, lastBin)
    dvtrack_d0Selected.Scale(sf)

    mvtrack_d0Selected.Draw("hist e0")
    dvtrack_d0Selected.Draw("hist e0 same")
    ATLASLabel(0.20, 0.955, label)
    sampleLabel.DrawLatex(0.615, 0.90, "{}, {}".format(tag, SR))
    sampleLabel.DrawLatex(0.615, 0.85, getNtrkLabel(ntrk))
    leg_track.Draw()
    c.Print("{}/{}.pdf".format(directory, "mvtrack_d0Selected_selected_"+ntrk))

    # d0
    mvtrack_d0.GetXaxis().SetRange(1, mvtrack_d0.FindBin(25.))
    dvtrack_d0.Sumw2()
    lastBin = dvtrack_d0.GetNbinsX() 
    sf = mvtrack_d0.Integral(1, lastBin) / dvtrack_d0.Integral(1, lastBin)
    dvtrack_d0.Scale(sf)

    mvtrack_d0.Draw("hist e0")
    dvtrack_d0.Draw("hist e0 same")
    ATLASLabel(0.20, 0.955, label)
    sampleLabel.DrawLatex(0.615, 0.90, "{}, {}".format(tag, SR))
    sampleLabel.DrawLatex(0.615, 0.85, getNtrkLabel(ntrk))
    leg_track.Draw()
    c.Print("{}/{}.pdf".format(directory, "mvtrack_d0_selected_"+ntrk))

#outputFile.Write()
outputFile.Close()
