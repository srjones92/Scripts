import os
import glob
import numpy as np
import matplotlib.pyplot as plt
import gpxpy
import fitdecode

from argparse import ArgumentParser

activitiesPath = '/home/scott/Strava_Data/export_800377/activities/*'

class Ride():
    def __init__(self,fname):
        self.fname = fname

class RideGPX(Ride):
    def __init__(self,fname):
        pass

class RideFIT(Ride):
    def __init__(self,fname):
        pass


def buildRideList(flist):
    rideList = []
    for f in flist:
        ride = buildRide(f)
        if ride is not None:
            rideList.append(ride)
    return rideList

def buildRide(fname):
    ext = os.path.splitext(fname)[1]
    if ext == '.fit':
        return RideFIT(fname)
    elif ext == '.gpx':
        return RideGPX(fname)
    elif ext == '.tcx':
        # Not implemented yet
        return None
    else:
        raise ValueError('Invalid file extension: {}'.format(ext))



if __name__=="__main__":
    activities = glob.glob(activitiesPath)
    rideList = buildRideList(activities)

    breakpoint()
