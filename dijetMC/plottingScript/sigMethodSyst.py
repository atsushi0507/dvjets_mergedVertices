import ROOT as r
from ctypes import c_double as double
import sys, os
sys.path.append("/Users/amizukam/DVJets/atlasstyle")
from AtlasStyle import *
from AtlasLabel import *
from utils import *

r.gROOT.SetBatch()
SetAtlasStyle()
label = "Internal"

plotType = "sigSyst"
directory = "pdfs/" + plotType
if (not os.path.isdir(directory)):
    os.makedirs(directory)
if (not os.path.isdir("results")):
    os.makedirs("results")

fileDir = "rootfiles/"
nominalFile = r.TFile(fileDir + "sigAndMass_mc16e.root", "READ")
norm200File = r.TFile(fileDir + "sigAndMass_mc16e_syst_norm200.root", "READ")
norm300File = r.TFile(fileDir + "sigAndMass_mc16e_syst_norm300.root", "READ")
norm400File = r.TFile(fileDir + "sigAndMass_mc16e_syst_norm400.root", "READ")

colors = [r.kBlack, r.kRed, r.kBlue, r.kGreen-2]
ntrkList = ["Ntrk4", "Ntrk5", "Ntrk6", "Ntrk>6"]
weightList = ["noWeight", "sigWeight", "weight"]

outputTexFile = open("results/syst_sigMethod.tex", "w")
texString  = "\\documentclass{article}\n"
texString += "\\usepackage{rotating, multirow}\n"
texString += "\\begin{document}\n"
texString += "\\begin{table}\n"
texString += "\\centering\n"
texString += "\\begin{tabular}{|c || c | c| c | c |}\n"
texString += "\\hline\n"
texString += "& Nominal & $S>200$ & $S>300$ & $S>400$ \\\\\n"
texString += "\\hline\n"

# Get Histograms
nominalMass = {}
norm200Mass = {}
norm300Mass = {}
norm400Mass = {}
for ntrk in ntrkList:
    nominalMass[ntrk] = {}
    norm200Mass[ntrk] = {}
    norm300Mass[ntrk] = {}
    norm400Mass[ntrk] = {}
    for weight in weightList:
        histName = "mergedMass"
        if weight == "noWeight":
            weightName = ""
        else:
            weightName = "_" + weight
        histName = histName + weightName + "_" + ntrk
        nominalMass[ntrk][weight] = nominalFile.Get(histName)
        norm200Mass[ntrk][weight] = norm200File.Get(histName)
        norm300Mass[ntrk][weight] = norm300File.Get(histName)
        norm400Mass[ntrk][weight] = norm400File.Get(histName)

# Calculate somethings
c = r.TCanvas("c", "c",  800, 700)
c.SetLogy(1)
countValue = {"Ntrk4": 20., "Ntrk5": 10., "Ntrk6": 10., "Ntrk>6": 10.}
for ntrk in ntrkList:
    for weight in weightList:
        nominalHist = nominalMass[ntrk][weight]
        norm200Hist = norm200Mass[ntrk][weight]
        norm300Hist = norm300Mass[ntrk][weight]
        norm400Hist = norm400Mass[ntrk][weight]

        nominalHist.SetLineColor(colors[0])
        nominalHist.SetMarkerColor(colors[0])
        norm200Hist.SetLineColor(colors[1])
        norm200Hist.SetMarkerColor(colors[1])
        norm300Hist.SetLineColor(colors[2])
        norm300Hist.SetMarkerColor(colors[2])
        norm400Hist.SetLineColor(colors[3])
        norm400Hist.SetMarkerColor(colors[3])

        normBin  = nominalHist.FindBin(countValue[ntrk])
        nbins = nominalHist.GetNbinsX() + 1

        try:
            sfnom = 10000. / nominalHist.Integral(1, nbins)
            sf200 = 10000. / norm200Hist.Integral(1, nbins)
            sf300 = 10000. / norm300Hist.Integral(1, nbins)
            sf400 = 10000. / norm400Hist.Integral(1, nbins)
        except ZeroDivisionError:
            sfnom = 1.
            sf200 = 1.
            sf300 = 1.
            sf400 = 1.

        if (weight == "noWeight"):
            nominalHist.Sumw2()
        nominalHist.Scale(sfnom)
        norm200Hist.Scale(sf200)
        norm300Hist.Scale(sf300)
        norm400Hist.Scale(sf400)
        
        leg = r.TLegend(0.63, 0.62, 0.78, 0.78)
        decorateLeg(leg)
        leg.AddEntry(nominalHist, "Normalized in S > 100", "l")
        leg.AddEntry(norm200Hist, "Normalized in S > 200", "l")
        leg.AddEntry(norm300Hist, "Normalized in S > 300", "l")
        leg.AddEntry(norm400Hist, "Normalized in S > 400", "l")

        sampleLabel = prepareLatex()
        
        nominalHist.Draw("hist e0")
        norm200Hist.Draw("hist e0 same")
        norm300Hist.Draw("hist e0 same")
        norm400Hist.Draw("hist e0 same")
        ATLASLabel(0.20, 0.955, label)
        leg.Draw()
        sampleLabel.DrawLatex(0.65, 0.94, "mc16e, di-jet MC")
        sampleLabel.DrawLatex(0.65, 0.90, "Event preselection")
        sampleLabel.DrawLatex(0.65, 0.86, getNtrkLabel(ntrk))
        sampleLabel.DrawLatex(0.65, 0.82, "Normalized to 10000")
        c.Print("{}/{}.pdf".format(directory, "sigMass_"+weight+ntrk))

        
        # Count hists
        errNominal = double(0.)
        errNorm200 = double(0.)
        errNorm300 = double(0.)
        errNorm400 = double(0.)

        countBin = nominalHist.FindBin(countValue[ntrk])
        
        cntNominal = nominalHist.IntegralAndError(countBin, nbins, errNominal)
        cntNorm200 = norm200Hist.IntegralAndError(countBin, nbins, errNorm200)
        cntNorm300 = norm300Hist.IntegralAndError(countBin, nbins, errNorm300)
        cntNorm400 = norm400Hist.IntegralAndError(countBin, nbins, errNorm400)

        diffNom = 100 * (cntNominal - cntNominal) / cntNominal
        diff200 = 100 * (cntNorm200 - cntNominal) / cntNominal
        diff300 = 100 * (cntNorm300 - cntNominal) / cntNominal
        diff400 = 100 * (cntNorm400 - cntNominal) / cntNominal

        print(ntrk, weight)
        print(cntNominal, errNominal.value)
        print(cntNorm200, errNorm200.value, str(diff200)+"%")
        print(cntNorm300, errNorm300.value, str(diff300)+"%")
        print(cntNorm400, errNorm400.value, str(diff400)+"%")

        print()

        texString += "\\verb| " + weight + "| & ${:.2f}".format(cntNominal) + " \pm {:.2f}$".format(errNominal.value) + " & ${:.2f}".format(cntNorm200) + " \pm {:.2f}$".format(errNorm200.value) +" & ${:.2f}".format(cntNorm300) + " \pm {:.2f}$".format(errNorm300.value) + " & ${:.2f}".format(cntNorm400) + " \pm {:.2f}$".format(errNorm400.value) + "\\\\\n"
        texString += "\\verb| " +  " |& ${:.2f}\%$".format(diffNom) + " & ${:.2f}\%$".format(diff200) +" & ${:.2f}\%$".format(diff300) + " & ${:.2f}\%$".format(diff400) + "\\\\\n"
    texString += "\\hline\n"

texString += "\\end{tabular}\n"
texString += "\\end{table}\n"
texString += "\\end{document}\n"

outputTexFile.write(texString)
outputTexFile.close()
