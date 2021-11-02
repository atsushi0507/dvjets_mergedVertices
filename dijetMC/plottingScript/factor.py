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
parser.add_argument("-tag", required=True, help="The campaign tag, 'a', 'd', or 'e'")
parser.add_argument("-sf", "--suffix", default="", help="File suffix if needed")
parser.add_argument("-label", default="Internal", help="Label for ATLASLabel")
parser.add_argument("-n", "--nbins", type=int, default=1, help="Rebin")
parser.add_argument("--logy", action="store_true", help="Use logy?")
args = parser.parse_args()

tag = "mc16{}".format(args.tag)
SR = args.SR
suffix = args.suffix
label = args.label
logy = args.logy

dataSet = "{}_{}_{}".format(tag, SR, suffix) if (suffix != "") else "{}_{}".format(tag, SR)

plotType = "mvFactor"
directory = "pdfs/" + plotType + "/" + dataSet
if (not os.path.isdir(directory)):
    os.makedirs(directory)
if (not os.path.isdir("data")):
    os.makedirs("data")

inputFile = r.TFile("../outputFiles/extractFactor_{}.root".format(dataSet), "READ")

ntrkList = ["Ntrk4", "Ntrk5", "Ntrk6", "Ntrk>6"]
normBinDict = {"Ntrk4": 5, "Ntrk5": 6, "Ntrk6": 7, "Ntrk>6":8}
h_noSel = {}
h_DVSel = {}
h_firstHit = {}
h_allPtSel = {}
h_ptOutsideBP = {}
h_ptOutsidePixel = {}
h_d0InsideBP = {}
h_d0InsidePixel = {}
h_d0Selected = {}
h_angle = {}
h_lowPtForward = {}
h_passTC = {}
h_fullSel = {}
h_ptSel = {}
h_d0Sel = {}
h_angleForward = {}
h_attachedPt = {}
h_exceptAllPt = {}
h_trackCleaning = {}
h_allPtSelAndPtOutsideBP = {}
h_nAttached_vs_dvType = {}
nbin = args.nbins
for ntrk in ntrkList:
    h_noSel[ntrk] = inputFile.Get("mvMass_"+ntrk).Rebin(nbin)
    h_DVSel[ntrk] = inputFile.Get("mvMass_DVSel_"+ntrk).Rebin(nbin)
    h_firstHit[ntrk] = inputFile.Get("mvMass_upstreamHitVeto_"+ntrk).Rebin(nbin)
    h_allPtSel[ntrk] = inputFile.Get("mvMass_allPtSel_"+ntrk).Rebin(nbin)
    h_ptOutsideBP[ntrk] = inputFile.Get("mvMass_ptOutsideBP_"+ntrk).Rebin(nbin)
    h_ptOutsidePixel[ntrk] = inputFile.Get("mvMass_ptOutsidePixel_"+ntrk).Rebin(nbin)
    h_d0InsideBP[ntrk] = inputFile.Get("mvMass_d0InsideBP_"+ntrk).Rebin(nbin)
    h_d0InsidePixel[ntrk] = inputFile.Get("mvMass_d0InsidePixel_"+ntrk).Rebin(nbin)
    h_d0Selected[ntrk] = inputFile.Get("mvMass_d0Selected_"+ntrk).Rebin(nbin)
    h_angle[ntrk] = inputFile.Get("mvMass_angle_"+ntrk).Rebin(nbin)
    h_lowPtForward[ntrk] = inputFile.Get("mvMass_lowPtForward_"+ntrk).Rebin(nbin)
    h_passTC[ntrk] = inputFile.Get("mvMass_passTC_"+ntrk).Rebin(nbin)
    h_fullSel[ntrk] = inputFile.Get("mvMass_fullSel_"+ntrk).Rebin(nbin)
    h_ptSel[ntrk] = inputFile.Get("mvMass_ptSel_"+ntrk).Rebin(nbin)
    h_d0Sel[ntrk] = inputFile.Get("mvMass_d0Sel_"+ntrk).Rebin(nbin)
    h_angleForward[ntrk] = inputFile.Get("mvMass_angleForward_"+ntrk).Rebin(nbin)
    h_attachedPt[ntrk] = inputFile.Get("mvMass_attachedPt_"+ntrk).Rebin(nbin)
    h_exceptAllPt[ntrk] = inputFile.Get("mvMass_exceptAllPt_"+ntrk).Rebin(nbin)
    h_trackCleaning[ntrk] = inputFile.Get("mvMass_trackCleaning_"+ntrk).Rebin(nbin)
    h_allPtSelAndPtOutsideBP[ntrk] = inputFile.Get("mvMass_allPtSelAndPtOutsideBP_"+ntrk).Rebin(nbin)
    h_nAttached_vs_dvType[ntrk] = inputFile.Get("nAttached_vs_dvType_"+ntrk+"_noSel")

c = r.TCanvas("c", "c", 800, 700)
c.cd()
sampleLabel = prepareLatex()
for ntrk in ntrkList:
    noSel = h_noSel[ntrk]
    DVSel = h_DVSel[ntrk]
    firstHit = h_firstHit[ntrk]
    allPtSel = h_allPtSel[ntrk]
    ptOutsideBP = h_ptOutsideBP[ntrk]
    ptOutsidePixel = h_ptOutsidePixel[ntrk]
    d0InsideBP = h_d0InsideBP[ntrk]
    d0InsidePixel = h_d0InsidePixel[ntrk]
    d0Selected = h_d0Selected[ntrk]
    angle = h_angle[ntrk]
    lowPtForward = h_lowPtForward[ntrk]
    passTC = h_passTC[ntrk]
    fullSel = h_fullSel[ntrk]
    ptSel = h_ptSel[ntrk]
    d0Sel = h_d0Sel[ntrk]
    angleForward = h_angleForward[ntrk]
    attachedPt = h_attachedPt[ntrk]
    exceptAllPt = h_exceptAllPt[ntrk]
    trackCleaning = h_trackCleaning[ntrk]
    allPtSelAndPtOutsideBP = h_allPtSelAndPtOutsideBP[ntrk]
    nAttached_vs_dvType = h_nAttached_vs_dvType[ntrk]

    setHistColor(noSel, r.kBlack)
    setHistColor(DVSel, r.kRed)
    setHistColor(firstHit, r.kRed)
    setHistColor(allPtSel, r.kRed)
    setHistColor(ptOutsideBP, r.kRed)
    setHistColor(ptOutsidePixel, r.kRed)
    setHistColor(d0InsideBP, r.kRed)
    setHistColor(d0InsidePixel, r.kRed)
    setHistColor(d0Selected, r.kRed)
    setHistColor(angle, r.kRed)
    setHistColor(lowPtForward, r.kRed)
    setHistColor(passTC, r.kRed)
    setHistColor(fullSel, r.kRed)
    setHistColor(ptSel, r.kRed)
    setHistColor(d0Sel, r.kRed)
    setHistColor(angleForward, r.kRed)
    setHistColor(attachedPt, r.kRed)
    setHistColor(exceptAllPt, r.kRed)
    setHistColor(trackCleaning, r.kRed)
    setHistColor(allPtSelAndPtOutsideBP, r.kRed)

    if (logy):
        c.SetLogy(True)
    
    # Compare with no selection MV mass hist
    # DV selection
    DVSel.SetMaximum(noSel.GetMaximum()*1.2)
    leg_DVSel = r.TLegend(0.50, 0.60, 0.80, 0.80)
    decorateLeg(leg_DVSel)
    leg_DVSel.AddEntry(noSel, "No selection", "l")
    leg_DVSel.AddEntry(DVSel, "DV selection", "l")
    DVSel.Draw("hist")
    noSel.Draw("hist same")
    leg_DVSel.Draw()
    ATLASLabel(0.20, 0.955, label)
    sampleLabel.DrawLatex(0.52, 0.90, "{}, {}".format(tag, SR))
    sampleLabel.DrawLatex(0.52, 0.85, getNtrkLabel(ntrk))
    c.Print("{}/{}.pdf".format(directory, "DVSel_"+ntrk))

    # First hit should after DV position
    firstHit.SetMaximum(noSel.GetMaximum()*1.2)
    leg_firstHit = r.TLegend(0.50, 0.60, 0.80, 0.80)
    decorateLeg(leg_firstHit)
    leg_firstHit.AddEntry(noSel, "No selection", "l")
    leg_firstHit.AddEntry(firstHit, "Hit after DV pos.", "l")
    firstHit.Draw("hist")
    noSel.Draw("hist same")
    leg_firstHit.Draw()
    ATLASLabel(0.20, 0.955, label)
    sampleLabel.DrawLatex(0.52, 0.90, "{}, {}".format(tag, SR))
    sampleLabel.DrawLatex(0.52, 0.85, getNtrkLabel(ntrk))
    c.Print("{}/{}.pdf".format(directory, "firstHit_"+ntrk))

    # pT selection for all track
    allPtSel.SetMaximum(noSel.GetMaximum()*1.2)
    leg_allPtSel = r.TLegend(0.50, 0.60, 0.80, 0.80)
    decorateLeg(leg_allPtSel)
    leg_allPtSel.AddEntry(noSel, "No selection", "l")
    leg_allPtSel.AddEntry(allPtSel, "pT > 2 GeV for all track", "l")
    allPtSel.Draw("hist")
    noSel.Draw("hist same")
    leg_allPtSel.Draw()
    ATLASLabel(0.20, 0.955, label)
    sampleLabel.DrawLatex(0.52, 0.90, "{}, {}".format(tag, SR))
    sampleLabel.DrawLatex(0.52, 0.85, getNtrkLabel(ntrk))
    c.Print("{}/{}.pdf".format(directory, "allPtSel_"+ntrk))

    # pT selection for attached tracks outside BP
    ptOutsideBP.SetMaximum(noSel.GetMaximum()*1.2)
    leg_ptOutsideBP = r.TLegend(0.50, 0.60, 0.80, 0.80)
    decorateLeg(leg_ptOutsideBP)
    leg_ptOutsideBP.AddEntry(noSel, "No selection", "l")
    leg_ptOutsideBP.AddEntry(ptOutsideBP, "pT > 3 GeV for attached outside BP", "l")
    ptOutsideBP.Draw("hist")
    noSel.Draw("hist same")
    leg_ptOutsideBP.Draw()
    ATLASLabel(0.20, 0.955, label)
    sampleLabel.DrawLatex(0.52, 0.90, "{}, {}".format(tag, SR))
    sampleLabel.DrawLatex(0.52, 0.85, getNtrkLabel(ntrk))
    c.Print("{}/{}.pdf".format(directory, "ptOutsideBP_"+ntrk))

    # pT selection for attached tracks outside Pixel
    ptOutsidePixel.SetMaximum(noSel.GetMaximum()*1.2)
    leg_ptOutsidePixel = r.TLegend(0.60, 0.60, 0.80, 0.80)
    decorateLeg(leg_ptOutsidePixel)
    leg_ptOutsidePixel.AddEntry(noSel, "No selection", "l")
    leg_ptOutsidePixel.AddEntry(ptOutsidePixel, "pT > 4 GeV for attached outside Pixel", "l")
    ptOutsidePixel.Draw("hist")
    noSel.Draw("hist same")
    leg_ptOutsidePixel.Draw()
    ATLASLabel(0.20, 0.955, label)
    sampleLabel.DrawLatex(0.62, 0.90, "{}, {}".format(tag, SR))
    sampleLabel.DrawLatex(0.62, 0.85, getNtrkLabel(ntrk))
    c.Print("{}/{}.pdf".format(directory, "ptOutsidePixel_"+ntrk))

    # d0-sig > 10 for inside BP
    d0InsideBP.SetMaximum(noSel.GetMaximum()*1.2)
    leg_d0InsideBP = r.TLegend(0.60, 0.60, 0.80, 0.80)
    decorateLeg(leg_d0InsideBP)
    leg_d0InsideBP.AddEntry(noSel, "No selection", "l")
    leg_d0InsideBP.AddEntry(d0InsideBP, "d0-sig > 10 for attached tracks inside BP", "l")
    d0InsideBP.Draw("hist")
    noSel.Draw("hist same")
    leg_d0InsideBP.Draw()
    ATLASLabel(0.20, 0.955, label)
    sampleLabel.DrawLatex(0.62, 0.90, "{}, {}".format(tag, SR))
    sampleLabel.DrawLatex(0.62, 0.85, getNtrkLabel(ntrk))
    c.Print("{}/{}.pdf".format(directory, "d0InsideBP_"+ntrk))

    # d0-sig > 15 for inside Pixel
    d0InsidePixel.SetMaximum(noSel.GetMaximum()*1.2)
    leg_d0InsidePixel = r.TLegend(0.60, 0.60, 0.80, 0.80)
    decorateLeg(leg_d0InsidePixel)
    leg_d0InsidePixel.AddEntry(noSel, "No selection", "l")
    leg_d0InsidePixel.AddEntry(d0InsidePixel, "d0-sig > 15 for attached tracks inside Pixel", "l")
    d0InsidePixel.Draw("hist")
    noSel.Draw("hist same")
    leg_d0InsidePixel.Draw()
    ATLASLabel(0.20, 0.955, label)
    sampleLabel.DrawLatex(0.62, 0.90, "{}, {}".format(tag, SR))
    sampleLabel.DrawLatex(0.62, 0.85, getNtrkLabel(ntrk))
    c.Print("{}/{}.pdf".format(directory, "d0InsidePixel_"+ntrk))

    # d0-sig > 10 for selected track outside Pixel
    d0Selected.SetMaximum(noSel.GetMaximum()*1.2)
    leg_d0Selected = r.TLegend(0.60, 0.60, 0.80, 0.80)
    decorateLeg(leg_d0Selected)
    leg_d0Selected.AddEntry(noSel, "No selection", "l")
    leg_d0Selected.AddEntry(d0Selected, "d0-sig > 10 for selected tracks outside Pixel", "l")
    d0Selected.Draw("hist")
    noSel.Draw("hist same")
    leg_d0Selected.Draw()
    ATLASLabel(0.20, 0.955, label)
    sampleLabel.DrawLatex(0.62, 0.90, "{}, {}".format(tag, SR))
    sampleLabel.DrawLatex(0.62, 0.85, getNtrkLabel(ntrk))
    c.Print("{}/{}.pdf".format(directory, "d0Selected_"+ntrk))

    # Angle
    angle.SetMaximum(noSel.GetMaximum()*1.2)
    leg_angle = r.TLegend(0.60, 0.60, 0.80, 0.80)
    decorateLeg(leg_angle)
    leg_angle.AddEntry(noSel, "No selection", "l")
    leg_angle.AddEntry(angle, "Anguler selection", "l")
    angle.Draw("hist")
    noSel.Draw("hist same")
    leg_angle.Draw()
    ATLASLabel(0.20, 0.955, label)
    sampleLabel.DrawLatex(0.62, 0.90, "{}, {}".format(tag, SR))
    sampleLabel.DrawLatex(0.62, 0.85, getNtrkLabel(ntrk))
    c.Print("{}/{}.pdf".format(directory, "angle_"+ntrk))

    # Low-pT forward selection
    lowPtForward.SetMaximum(noSel.GetMaximum()*1.2)
    leg_lowPtForward = r.TLegend(0.60, 0.60, 0.80, 0.80)
    decorateLeg(leg_lowPtForward)
    leg_lowPtForward.AddEntry(noSel, "No selection", "l")
    leg_lowPtForward.AddEntry(lowPtForward, "Low-pT forward selection", "l")
    lowPtForward.Draw("hist")
    noSel.Draw("hist same")
    leg_lowPtForward.Draw()
    ATLASLabel(0.20, 0.955, label)
    sampleLabel.DrawLatex(0.62, 0.90, "{}, {}".format(tag, SR))
    sampleLabel.DrawLatex(0.62, 0.85, getNtrkLabel(ntrk))
    c.Print("{}/{}.pdf".format(directory, "lowPtForward_"+ntrk))

    # All track cleaning 
    passTC.SetMaximum(noSel.GetMaximum()*1.2)
    leg_passTC = r.TLegend(0.60, 0.60, 0.80, 0.80)
    decorateLeg(leg_passTC)
    leg_passTC.AddEntry(noSel, "No selection", "l")
    leg_passTC.AddEntry(passTC, "Full track cleaning", "l")
    passTC.Draw("hist")
    noSel.Draw("hist same")
    leg_passTC.Draw()
    ATLASLabel(0.20, 0.955, label)
    sampleLabel.DrawLatex(0.62, 0.90, "{}, {}".format(tag, SR))
    sampleLabel.DrawLatex(0.62, 0.85, getNtrkLabel(ntrk))
    c.Print("{}/{}.pdf".format(directory, "passTC_"+ntrk))

    # Full selection
    fullSel.SetMaximum(noSel.GetMaximum()*1.2)
    leg_fullSel = r.TLegend(0.60, 0.60, 0.80, 0.80)
    decorateLeg(leg_fullSel)
    leg_fullSel.AddEntry(noSel, "No selection", "l")
    leg_fullSel.AddEntry(fullSel, "DV selection + track cleaning", "l")
    fullSel.Draw("hist")
    noSel.Draw("hist same")
    leg_fullSel.Draw()
    ATLASLabel(0.20, 0.955, label)
    sampleLabel.DrawLatex(0.62, 0.90, "{}, {}".format(tag, SR))
    sampleLabel.DrawLatex(0.62, 0.85, getNtrkLabel(ntrk))
    c.Print("{}/{}.pdf".format(directory, "fullSel_"+ntrk))

    # pt selection
    ptSel.SetMaximum(noSel.GetMaximum()*1.2)
    leg_ptSel = r.TLegend(0.60, 0.60, 0.80, 0.80)
    decorateLeg(leg_ptSel)
    leg_ptSel.AddEntry(noSel, "No selection", "l")
    leg_ptSel.AddEntry(ptSel, "Inclusive pT selection", "l")
    ptSel.Draw("hist")
    noSel.Draw("hist same")
    leg_ptSel.Draw()
    ATLASLabel(0.20, 0.955, label)
    sampleLabel.DrawLatex(0.62, 0.90, "{}, {}".format(tag, SR))
    sampleLabel.DrawLatex(0.62, 0.85, getNtrkLabel(ntrk))
    c.Print("{}/{}.pdf".format(directory, "ptSel_"+ntrk))

    # d0 selection
    d0Sel.SetMaximum(noSel.GetMaximum()*1.2)
    leg_d0Sel = r.TLegend(0.60, 0.60, 0.80, 0.80)
    decorateLeg(leg_d0Sel)
    leg_d0Sel.AddEntry(noSel, "No selection", "l")
    leg_d0Sel.AddEntry(d0Sel, "Inclusive d0 selection", "l")
    d0Sel.Draw("hist")
    noSel.Draw("hist same")
    leg_d0Sel.Draw()
    ATLASLabel(0.20, 0.955, label)
    sampleLabel.DrawLatex(0.62, 0.90, "{}, {}".format(tag, SR))
    sampleLabel.DrawLatex(0.62, 0.85, getNtrkLabel(ntrk))
    c.Print("{}/{}.pdf".format(directory, "d0Sel_"+ntrk))

    # angle and forward pt selection
    angleForward.SetMaximum(noSel.GetMaximum()*1.2)
    leg_angleForward = r.TLegend(0.60, 0.60, 0.80, 0.80)
    decorateLeg(leg_angleForward)
    leg_angleForward.AddEntry(noSel, "No selection", "l")
    leg_angleForward.AddEntry(angleForward, "angle and low-pT forward selection", "l")
    angleForward.Draw("hist")
    noSel.Draw("hist same")
    leg_angleForward.Draw()
    ATLASLabel(0.20, 0.955, label)
    sampleLabel.DrawLatex(0.62, 0.90, "{}, {}".format(tag, SR))
    sampleLabel.DrawLatex(0.62, 0.85, getNtrkLabel(ntrk))
    c.Print("{}/{}.pdf".format(directory, "angleForward_"+ntrk))

    # pT selection for attached tracks
    attachedPt.SetMaximum(noSel.GetMaximum()*1.2)
    leg_attachedPt = r.TLegend(0.50, 0.60, 0.80, 0.80)
    decorateLeg(leg_attachedPt)
    leg_attachedPt.AddEntry(noSel, "No selection", "l")
    leg_attachedPt.AddEntry(attachedPt, "pT selection for atttached track", "l")
    attachedPt.Draw("hist")
    noSel.Draw("hist same")
    leg_attachedPt.Draw()
    ATLASLabel(0.20, 0.955, label)
    sampleLabel.DrawLatex(0.52, 0.90, "{}, {}".format(tag, SR))
    sampleLabel.DrawLatex(0.52, 0.85, getNtrkLabel(ntrk))
    c.Print("{}/{}.pdf".format(directory, "attachedPt_"+ntrk))

    # Track cleaning except all track pT selection
    exceptAllPt.SetMaximum(noSel.GetMaximum()*1.2)
    leg_exceptAllPt = r.TLegend(0.50, 0.60, 0.80, 0.80)
    decorateLeg(leg_exceptAllPt)
    leg_exceptAllPt.AddEntry(noSel, "No selection", "l")
    leg_exceptAllPt.AddEntry(exceptAllPt, "Track cleaning except all pT selection", "l")
    exceptAllPt.Draw("hist")
    noSel.Draw("hist same")
    leg_exceptAllPt.Draw()
    ATLASLabel(0.20, 0.955, label)
    sampleLabel.DrawLatex(0.52, 0.90, "{}, {}".format(tag, SR))
    sampleLabel.DrawLatex(0.52, 0.85, getNtrkLabel(ntrk))
    c.Print("{}/{}.pdf".format(directory, "exceptAllPt_"+ntrk))

    # Track cleaning
    trackCleaning.SetMaximum(noSel.GetMaximum()*1.2)
    leg_trackCleaning = r.TLegend(0.50, 0.60, 0.80, 0.80)
    decorateLeg(leg_trackCleaning)
    leg_trackCleaning.AddEntry(noSel, "No selection", "l")
    leg_trackCleaning.AddEntry(trackCleaning, "Track cleaning", "l")
    trackCleaning.Draw("hist")
    noSel.Draw("hist same")
    leg_trackCleaning.Draw()
    ATLASLabel(0.20, 0.955, label)
    sampleLabel.DrawLatex(0.52, 0.90, "{}, {}".format(tag, SR))
    sampleLabel.DrawLatex(0.52, 0.85, getNtrkLabel(ntrk))
    c.Print("{}/{}.pdf".format(directory, "trackCleaning_"+ntrk))

    # pT selection for all track
    allPtSelAndPtOutsideBP.SetMaximum(noSel.GetMaximum()*1.2)
    leg_allPtSelAndPtOutsideBP = r.TLegend(0.50, 0.60, 0.80, 0.80)
    decorateLeg(leg_allPtSelAndPtOutsideBP)
    leg_allPtSelAndPtOutsideBP.AddEntry(noSel, "No selection", "l")
    leg_allPtSelAndPtOutsideBP.AddEntry(allPtSelAndPtOutsideBP, "allPtSel and outsideBP", "l")
    allPtSelAndPtOutsideBP.Draw("hist")
    noSel.Draw("hist same")
    leg_allPtSelAndPtOutsideBP.Draw()
    ATLASLabel(0.20, 0.955, label)
    sampleLabel.DrawLatex(0.52, 0.90, "{}, {}".format(tag, SR))
    sampleLabel.DrawLatex(0.52, 0.85, getNtrkLabel(ntrk))
    c.Print("{}/{}.pdf".format(directory, "allPtSelAndPtOutsideBP_"+ntrk))

    # Count
    err_nominal = double(0.)
    err_DVSel = double(0.)
    err_firstHit = double(0.)
    err_allPtSel = double(0.)
    err_ptOutsideBP = double(0.)
    err_ptOutsidePixel = double(0.)
    err_d0InsideBP = double(0.)
    err_d0InsidePixel = double(0.)
    err_d0Selected = double(0.)
    err_angle = double(0.)
    err_lowPtForward = double(0.)
    err_passTC = double(0.)
    err_fullSel = double(0.)
    err_ptSel = double(0.)
    err_d0Sel = double(0.)
    err_angleForward = double(0.)
    err_attachedPt = double(0.)
    err_exceptAllPt = double(0.)
    err_trackCleaning = double(0.)
    err_allPtSelAndPtOutsideBP = double(0.)

    bin1 = noSel.FindBin(normBinDict[ntrk])
    nbins = noSel.GetNbinsX() + 1

    nNominal = noSel.IntegralAndError(bin1, nbins, err_nominal)
    nDVSel = DVSel.IntegralAndError(bin1, nbins, err_DVSel)
    nFirstHit = firstHit.IntegralAndError(bin1, nbins, err_firstHit)
    nAllPtSel = allPtSel.IntegralAndError(bin1, nbins, err_allPtSel)
    nPtOutsideBP = ptOutsideBP.IntegralAndError(bin1, nbins, err_ptOutsideBP)
    nPtOutsidePixel = ptOutsidePixel.IntegralAndError(bin1, nbins, err_ptOutsidePixel)
    nd0InsideBP = d0InsideBP.IntegralAndError(bin1, nbins, err_d0InsideBP)
    nd0InsidePixel = d0InsidePixel.IntegralAndError(bin1, nbins, err_d0InsidePixel)
    nd0Selected = d0Selected.IntegralAndError(bin1, nbins, err_d0Selected)
    nAngle = angle.IntegralAndError(bin1, nbins, err_angle)
    nLowPtForward = lowPtForward.IntegralAndError(bin1, nbins, err_lowPtForward)
    nPassTC = passTC.IntegralAndError(bin1, nbins, err_passTC)
    nFullSel = fullSel.IntegralAndError(bin1, nbins, err_fullSel)
    nPtSel = ptSel.IntegralAndError(bin1, nbins, err_ptSel)
    nd0Sel = d0Sel.IntegralAndError(bin1, nbins, err_d0Sel)
    nAngleForward = angleForward.IntegralAndError(bin1, nbins, err_angleForward)
    nAttachedPt = attachedPt.IntegralAndError(bin1, nbins, err_attachedPt)
    nExceptAllPt = exceptAllPt.IntegralAndError(bin1, nbins, err_exceptAllPt)
    nTrackCleaning = trackCleaning.IntegralAndError(bin1, nbins, err_trackCleaning)
    nAllPtSelAndPtOutsideBP = allPtSelAndPtOutsideBP.IntegralAndError(bin1, nbins, err_allPtSelAndPtOutsideBP)

    rateDVSel, errRateDVSel = divideError(nDVSel, nNominal, err_DVSel.value, err_nominal.value)
    rateFirstHit, errRateFirstHit = divideError(nFirstHit, nNominal, err_firstHit.value, err_nominal.value)
    rateAllPtSel, errRateAllPtSel = divideError(nAllPtSel, nNominal, err_allPtSel.value, err_nominal.value)
    ratePtOutsideBP, errRatePtOutsideBP = divideError(nPtOutsideBP, nNominal, err_ptOutsideBP.value, err_nominal.value)
    ratePtOutsidePixel, errRatePtOutsidePixel = divideError(nPtOutsidePixel, nNominal, err_ptOutsidePixel.value, err_nominal.value)
    rated0InsideBP, errRated0InsideBP = divideError(nd0InsideBP, nNominal, err_d0InsideBP.value, err_nominal.value)
    rated0InsidePixel, errRated0InsidePixel = divideError(nd0InsidePixel, nNominal, err_d0InsidePixel.value, err_nominal.value)
    rated0Selected, errRated0Selected = divideError(nd0Selected, nNominal, err_d0Selected.value, err_nominal.value)
    rateAngle, errRateAngle = divideError(nAngle, nNominal, err_angle.value, err_nominal.value)
    rateLowPtForward, errRateLowPtForward = divideError(nLowPtForward, nNominal, err_lowPtForward.value, err_nominal.value)
    ratePassTC, errRatePassTC = divideError(nPassTC, nNominal, err_passTC.value, err_nominal.value)
    rateFullSel, errRateFullSel = divideError(nFullSel, nNominal, err_fullSel.value, err_nominal.value)
    ratePtSel, errRatePtSel = divideError(nPtSel, nNominal, err_ptSel.value, err_nominal.value)
    rated0Sel, errRated0Sel = divideError(nd0Sel, nNominal, err_d0Sel.value, err_nominal.value)
    rateAngleForward, errRateAngleForward = divideError(nAngleForward, nNominal, err_angleForward.value, err_nominal.value)
    rateAttachedPt, errRateAttachedPt = divideError(nAttachedPt, nNominal, err_attachedPt.value, err_nominal.value)
    rateExceptAllPt, errRateExceptAllPt = divideError(nExceptAllPt, nNominal, err_exceptAllPt.value, err_nominal.value)
    rateTrackCleaning, errRateTrackCleaning = divideError(nTrackCleaning, nNominal, err_trackCleaning.value, err_nominal.value)
    rateAllPtSelAndPtOutsideBP, errRateAllPtSelAndPtOutsideBP = divideError(nAllPtSelAndPtOutsideBP, nNominal, err_allPtSelAndPtOutsideBP.value, err_nominal.value)

    print("DVSel: {:.3f} +- {:.3f}".format(rateDVSel, errRateDVSel))
    print("firstHit: {:.3f} +- {:.3f}".format(rateFirstHit, errRateFirstHit))
    print("AllPtSel: {:.3f} +- {:.3f}".format(rateAllPtSel, errRateAllPtSel))
    print("PtOutsideBP: {:.3f} +- {:.3f}".format(ratePtOutsideBP, errRatePtOutsideBP))
    print("PtOutsidePixel: {:.3f} +- {:.3f}".format(ratePtOutsidePixel, errRatePtOutsidePixel))
    print("d0InsideBP: {:.3f} +- {:.3f}".format(rated0InsideBP, errRated0InsideBP))
    print("d0InsidePixel: {:.3f} +- {:.3f}".format(rated0InsidePixel, errRated0InsidePixel))
    print("d0Selected: {:.3f} +- {:.3f}".format(rated0Selected, errRated0Selected))
    print("Angle: {:.3f} +- {:.3f}".format(rateAngle, errRateAngle))
    print("LowPtForward: {:.3f} +- {:.3f}".format(rateLowPtForward, errRateLowPtForward))
    print("PassTC: {:.3f} +- {:.3f}".format(ratePassTC, errRatePassTC))
    print("fullSel: {:.3f} +- {:.3f}".format(rateFullSel, errRateFullSel))
    print("PtSel: {:.3f} +- {:.3f}".format(ratePtSel, errRatePtSel))
    print("d0Sel: {:.3f} +- {:.3f}".format(rated0Sel, errRated0Sel))
    print("AngleForward: {:.3f} +- {:.3f}".format(rateAngleForward, errRateAngleForward))
    print("AttachedPt: {:.3f} +- {:.3f}".format(rateAttachedPt, errRateAttachedPt))
    print("ExceptAllPt: {:.3f} +- {:.3f}".format(rateExceptAllPt, errRateExceptAllPt))
    print("TrackCleaning: {:.3f} +- {:.3f}".format(rateTrackCleaning, errRateTrackCleaning))
    print("AllPtSelAndPtOutsideBP: {:.3f} +- {:.3f}".format(rateAllPtSelAndPtOutsideBP, errRateAllPtSelAndPtOutsideBP))

    c.SetLogy(False)
    nAttached_vs_dvType.Draw("colz text")
    ATLASLabel(0.20, 0.955, label)
    sampleLabel.DrawLatex(0.70, 0.90, "{}, {}".format(tag, SR))
    sampleLabel.DrawLatex(0.70, 0.85, getNtrkLabel(ntrk))
    c.Print("{}/{}.pdf".format(directory, "nAttached_vs_dvType_"+ntrk))

outFile.close()
