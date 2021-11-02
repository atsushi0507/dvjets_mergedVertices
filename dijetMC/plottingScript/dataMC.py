import ROOT as r
import os, sys
sys.path.append("/Users/amizukam/DVJets/atlasstyle")
from AtlasStyle import *
from AtlasLabel import *
from utils import *
import argparse

r.gROOT.SetBatch()
SetAtlasStyle()

parser = argparse.ArgumentParser()
parser.add_argument("-sr", "--SR", required=True, help="Signal region, 'HighPtSR' or 'TracklessSR'")
parser.add_argument("-label", default="Internal", help="Label for ATLASLabel")
parser.add_argument("-n", "--nbins", default=1, type=int, help="Divide number of histograms")
args = parser.parse_args()

SR = args.SR
label = args.label

plotType = "dataMC"
directory = "pdfs/" + plotType
if (not os.path.isdir(directory)):
    os.makedirs(directory)

dataDir = "/Users/amizukam/DVJets/trackCleaning/rootfiles/"
data1516File = r.TFile(dataDir + "data1516_DV_mass_{}.root".format(SR), "READ")
data17File = r.TFile(dataDir + "data17_DV_mass_{}.root".format(SR), "READ")
data18File = r.TFile(dataDir + "data18_DV_mass_{}.root".format(SR), "READ")
mc16a = r.TFile("../outputFiles/dvMass_mc16a_{}.root".format(SR), "READ")
mc16d = r.TFile("../outputFiles/dvMass_mc16d_{}.root".format(SR), "READ")
mc16e = r.TFile("../outputFiles/dvMass_mc16e_{}.root".format(SR), "READ")

ntrkList = ["Ntrk4", "Ntrk5", "Ntrk6"]

massDict_1516_noSel = {}
massDict_1516_DVSel = {}
massDict_1516_fullSel = {}
massDict_17_noSel = {}
massDict_17_DVSel = {}
massDict_17_fullSel = {}
massDict_18_noSel = {}
massDict_18_DVSel = {}
massDict_18_fullSel = {}
mc16a_noSel = {}
mc16a_DVSel = {}
mc16a_fullSel = {}
mc16d_noSel = {}
mc16d_DVSel = {}
mc16d_fullSel = {}
mc16e_noSel = {}
mc16e_DVSel = {}
mc16e_fullSel = {}
nbins = args.nbins
for ntrk in ntrkList:
    massDict_1516_noSel[ntrk] = data1516File.Get("mDV_{}".format(ntrk)).Rebin(nbins)
    massDict_1516_DVSel[ntrk] = data1516File.Get("mDV_DVSel_{}".format(ntrk)).Rebin(nbins)
    massDict_1516_fullSel[ntrk] = data1516File.Get("mDV_fullSel_{}".format(ntrk)).Rebin(nbins)
    massDict_17_noSel[ntrk] = data17File.Get("mDV_{}".format(ntrk)).Rebin(nbins)
    massDict_17_DVSel[ntrk] = data17File.Get("mDV_DVSel_{}".format(ntrk)).Rebin(nbins)
    massDict_17_fullSel[ntrk] = data17File.Get("mDV_fullSel_{}".format(ntrk)).Rebin(nbins)
    massDict_18_noSel[ntrk] = data18File.Get("mDV_{}".format(ntrk)).Rebin(nbins)
    massDict_18_DVSel[ntrk] = data18File.Get("mDV_DVSel_{}".format(ntrk)).Rebin(nbins)
    massDict_18_fullSel[ntrk] = data18File.Get("mDV_fullSel_{}".format(ntrk)).Rebin(nbins)
    mc16a_noSel[ntrk] = mc16a.Get("dvMass_noSelection_{}".format(ntrk)).Rebin(nbins)
    mc16a_DVSel[ntrk] = mc16a.Get("dvMass_DVSel_{}".format(ntrk)).Rebin(nbins)
    mc16a_fullSel[ntrk] = mc16a.Get("dvMass_fullSel_{}".format(ntrk)).Rebin(nbins)
    mc16d_noSel[ntrk] = mc16d.Get("dvMass_noSelection_{}".format(ntrk)).Rebin(nbins)
    mc16d_DVSel[ntrk] = mc16d.Get("dvMass_DVSel_{}".format(ntrk)).Rebin(nbins)
    mc16d_fullSel[ntrk] = mc16d.Get("dvMass_fullSel_{}".format(ntrk)).Rebin(nbins)
    mc16e_noSel[ntrk] = mc16e.Get("dvMass_noSelection_{}".format(ntrk)).Rebin(nbins)
    mc16e_DVSel[ntrk] = mc16e.Get("dvMass_DVSel_{}".format(ntrk)).Rebin(nbins)
    mc16e_fullSel[ntrk] = mc16e.Get("dvMass_fullSel_{}".format(ntrk)).Rebin(nbins)

c = r.TCanvas("c", "c", 800, 700)
c.cd()
sampleLabel = prepareLatex()
for ntrk in ntrkList:
    mass1516_noSel = massDict_1516_noSel[ntrk]
    mass1516_DVSel = massDict_1516_DVSel[ntrk]
    mass1516_fullSel = massDict_1516_fullSel[ntrk]
    mass17_noSel = massDict_17_noSel[ntrk]
    mass17_DVSel = massDict_17_DVSel[ntrk]
    mass17_fullSel = massDict_17_fullSel[ntrk]
    mass18_noSel = massDict_18_noSel[ntrk]
    mass18_DVSel = massDict_18_DVSel[ntrk]
    mass18_fullSel = massDict_18_fullSel[ntrk]
    mass16a_noSel = mc16a_noSel[ntrk]
    mass16a_DVSel = mc16a_DVSel[ntrk]
    mass16a_fullSel = mc16a_fullSel[ntrk]
    mass16d_noSel = mc16d_noSel[ntrk]
    mass16d_DVSel = mc16d_DVSel[ntrk]
    mass16d_fullSel = mc16d_fullSel[ntrk]
    mass16e_noSel = mc16e_noSel[ntrk]
    mass16e_DVSel = mc16e_DVSel[ntrk]
    mass16e_fullSel = mc16e_fullSel[ntrk]

    setHistColor(mass16a_noSel, r.kRed)
    setHistColor(mass16a_DVSel, r.kRed)
    setHistColor(mass16a_fullSel, r.kRed)
    setHistColor(mass16d_noSel, r.kRed)
    setHistColor(mass16d_DVSel, r.kRed)
    setHistColor(mass16d_fullSel, r.kRed)
    setHistColor(mass16e_noSel, r.kRed)
    setHistColor(mass16e_DVSel, r.kRed)
    setHistColor(mass16e_fullSel, r.kRed)

    ### 1516 vs mc16a
    # No Selection
    leg_noSel_a = r.TLegend(0.62, 0.60, 0.85, 0.80)
    decorateLeg(leg_noSel_a)
    leg_noSel_a.AddEntry(mass1516_noSel, "Data", "l")
    leg_noSel_a.AddEntry(mass16a_noSel, "MC16a", "l")
    mass1516_noSel.Draw("hist")
    mass16a_noSel.Draw("hist e0 same")
    ATLASLabel(0.20, 0.955, label)
    leg_noSel_a.Draw()
    sampleLabel.DrawLatex(0.60, 0.90, getNtrkLabel(ntrk))
    sampleLabel.DrawLatex(0.60, 0.85, "{}, no DV selection".format(SR))
    c.Print("{}/{}.pdf".format(directory, "dvMass_1516_{}_noSel_{}".format(SR, ntrk)))

    # DV Selection
    leg_DVSel_a = r.TLegend(0.62, 0.60, 0.85, 0.80)
    decorateLeg(leg_DVSel_a)
    leg_DVSel_a.AddEntry(mass1516_DVSel, "Data:1516", "l")
    leg_DVSel_a.AddEntry(mass16a_DVSel, "MC16a", "l")
    mass1516_DVSel.Draw("hist")
    mass16a_DVSel.Draw("hist e0 same")
    ATLASLabel(0.20, 0.955, label)
    leg_DVSel_a.Draw()
    sampleLabel.DrawLatex(0.60, 0.90, getNtrkLabel(ntrk))
    sampleLabel.DrawLatex(0.60, 0.85, "{}, DV selection".format(SR))
    c.Print("{}/{}.pdf".format(directory, "dvMass_1516_{}_DVSel_{}".format(SR, ntrk)))

    # Full Selection
    leg_fullSel_a = r.TLegend(0.62, 0.60, 0.85, 0.80)
    decorateLeg(leg_fullSel_a)
    leg_fullSel_a.AddEntry(mass1516_fullSel, "Data:1516", "l")
    leg_fullSel_a.AddEntry(mass16a_fullSel, "MC16a", "l")
    mass1516_fullSel.Draw("hist")
    mass16a_fullSel.Draw("hist e0 same")
    ATLASLabel(0.20, 0.955, label)
    leg_fullSel_a.Draw()
    sampleLabel.DrawLatex(0.60, 0.90, getNtrkLabel(ntrk))
    sampleLabel.DrawLatex(0.60, 0.85, "{}, full selection".format(SR))
    c.Print("{}/{}.pdf".format(directory, "dvMass_1516_{}_fullSel_{}".format(SR, ntrk)))

    ### 17 vs mc16d
    # No Selection
    leg_noSel_d = r.TLegend(0.62, 0.60, 0.85, 0.80)
    decorateLeg(leg_noSel_d)
    leg_noSel_d.AddEntry(mass17_noSel, "Data:1516", "l")
    leg_noSel_d.AddEntry(mass16d_noSel, "MC16d", "l")
    mass17_noSel.Draw("hist")
    mass16d_noSel.Draw("hist e0 same")
    ATLASLabel(0.20, 0.955, label)
    leg_noSel_d.Draw()
    sampleLabel.DrawLatex(0.60, 0.90, getNtrkLabel(ntrk))
    sampleLabel.DrawLatex(0.60, 0.85, "{}, no DV selection".format(SR))
    c.Print("{}/{}.pdf".format(directory, "dvMass_17_{}_noSel_{}".format(SR, ntrk)))

    # DV Selection
    leg_DVSel_d = r.TLegend(0.62, 0.60, 0.85, 0.80)
    decorateLeg(leg_DVSel_d)
    leg_DVSel_d.AddEntry(mass17_DVSel, "Data:17", "l")
    leg_DVSel_d.AddEntry(mass16d_DVSel, "MC16d", "l")
    mass17_DVSel.Draw("hist")
    mass16d_DVSel.Draw("hist e0 same")
    ATLASLabel(0.20, 0.955, label)
    leg_DVSel_d.Draw()
    sampleLabel.DrawLatex(0.60, 0.90, getNtrkLabel(ntrk))
    sampleLabel.DrawLatex(0.60, 0.85, "{}, DV selection".format(SR))
    c.Print("{}/{}.pdf".format(directory, "dvMass_17_{}_DVSel_{}".format(SR, ntrk)))

    # Full Selection
    leg_fullSel_d = r.TLegend(0.62, 0.60, 0.85, 0.80)
    decorateLeg(leg_fullSel_d)
    leg_fullSel_d.AddEntry(mass17_fullSel, "Data:17", "l")
    leg_fullSel_d.AddEntry(mass16d_fullSel, "MC16d", "l")
    mass17_fullSel.Draw("hist")
    mass16d_fullSel.Draw("hist e0 same")
    ATLASLabel(0.20, 0.955, label)
    leg_fullSel_d.Draw()
    sampleLabel.DrawLatex(0.60, 0.90, getNtrkLabel(ntrk))
    sampleLabel.DrawLatex(0.60, 0.85, "{}, full selection".format(SR))
    c.Print("{}/{}.pdf".format(directory, "dvMass_17_{}_fullSel_{}".format(SR, ntrk)))

    ### 18 vs mc16e
    # No Selection
    leg_noSel_e = r.TLegend(0.62, 0.60, 0.85, 0.80)
    decorateLeg(leg_noSel_e)
    leg_noSel_e.AddEntry(mass18_noSel, "Data:18", "l")
    leg_noSel_e.AddEntry(mass16e_noSel, "MC16e", "l")
    mass18_noSel.Draw("hist")
    mass16e_noSel.Draw("hist e0 same")
    ATLASLabel(0.20, 0.955, label)
    leg_noSel_e.Draw()
    sampleLabel.DrawLatex(0.60, 0.90, getNtrkLabel(ntrk))
    sampleLabel.DrawLatex(0.60, 0.85, "{}, no DV selection".format(SR))
    c.Print("{}/{}.pdf".format(directory, "dvMass_18_{}_noSel_{}".format(SR, ntrk)))

    # DV Selection
    leg_DVSel_e = r.TLegend(0.62, 0.60, 0.85, 0.80)
    decorateLeg(leg_DVSel_e)
    leg_DVSel_e.AddEntry(mass18_DVSel, "Data:18", "l")
    leg_DVSel_e.AddEntry(mass16e_DVSel, "MC16e", "l")
    mass18_DVSel.Draw("hist")
    mass16e_DVSel.Draw("hist e0 same")
    ATLASLabel(0.20, 0.955, label)
    leg_DVSel_e.Draw()
    sampleLabel.DrawLatex(0.60, 0.90, getNtrkLabel(ntrk))
    sampleLabel.DrawLatex(0.60, 0.85, "{}, DV selection".format(SR))
    c.Print("{}/{}.pdf".format(directory, "dvMass_18_{}_DVSel_{}".format(SR, ntrk)))

    # Full Selection
    leg_fullSel_e = r.TLegend(0.62, 0.60, 0.85, 0.80)
    decorateLeg(leg_fullSel_e)
    leg_fullSel_e.AddEntry(mass18_fullSel, "Data:18", "l")
    leg_fullSel_e.AddEntry(mass16e_fullSel, "MC16e", "l")
    mass18_fullSel.Draw("hist")
    mass16e_fullSel.Draw("hist e0 same")
    ATLASLabel(0.20, 0.955, label)
    leg_fullSel_e.Draw()
    sampleLabel.DrawLatex(0.60, 0.90, getNtrkLabel(ntrk))
    sampleLabel.DrawLatex(0.60, 0.85, "{}, full selection".format(SR))
    c.Print("{}/{}.pdf".format(directory, "dvMass_18_{}_fullSel_{}".format(SR, ntrk)))

    if (ntrk == "Ntrk4"):
        bin20 = mass16e_noSel.FindBin(20.) - 1
    else:
        bin20 = mass16e_noSel.FindBin(10.) - 1

    nData = mass18_noSel.Integral(1, bin20)
    nMC = mass16e_noSel.Integral(1, bin20)
    nDiff = 1 - nMC/nData
    print(nData, nMC, nDiff)

    nData = mass18_DVSel.Integral(1, bin20)
    nMC = mass16e_DVSel.Integral(1, bin20)
    nDiff = 1 - nMC/nData
    print(nData, nMC, nDiff)

    nData = mass18_fullSel.Integral(1, bin20)
    nMC = mass16e_fullSel.Integral(1, bin20)
    nDiff = 1 - nMC/nData
    print(nData, nMC, nDiff)
