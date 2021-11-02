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
parser.add_argument("-tag", required=True, help="The campaign tag, 'a', 'd', or 'e'")
parser.add_argument("-label", default="Internal", help="Label for ATLASLabel")
parser.add_argument("-n", "--nbins", type=int, default=1, help="Rebin")
parser.add_argument("-t", "--trackCleaning", action="store_true", help="Use track cleaning file?")
parser.add_argument("-logy", action="store_true", help="User logy?")
parser.add_argument("-m", "--materialVeto", action="store_true", help="Use material veto file")
parser.add_argument("-d", "--DVSel", action="store_true", help="Use DV selection file")
parser.add_argument("-w", "--weight", action="store_true", help="Use weighted file?")
args = parser.parse_args()

tag = "mc16{}".format(args.tag)
SR = args.SR
label = args.label
logy = args.logy
nbins = args.nbins
useTC = args.trackCleaning # TC: track cleaning
matVeto = args.materialVeto
DVSel = args.DVSel
useWeight = args.weight

if (matVeto and DVSel):
    print(">> Warning! You can't turn on both matVeto and DVSel.")
    print(">> Switch off for the flag")
    matVeto = False
    DVSel = False

lastSuffix = ""
if matVeto:
    lastSuffix += "_matVeto"
if DVSel:
    lastSuffix += "_DVSel"
if useTC:
    lastSuffix += "_trackCleaning"

dataSet = "{}_{}".format(tag, SR)

if (args.tag == "a"):
    year = 1516
if (args.tag == "d"):
    year = 17
if (args.tag == "e"):
    year = 18


inputFile = r.TFile("../outputFiles/significance_{}{}.root".format(dataSet, lastSuffix), "READ")
if (not inputFile.IsOpen()):
    print(">> Input file: {} not opened successfully...".format(r.TFile.GetName()))
    print(">> Exit...")
    exit()

plotType = "sigNormalize"
directory = "pdfs/" + plotType + "/" + dataSet if (lastSuffix == "") else "pdfs/"+ plotType + "/" + dataSet + lastSuffix
if (not os.path.isdir(directory)):
    os.makedirs(directory)

ntrkList = ["Ntrk4", "Ntrk5", "Ntrk6", "Ntrk>6"]
sigSameDict = {}
sigMixedDict = {}
mvMassSameDict = {}
mvMassMixedDict = {}
distSameDict = {}
distMixedDict = {}
dvdvSameDict = {}
dvdvMixedDict = {}
dv1Jet_sameDict = {}
dv1Jet_mixedDict = {}
dv2Jet_sameDict = {}
dv2Jet_mixedDict = {}
sigSameDict_type = {}
sigMixedDict_type = {}
distSameDict_type = {}
distMixedDict_type = {}
rxyDict = {}
for ntrk in ntrkList:
    sigSameDict[ntrk] = inputFile.Get("sigSame_"+ntrk).Rebin(nbins)
    sigMixedDict[ntrk] = inputFile.Get("sigMixed_"+ntrk).Rebin(nbins)
    mvMassSameDict[ntrk] = inputFile.Get("mvMass_same_"+ntrk).Rebin(nbins)
    mvMassMixedDict[ntrk] = inputFile.Get("mvMass_mixed_"+ntrk).Rebin(nbins)
    distSameDict[ntrk] = inputFile.Get("distSame_"+ntrk).Rebin(20)
    distMixedDict[ntrk] = inputFile.Get("distMixed_"+ntrk).Rebin(20)
    dvdvSameDict[ntrk] = inputFile.Get("dvdv_same_"+ntrk)
    dvdvMixedDict[ntrk] = inputFile.Get("dvdv_mixed_"+ntrk)
    dv1Jet_sameDict[ntrk] = inputFile.Get("dv1Jet_same_"+ntrk)
    dv1Jet_mixedDict[ntrk] = inputFile.Get("dv1Jet_mixed_"+ntrk)
    dv2Jet_sameDict[ntrk] = inputFile.Get("dv2Jet_same_"+ntrk)
    dv2Jet_mixedDict[ntrk] = inputFile.Get("dv2Jet_mixed_"+ntrk)
    rxyDict[ntrk] = inputFile.Get("mvRxy_"+ntrk).Rebin(10)
    sigSameDict_type[ntrk] = {}
    sigMixedDict_type[ntrk] = {}
    distSameDict_type[ntrk] = {}
    distMixedDict_type[ntrk] = {}
    for dvType in range(1, 8):
        sigSameDict_type[ntrk][dvType] = inputFile.Get("sigSame_{}_{}".format(ntrk, dvType))
        sigMixedDict_type[ntrk][dvType] = inputFile.Get("sigMixed_{}_{}".format(ntrk, dvType))
        distSameDict_type[ntrk][dvType] = inputFile.Get("distSame_{}_{}".format(ntrk, dvType)).Rebin(50)
        distMixedDict_type[ntrk][dvType] = inputFile.Get("distMixed_{}_{}".format(ntrk, dvType)).Rebin(50)

c = r.TCanvas("c", "c", 800, 700)
c.cd()
sampleLabel = prepareLatex()
for ntrk in ntrkList:
    sigSame = sigSameDict[ntrk]
    sigMixed = sigMixedDict[ntrk]
    mvMassSame = mvMassSameDict[ntrk]
    mvMassMixed = mvMassMixedDict[ntrk]
    distSame = distSameDict[ntrk]
    distMixed = distMixedDict[ntrk]
    dvdvSame = dvdvSameDict[ntrk]
    dvdvMixed = dvdvMixedDict[ntrk]
    dv1JetSame = dv1Jet_sameDict[ntrk]
    dv1JetMixed = dv1Jet_mixedDict[ntrk]
    dv2JetSame = dv2Jet_sameDict[ntrk]
    dv2JetMixed = dv2Jet_mixedDict[ntrk]
    rxy = rxyDict[ntrk]

    setHistColor(sigMixed, r.kRed)
    setHistColor(mvMassMixed, r.kRed)
    setHistColor(distMixed, r.kRed)
    setHistColor(dvdvMixed, r.kRed)
    setHistColor(dv1JetMixed, r.kRed)
    setHistColor(dv2JetMixed, r.kRed)

    bin100 = sigSame.FindBin(100.)
    lastBin = sigSame.GetNbinsX() +1

    sf = sigSame.Integral(bin100, lastBin) / sigMixed.Integral(bin100, lastBin)
    sigMixed.Sumw2()
    sigMixed.Scale(sf)

    legSig = r.TLegend(0.65, 0.70, 0.85, 0.80)
    decorateLeg(legSig)
    legSig.AddEntry(sigSame, "Same-event", "l")
    legSig.AddEntry(sigMixed, "Mixed-event", "l")
    
    sigSame.Draw("hist e0")
    sigMixed.Draw("hist e0 same")
    ATLASLabel(0.20, 0.955, label)
    sampleLabel.DrawLatex(0.67, 0.90, "{}, {}".format(tag, SR))
    if useTC:
        sampleLabel.DrawLatex(0.67, 0.85, getNtrkLabel(ntrk)+", track cleaning")
    else:
        sampleLabel.DrawLatex(0.67, 0.85, getNtrkLabel(ntrk))
    legSig.Draw()
    c.Print("{}/{}.pdf".format(directory, "sig_"+ntrk))

    diffSig = sigMixed.Clone("diff_"+ntrk)
    setHistColor(diffSig, r.kBlack)
    diffSig.Add(sigSame, -1)
    
    errMV = double(0.)
    nMV = diffSig.IntegralAndError(1, bin100-1, errMV)

    print(ntrk)
    print("nMV = {:.2f} +- {:.2f}".format(nMV, errMV.value))

    # Distance
    distSame.SetMaximum(distSame.GetMaximum()*1.2)
    distMixed.Sumw2()
    leg_dist = r.TLegend(0.65, 0.70, 0.85, 0.80)
    decorateLeg(leg_dist)
    leg_dist.AddEntry(distSame, "Same-event", "l")
    leg_dist.AddEntry(distMixed, "Mixed-event", "l")
    nbins = distSame.GetNbinsX() + 1
    distSF = distSame.Integral(1, nbins) / distMixed.Integral(1, nbins)
    distMixed.Scale(distSF)
    distSame.Draw("hist")
    distMixed.Draw("hist same")
    ATLASLabel(0.20, 0.955, label)
    sampleLabel.DrawLatex(0.67, 0.90, "{}, {}".format(tag, SR))
    sampleLabel.DrawLatex(0.67, 0.85, getNtrkLabel(ntrk))
    leg_dist.Draw()
    c.Print("{}/{}.pdf".format(directory, "dist_"+ntrk))

    # DV-DV correlation
    leg_dvdv = r.TLegend(0.65, 0.70, 0.85, 0.80)
    decorateLeg(leg_dvdv)
    leg_dvdv.AddEntry(dvdvSame, "Same-event", "l")
    leg_dvdv.AddEntry(dvdvMixed, "Mixed-event", "l")
    dvdvSame.SetMaximum(dvdvSame.GetMaximum()*1.2)
    bin1 = dvdvSame.FindBin(3.)
    nbins = dvdvSame.GetNbinsX() + 1
    dvdvSF = dvdvSame.Integral(bin1, nbins) / dvdvMixed.Integral(bin1, nbins)
    dvdvMixed.Sumw2()
    dvdvMixed.Scale(dvdvSF)
    dvdvSame.Draw("hist")
    dvdvMixed.Draw("hist same")
    ATLASLabel(0.20, 0.955, label)
    sampleLabel.DrawLatex(0.67, 0.90, "{}, {}".format(tag, SR))
    sampleLabel.DrawLatex(0.67, 0.85, getNtrkLabel(ntrk))
    leg_dvdv.Draw()
    c.Print("{}/{}.pdf".format(directory, "dvdv_"+ntrk))

    # DV1-Jet correlation
    leg_dv1Jet = r.TLegend(0.65, 0.70, 0.85, 0.80)
    decorateLeg(leg_dv1Jet)
    leg_dv1Jet.AddEntry(dv1JetSame, "Same-event", "l")
    leg_dv1Jet.AddEntry(dv1JetMixed, "Mixed-event", "l")
    dv1JetSame.SetMaximum(dv1JetSame.GetMaximum()*1.2)
    bin1 = dv1JetSame.FindBin(3.)
    nbins = dv1JetSame.GetNbinsX() + 1
    dv1JetSF = dv1JetSame.Integral(bin1, nbins) / dv1JetMixed.Integral(bin1, nbins)
    dv1JetMixed.Sumw2()
    dv1JetMixed.Scale(dv1JetSF)
    dv1JetSame.Draw("hist")
    dv1JetMixed.Draw("hist same")
    ATLASLabel(0.20, 0.955, label)
    sampleLabel.DrawLatex(0.67, 0.90, "{}, {}".format(tag, SR))
    sampleLabel.DrawLatex(0.67, 0.85, getNtrkLabel(ntrk))
    leg_dv1Jet.Draw()
    c.Print("{}/{}.pdf".format(directory, "dv1Jet_"+ntrk))

    # DV2-Jet correlation
    leg_dv2Jet = r.TLegend(0.65, 0.70, 0.85, 0.80)
    decorateLeg(leg_dv2Jet)
    leg_dv2Jet.AddEntry(dv2JetSame, "Same-event", "l")
    leg_dv2Jet.AddEntry(dv2JetMixed, "Mixed-event", "l")
    dv2JetSame.SetMaximum(dv2JetSame.GetMaximum()*1.2)
    bin1 = dv2JetSame.FindBin(3.)
    nbins = dv2JetSame.GetNbinsX() + 1
    dv2JetSF = dv2JetSame.Integral(bin1, nbins) / dv2JetMixed.Integral(bin1, nbins)
    dv2JetMixed.Sumw2()
    dv2JetMixed.Scale(dv2JetSF)
    dv2JetSame.Draw("hist")
    dv2JetMixed.Draw("hist same")
    ATLASLabel(0.20, 0.955, label)
    sampleLabel.DrawLatex(0.67, 0.90, "{}, {}".format(tag, SR))
    sampleLabel.DrawLatex(0.67, 0.85, getNtrkLabel(ntrk))
    leg_dv2Jet.Draw()
    c.Print("{}/{}.pdf".format(directory, "dv2Jet_"+ntrk))

    # Rxy
    sel = "Event selection only"
    if DVSel:
        sel = "DV selection"
    if matVeto:
        sel = "Material veto"
    rxy.Draw("hist")
    ATLASLabel(0.20, 0.955, label)
    sampleLabel.DrawLatex(0.67, 0.90, "{}, {}".format(tag, SR))
    sampleLabel.DrawLatex(0.67, 0.85, getNtrkLabel(ntrk)+", "+sel)
    c.Print("{}/{}.pdf".format(directory, "rxy_"+ntrk))


    for dvType in range(1, 8):
        sigSame = sigSameDict_type[ntrk][dvType]
        sigMixed = sigMixedDict_type[ntrk][dvType]
        distSame = distSameDict_type[ntrk][dvType]
        distMixed = distMixedDict_type[ntrk][dvType]

        setHistColor(sigMixed, r.kRed)
        setHistColor(distMixed, r.kRed)
        
        # Significance
        bin100 = sigSame.FindBin(100.)
        lastBin = sigSame.GetNbinsX() + 1

        sf = sigSame.Integral(bin100, lastBin) / sigMixed.Integral(bin100, lastBin)
        sigMixed.Sumw2()
        sigMixed.Scale(sf)

        legSig = r.TLegend(0.65, 0.70, 0.85, 0.80)
        decorateLeg(legSig)
        legSig.AddEntry(sigSame, "Same-event", "l")
        legSig.AddEntry(sigMixed, "Mixed-event", "l")

        sigSame.Draw("hist e0")
        sigMixed.Draw("hist e0 same")
        ATLASLabel(0.20, 0.955, label)
        sampleLabel.DrawLatex(0.67, 0.90, "{}, {}".format(tag, SR))
        sampleLabel.DrawLatex(0.67, 0.85, getNtrkLabel(ntrk) + ", " + getDVTypeLabel(dvType))
        legSig.Draw()
        c.Print("{}/{}.pdf".format(directory, "sig_{}_dvType{}".format(ntrk, dvType)))
        errMV = double(0.)
        est = sigMixed.Clone("est_"+ntrk)
        est.Add(sigSame, -1)
        nMV = est.IntegralAndError(1, bin100-1, errMV)
        print(ntrk, dvType, nMV, "{:.2f}".format(errMV.value))

        # Distance
        lastBin = distSame.GetNbinsX() + 1

        try:
            sf = distSame.Integral(1, lastBin) / distMixed.Integral(1, lastBin)
        except ZeroDivisionError:
            print("Denominator = 0. Set scaleFactor = 1.0")
            sf = 1.0
        distMixed.Sumw2()
        distMixed.Scale(sf)

        legDist = r.TLegend(0.65, 0.70, 0.85, 0.80)
        decorateLeg(legDist)
        legDist.AddEntry(distSame, "Same-event", "l")
        legDist.AddEntry(distMixed, "Mixed-event", "l")

        distSame.Draw("hist e0")
        distMixed.Draw("hist e0 same")
        ATLASLabel(0.20, 0.955, label)
        sampleLabel.DrawLatex(0.67, 0.90, "{}, {}".format(tag, SR))
        sampleLabel.DrawLatex(0.67, 0.85, getNtrkLabel(ntrk) + ", " + getDVTypeLabel(dvType))
        legDist.Draw()
        c.Print("{}/{}.pdf".format(directory, "dist_{}_dvType{}".format(ntrk, dvType)))
