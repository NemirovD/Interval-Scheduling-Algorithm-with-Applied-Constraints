from course import *
from userpreferences import UserPrefs
import amberWeighting
import dinoWeighting
import math
from userpreferences import UserPrefs

def addWeights(Schedule):
   weight = 0.0
   for CRN in Schedule:
      weight += CRN.weight
   return weight


def optimumTimeOfDay(Schedule):
   """KYLE:  Weights each course highly based on a Gaussian curve centered aroung
             a time in the desired block."""
   opt = { "Morning":"0900","Afternoon":"1400","Evening":"1900" }
   optimum_time = float(opt[UserPrefs.PreferTimeOfDay])
   counter = 0.
   score = 0.
   for CRN in Schedule:
      for ts in CRN.timeslots:
         counter += (int(ts.eTime) - int(ts.sTime))
         score += (int(ts.eTime) - int(ts.sTime)) * (2.0 * math.exp( -1.3e-5 * ( (float(ts.sTime)+float(ts.eTime))/2.0 - optimum_time)**2 ) - 1.0)
   return score/counter

def campusPref(Schedule):
   """DINO"""
   for CRN in Schedule:
      if UserPrefs.preferredCampus == "North" and CRN.campus == "North":
         CRN.weight += 900
      if UserPrefs.preferredCampus == "Downtown" and CRN.campus == "Downtown":
         CRN.weight += 900
      if UserPrefs.preferredCampus == "Other" and CRN.campus == "Other":
         CRN.weight += 900


def preferred_crn(Schedule):
    """DINO"""
    for CRN in Schedule:
        if CRN.CRN in UserPrefs.preferredCRNs:
            CRN.weight+=1.e6


def course_density(Schedule):
   """DINO"""
   weight = 0.
   counter = 0.
   for iCRN in Schedule:
      if not(iCRN.CRN=="55555"):
         for jCRN in Schedule:
            for i in iCRN.timeslots:
               for j in jCRN.timeslots:
                  if i.day==j.day:
                     time = int(j.eTime) - int(i.sTime)
                     if time<=40:
                        weight +=1.
                        counter+=1.
   return weight/counter




def compute_schedule_score(Schedule):
   score = 0.0

   score += optimumTimeOfDay(Schedule)
   score += addWeights(Schedule)
#   score += myScore(Schedule)

   if not(UserPrefs.preferredCampus=="None"):
      score += campusPref(Schedule)

   if UserPrefs.preferMinGaps == True:
      score +=course_density(Schedule)
   return score




