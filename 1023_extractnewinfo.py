#Find sigmaeff, numevents, weights?, find all fsp pdgs; print them out to a pickle file. Hacked right now to give sigmaeff values calculated from xsec spline TGraphs. (1021_....py)
#usage: python 1023_... rootfilename.root

from ROOT import *
import sys, pickle
ifile = sys.argv[1]
filename= ifile[:-5]
print filename

#fluxfile is same for nu, nubar as long as you have right flavour (e/mu)
#if adding nubar, weight of each event is half

inputfile = TFile(ifile)
t1 = inputfile.Get("gst")

def getflux(x):
#    fluxdat = "MuonNeutrinoFluxForGenie.dat" #0, 0,025, 0.05
    fluxdat = "ElectronNeutrinoFluxForGenie.dat" 
    with open(fluxdat) as f1:
        lines = f1.read().splitlines()
    fluxlist = lines[x].split(',')
    flux = fluxlist[1]
    return flux

weights=[]
pdgs=[]
pdgfreq=[]

inputev=t1.GetEntries()

for i in range(inputev): #for each event
    t1.GetEntry(i)

    a = int(t1.Ev/0.025)
    wt = float(getflux(a))
    weights.append(wt)

    for j in range(len(t1.pdgf)):
        pdgs.append(t1.pdgf[j])

sigmaeff = 676.306774013
#E bar (-12) N,O:0.768117,0.231883 0-1, 1-2, 2-10GeV 
#330.8160989
#2.54319851116
#10.0295655163
#318.243334873

#e (12) N,O:0.768117,0.231883 0-1, 1-2, 2-10GeV 
#710.562876739
#8.42080598672
#25.8352967393
#676.306774013

#Mu bar (-14) N,O:0.768117,0.231883 0-1, 1-2, 2-10GeV
#328.999794719
#2.42909444425
#9.8830105472
#316.687689727

#Muon below (14)
#705.295231671 N,O:0.768117,0.231883 0-10GeV
#7.96158076978 N,O:0.768117,0.231883 0-1 GeV
#25.4054828351 N,O:0.768117,0.231883 1-2 GeV
#671.928168066 N,O:0.768117,0.231883 2-10 GeV

#728.546934612 N,O,Ar:0.7512,0.2315,0.0173 0-10GeV
#8.29922878357 N,O,Ar:0.7512,0.2315,0.0173 0-1 GeV
#720.247705829 N,O,Ar:0.7512,0.2315,0.0173 1-10 GeV

#705.904624752 N,O:0.768117,0.231883 0-10GeV
#8.04110588549 N,O:0.768117,0.231883 0-1 GeV
#697.863518866 N,O:0.768117,0.231883 1-10 GeV

from itertools import groupby
pdgs.sort()
pdgfreq = [len(list(group)) for key, group in groupby(pdgs)]

pdgs = list(set(pdgs))
pdgs.sort()

#pickle: filename, inputev, sigmaeff, weights
with open(filename+'.pickle', 'wb') as f:
    pickle.dump(inputev, f)
    pickle.dump(sigmaeff, f)
    pickle.dump(weights, f)
    pickle.dump(pdgs, f)
    pickle.dump(pdgfreq, f)

print len(weights)
print inputev
print sigmaeff
print pdgs
print pdgfreq
