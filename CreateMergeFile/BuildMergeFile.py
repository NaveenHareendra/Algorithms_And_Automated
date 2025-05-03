import os
from pathlib import Path, PurePath
import random



class FileBuildMerger:

    path=Path()
    # pathListMerge = []
    invalidFileNames =[]
    validFiles =[]
    invalidFiles =[]
    heapSize=0
    pos=0
    pathName=""

    def __init__(self): 
        print('\n---------------------------- File Merger ------------------------------------------\n')
        print('\nInsert the file path under format ex:- D:\\DBA UPGRADE\\CI CD\\Final2 \n')

        while True:
            print("\n\nProvide the folder path(n to terminate): ")
            self.pathName=os.path.normpath(input()) 
            if(self.pathName =='n' or self.pathName =='N'):
                return;
            self.BuildMergeFile(self.pathName)
            # p = Path("D:\\Work\\Projects\\Releases\\EIM\\V9\\9.8 RC\\Oct 23, 2024\\04_ALTERSCRIPT_[EIMV9(RC98)]_Version_9.7258.0_to_Version_9.7259.0_SQL.txt")
            # p.rename("D:\\Work\\Projects\\Releases\\EIM\\V9\\9.8 RC\\Oct 23, 2024\\04_ALTERSCRIPT_[EIMV9(RC98)]_Version_9.7258.0_to_Version_9.7259.0_SQL -2.txt")
            self.pathName="";
            self.classValInit()
    
    def classValInit(self):
        self.path=Path()
        # self.pathListMerge = []
        self.invalidFileNames =[]
        self.validFiles =[]
        self.invalidFiles =[]
        self.heapSize=0
        self.pos=0

    def Exchange(self,  i=0, largest=0):
        temp = self.validFiles[self.pos][1][i]
        self.validFiles[self.pos][1][i] = self.validFiles[self.pos][1][largest]
        self.validFiles[self.pos][1][largest] = temp

        #Extra step to exchange filenames as well
        temp = self.validFiles[self.pos][2][i]
        self.validFiles[self.pos][2][i] = self.validFiles[self.pos][2][largest]
        self.validFiles[self.pos][2][largest] = temp

    def Quicksort(self, p, r):
        q=0
        if(p<r):
            q=self.RandomizedPartition(  p, r)
            self.Quicksort(  p, q-1)
            self.Quicksort(  q+1, r)

    def RandomizedPartition(self, p, r):
        i = random.randint(p,r)
        self.Exchange(r, i) 
        return self.Partition( p, r)
    
    def Partition(self, p, r):
        x = int(self.validFiles[self.pos][1][r])
        i = (p-1)
        beforePivot = r
        for j in range(p,beforePivot):
            if(int(self.validFiles[self.pos][1][j])<=x):
                i+=1
                self.Exchange(i, j)
        self.Exchange(i+1, r)
        return i+1
    
    def RenameFileName(self,FilePath):
        #renameFileName Code
        tempFilePath = Path(FilePath)
        fileName = PurePath(tempFilePath).name
        # print(fileName)
        directoryPath= PurePath(tempFilePath).parents[0]
        newFilePath = os.path.join(directoryPath, fileName[1:len(fileName)])
        print("new path: ", newFilePath)
        tempFilePath.rename(newFilePath)
        return newFilePath;
        #print("Directory: "+winPath)
        #print(PurePath(tempFilePath).name)
        #fileName = PurePath(tempFilePath).name
        #print("Directory: "+PurePath(tempFilePath).parent[0])
        # newFilePath =directoryPath+"\\"+fileName[1:len(fileName)]
        # tempFilePath.rename(directoryPath+"\\"+fileName[1:len(fileName)])

    #Validates if file name is with the sequence 2_ , 1_ etc.
    def CheckFileName(self, pos, root, files=[]):
        i=0
        charCheck = ""
        invalidFlag = 0
        for fileName in files:
            for index in range(len(fileName)):
                if((fileName[index] != "_")&((ord(fileName[index]) < 48 )| (ord(fileName[index]) >57))):
                    invalidFlag = -1 
                    break
                if((fileName[index] == "_")  ):
                    break
                else:
                    charCheck += fileName[index]
            
            try:

                if((charCheck[0]=="0")& (len(charCheck)-1>0) & (invalidFlag!=-1)):
                    if(i==0):
                        self.validFiles.append( [[root],[0],[0]])
                        self.validFiles[pos][1][0]=charCheck[1:len(charCheck)]
                        self.validFiles[pos][2][0]=fileName[0:len(fileName)]                
                    else:
                        self.validFiles[pos][1].append(charCheck[1:len(charCheck)])
                        self.validFiles[pos][2].append(fileName[0:len(fileName)])
                    i+=1

                else:
                    if(invalidFlag==-1):
                        # print("File Neither in Format : ",fileName)
                        self.invalidFiles.append(fileName)
                    else:
                        if(i==0):
                            self.validFiles.append( [[root],[0],[0]])
                            self.validFiles[pos][1][0]=charCheck
                            self.validFiles[pos][2][0]=fileName
                        else:
                            self.validFiles[pos][1].append(charCheck)
                            self.validFiles[pos][2].append(fileName)
                        # print("FilePath type: ",type(FilePath))

                        i+=1
            except  Exception as error:
                if(invalidFlag==-1):
                    self.invalidFiles.append(fileName)
                    # stringPrepped ='"'+str(FilePath)+'",'
                    # self.invalidFileNames.append(stringPrepped)
                    # print("File Neither in Format : ",fileName)
                else:
                    print("OOpss! Something went wrong ... :"+str(error));

            charCheck =""
            invalidFlag=0
        try:
            if(len(self.validFiles[pos][1])>0):
                return pos+1
        except:
                
            return pos

        # print(fileName[0])
    
    # Below Algorithm runs in O(n * J) time... but
    # it changes a whole lot more due to len(filename) nver iterating over the WHOLE string.
    # one other thing, j<n or j=n=1
    # but due to j<n, & whenever j=1 time complexity is O(n) but other scenarios, O(n*J) J<5 we wont be using 5<n files that means a whole
    # lot number of files....
    def BuildMergeFile(self, pathName):
        self.path = Path(pathName)
        # for child in sorted(self.path.glob("**/*")):
        #     if(child.is_file()):
        #         print(child)
                # self.CheckFileName(FilePath=child)
        if(self.path.exists()==True):
            pos=0
            for root, dirs, files in self.path.walk(top_down=False, on_error=print):
                # print(str(root)+'\n\n')
                # print(str(files)+'\n\n')
                if(files!=[]):
                    pos=self.CheckFileName(pos, root, files=files)
            # for i in range(len(self.validFiles)):   
            #     print("Valid Files: "+str(self.validFiles[i])+"\n\n")
            #     break;

            # print("Invalid Files: "+str(self.invalidFiles)+"\n\n")

            if(len(self.validFiles)>0):
                for i in range(len(self.validFiles)):
                    r=len(self.validFiles[i][1])-1
                    p=0
                    self.pos=i
                    self.Quicksort(p,r )  
                try:
                    self.createMergeFile()
                except Exception as e:
                    print("\n\n------Error---------\n\nSomething went wrong, merge file creation wasn't success,\n error: "+str(e)+"\n\n There is a chance that some file may have not copied properly, while others were a success...\n\n Please check carefully ... \n\n----------------\n")
                self.generateLogs()
                # for i in range(len(self.validFiles)):   
                #     print("Valid Files: "+str(self.validFiles[i])+"\n\n")
            else:
                self.generateLogs()
                print("Operation  abort, no valid files found... Check the log at: "+self.pathName)
        else:
            print("\n\nPath does not exists... Please try with a valid path ...\n\n")
            
    def generateLogs(self):
        print("Generating log files ...");
        os.makedirs(self.pathName+"\\File_Merger_Logs", exist_ok=True)
        if(len(self.invalidFiles)>0):
            self.generateErrorLog()
        if(len(self.validFiles)>0):
            self.generateCopiedFiles();
        print("Log files generated successfully ...");
    
    def generateCopiedFiles(self):
        Path.touch(self.pathName+"\\File_Merger_Logs\\Merged_File_List_Log.txt",exist_ok=True)
        with open(self.pathName+"\\File_Merger_Logs\\Merged_File_List_Log.txt", 'w',encoding="utf8") as fileWriter:
           fileWriter.write('-------------------------------------------------- Merged Workflow --------------------------------------------------\n\n\n')
           for i in range(0,len(self.validFiles)):
                fileWriter.write(str(self.validFiles[i][0][0])+"\\"+str(self.validFiles[i][2]) +'\n\n\n')

    def generateErrorLog(self):
        Path.touch(self.pathName+"\\File_Merger_Logs\\Invalid_Files_Found_Log.txt",exist_ok=True)
        with open(self.pathName+"\\File_Merger_Logs\\Invalid_Files_Found_Log.txt", 'w',encoding="utf8") as fileWriter:
           fileWriter.write('-------------------------------------------------- Invalid File List --------------------------------------------------\n\n\n')
           for i in range(0,len(self.invalidFiles)):
                fileWriter.write(str(self.invalidFiles[i])+'\n\n\n')
                
    def encodeDetector(self, filePath):
        line="";
        encodingType="";

        fileReader= open(filePath, 'r',encoding="utf8") 
        while True:
            try:
                line = fileReader.readline()
            except UnicodeDecodeError:
                fileReader.close()
                encodingType='ansi'
                break
            if not line:
                fileReader.close();
                encodingType='utf8'
                break
        return encodingType;

    def createMergeFile(self):
        Path.touch(self.pathName+"\\File_Merger_Merged_File.txt",exist_ok=True)
        with open(self.pathName+"\\File_Merger_Merged_File.txt", 'w',encoding="utf8") as fileWriter:
           for i in range(0,len(self.validFiles)):
                for fileName in range(0,len(self.validFiles[i][2])):
                    filePath = os.path.join(self.validFiles[i][0][0],self.validFiles[i][2][fileName] )
                    encodingType =self.encodeDetector(filePath)
                    with open(filePath, 'r',encoding=encodingType) as fileReader:
                        fileWriter.write(fileReader.read()+'\n\n\n')
            # with open(pathName+"\\mergeFile.txt", 'r') as fd:
            #     print(fd.read())
                # fd.write(f'\n{name}')
        print("File merge successfully completed ...");



#Test path = "D:\\DBA UPGRADE\\CI CD\\Final"
if __name__ == "__main__":
    FileBuildMerger()