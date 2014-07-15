#!/usr/bin/env python

from ROOT import *
import sys

gROOT.Reset()
gSystem.Load("/afs/cern.ch/work/y/youngjo/slc6/Delphes/Delphes-3.1.2/libDelphes.so");

#ROOT.gROOT.SetBatch(True)

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

def CX(i):
  nameid = ilistn[i]
  fname = 'result_'+nameid+'.root'
#  print fname
  f = TFile(fname)
  t1 = f.Get("t1")
#  t1.Draw("ttbb","weight","", -1, 0)
  h1 = TH1F("h1","h1",2,0,2)
  t1.Project("h1","ttbb","weight")
  print nameid+(" : %.2f"% (h1.GetBinContent(2)*1000))+" fb"
#  t1.Print()

#### Run read function
if __name__ == '__main__':
  cutlist = ["not from top", "p_T>40, |eta|<2.5","", "not decay to top","", "not decay to bottom","", "DRbb>0.5",""]
  print cutlist

  for i in range(32): 
    CX(i)

