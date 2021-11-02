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

def getDVTypeLabel(dvType):
    typeLabel = ""
    if dvType == 1:
        typeLabel = "G4 DV"
    if dvType == 2:
        typeLabel = "G4 + PU DV"
    if dvType == 3:
        typeLabel = "G4 + Gen DV"
    if dvType == 4:
        typeLabel = "PU DV"
    if dvType == 5:
        typeLabel = "Gen + PU DV"
    if dvType == 6:
        typeLabel = "Gen DV"
    if dvType == 7:
        typeLabel = "G4 + Gen + PU DV"
    return typeLabel

def prepareLatex():
    sampleLabel = r.TLatex()
    sampleLabel.SetNDC()
    sampleLabel.SetTextFont(42)
    sampleLabel.SetTextAlign(13)
    sampleLabel.SetTextSize(0.03)
    return sampleLabel

def setHistColor(hist, col):
    hist.SetLineColor(col)
    hist.SetMarkerColor(col)

def divideError(num1, num2, e1, e2):
    centerValue = num1 / num2
    term1 = e1/num2
    term2 = (num1*e2)/(num2*num2)
    error = r.TMath.Sqrt(term1**2 + term2**2)
    return centerValue, error

def multiplyError(num1, num2, e1, e2):
    centerValue = num1 * num2
    term1 = num2 * e1
    term2 = num1 * e2
    error = r.TMath.Sqrt(term1**2 + term2**2)
    return centerValue, error

def getTotalRate(rateList, errList):
    totalRate = rateList[0]
    totalError = errList[0]
    for i in range(1, len(rateList)):
        if (rateList[i] != 0):
            totalRate *= rateList[i]
    for i in range(len(errList)-1):
        if (errList[i] != 0 and errList[i+1] != 0):
            tmpRate, tmpError = multiplyError(rateList[i+1], rateList[i], errList[i+1], errList[i])
            totalError *= tmpError

    return totalRate, totalError
