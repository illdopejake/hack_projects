import os,sys
import numpy as np
import nibabel as ni
from copy import deepcopy
sys.path.insert(0,'/Users/jakevogel/git/tPSO_scripts')
from propagation_correlations import codegen,pthswp


def import_atlas(wdir,atlas,mask=False):
    mtx = ni.load(atlas).get_data()
    cde = codegen(6)

    if mask:
        binar = False
        msk = ni.load(mask).get_data()
        x,y,z = msk.shape
        for i in range(y):
            if any(msk[:][i][i]) > 0:
                for j in msk[:][i][i]:
                    if j != 0 and j != 1:
                        binar = True
        if binar == True:
            oldpth = pthswp(wdir)
            os.system('fslmaths %s -bin %s_binmsk'%(mask,cde))
            msk = ni.load('%s_binmsk.nii.gz'%(cde)).get_data()
            mtx = np.ma.masked_array(mtx,msk.astype(bool)) 

    return mtx


#def ID_noncontiguous_rois(mtx)

#    for lab in range(1,(np.ptp(mtx)+1)):
#        

def master_search(atl,lab,coord,clist,setting):
    a = lab
    x,y,z = coord
    while a == lab:
        if setting == 0:
            x = x+1
            y = y+1
        elif setting == 1:
            x = x+1
            y = y-1
        elif setting == 2:
            x = x-1
            y = y+1
        elif setting == 3:
            x = x-1
            y = y-1
        elif setting == 4:
            y = y+1
            z = z+1
        elif setting == 5:
            y = y+1
            z = z-1
        elif setting == 6:
            y = y-1
            z = z+1
        elif setting == 7:
            y = y-1
            z = z-1
        a = atl[x][y][z]
        if a == lab:
            if (x,y,z) not in clist:
                clist.append((x,y,z))
        ln = len(deepcopy(clist)) + 1
        while len(clist) != ln:
            nclist = search_around_voxel(atl,lab,(x,y,z))
            for c in nclist:
                if c not in clist:
                    clist.append(c)
            ln = len(clist)

    return clist

def search_around_voxel(atl,lab,coord):
    a = lab
    x,y,z = coord
    clist = []
    while a == lab:
        x = x+1
        a = atl[x][y][z]
        if a==lab and (x,y,z) not in clist:
            clist.append((x,y,z))
    a = lab
    x,y,z = coord
    while a == lab:
        x = x-1
        a = atl[x][y][z]
        if a==lab and (x,y,z) not in clist:
            clist.append((x,y,z,))
    a = lab
    x,y,z = coord
    while a == lab:
        y = y+1
        a = atl[x][y][z]
        if a==lab and (x,y,z) not in clist:
            clist.append((x,y,z))
    a = lab
    x,y,z = coord
    while a == lab:
        y = y-1
        a = atl[x][y][z]
        if a==lab and (x,y,z) not in clist:
            clist.append((x,y,z))
    a = lab
    x,y,z = coord
    while a == lab:
        z = z+1
        a = atl[x][y][z]
        if a==lab and (x,y,z) not in clist:
            clist.append((x,y,z))
    a = lab
    x,y,z == coord
    while a == lab:
        z = z-1
        a = atl[x][y][z]
        if a==lab and (x,y,z) not in clist:
            clist.append((x,y,z))

    return clist

#def compute_center_of_mass

#def compute_distance
