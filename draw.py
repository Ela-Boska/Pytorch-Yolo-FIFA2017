import matplotlib.pyplot as plt 

def read_fscores(file):
    File = open(file,'r')
    lines = File.readlines()
    fscores = []
    for line in lines:
        fscore = float(line.split()[-1])
        fscores.append(fscore)
    return fscores

def read_precisions(file):
    File = open(file,'r')
    lines = File.readlines()
    fscores = []
    for line in lines:
        fscore = float(line.split()[4])
        fscores.append(fscore)
    return fscores

def read_recalls(file):
    File = open(file,'r')
    lines = File.readlines()
    fscores = []
    for line in lines:
        fscore = float(line.split()[7])
        fscores.append(fscore)
    return fscores

def read_all(file):
    return (read_precisions(file),read_recalls(file),read_fscores(file))