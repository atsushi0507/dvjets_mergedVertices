import ROOT as r

def decorateRatioPlot(rp):
    rp.SetH2DrawOpt("hist")
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

def getNtrkBin_from2(ntrk):
    ntrkBin = ""
    if ntrk == 2:
        ntrkBin = "Ntrk4"
    if ntrk == 3:
        ntrkBin = "Ntrk5"
    if ntrk == 4:
        ntrkBin = "Ntrk6"
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

def getNtrkLabel_from2(ntrkBin):
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

def prepareLatex():
    sampleLabel = r.TLatex()
    sampleLabel.SetNDC()
    sampleLabel.SetTextFont(42)
    sampleLabel.SetTextAlign(13)
    sampleLabel.SetTextSize(0.03)
    return sampleLabel
