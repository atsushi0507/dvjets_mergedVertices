import glob
import os, math
from glob import glob

directory = "/Volumes/LaCie/DVJets/data/skimmedFiles/skimmedFiles/"
fileSuffix = "output_"

outputDir = "inputList/"
if (not os.path.isdir(outputDir)):
    os.makedirs(outputDir)

nSplit = 1

files = sorted(glob(directory+"*.root"))
n = int(math.ceil(len(files) / nSplit))
fileList = [files[idx: idx + n] for idx in range(0, len(files), n)]
baseName = "inputList/inputList_dr"
for i in range(len(fileList)):
    fileName = baseName + "_{:0>2}.txt".format(i+1)
    with open(fileName, "w") as f:
        for j in range(len(fileList[i])):
            f.write(fileList[i][j] + "\n")
