#Takes as input root file + pickle file that has nevents, xsec, nparticles etc. Makes plots.
#UPDATE JAN2020: change binning of ev to 0.025, sigmafac constt to *40 to account for david's fluxtable
#USAGE: python 0130...py e (or ebar or mu or mubar)

from ROOT import *
from array import array
from math import *
import sys, os, glob, fnmatch, time
import pickle
from datetime import datetime
datetime = datetime.now().strftime('%Y%m%d_%H%M%S')
import satstyle1

satstyle1.setsatstyle1()

flavour = sys.argv[1] #mu, e, ebar, mubar
print "Type: ", flavour 

inputfiles = [ \
"/afs/cern.ch/work/s/sthayil/experimentalneutrinos/1115_threerangesamples/nu"+flavour+"_0-1Gev_100kev_gntp.0.gst.root", \
"/afs/cern.ch/work/s/sthayil/experimentalneutrinos/1115_threerangesamples/nu"+flavour+"_1-2Gev_100kev_gntp.0.gst.root", \
"/afs/cern.ch/work/s/sthayil/experimentalneutrinos/1115_threerangesamples/nu"+flavour+"_2-10Gev_100kev_gntp.0.gst.root", \
]

outputfile = "newplotstest_"+flavour+".root"
out_file = TFile(outputfile, 'recreate')

#Constants
if flavour=='ebar' or flavour=='e':
    nbench=1.94968984573508 #el
else:
    nbench=4.070260816327924 #mu
print nbench

constt=3.21*0.5 #*0.5 to account for equal contribution from nu and anti nu
pdgs = [11, 12, 13, 14, 22, 2112, 2212, 1000070140, 1000080160]

testbeta=0.8

#Declare histograms
hist_unweighednuE            = TH1F('hist_unweighednuE',         'hist_unweighednuE',400,0,10)
hist_xsecweighednuE          = TH1F('hist_xsecweighednuE',       'hist_xsecweighednuE',400,0,10)
hist_xsecfluxweighednuE      = TH1F('hist_xsecfluxweighednuE',   'hist_xsecfluxweighednuE',400,0,10)
hist_xsecfluxfacweighednuE   = TH1F('hist_xsecfluxfacweighednuE','hist_xsecfluxfacweighednuE',400,0,10)

hist_twotracksbetapt5        = TH1F('hist_twotracksbetapt5','hist_twotracksbetapt5',400,0,10)
hist_twotracksbetapt9        = TH1F('hist_twotracksbetapt9','hist_twotracksbetapt9',400,0,10)
hist_twotracksbetapt95       = TH1F('hist_twotracksbetapt95','hist_twotracksbetapt95',400,0,10)
hist_twotracksbetatest       = TH1F('hist_twotracksbetatest','hist_twotracksbetatest',400,0,10)
hist_twoparticlesbetapt5     = TH1F('hist_twoparticlesbetapt5', 'hist_twoparticlesbetapt5',400,0,10)
hist_twoparticlesbetapt9     = TH1F('hist_twoparticlesbetapt9', 'hist_twoparticlesbetapt9',400,0,10)
hist_twoparticlesbetapt95    = TH1F('hist_twoparticlesbetapt95','hist_twoparticlesbetapt95',400,0,10)
hist_twoparticlesbetatest    = TH1F('hist_twoparticlesbetatest','hist_twoparticlesbetatest',400,0,10)
hist_threetracksbetapt5      = TH1F('hist_threetracksbetapt5', 'hist_threetracksbetapt5',400,0,10)
hist_threetracksbetapt9      = TH1F('hist_threetracksbetapt9', 'hist_threetracksbetapt9',400,0,10)
hist_threetracksbetapt95     = TH1F('hist_threetracksbetapt95','hist_threetracksbetapt95',400,0,10)
hist_threetracksbetatest     = TH1F('hist_threetracksbetatest','hist_threetracksbetatest',400,0,10)
hist_threeparticlesbetapt5   = TH1F('hist_threeparticlesbetapt5', 'hist_threeparticlesbetapt5',400,0,10)
hist_threeparticlesbetapt9   = TH1F('hist_threeparticlesbetapt9', 'hist_threeparticlesbetapt9',400,0,10)
hist_threeparticlesbetapt95  = TH1F('hist_threeparticlesbetapt95','hist_threeparticlesbetapt95',400,0,10)
hist_threeparticlesbetatest  = TH1F('hist_threeparticlesbetatest','hist_threeparticlesbetatest',400,0,10)

hist_eventangleweight_b0pt0  = TH1D('hist_eventangleweight_b0pt0' ,'hist_eventangleweight_b0pt0',100,0,1)
hist_eventangleweight_b0pt5  = TH1D('hist_eventangleweight_b0pt5' ,'hist_eventangleweight_b0pt5',100,0,1)
hist_eventangleweight_b0pt9  = TH1D('hist_eventangleweight_b0pt9' ,'hist_eventangleweight_b0pt9',100,0,1)
hist_eventangleweight_b0pt95 = TH1D('hist_eventangleweight_b0pt95','hist_eventangleweight_b0pt95',100,0,1)
hist_eventangleweight_b0test = TH1D('hist_eventangleweight_b0test','hist_eventangleweight_b0test',100,0,1)

hist_chargedeventangleweight_b0pt0  = TH1D('hist_chargedeventangleweight_b0pt0' ,'hist_chargedeventangleweight_b0pt0',100,0,1)
hist_chargedeventangleweight_b0pt5  = TH1D('hist_chargedeventangleweight_b0pt5' ,'hist_chargedeventangleweight_b0pt5',100,0,1)
hist_chargedeventangleweight_b0pt9  = TH1D('hist_chargedeventangleweight_b0pt9' ,'hist_chargedeventangleweight_b0pt9',100,0,1)
hist_chargedeventangleweight_b0pt95 = TH1D('hist_chargedeventangleweight_b0pt95','hist_chargedeventangleweight_b0pt95',100,0,1)
hist_chargedeventangleweight_b0test = TH1D('hist_chargedeventangleweight_b0test','hist_chargedeventangleweight_b0test',100,0,1)

hist_angleweighedtwotracks               = TH1F('hist_angleweighedtwotracks',           'hist_angleweighedtwotracks',400,0,10)
hist_angleweighedtwotracksbetapt5        = TH1F('hist_angleweighedtwotracksbetapt5',    'hist_angleweighedtwotracksbetapt5',400,0,10)
hist_angleweighedtwotracksbetapt9        = TH1F('hist_angleweighedtwotracksbetapt9',    'hist_angleweighedtwotracksbetapt9',400,0,10)
hist_angleweighedtwotracksbetapt95       = TH1F('hist_angleweighedtwotracksbetapt95',   'hist_angleweighedtwotracksbetapt95',400,0,10)
hist_angleweighedtwotracksbetatest       = TH1F('hist_angleweighedtwotracksbetatest',   'hist_angleweighedtwotracksbetatest',400,0,10)
hist_angleweighedtwoparticles            = TH1F('hist_angleweighedtwoparticles',        'hist_angleweighedtwoparticles',400,0,10)
hist_angleweighedtwoparticlesbetapt5     = TH1F('hist_angleweighedtwoparticlesbetapt5', 'hist_angleweighedtwoparticlesbetapt5',400,0,10)
hist_angleweighedtwoparticlesbetapt9     = TH1F('hist_angleweighedtwoparticlesbetapt9', 'hist_angleweighedtwoparticlesbetapt9',400,0,10)
hist_angleweighedtwoparticlesbetapt95    = TH1F('hist_angleweighedtwoparticlesbetapt95','hist_angleweighedtwoparticlesbetapt95',400,0,10)
hist_angleweighedtwoparticlesbetatest    = TH1F('hist_angleweighedtwoparticlesbetatest','hist_angleweighedtwoparticlesbetatest',400,0,10)

hist_tetrahedangle = TH1F('hist_tetrahedangle','hist_tetrahedangle',126,0,12.6)
hist_tetrahedangle.Sumw2()

hist_unweighednuE.Sumw2()            
hist_xsecweighednuE.Sumw2()
hist_xsecfluxweighednuE.Sumw2()        
hist_xsecfluxfacweighednuE.Sumw2()     
hist_twotracksbetapt5.Sumw2()
hist_twotracksbetapt9.Sumw2()
hist_twotracksbetapt95.Sumw2()
hist_twotracksbetatest.Sumw2()
hist_twoparticlesbetapt5.Sumw2()
hist_twoparticlesbetapt9.Sumw2()
hist_twoparticlesbetapt95.Sumw2()
hist_twoparticlesbetatest.Sumw2()
hist_threetracksbetapt5.Sumw2()
hist_threetracksbetapt9.Sumw2()
hist_threetracksbetapt95.Sumw2()
hist_threetracksbetatest.Sumw2()
hist_threeparticlesbetapt5.Sumw2()
hist_threeparticlesbetapt9.Sumw2()
hist_threeparticlesbetapt95.Sumw2()
hist_threeparticlesbetatest.Sumw2()
hist_eventangleweight_b0pt0.Sumw2()
hist_eventangleweight_b0pt5.Sumw2()
hist_eventangleweight_b0pt9.Sumw2()
hist_eventangleweight_b0pt95.Sumw2()
hist_eventangleweight_b0test.Sumw2()
hist_chargedeventangleweight_b0pt0.Sumw2()
hist_chargedeventangleweight_b0pt5.Sumw2()
hist_chargedeventangleweight_b0pt9.Sumw2()
hist_chargedeventangleweight_b0pt95.Sumw2()
hist_chargedeventangleweight_b0test.Sumw2()
hist_angleweighedtwotracks.Sumw2()
hist_angleweighedtwotracksbetapt5.Sumw2()
hist_angleweighedtwotracksbetapt9.Sumw2()
hist_angleweighedtwotracksbetapt95.Sumw2()
hist_angleweighedtwotracksbetatest.Sumw2()
hist_angleweighedtwoparticles.Sumw2()
hist_angleweighedtwoparticlesbetapt5.Sumw2()
hist_angleweighedtwoparticlesbetapt9.Sumw2()
hist_angleweighedtwoparticlesbetapt95.Sumw2()
hist_angleweighedtwoparticlesbetatest.Sumw2()

hist_angleweighedbetaofalltracks  = TH1D('hist_angleweighedbetaofalltracks' ,'hist_angleweighedbetaofalltracks',100,0,1)
hist_angleweighedbetaofallparticles  = TH1D('hist_angleweighedbetaofallparticles' ,'hist_angleweighedbetaofallparticles',100,0,1)
hist_angleweighednumtracks = TH1D('hist_angleweighednumtracks' ,'hist_angleweighednumtracks',25,0,25)
hist_angleweighednumparticles = TH1D('hist_angleweighednumparticles' ,'hist_angleweighednumparticles',45,0,45)

#Declare arrays
chargedbetaover0,chargedbetaoverpt5,chargedbetaoverpt9,chargedbetaoverpt95,chargedbetaovertest=[],[],[],[],[]
betaover0,betaoverpt5,betaoverpt9,betaoverpt95,betaovertest=[],[],[],[],[]
threechargedbetaover0,threechargedbetaoverpt5,threechargedbetaoverpt9,threechargedbetaoverpt95,threechargedbetaovertest=[],[],[],[],[]
threebetaover0,threebetaoverpt5,threebetaoverpt9,threebetaoverpt95,threebetaovertest=[],[],[],[],[]
allchargedparticles_b0pt0,allchargedparticles_b0pt5,allchargedparticles_b0pt9,allchargedparticles_b0pt95,allchargedparticles_b0test=[],[],[],[],[]
allparticles_b0pt0,allparticles_b0pt5,allparticles_b0pt9,allparticles_b0pt95,allparticles_b0test=[],[],[],[],[]
allanglescharged_b0pt0 ,allanglescharged_b0pt5 ,allanglescharged_b0pt9 ,allanglescharged_b0pt95 ,allanglescharged_b0test =[],[],[],[],[]
allangles_b0pt0 ,allangles_b0pt5 ,allangles_b0pt9 ,allangles_b0pt95 ,allangles_b0test =[],[],[],[],[]
eventangleweight_b0pt0 ,eventangleweight_b0pt5 ,eventangleweight_b0pt9 ,eventangleweight_b0pt95 ,eventangleweight_b0test =[],[],[],[],[]
eventangleweightcharged_b0pt0 ,eventangleweightcharged_b0pt5 ,eventangleweightcharged_b0pt9 ,eventangleweightcharged_b0pt95 ,eventangleweightcharged_b0test =[],[],[],[],[]


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
    sigmafac=sigmaeff*40/inputev #0.025 GeV bins
    consttfac = nbench*constt

    for i in range(tree.GetEntries()): #for each event
        tree.GetEntry(i)

        #fspbetas=[]

        numchargedpart0=        numchargedpart5=        numchargedpart9=        numchargedpart95=        numchargedparttest=0
        numpart0=        numpart5=        numpart9=        numpart95=        numparttest=0
        eventchargedparticles_b0pt0,        eventchargedparticles_b0pt5,        eventchargedparticles_b0pt9,        eventchargedparticles_b0pt95,        eventchargedparticles_b0test=[],[],[],[],[]
        eventparticles_b0pt0,        eventparticles_b0pt5,        eventparticles_b0pt9,        eventparticles_b0pt95,   eventparticles_b0test=[],[],[],[],[]

        #In an event, loop over particles. If  beta>0.5, set flag. If >0.9, set other flag.
        for j in range(len(tree.pdgf)): #for each final state particle in that event
            beta = float(tree.pf[j])/float(tree.Ef[j])
            #fspbetas.append(beta)
            #if int( all(beta >= 0.9 for i in fspbetas) )
            particle = TLorentzVector(tree.pxf[j],tree.pyf[j],tree.pzf[j],tree.Ef[j])
                
            if tree.chargef[j]==0: #neutral particles
                numpart0+=1
                eventparticles_b0pt0.append(particle)
                if beta>0.5:
                    numpart5+=1
                    eventparticles_b0pt5.append(particle)
                if beta>0.9:
                    numpart9+=1
                    eventparticles_b0pt9.append(particle)
                if beta>0.95:
                    numpart95+=1
                    eventparticles_b0pt95.append(particle)
                if beta>testbeta:
                    numparttest+=1
                    eventparticles_b0test.append(particle)

            else: #charged particles
                numchargedpart0+=1
                eventchargedparticles_b0pt0.append(particle)
                numpart0+=1
                eventparticles_b0pt0.append(particle)
                if beta>0.5:
                    numchargedpart5+=1
                    eventchargedparticles_b0pt5.append(particle)
                    numpart5+=1
                    eventparticles_b0pt5.append(particle)
                if beta>0.9:
                    numchargedpart9+=1
                    eventchargedparticles_b0pt9.append(particle)
                    numpart9+=1
                    eventparticles_b0pt9.append(particle)
                if beta>0.95:
                    numchargedpart95+=1
                    eventchargedparticles_b0pt95.append(particle)
                    numpart95+=1
                    eventparticles_b0pt95.append(particle)
                if beta>testbeta:
                    numchargedparttest+=1
                    eventchargedparticles_b0test.append(particle)
                    numparttest+=1
                    eventparticles_b0test.append(particle)

        if numchargedpart0>1: chargedbetaover0.append(1)
        else: chargedbetaover0.append(0)
        if numchargedpart5>1: chargedbetaoverpt5.append(1)
        else: chargedbetaoverpt5.append(0)
        if numchargedpart9>1: chargedbetaoverpt9.append(1)
        else: chargedbetaoverpt9.append(0)
        if numchargedpart95>1: chargedbetaoverpt95.append(1)
        else: chargedbetaoverpt95.append(0)
        if numchargedparttest>1: chargedbetaovertest.append(1)
        else: chargedbetaovertest.append(0)

        if numpart0>1: betaover0.append(1)
        else: betaover0.append(0)
        if numpart5>1: betaoverpt5.append(1)
        else: betaoverpt5.append(0)
        if numpart9>1: betaoverpt9.append(1)
        else: betaoverpt9.append(0)
        if numpart95>1: betaoverpt95.append(1)
        else: betaoverpt95.append(0)
        if numparttest>1: betaovertest.append(1)
        else: betaovertest.append(0)

        if numchargedpart0>2: threechargedbetaover0.append(1)
        else: threechargedbetaover0.append(0)
        if numchargedpart5>2: threechargedbetaoverpt5.append(1)
        else: threechargedbetaoverpt5.append(0)
        if numchargedpart9>2: threechargedbetaoverpt9.append(1)
        else: threechargedbetaoverpt9.append(0)
        if numchargedpart95>2: threechargedbetaoverpt95.append(1)
        else: threechargedbetaoverpt95.append(0)
        if numchargedparttest>2: threechargedbetaovertest.append(1)
        else: threechargedbetaovertest.append(0)

        if numpart0>2: threebetaover0.append(1)
        else: threebetaover0.append(0)
        if numpart5>2: threebetaoverpt5.append(1)
        else: threebetaoverpt5.append(0)
        if numpart9>2: threebetaoverpt9.append(1)
        else: threebetaoverpt9.append(0)
        if numpart95>2: threebetaoverpt95.append(1)
        else: threebetaoverpt95.append(0)
        if numparttest>2: threebetaovertest.append(1)
        else: threebetaovertest.append(0)

        allchargedparticles_b0pt0.append( eventchargedparticles_b0pt0) #event particles is an array of tlorentzvectors; allparticles is an array of these arrays
        allchargedparticles_b0pt5.append( eventchargedparticles_b0pt5)
        allchargedparticles_b0pt9.append( eventchargedparticles_b0pt9)
        allchargedparticles_b0pt95.append(eventchargedparticles_b0pt95)
        allchargedparticles_b0test.append(eventchargedparticles_b0test)

        allparticles_b0pt0.append( eventparticles_b0pt0)
        allparticles_b0pt5.append( eventparticles_b0pt5)
        allparticles_b0pt9.append( eventparticles_b0pt9)
        allparticles_b0pt95.append(eventparticles_b0pt95)
        allparticles_b0test.append(eventparticles_b0test)

#Calculate angles
    for i in range(tree.GetEntries()): #for every event,
        eventanglescharged_b0pt0 =[]
        eventanglescharged_b0pt5 =[]
        eventanglescharged_b0pt9 =[]
        eventanglescharged_b0pt95 =[]
        eventanglescharged_b0test =[]

        eventangles_b0pt0 =[]
        eventangles_b0pt5 =[]
        eventangles_b0pt9 =[]
        eventangles_b0pt95 =[]
        eventangles_b0test =[]

        if chargedbetaover0[i]==1:
            for j in range(len(allchargedparticles_b0pt0[i])): #for every charged particle w/ beta>xx in that event,
                for k in range(j+1,len(allchargedparticles_b0pt0[i])):
                    angle = allchargedparticles_b0pt0[i][j].Vect().Angle(allchargedparticles_b0pt0[i][k].Vect())
                    eventanglescharged_b0pt0.append(angle)

        if chargedbetaoverpt5[i]==1:
            for j in range(len(allchargedparticles_b0pt5[i])): 
                for k in range(j+1,len(allchargedparticles_b0pt5[i])):
                    angle = allchargedparticles_b0pt5[i][j].Vect().Angle(allchargedparticles_b0pt5[i][k].Vect())
                    eventanglescharged_b0pt5.append(angle)

        if chargedbetaoverpt9[i]==1:
            for j in range(len(allchargedparticles_b0pt9[i])): 
                for k in range(j+1,len(allchargedparticles_b0pt9[i])):
                    angle = allchargedparticles_b0pt9[i][j].Vect().Angle(allchargedparticles_b0pt9[i][k].Vect())
                    eventanglescharged_b0pt9.append(angle)

        if chargedbetaoverpt95[i]==1:
            for j in range(len(allchargedparticles_b0pt95[i])):
                for k in range(j+1,len(allchargedparticles_b0pt95[i])):
                    angle = allchargedparticles_b0pt95[i][j].Vect().Angle(allchargedparticles_b0pt95[i][k].Vect())
                    eventanglescharged_b0pt95.append(angle)

        if chargedbetaovertest[i]==1:
            for j in range(len(allchargedparticles_b0test[i])):
                for k in range(j+1,len(allchargedparticles_b0test[i])):
                    angle = allchargedparticles_b0test[i][j].Vect().Angle(allchargedparticles_b0test[i][k].Vect())
                    eventanglescharged_b0test.append(angle)

        if betaover0[i]==1:
            for j in range(len(allparticles_b0pt0[i])): #for all particles w/ beta>xx in that event,
                for k in range(j+1,len(allparticles_b0pt0[i])):
                    angle = allparticles_b0pt0[i][j].Vect().Angle(allparticles_b0pt0[i][k].Vect())
                    eventangles_b0pt0.append(angle)

        if betaoverpt5[i]==1:
            for j in range(len(allparticles_b0pt5[i])): 
                for k in range(j+1,len(allparticles_b0pt5[i])):
                    angle = allparticles_b0pt5[i][j].Vect().Angle(allparticles_b0pt5[i][k].Vect())
                    eventangles_b0pt5.append(angle)

        if betaoverpt9[i]==1:
            for j in range(len(allparticles_b0pt9[i])): 
                for k in range(j+1,len(allparticles_b0pt9[i])):
                    angle = allparticles_b0pt9[i][j].Vect().Angle(allparticles_b0pt9[i][k].Vect())
                    eventangles_b0pt9.append(angle)

        if betaoverpt95[i]==1:
            for j in range(len(allparticles_b0pt95[i])):
                for k in range(j+1,len(allparticles_b0pt95[i])):
                    angle = allparticles_b0pt95[i][j].Vect().Angle(allparticles_b0pt95[i][k].Vect())
                    eventangles_b0pt95.append(angle)

        if betaovertest[i]==1:
            for j in range(len(allparticles_b0test[i])):
                for k in range(j+1,len(allparticles_b0test[i])):
                    angle = allparticles_b0test[i][j].Vect().Angle(allparticles_b0test[i][k].Vect())
                    eventangles_b0test.append(angle)

        allanglescharged_b0pt0.append(eventanglescharged_b0pt0)
        allanglescharged_b0pt5.append(eventanglescharged_b0pt5)
        allanglescharged_b0pt9.append(eventanglescharged_b0pt9)
        allanglescharged_b0pt95.append(eventanglescharged_b0pt95)
        allanglescharged_b0test.append(eventanglescharged_b0test)

        eventanglescharged_b0pt0.sort(reverse = True)
        eventanglescharged_b0pt5.sort(reverse = True)
        eventanglescharged_b0pt9.sort(reverse = True)
        eventanglescharged_b0pt95.sort(reverse = True)
        eventanglescharged_b0test.sort(reverse = True)

        allangles_b0pt0.append( eventangles_b0pt0)
        allangles_b0pt5.append( eventangles_b0pt5)
        allangles_b0pt9.append( eventangles_b0pt9)
        allangles_b0pt95.append(eventangles_b0pt95)
        allangles_b0test.append(eventangles_b0test)

        eventangles_b0pt0.sort(reverse = True)
        eventangles_b0pt5.sort(reverse = True)
        eventangles_b0pt9.sort(reverse = True)
        eventangles_b0pt95.sort(reverse = True)
        eventangles_b0test.sort(reverse = True)
    
        if chargedbetaover0[i]==1:    
            chargedangleweight_b0pt0 =  pow( sin(eventanglescharged_b0pt0[0]/4) , 2)
            eventangleweightcharged_b0pt0.append(chargedangleweight_b0pt0)
            hist_chargedeventangleweight_b0pt0.Fill(chargedangleweight_b0pt0)
        if chargedbetaoverpt5[i]==1:  
            chargedangleweight_b0pt5 =  pow( sin(eventanglescharged_b0pt5[0]/4) , 2)
            eventangleweightcharged_b0pt5.append(chargedangleweight_b0pt5)
            hist_chargedeventangleweight_b0pt5.Fill(chargedangleweight_b0pt5)
        if chargedbetaoverpt9[i]==1:  
            chargedangleweight_b0pt9 =  pow( sin(eventanglescharged_b0pt9[0]/4) , 2)
            eventangleweightcharged_b0pt9.append(chargedangleweight_b0pt9)
            hist_chargedeventangleweight_b0pt9.Fill(chargedangleweight_b0pt9)
        if chargedbetaoverpt95[i]==1: 
            chargedangleweight_b0pt95 = pow( sin(eventanglescharged_b0pt95[0]/4) , 2)
            eventangleweightcharged_b0pt95.append(chargedangleweight_b0pt95)
            hist_chargedeventangleweight_b0pt95.Fill(chargedangleweight_b0pt95)
        if chargedbetaovertest[i]==1: 
            chargedangleweight_b0test = pow( sin(eventanglescharged_b0test[0]/4) , 2)
            eventangleweightcharged_b0test.append(chargedangleweight_b0test)
            hist_chargedeventangleweight_b0test.Fill(chargedangleweight_b0test)

        if betaover0[i]==1:    
            angleweight_b0pt0 =  pow( sin(eventangles_b0pt0[0]/4) , 2)
            eventangleweight_b0pt0.append(angleweight_b0pt0)
            hist_eventangleweight_b0pt0.Fill(angleweight_b0pt0)
        if betaoverpt5[i]==1:  
            angleweight_b0pt5 =  pow( sin(eventangles_b0pt5[0]/4) , 2)
            eventangleweight_b0pt5.append(angleweight_b0pt5)
            hist_eventangleweight_b0pt5.Fill(angleweight_b0pt5)
        if betaoverpt9[i]==1:  
            angleweight_b0pt9 =  pow( sin(eventangles_b0pt9[0]/4) , 2)
            eventangleweight_b0pt9.append(angleweight_b0pt9)
            hist_eventangleweight_b0pt9.Fill(angleweight_b0pt9)
        if betaoverpt95[i]==1: 
            angleweight_b0pt95 = pow( sin(eventangles_b0pt95[0]/4) , 2)
            eventangleweight_b0pt95.append(angleweight_b0pt95)
            hist_eventangleweight_b0pt95.Fill(angleweight_b0pt95)
        if betaovertest[i]==1: 
            angleweight_b0test = pow( sin(eventangles_b0test[0]/4) , 2)
            eventangleweight_b0test.append(angleweight_b0test)
            hist_eventangleweight_b0test.Fill(angleweight_b0test)

    # if len(eventangles_b0pt5)>0: hist_largestparticlepairangle_b0pt5.Fill(eventangles_b0pt5[0])
    # if len(eventangles_b0pt9)>0: hist_largestparticlepairangle_b0pt9.Fill(eventangles_b0pt9[0])

#Tetrahedral angle for three tracks
    for i in range(tree.GetEntries()): #for every event,
        eventtetrahedanglescharged_b0pt0 =[]
        eventtetrahedanglescharged_b0pt5 =[]
        eventtetrahedanglescharged_b0pt9 =[]
        eventtetrahedanglescharged_b0pt95 =[]
        eventtetrahedanglescharged_b0test =[]

        eventtetrahedangles_b0pt0 =[]
        eventtetrahedangles_b0pt5 =[]
        eventtetrahedangles_b0pt9 =[]
        eventtetrahedangles_b0pt95 =[]
        eventtetrahedangles_b0test =[]

        if threechargedbetaover0[i]==1:
            for j in range(len(allchargedparticles_b0pt0[i])): #for every charged particle w/ beta>xx in that event, #change upper limit to ...-2?
                for k in range(j+1,len(allchargedparticles_b0pt0[i])): #and ...-1?
                    for l in range(k+1,len(allchargedparticles_b0pt0[i])):
#                        print i, j, k, l,
                        a = allchargedparticles_b0pt0[i][j].Vect().Mag()
                        b = allchargedparticles_b0pt0[i][k].Vect().Mag()
                        c = allchargedparticles_b0pt0[i][l].Vect().Mag()
                        adotb = allchargedparticles_b0pt0[i][j].Vect().Dot(allchargedparticles_b0pt0[i][k].Vect())
                        bdotc = allchargedparticles_b0pt0[i][k].Vect().Dot(allchargedparticles_b0pt0[i][l].Vect())
                        cdota = allchargedparticles_b0pt0[i][l].Vect().Dot(allchargedparticles_b0pt0[i][j].Vect())
                        bcrossc = allchargedparticles_b0pt0[i][k].Vect().Cross(allchargedparticles_b0pt0[i][l].Vect())
                        adotbcrossc =  allchargedparticles_b0pt0[i][j].Vect().Dot(bcrossc)
#                        print a, b, c, adotb, bdotc, cdota, adotbcrossc,
                        denom = ((a*b*c) + (adotb*c) + (bdotc*a) + (cdota*b))
                        if denom != 0: Omega = abs( 2 * atan( (adotbcrossc) / (denom) ) )
                        #print Omega
                        eventtetrahedanglescharged_b0pt0.append(Omega)
        eventtetrahedanglescharged_b0pt0.sort(reverse = True)
        if threechargedbetaover0[i]==1: hist_tetrahedangle.Fill(eventtetrahedanglescharged_b0pt0[0])

#Fill histos
    cnt_0pt0=0
    cnt_0pt5=0    
    cnt_0pt9=0    
    cnt_0pt95=0    
    cnt_0test=0    
    cnt_charged0pt0=0
    cnt_charged0pt5=0
    cnt_charged0pt9=0
    cnt_charged0pt95=0
    cnt_charged0test=0

    for i in range(tree.GetEntries()): #for each event
        tree.GetEntry(i)
        fluxwt=weights[i]

        hist_unweighednuE.Fill(tree.Ev)
        hist_xsecweighednuE.Fill(tree.Ev,sigmafac)
        hist_xsecfluxweighednuE.Fill(tree.Ev,sigmafac*fluxwt)
        hist_xsecfluxfacweighednuE.Fill(tree.Ev,sigmafac*fluxwt*consttfac)

        if chargedbetaover0[i]==1: #if two tracks 
            hist_angleweighedtwotracks.Fill(tree.Ev,sigmafac*fluxwt*consttfac*eventangleweightcharged_b0pt0[cnt_charged0pt0])
            hist_angleweighednumtracks.Fill(len(allchargedparticles_b0pt0[i]),sigmafac*fluxwt*consttfac*eventangleweightcharged_b0pt0[cnt_charged0pt0])
            for j in range(len(allchargedparticles_b0pt0[i])): #for every charged particle in that event,
                hist_angleweighedbetaofalltracks.Fill(float(allchargedparticles_b0pt0[i][j].Pt())/float(allchargedparticles_b0pt0[i][j].E()),sigmafac*fluxwt*consttfac*eventangleweightcharged_b0pt0[cnt_charged0pt0])
            cnt_charged0pt0+=1
        if chargedbetaoverpt5[i]==1: #if two tracks w beta over pt5        
            hist_twotracksbetapt5.Fill( tree.Ev,sigmafac*fluxwt*consttfac)
            hist_angleweighedtwotracksbetapt5.Fill( tree.Ev,sigmafac*fluxwt*consttfac*eventangleweightcharged_b0pt5[cnt_charged0pt5])
            cnt_charged0pt5+=1
        if chargedbetaoverpt9[i]==1:         
            hist_twotracksbetapt9.Fill( tree.Ev,sigmafac*fluxwt*consttfac)
            hist_angleweighedtwotracksbetapt9.Fill( tree.Ev,sigmafac*fluxwt*consttfac*eventangleweightcharged_b0pt9[cnt_charged0pt9])
            cnt_charged0pt9+=1
        if chargedbetaoverpt95[i]==1:        
            hist_twotracksbetapt95.Fill(tree.Ev,sigmafac*fluxwt*consttfac)
            hist_angleweighedtwotracksbetapt95.Fill( tree.Ev,sigmafac*fluxwt*consttfac*eventangleweightcharged_b0pt95[cnt_charged0pt95])
            cnt_charged0pt95+=1
        if chargedbetaovertest[i]==1:        
            hist_twotracksbetatest.Fill(tree.Ev,sigmafac*fluxwt*consttfac)
            hist_angleweighedtwotracksbetatest.Fill( tree.Ev,sigmafac*fluxwt*consttfac*eventangleweightcharged_b0test[cnt_charged0test])
            cnt_charged0test+=1

        if threechargedbetaoverpt5[i]==1:  hist_threetracksbetapt5.Fill( tree.Ev,sigmafac*fluxwt*consttfac)
        if threechargedbetaoverpt9[i]==1:  hist_threetracksbetapt9.Fill( tree.Ev,sigmafac*fluxwt*consttfac)
        if threechargedbetaoverpt95[i]==1: hist_threetracksbetapt95.Fill(tree.Ev,sigmafac*fluxwt*consttfac)
        if threechargedbetaovertest[i]==1: hist_threetracksbetatest.Fill(tree.Ev,sigmafac*fluxwt*consttfac)

        if betaover0[i]==1:
            hist_angleweighedtwoparticles.Fill(tree.Ev,sigmafac*fluxwt*consttfac*eventangleweight_b0pt0[cnt_0pt0])
            hist_angleweighednumparticles.Fill(len(allparticles_b0pt0[i]),sigmafac*fluxwt*consttfac*eventangleweight_b0pt0[cnt_0pt0])
            for j in range(len(allparticles_b0pt0[i])): 
                hist_angleweighedbetaofallparticles.Fill(float(allparticles_b0pt0[i][j].Pt())/float(allparticles_b0pt0[i][j].E()),sigmafac*fluxwt*consttfac*eventangleweight_b0pt0[cnt_0pt0])
            cnt_0pt0+=1
        if betaoverpt5[i]==1:             
            hist_twoparticlesbetapt5.Fill( tree.Ev,sigmafac*fluxwt*consttfac)
            hist_angleweighedtwoparticlesbetapt5.Fill(tree.Ev,sigmafac*fluxwt*consttfac*eventangleweight_b0pt5[cnt_0pt5])
            cnt_0pt5+=1
        if betaoverpt9[i]==1:             
            hist_twoparticlesbetapt9.Fill( tree.Ev,sigmafac*fluxwt*consttfac)
            hist_angleweighedtwoparticlesbetapt9.Fill(tree.Ev,sigmafac*fluxwt*consttfac*eventangleweight_b0pt9[cnt_0pt9])
            cnt_0pt9+=1
        if betaoverpt95[i]==1:            
            hist_twoparticlesbetapt95.Fill(tree.Ev,sigmafac*fluxwt*consttfac)
            hist_angleweighedtwoparticlesbetapt95.Fill(tree.Ev,sigmafac*fluxwt*consttfac*eventangleweight_b0pt95[cnt_0pt95])
            cnt_0pt95+=1
        if betaovertest[i]==1:            
            hist_twoparticlesbetatest.Fill(tree.Ev,sigmafac*fluxwt*consttfac)
            hist_angleweighedtwoparticlesbetatest.Fill(tree.Ev,sigmafac*fluxwt*consttfac*eventangleweight_b0test[cnt_0test])
            cnt_0test+=1

        if threebetaoverpt5[i]==1:      hist_threeparticlesbetapt5.Fill( tree.Ev,sigmafac*fluxwt*consttfac)
        if threebetaoverpt9[i]==1:      hist_threeparticlesbetapt9.Fill( tree.Ev,sigmafac*fluxwt*consttfac)
        if threebetaoverpt95[i]==1:     hist_threeparticlesbetapt95.Fill(tree.Ev,sigmafac*fluxwt*consttfac)
        if threebetaovertest[i]==1:     hist_threeparticlesbetatest.Fill(tree.Ev,sigmafac*fluxwt*consttfac)

print "\n\nTot #events: ", hist_xsecfluxfacweighednuE.Integral(2,400) #skip first bin, assumes 400 bins

print "\nTot #events, two tracks over beta 0.5: ",  hist_twotracksbetapt5.Integral()
print "Tot #events, two tracks over beta 0.9: ",  hist_twotracksbetapt9.Integral()
print "Tot #events, two tracks over beta 0.95: ", hist_twotracksbetapt95.Integral()
print "Tot #events, two tracks over beta testbeta: ", hist_twotracksbetatest.Integral()
#print "Tot #events, two particles over beta 0.5: ",  hist_twoparticlesbetapt5.Integral()
#print "Tot #events, two particles over beta 0.9: ",  hist_twoparticlesbetapt9.Integral()
#print "Tot #events, two particles over beta 0.95: ", hist_twoparticlesbetapt95.Integral()
#print "Tot #events, two particles over beta testbeta: ", hist_twoparticlesbetatest.Integral()

print "\nTot #events, weighed by max opening angle, two tracks over beta 0.5: ",     hist_angleweighedtwotracksbetapt5.Integral()
print "Tot #events, weighed by max opening angle, two tracks over beta 0.9: ",     hist_angleweighedtwotracksbetapt9.Integral()
print "Tot #events, weighed by max opening angle, two tracks over beta 0.95: ",    hist_angleweighedtwotracksbetapt95.Integral()
print "Tot #events, weighed by max opening angle, two tracks over beta testbeta: ",    hist_angleweighedtwotracksbetatest.Integral()
#print "Tot #events, weighed by max opening angle, two particles over beta 0.5: ",  hist_angleweighedtwoparticlesbetapt5.Integral()
#print "Tot #events, weighed by max opening angle, two particles over beta 0.9: ",  hist_angleweighedtwoparticlesbetapt9.Integral()
#print "Tot #events, weighed by max opening angle, two particles over beta 0.95: ", hist_angleweighedtwoparticlesbetapt95.Integral()
#print "Tot #events, weighed by max opening angle, two particles over beta testbeta: ", hist_angleweighedtwoparticlesbetatest.Integral()

print "\nTot #events, weighed by max opening angle, two tracks: ",                   hist_angleweighedtwotracks.Integral()
#print "Tot #events, weighed by max opening angle, two particles: ",                hist_angleweighedtwoparticles.Integral()

print "\nTot #events, three tracks over beta 0.5: ",  hist_threetracksbetapt5.Integral()
print "Tot #events, three tracks over beta 0.9: ",  hist_threetracksbetapt9.Integral()
print "Tot #events, three tracks over beta 0.95: ", hist_threetracksbetapt95.Integral()
print "Tot #events, three tracks over beta testbeta: ", hist_threetracksbetatest.Integral()
#print "Tot #events, three particles over beta 0.5: ",  hist_threeparticlesbetapt5.Integral()
#print "Tot #events, three particles over beta 0.9: ",  hist_threeparticlesbetapt9.Integral()
#print "Tot #events, three particles over beta 0.95: ", hist_threeparticlesbetapt95.Integral()
#print "Tot #events, three particles over beta testbeta: ", hist_threeparticlesbetatest.Integral()

#Write to output root file
out_file.cd()
out_file.Write()
out_file.Close()
