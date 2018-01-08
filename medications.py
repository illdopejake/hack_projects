import pandas
import sys
sys.path.insert(0,'/Users/jakevogel/git/pycourse_VUMC')
from pycourse_lesson3_4_scripts import simplify


# set med col
allmeds = ''

# also import med dictionary

def mstrip(med):
    
    if '(' in med:
        lp = med.index('(')
        med = med[:lp]
    for l in med:
        if l.isnumeric():
            med = med.replace(l,'')
    meas = ['mg', ' g ', 'mcg', ' L ', 'mL', 'a day', 'daily', ' x ']
    for x in meas:
        med = med.replace(x,'')
    med = med.strip()

    med = med.lower()

    return med

def redundancy removal(allmeds,inwords=None)
# Perform initial steps to remove redundancy

    starting_len = len(allmeds)
    # fix-up individual medicine entries
    newmed = list(map(mstrip, allmeds)) 

    # get rid of very small entries
    newmed = [x for x in newmed if len(x) > 2] 

    # separate stuck-together entries
    for med in lessmed:
        for sep in seps:
            if sep in med:
                print('removing %s from %s'%(sep,med))
                items = med.split(sep)
                for item in items:
                    lessmed.append(item)
                try:
                    lessmed.remove(med)
                except:
                    continue
                continue


    # do some intelligent redundancy removal
    reduction = True
    while reduction:
        curr_len = len(newmed)
        newmed, suggs = simplify(pandas.Series(newmed),mode='apply',inwords=inwords,integrate = True)
        new_len = len(newmed)
        if (curr_len - new_len) == 0:
            reduction = False

    # Function that takes suggs and takes user input to deal with the ties. Should check
    # if ties are going toward same value in dict. If so, skip user input and automatically
    # assign an input
    
    newmed, suggs = simplify(newmed,mode='apply',inwords=inwords,integrate = True)
    newmed = newmed.unique()

    print ('started with %s medications, now there are only %s'%(starting_len, len(newmed)))

    return newmed

# Go back to actual column input and integrate into a medication spreadsheet based on dict
def populate_spreadsheet(med_subdf,medf)
    #med_subdf should have subject as index...
    # in its current state this won't work
typedf = pandas.DataFrame(np.zeros((len(sdf.index),len(medf.Type.unique()))),index=sdf.index,columns = medf.Type.unique())
stdf = pandas.DataFrame(np.zeros((len(sdf.index),len(medf.Spec_type.unique()))),index=sdf.index,columns = medf.Spec_type.unique())
usedf = pandas.DataFrame(np.zeros((len(sdf.index),len(medf.Use.unique()))),index=sdf.index,columns = medf.Use.unique())
for sub in newdf.index:
    row = newdf.ix[sub,'medications']
    for entry in row.split(','):
        entry = mstrip(entry)
        suggs = difflib.get_close_matches(entry,med_lib,cutoff=0.7)
        if len(suggs) == 1:
            choice = suggs[0]
        if len(suggs) > 1:
            cnt = 0
            for i in range(len(suggs)-1):
                if all(medf.loc[suggs[i+1]][1:4] == medf.loc[suggs[0]][1:4]):
                    cnt += 1
            if cnt == len(suggs)-1:
                choice = suggs[0]
            else:
                print('Whoops.. im not sure.')
                print('my best guess for %s is %s'%(entry,suggs[0]))
                notok = input('if this is correct, press enter. For other options, type no and press enter:')
                if notok:
                    print('Okay, here are all my guesses \n',suggs)
                    usr = input('Please enter the position (0 to %s) of the best answer:'%(len(suggs)-1))
                    choice = suggs[int(usr)]
                    print('chose %s'%(choice))
            t = medf.ix[choice,'Type']                                                                                     
            s = medf.ix[choice,'Spec_type']                                 
            u = medf.ix[choice,'Use']
            typedf.ix[sub,t] = typedf.ix[sub,t] + 1
            stdf.ix[sub,s] = stdf.ix[sub,s] + 1
            usedf.ix[sub,u] = usedf.ix[sub,u] + 1

            # for next lines, need to add part that finds and get rid of nans
            ncol = ['use_'+x for x in usedf.columns]
            usedf.columns = ncol
            ncol = ['type_'+x for x in typedf.columns]
            typedf.columns = ncol
            ncol = ['spectype_'+x for x in stdf.columns]
            stdf.columns = ncol
            
