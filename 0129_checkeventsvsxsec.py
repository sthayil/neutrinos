#Takes as input root file + picke file that has nevents, xsec, nparticles etc. Makes plots.
#UPDATE: change binning to 0.025, sigmafac constt to *40

from ROOT import *
from array import array
from math import *
import sys, os, glob, fnmatch, time
import pickle
from datetime import datetime
datetime = datetime.now().strftime('%Y%m%d_%H%M%S')
import satstyle1

satstyle1.setsatstyle1()

inputfiles = [ \
"/afs/cern.ch/work/s/sthayil/experimentalneutrinos/1115_threerangesamples/numu_0-1Gev_100kev_gntp.0.gst.root", \
"/afs/cern.ch/work/s/sthayil/experimentalneutrinos/1115_threerangesamples/numu_1-2Gev_100kev_gntp.0.gst.root", \
"/afs/cern.ch/work/s/sthayil/experimentalneutrinos/1115_threerangesamples/numu_2-10Gev_100kev_gntp.0.gst.root", \
]

# outputfile = "overlay_1029.root"
# out_file = TFile(outputfile, 'recreate')

#Constants
nbench=4.070260816327924
constt=3.21
pdgs = [11, 12, 13, 14, 22, 2112, 2212, 1000070140, 1000080160]

#Declare histograms
hist_unweighednuE            = TH1F('hist_unweighednuE',         'hist_unweighednuE',400,0,10)
hist_xsecweighednuE          = TH1F('hist_xsecweighednuE',       'hist_xsecweighednuE',400,0,10)
hist_xsecfluxweighednuE      = TH1F('hist_xsecfluxweighednuE',   'hist_xsecfluxweighednuE',400,0,10)
hist_xsecfluxfacweighednuE   = TH1F('hist_xsecfluxfacweighednuE','hist_xsecfluxfacweighednuE',400,0,10)

hist_unweighednuE.Sumw2()            
hist_xsecweighednuE.Sumw2()
hist_xsecfluxweighednuE.Sumw2()        
hist_xsecfluxfacweighednuE.Sumw2()     

#First event loop
for inputfile in inputfiles:
    picklename = inputfile[:-5]+'.pickle'
    
    ifile = TFile(inputfile)
    tree = ifile.Get("gst")

    with open(picklename, 'rb') as f:
        inputev = pickle.load(f)
        sigmaeff = pickle.load(f)
        weights = pickle.load(f)
        pdgs = pickle.load(f)
        pdgfreq = pickle.load(f)
        
    print inputfile    
    print 'inputev = ', inputev
    print 'sigmaeff =', sigmaeff
    print 'pdgids  = ', pdgs
    print 'pdgfreq = ', pdgfreq

    #Constants
    sigmafac=sigmaeff*40/inputev
    consttfac = nbench*constt#*4*pi

#Fill histos
    for i in range(tree.GetEntries()): #for each event
        tree.GetEntry(i)
        fluxwt=weights[i]

        hist_unweighednuE.Fill(tree.Ev)
        hist_xsecweighednuE.Fill(tree.Ev,sigmafac)
        hist_xsecfluxweighednuE.Fill(tree.Ev,sigmafac*fluxwt)
        hist_xsecfluxfacweighednuE.Fill(tree.Ev,sigmafac*fluxwt*consttfac)

print "Tot #events: ", hist_xsecfluxfacweighednuE.Integral(2,400) #skip first bin, assumes 400 bins

c = TCanvas()

hist_xsecweighednuE.Draw()
hist_xsecweighednuE.GetXaxis().SetTitle("E_{#nu} (GeV)")
hist_xsecweighednuE.GetYaxis().SetTitle("Cross section (10^{-38} cm^{2})")

xsecfile = TFile("summedxsecplotON_mu_DefaultPlusMEC.root")
xsec = xsecfile.Get("xsec")
xsec.SetLineColor(kBlue)
xsec.Draw("C")

gStyle.SetOptStat(0)

legend = TLegend(0.1,0.7,0.48,0.9)
legend.AddEntry(xsec,"xsec from GENIE splines","l")
legend.AddEntry(hist_xsecweighednuE,"MC events","l")
legend.SetBorderSize(0)
legend.SetFillColor(0)
legend.Draw()

c.Update()

#Write to output root file
# out_file.cd()
# out_file.Write()
# out_file.Close()
