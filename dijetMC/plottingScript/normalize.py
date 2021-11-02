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
parser.add_argument("-sr", "--SR", required=True, help="Signal region, 'HighPtSR' or 'TracklessSR'")
parser.add_argument("-tag", required=True, help="THe campaign tag, 'a', 'd', or 'e'")
parser.add_argument("-label", default="Internal", help="Label for ATLASLabel")
parser.add_argument("-suffix", default="", help="File name suffix")
args = parser.parse_args()

tag = "mc16{}".format(args.tag)
SR = args.SR
label = args.label
suffix = args.suffix

dataSet = "{}_{}".format(tag, SR)
dataSet_mv = dataSet + "_" + suffix if (suffix != "") else dataSet

plotType = "norm"
directory = "pdfs/" + plotType + "/" + dataSet_mv
if (not os.path.isdir(directory)):
    os.makedirs(directory)


dataFile = r.TFile("/Users/amizukam/DVJets/trackCleaning/rootfiles/DV_mass_{}.root".format(SR), "READ")
mcFile = r.TFile("/Users/amizukam/dvjets_mergedVertices/dijetMC/outputFiles/dvMass_{}.root".format(dataSet), "READ")
mvFile = r.TFile("/Users/amizukam/dvjets_mergedVertices/dijetMC/outputFiles/extractFactor_{}.root".format(dataSet_mv), "READ")

ntrkList = ["Ntrk4", "Ntrk5", "Ntrk6" ]
normBinDict = {"Ntrk4": 20., "Ntrk5": 10., "Ntrk6": 10., "Ntrk>6": 10.}

data_noSel = {}
data_DVSel = {}
data_fullSel = {}
mc_noSel = {}
mc_DVSel = {}
mc_fullSel = {}
mv_noSel = {}
mv_DVSel = {}
mv_fullSel = {}
for ntrk in ntrkList:
    data_noSel[ntrk] = dataFile.Get("mDV_"+ntrk)
    data_DVSel[ntrk] = dataFile.Get("mDV_DVSel_"+ntrk)
    data_fullSel[ntrk] = dataFile.Get("mDV_fullSel_"+ntrk)
    mc_noSel[ntrk] = mcFile.Get("dvMass_noSelection_"+ntrk)
    mc_DVSel[ntrk] = mcFile.Get("dvMass_DVSel_"+ntrk)
    mc_fullSel[ntrk] = mcFile.Get("dvMass_fullSel_"+ntrk)
    mv_noSel[ntrk] = mvFile.Get("mvMass_"+ntrk)
    mv_DVSel[ntrk] = mvFile.Get("mvMass_DVSel_"+ntrk)
    mv_fullSel[ntrk] = mvFile.Get("mvMass_fullSel_"+ntrk)

c = r.TCanvas("c", "c", 800, 700)
c.cd()
sampleLabel = prepareLatex()
leg = r.TLegend(0.65, 0.65, 0.80, 0.85)
decorateLeg(leg)
for ntrk in ntrkList:
    histNoSel_data = data_noSel[ntrk]
    histNoSel_mc = mc_noSel[ntrk]
    histNoSel_mv = mv_noSel[ntrk]

    setHistColor(histNoSel_mc, r.kRed)
    setHistColor(histNoSel_mv, r.kBlue)

    c.SetLogy(True)

    normBin = histNoSel_data.FindBin(normBinDict[ntrk])
    nbins = histNoSel_mc.GetNbinsX() + 1
    sf = histNoSel_data.Integral(1, normBin) / histNoSel_mc.Integral(1, normBin)
    
    histNoSel_mc.Sumw2()
    histNoSel_mc.Scale(sf)
    histNoSel_mv.Sumw2()
    histNoSel_mv.Scale(sf)

    print(histNoSel_mv.Integral(1, nbins))

    histNoSel_data.SetMinimum(0.5)

    leg.AddEntry(histNoSel_data, "Data", "l")
    leg.AddEntry(histNoSel_mc, "Dijet MC", "l")
    leg.AddEntry(histNoSel_mv, "Truth MV", "l")

    histNoSel_data.Draw("e0")
    histNoSel_mc.Draw("hist same")
    histNoSel_mv.Draw("hist same")
    leg.Draw()
    ATLASLabel(0.20, 0.955, label)
    sampleLabel.DrawLatex(0.67, 0.90, getNtrkLabel(ntrk))
    c.Print("{}/{}.pdf".format(directory, "mDV_noSel_"+ntrk))
    
    
    histDVSel_data = data_DVSel[ntrk]
    histDVSel_mc = mc_DVSel[ntrk]
    histDVSel_mv = mv_DVSel[ntrk]
    setHistColor(histDVSel_mc, r.kRed)
    setHistColor(histDVSel_mv, r.kBlue)

    sf = histDVSel_data.Integral(1, normBin) / histDVSel_mc.Integral(1, normBin)

    histDVSel_mc.Sumw2()
    histDVSel_mc.Scale(sf)
    histDVSel_mv.Sumw2()
    histDVSel_mv.Scale(sf)

    histDVSel_data.SetMinimum(0.5)
    
    histDVSel_data.Draw("hist")
    histDVSel_mc.Draw("hist same")
    histDVSel_mv.Draw("hist same")
    c.Print("{}/{}.pdf".format(directory, "mDV_DVSel_"+ntrk))


    histfullSel_data = data_fullSel[ntrk]
    histfullSel_mc = mc_fullSel[ntrk]
    histfullSel_mv = mv_fullSel[ntrk]
    setHistColor(histfullSel_mc, r.kRed)
    setHistColor(histfullSel_mv, r.kBlue)

    sf = histfullSel_data.Integral(1, normBin) / histfullSel_mc.Integral(1, normBin)

    histfullSel_mc.Sumw2()
    histfullSel_mc.Scale(sf)
    histfullSel_mv.Sumw2()
    histfullSel_mv.Scale(sf)

    histfullSel_data.SetMinimum(0.5)
    
    histfullSel_data.Draw("hist")
    histfullSel_mc.Draw("hist same")
    histfullSel_mv.Draw("hist same")
    c.Print("{}/{}.pdf".format(directory, "mDV_fullSel_"+ntrk))
