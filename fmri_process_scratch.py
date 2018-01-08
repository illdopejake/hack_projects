import os
from glob import glob
import nibabel as ni
import numpy as np
import pandas
import itertools
from copy import deepcopy

sids = [x.split('/')[-1].split('_')[1] for x in fmri.keys()]
final_mtx = pandas.DataFrame(index = sids, columns = range(444))

dat = ni.load(tst).get_data() #takes awhile
sub_mat = pandas.DataFrame(index = range(444),columns = range(dat.shape[0]))
tot = np.bincount(atl.astype(int).flat)
for frm in range(dat.shape[0]):
     mtx = dat[frm,:,:,:]
     sums = np.bincount(atl.astype(int).flat,weights=mtx.flat)
     rois = (sums/tot)[1:]
     sub_mat[sub_mat.columns[frm]] = rois
cmtx = np.corrcoef(sub_mat)
cmtx = np.arctanh(cmtx)
features = cmtx[[x[0] for x in itertools.combinations(range(444),2)],
                       [y[1] for y in itertools.combinations(range(444),2)]]
binval = sorted(features)[int(len(features) * .95)]
cmtx[cmtx<binval] = 0
cmtx[cmtx>0] = 1
lds = [cmtx[:,x].sum() for x in range(cmtx.shape[-1])]





 def extract_cmat(dat, atl):
    sub_mat = pandas.DataFrame(index = range(443),columns = range(dat.shape[0]))
    tot = np.bincount(atl.astype(int).flat)
    for frm in range(dat.shape[0]):
        mtx = dat[frm,:,:,:]
        sums = np.bincount(atl.astype(int).flat,weights=mtx.flat)
        rois = (sums/tot)[1:-1]
        sub_mat[sub_mat.columns[frm]] = rois
    cmtx = np.corrcoef(sub_mat)
    cmtx = np.arctanh(cmtx)
    
    return cmtx


for sub,scnz in scans.items():
    dat1 = ni.load(scnz[0]).get_data()
    dat2 = ni.load(scnz[1]).get_data()
    cmtx1 = extract_cmat(dat1,atl)
    cmtx2 = extract_cmat(dat2,atl)
    cmtx = (cmtx1 + cmtx2) / 2
    features = cmtx[[x[0] for x in itertools.combinations(range(443),2)],
                       [y[1] for y in itertools.combinations(range(443),2)]]
    for d in densities:
        nmtx = deepcopy(cmtx)
        thr = (100 - d) * .01
        binval = sorted(features)[int(len(features) * thr)]
        nmtx[nmtx<binval] = 0
        nmtx[nmtx>0] = 1
        lds = [nmtx[:,x].sum() for x in range(nmtx.shape[-1])]
        outputs[d].loc[sub] = lds
        outputs[d].to_csv('/sf1/project/yai-974-aa/users/jvogel44/link_density443_%s'%d)
    print('finished',sub)