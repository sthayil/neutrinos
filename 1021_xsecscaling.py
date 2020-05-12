#Read xsec splines. print integral from 0-1, 1-2, 2-10 Gev. Make summed xsec TGraph.

from ROOT import *
from array import array
from math import *
import sys, os, glob, fnmatch, time
from datetime import datetime
datetime = datetime.now().strftime('%Y%m%d_%H%M%S')

outputfile = "xsecsplines"+datetime+".root" #output summed xsec tgraph here
out_file = TFile(outputfile, 'recreate')
c1 = TCanvas("c1","",200,10,700,500)
xsecs = []
es = []

#air mix
Nfrac = 0.768117 #0.7512
Ofrac = 0.231883 #0.2315
Arfrac = 0.0 #0.0173
numpts = 10001
stepsize = 0.001

f1 = TFile('DefaultPlusMECWithNC_muon_gxsec.root') #file with xsec splines as root plots; make using gspl2root

dir = f1.Get('nu_mu_N14') #mu_bar, e_bar
energy = 0
for step in range(0,numpts):
    graph1=TGraph(dir.Get('tot_cc'))
    graph2=TGraph(dir.Get('tot_nc'))
    val1=graph1.Eval(energy)
    val2=graph2.Eval(energy)
    xs=val1+val2
    xsecs.append(Nfrac*float(xs))
    es.append(float(energy))
    energy+=stepsize

dir = f1.Get('nu_mu_O16')
energy = 0
for step in range(0,numpts):
    graph1=TGraph(dir.Get('tot_cc'))
    graph2=TGraph(dir.Get('tot_nc'))
    val1=graph1.Eval(energy)
    val2=graph2.Eval(energy)
    xs=val1+val2
    xsecs[step]+=(Ofrac*float(xs))
    energy+=stepsize

dir = f1.Get('nu_mu_Ar40')
energy = 0
for step in range(0,numpts):
    graph1=TGraph(dir.Get('tot_cc'))
    graph2=TGraph(dir.Get('tot_nc'))
    val1=graph1.Eval(energy)
    val2=graph2.Eval(energy)
    xs=val1+val2
    xsecs[step]+=(Arfrac*float(xs))
    energy+=stepsize

xsec = TGraph(numpts, array('f',es), array('f',xsecs))
xsec.SetName("xsec")
xsec.Draw("C")

area = 0
for i in range(len(xsecs)): area+=stepsize*xsecs[i]
print area

area1=0
for i in range(1001): area1+=stepsize*xsecs[i]
print area1
area2=0
for i in range(1001,2001): area2+=stepsize*xsecs[i]
print area2
area3=0
for i in range(2001,10001): area3+=stepsize*xsecs[i]
print area3

out_file.cd()
xsec.Write()
out_file.Close()
