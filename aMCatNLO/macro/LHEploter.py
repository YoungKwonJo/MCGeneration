#!/usr/bin/env python

from ROOT import *
import sys

gROOT.Reset()
gSystem.Load("/afs/cern.ch/work/y/youngjo/slc6/Delphes/Delphes-3.1.2/libDelphes.so");

ROOT.gROOT.SetBatch(True)

fid = 0
fname = ["test","100000"]
cxlist= [  0.3972, 15.84]

cut1 =  False # True #
cut2 =  False # True #
cut3 =  False # True #
cut4 =  False # True #
cut5 =  True # True #

ilist =[]
ilistn=[]
nameid=''

ccc = []
for i in range(32):
  bbb=i
  aaa=bin(i+32)[3:]
  ilistn.append(aaa)
  ccc = []
  for j in range(5):
    ccc.append(int(aaa[j]))
  ilist.append(ccc)

#print ilistn

def str2bool(str):
  return str.lower() in ("yes", "true", "t", "1")

for i,arg in  enumerate(sys.argv):
 if(i==1):
   cut1=ilist[int(arg)][0]
   cut2=ilist[int(arg)][1]
   cut3=ilist[int(arg)][2]
   cut4=ilist[int(arg)][3]
   cut5=ilist[int(arg)][4]
   nameid=ilistn[int(arg)] 
#   fid =ilist[int(arg)][5]

cut1_s = ["iM6",""]
cut2_s = ["pt40eta25",""]
cut3_s = ["iD6",""]
cut4_s = ["iD5",""]
cut5_s = ["DR05",""]

cut1_s1 = ["ID of mother!=6",""]
cut2_s1 = ["p_T>40, |#eta|<2.5",""]
cut3_s1 = ["ID of daugther!=6",""]
cut4_s1 = ["ID of daugther!=5",""]
cut5_s1 = ["#DeltaR>0.5",""]

def fromTop(gen,ii):
  check=False
  checkg=False
  iii=ii
  while iii>2 and check !=True :
    if (abs(gen[gen[iii].M1].PID)==21):
      checkg=True
      iii=gen[iii].M1
    elif (abs(gen[gen[iii].M2].PID)==21):
      checkg=True
      iii=gen[iii].M2
    elif (abs(gen[gen[iii].M1].PID)==6 and checkg==False):
      check=True
      iii=gen[iii].M1
    elif (abs(gen[gen[iii].M2].PID)==6 and checkg==False):
      check=True
      iii=gen[iii].M2
    else :
      iii=gen[iii].M1
  return check

def isLastBottom(gen,ii):
  check=False
  if (abs(gen[gen[ii].D1].PID) !=5 and abs(gen[gen[ii].D2].PID) !=5):
    check=True
  return check

def isLastCharm(gen,ii):
  check=False
  if (abs(gen[gen[ii].D1].PID) !=4 and abs(gen[gen[ii].D2].PID) !=4):
    check=True
  return check

def decay2Top(gen,ii):
  check=False
  if (abs(gen[gen[ii].D1].PID) ==6 or abs(gen[gen[ii].D2].PID) ==6):
    check=True
  return check

def cutPt20Eta2p5(gen,ii):
  check=False
  if (gen[ii].PT>20 and abs(gen[ii].Eta)<2.5):
    check=True
  return check

def cutPt40Eta2p5(gen,ii):
  check=False
  if (gen[ii].PT>40 and abs(gen[ii].Eta)<2.5):
    check=True
  return check

def cutDR05(l,l2):
  check=False
  if (abs(l.DeltaR(l2))>0.5):
    check=True
  return check

def isTTBB(particles):
  mm=0
  gen = []
  for i,p in enumerate(particles):
    gen.append(p)
  l = TLorentzVector()
  l2 = TLorentzVector()
  for i in range(len(gen)):
    if ( abs(gen[i].PID) == 5 and ( cut1 or (fromTop(gen,i)==False)) and ( cut2 or cutPt40Eta2p5(gen,i)==True)):
      if ( (cut3 or (decay2Top(gen,i)==False)) and ( cut4 or (isLastBottom(gen,i)==True)) ):
        if (mm==0):
          l.SetPtEtaPhiM(gen[i].PT,gen[i].Eta,gen[i].Phi,gen[i].Mass)
        if (mm==1):
          l2.SetPtEtaPhiM(gen[i].PT,gen[i].Eta,gen[i].Phi,gen[i].Mass)
#      print ("i:", i, ", pid:", gen[i].PID,", m1:", gen[i].M1,", pt:", gen[i].PT )
        mm+=1
  if(mm>1):
    DR= abs(l.DeltaR(l2))
    if ( cut5 or cutDR05(l,l2)==True ):
      #DR = abs(l.DeltaR(l2))
      return [1, DR]
    else:
      return [0, DR]
  else:
    return [0, -1]


def getWeight(Rwgt):
  weight=1
  for wei in Rwgt:
    weight=weight*wei.Weight
  return weight

def readTree(t, name):
  fname = 'result_'+nameid+'.root'
  print fname
  f = TFile( fname, 'recreate' )
  tN = TTree( 't1', 'tree with histos' )

  gROOT.ProcessLine(
  "struct MyStruct {\
   Int_t      ttbb_;\
   Double_t    DRbb_;\
   Double_t    weight_;\
   };" );
  from ROOT import MyStruct

  s = MyStruct()
  tN.Branch('ttbb',AddressOf(s,'ttbb_'),'ttbb_/I')
  tN.Branch('DRbb',AddressOf(s,'DRbb_'),'DRbb_/D')
  tN.Branch('weight',AddressOf(s,'weight_'),'weight_/D')

  l = TLorentzVector() 
  l2 = TLorentzVector() 
  l3 = TLorentzVector()

  # Event loop
  nev = t.GetEntries()
  for n in t:
    particles = n.Particle
#    weights = n.Rwgt
    event = n.Event

    output = isTTBB(particles)
    s.ttbb_=output[0]
    s.DRbb_=output[1]
    s.weight_= cxlist[fid]/nev
    tN.Fill()

  f.Write()
  f.Close()

#### Run read function
if __name__ == '__main__':
  ffname = ["cut","nocut"]
  name = ffname[fid]+"_"+cut1_s[cut1]+cut2_s[cut2]+cut3_s[cut3]+cut4_s[cut4]+cut5_s[cut5]
  print "starting about ", name

#  f = TFile('events_100000.root')
  fN = ("events_%s.root" % fname[fid])
  print "open ", fN
  f = TFile(fN)
  t = f.Get("Delphes")
#  t.Print()

  readTree(t,name)#h22,h33,h11)

