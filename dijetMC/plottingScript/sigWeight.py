import ROOT as r
import sys, os
sys.path.append("/Users/amizukam/DVJets/atlasstyle")
from AtlasStyle import *
from AtlasLabel import *

r.gROOT.SetBatch()
SetAtlasStyle()
label = "Internal"

dataSet = "mc16e_new"

plotType = "sigWeight"
directory = "pdfs/" + plotType + "/" + dataSet + "/"
if (not os.path.isdir(directory)):
    os.makedirs(directory)
if (not os.path.isdir("rootfiles")):
    os.makedirs("rootfiles")

inputFile = r.TFile("../outputFiles/significance_{}.root".format(dataSet), "READ")
tree = inputFile.Get("trees_SRDV_")

outputFile = r.TFile("rootfiles/{}_{}.root".format(plotType, dataSet), "RECREATE")

colors = [r.kGreen, r.kRed, r.kBlue, r.kOrange, r.kMagenta, r.kCyan, r.kViolet]
ntrkList = ["Ntrk4", "Ntrk5", "Ntrk6", "Ntrk>6"]

def getNtrkBin(ntrk):
    ntrkBin = ""
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
    if ntrkBin == "Ntrk4":
        ntrkLabel = "N_{trk} = 4"
    if ntrkBin == "Ntrk5":
        ntrkLabel = "N_{trk} = 5"
    if ntrkBin == "Ntrk6":
        ntrkLabel = "N_{trk} = 6"
    if ntrkBin == "Ntrk>6":
        ntrkLabel = "N_{trk} > 6"
    return ntrkLabel

def decoRatioPlot(rp, max, min):
    rp.SetH2DrawOpt("hist e")
    rp.Draw()
    rp.GetLowerRefGraph().SetMaximum(max)
    rp.GetLowerRefGraph().SetMinimum(min)
    #rp.GetLowYaxis().SetNdivisions(4)
    rp.SetSeparationMargin(0.02)
    rp.SetLeftMargin(0.1575)
    rp.SetLowBottomMargin(0.50)

def decoLegend(leg):
    leg.SetFillStyle(0)
    leg.SetBorderSize(0)
    leg.SetLineStyle(0)
    leg.SetTextSize(0.035)
    leg.SetTextFont(42)

# Get ratio histograms
dzRatioHistDict = {}
for ntrk in ntrkList:
    dzRatioHistDict[ntrk] = inputFile.Get("dzRatio_"+ntrk)
    
# Define histograms
sigSameDict = {}
sigMixedDict = {}
sigSameBeforeDict = {}
sigMixedBeforeDict = {}
sig_det_sameDict = {}
sig_det_mixedDict = {}
for ntrk in ntrkList:
    sigSameDict[ntrk] = r.TH1D("sigSame_"+ntrk, ";Significance", 100, 0., 1000.)
    sigMixedDict[ntrk] = r.TH1D("sigMixed_"+ntrk, ";Significance", 100, 0., 1000.)
    sigSameBeforeDict[ntrk] = r.TH1D("sigSameBefore_"+ntrk, ";Significance", 100, 0., 1000.)
    sigMixedBeforeDict[ntrk] = r.TH1D("sigMixedBefore_"+ntrk, ";Significance", 100, 0., 1000.)
    sig_det_sameDict[ntrk] = r.TH2D("sig_det_same_"+ntrk, ";Significance;log_{10}|C|", 100, 0., 1000., 25, -10., 15.)
    sig_det_mixedDict[ntrk] = r.TH2D("sig_det_mixed_"+ntrk, ";Significance;log_{10}|C|", 100, 0., 1000., 25, -10., 15.)

entries = tree.GetEntries()
evtCounter = 0
for dv in tree:
    evtCounter += 1
    if (evtCounter % 100000 == 0):
        print("Processed {}/{}".format(evtCounter, entries))

    ntrk = dv.ntrk
    sig = dv.significance
    mass = dv.mass
    isSame = dv.sameEvent
    dR = dv.dR
    dz = r.TMath.Abs(dv.deltaZ)
    det = r.TMath.Log10(dv.det)

    ntrkBin = getNtrkBin(ntrk)
    dzBin = dzRatioHistDict[ntrkBin].FindBin(dz)
    dzWeight = dzRatioHistDict[ntrkBin].GetBinContent(dzBin)
    if (isSame):
        sigSameDict[ntrkBin].Fill(sig)
        sigSameBeforeDict[ntrkBin].Fill(sig)
        sig_det_sameDict[ntrkBin].Fill(sig, det)
    else:
        sigMixedDict[ntrkBin].Fill(sig, dzWeight)
        sigMixedBeforeDict[ntrkBin].Fill(sig)
        sig_det_mixedDict[ntrkBin].Fill(sig, det)

# Save histograms
c = r.TCanvas("c", "c", 800, 700)
c.cd()
sampleLabel = r.TLatex()
sampleLabel.SetNDC()
sampleLabel.SetTextFont(42)
sampleLabel.SetTextSize(0.03)
sampleLabel.SetTextAlign(13)
dataLabel = dataSet + ", di-jet"

for ntrk in ntrkList:
    sigSameHist = sigSameDict[ntrk]
    sigMixedHist = sigMixedDict[ntrk]
    sigSameBeforeHist = sigSameBeforeDict[ntrk]
    sigMixedBeforeHist = sigMixedBeforeDict[ntrk]

    # With dz weight
    sigRatioHist = sigSameHist.Clone("sigRatio_"+ntrk)
    bin1 = sigSameHist.FindBin(100.)
    bin2 = sigSameHist.GetNbinsX() + 1
    sf = sigRatioHist.Integral(bin1, bin2) / sigMixedHist.Integral(bin1, bin2)
    sigMixedHist.Sumw2()
    sigMixedHist.Scale(sf)
    sigRatioHist.Divide(sigMixedHist)

    c.SetLogy(0)
    sigRatioHist.Draw("hist")
    ATLASLabel(0.20, 0.955, label)
    sampleLabel.DrawLatex(0.65, 0.85, dataLabel)
    sampleLabel.DrawLatex(0.65, 0.80, "Event preselection")
    sampleLabel.DrawLatex(0.65, 0.75, getNtrkLabel(ntrk))
    c.Print("{}/{}.pdf".format(directory, "sigRatio_"+ntrk))


    sigMixedHist.SetLineColor(r.kRed)
    sigSameHist.Draw("hist")
    sigMixedHist.Draw("hist same")
    ATLASLabel(0.20, 0.955, label)
    sampleLabel.DrawLatex(0.65, 0.85, dataLabel)
    sampleLabel.DrawLatex(0.65, 0.80, "Event preselection")
    sampleLabel.DrawLatex(0.65, 0.75, getNtrkLabel(ntrk))
    c.Print("{}/{}.pdf".format(directory, "same_vs_mixed_"+ntrk))

    # Before dz weight
    sigRatioBeforeHist = sigSameBeforeHist.Clone("sigRatioBefore_"+ntrk)
    bin1 = sigSameHist.FindBin(100.)
    bin2 = sigSameHist.GetNbinsX() + 1
    sf = sigRatioBeforeHist.Integral(bin1, bin2) / sigMixedBeforeHist.Integral(bin1, bin2)
    sigMixedBeforeHist.Sumw2()
    sigMixedBeforeHist.Scale(sf)
    sigRatioBeforeHist.Divide(sigMixedBeforeHist)

    c.SetLogy(0)
    sigRatioBeforeHist.Draw("hist")
    ATLASLabel(0.20, 0.955, label)
    sampleLabel.DrawLatex(0.65, 0.85, dataLabel)
    sampleLabel.DrawLatex(0.65, 0.80, "Event preselection")
    sampleLabel.DrawLatex(0.65, 0.75, getNtrkLabel(ntrk))
    c.Print("{}/{}.pdf".format(directory, "sigRatioBefore_"+ntrk))


    sigMixedBeforeHist.SetLineColor(r.kRed)
    sigSameBeforeHist.Draw("hist")
    sigMixedBeforeHist.Draw("hist same")
    ATLASLabel(0.20, 0.955, label)
    sampleLabel.DrawLatex(0.65, 0.85, dataLabel)
    sampleLabel.DrawLatex(0.65, 0.80, "Event preselection")
    sampleLabel.DrawLatex(0.65, 0.75, getNtrkLabel(ntrk))
    c.Print("{}/{}.pdf".format(directory, "same_vs_mixed_before_"+ntrk))


    # Before vs after
    sigMixedHist.SetLineColor(r.kBlack)
    sigMixedHist.Draw("hist")
    sigMixedBeforeHist.Draw("hist same")
    ATLASLabel(0.20, 0.955, label)
    sampleLabel.DrawLatex(0.65, 0.85, dataLabel)
    sampleLabel.DrawLatex(0.65, 0.80, "Event preselection")
    sampleLabel.DrawLatex(0.65, 0.75, getNtrkLabel(ntrk))
    c.Print("{}/{}.pdf".format(directory, "mixed_before_after_"+ntrk))


    # sig vs det
    sig_det_sameHist = sig_det_sameDict[ntrk]
    sig_det_sameHist.Draw("colz")
    ATLASLabel(0.20, 0.955, label)
    sampleLabel.DrawLatex(0.65, 0.85, dataLabel)
    sampleLabel.DrawLatex(0.65, 0.80, "Event preselection")
    sampleLabel.DrawLatex(0.65, 0.75, getNtrkLabel(ntrk))
    c.Print("{}/{}.pdf".format(directory, "sig_det_same_"+ntrk))

    sig_det_mixedHist = sig_det_mixedDict[ntrk]
    sig_det_mixedHist.Draw("colz")
    ATLASLabel(0.20, 0.955, label)
    sampleLabel.DrawLatex(0.65, 0.85, dataLabel)
    sampleLabel.DrawLatex(0.65, 0.80, "Event preselection")
    sampleLabel.DrawLatex(0.65, 0.75, getNtrkLabel(ntrk))
    c.Print("{}/{}.pdf".format(directory, "sig_det_mixed_"+ntrk))

    sigDetSame_profX = sig_det_sameHist.ProfileX()
    sigDetMixed_profX = sig_det_mixedHist.ProfileX()
    sigDetSame_profY = sig_det_sameHist.ProfileY()
    sigDetMixed_profY = sig_det_mixedHist.ProfileY()

    sigDetMixed_profX.SetLineColor(r.kRed)
    sigDetMixed_profX.SetMarkerColor(r.kRed)
    sigDetMixed_profY.SetLineColor(r.kRed)
    sigDetMixed_profY.SetMarkerColor(r.kRed)

    leg = r.TLegend(0.65, 0.55, 0.85, 0.70)
    decoLegend(leg)
    leg.AddEntry(sigDetSame_profX, "Same-event", "l")
    leg.AddEntry(sigDetMixed_profX, "Mixed-event", "l")
    
    if (sigDetSame_profX.GetMaximum() > sigDetMixed_profX.GetMaximum()):
        maximum = sigDetSame_profX.GetMaximum()
    else:
        maximum = sigDetMixed_profX.GetMaximum()
    sigDetSame_profX.SetMaximum(maximum*1.2)
    sigDetSame_profX.Draw("hist e")
    sigDetMixed_profX.Draw("hist e same")
    ATLASLabel(0.20, 0.955, label)
    sampleLabel.DrawLatex(0.65, 0.85, dataLabel)
    sampleLabel.DrawLatex(0.65, 0.80, "Event preselection")
    sampleLabel.DrawLatex(0.65, 0.75, getNtrkLabel(ntrk))
    leg.Draw()
    c.Print("{}/{}.pdf".format(directory, "sigDet_profX_"+ntrk))

    rp_profX = r.TRatioPlot(sigDetSame_profX, sigDetMixed_profX)
    decoRatioPlot(rp_profX, 2.0, 0.0)
    ATLASLabel(0.20, 0.955, label)
    sampleLabel.DrawLatex(0.65, 0.85, dataLabel)
    sampleLabel.DrawLatex(0.65, 0.80, "Event preselection")
    sampleLabel.DrawLatex(0.65, 0.75, getNtrkLabel(ntrk))
    leg.Draw()
    c.Print("{}/{}.pdf".format(directory, "profX_ratio_"+ntrk))


    if (sigDetSame_profY.GetMaximum() > sigDetMixed_profY.GetMaximum()):
        maximum = sigDetSame_profY.GetMaximum()
    else:
        maximum = sigDetMixed_profY.GetMaximum()
    sigDetSame_profY.SetMaximum(maximum*1.2)
    sigDetSame_profY.Draw("hist e")
    sigDetMixed_profY.Draw("hist e same")
    ATLASLabel(0.20, 0.955, label)
    sampleLabel.DrawLatex(0.65, 0.85, dataLabel)
    sampleLabel.DrawLatex(0.65, 0.80, "Event preselection")
    sampleLabel.DrawLatex(0.65, 0.75, getNtrkLabel(ntrk))
    leg.Draw()
    c.Print("{}/{}.pdf".format(directory, "sigDet_profY_"+ntrk))

    rp_profY = r.TRatioPlot(sigDetSame_profY, sigDetMixed_profY)
    decoRatioPlot(rp_profY, 1.8, 0.2)
    ATLASLabel(0.20, 0.955, label)
    sampleLabel.DrawLatex(0.65, 0.85, dataLabel)
    sampleLabel.DrawLatex(0.65, 0.80, "Event preselection")
    sampleLabel.DrawLatex(0.65, 0.75, getNtrkLabel(ntrk))
    leg.Draw()
    c.Print("{}/{}.pdf".format(directory, "profY_ratio_"+ntrk))
