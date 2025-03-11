from Utils.const import REGIONS_DATA

def getJudeteRepo()->list:

    judete = list(REGIONS_DATA.keys())


    return judete

def getOraseRepo(oras)->list:

    orase = list(REGIONS_DATA[oras])

    return orase

