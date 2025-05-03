import os
from pathlib import Path, PurePath,PureWindowsPath
import random

class FileBuildMerger:

    path=Path()
    pathListMerge = []
    invalidFileNames =[]
    validFiles =[]
    invalidFiles =[]
    heapSize=0
    pos=0
    def __init__(self, pathName=""): 
        self.BuildMergeFile(pathName=pathName)
        # p = Path("D:\\Work\\Projects\\Releases\\EIM\\V9\\9.8 RC\\Oct 23, 2024\\04_ALTERSCRIPT_[EIMV9(RC98)]_Version_9.7258.0_to_Version_9.7259.0_SQL.txt")
        # p.rename("D:\\Work\\Projects\\Releases\\EIM\\V9\\9.8 RC\\Oct 23, 2024\\04_ALTERSCRIPT_[EIMV9(RC98)]_Version_9.7258.0_to_Version_9.7259.0_SQL -2.txt")
    
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
                        self.validFiles[pos][2][0]=fileName[1:len(fileName)]                
                    else:
                        self.validFiles[pos][1].append(charCheck[1:len(charCheck)])
                        self.validFiles[pos][2].append(fileName[1:len(fileName)])
                    i+=1

                else:
                    if(invalidFlag==-1):
                        print("File Neither in Format : ",fileName)
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
                    print("File Neither in Format : ",fileName)
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
        # p=Path("D:\\DBA UPGRADE\\CI CD\\Final")
        self.path = Path(pathName)
        # for child in sorted(self.path.glob("**/*")):
        #     if(child.is_file()):
        #         print(child)
                # self.CheckFileName(FilePath=child)
        pos=0
        for root, dirs, files in self.path.walk(top_down=False, on_error=print):
            # print(str(root)+'\n\n')
            # print(str(files)+'\n\n')
            if(files!=[]):
                pos=self.CheckFileName(pos, root, files=files)
        for i in range(len(self.validFiles)):   
            print("Valid Files: "+str(self.validFiles[i])+"\n\n")
            break;


        # for i in range(len(self.validFiles)):   
        #     print("Valid Files: "+str(self.validFiles[i])+"\n\n")

        print("Invalid Files: "+str(self.invalidFiles)+"\n\n")

        for i in range(len(self.validFiles)):
            r=len(self.validFiles[i][1])-1
            p=0
            self.pos=i
            self.Quicksort(p,r )  

        for i in range(len(self.validFiles)):   
            print("Valid Files: "+str(self.validFiles[i])+"\n\n")

        # print("Just test Files: "+str(self.validFiles[0][1][0])+"\n\n")
            # print(
            #     root,
            #     "consumes",
            #     sum((root / file).stat().st_size for file in files),
            #     "bytes in",
            #     len(files),
            #     "non-directory files"
            # )
        # print("----------------------- Valid File Paths ------------------------------------")
        # try:
        #     # tempPath = Path(pathName+"\\File_Merger_List.txt")
        #     Path.touch(pathName+"\\File_Merger_List.txt",exist_ok=True)
        #     # tempPath.open("a")
        #     # tempPath.write_text('my text')
        #     # tempPath.write_text('my text 2')
        #     # with Path.open(pathName+"\\mergeFile.txt") as f:
        #     #     for i in range(0,len(self.pathListMerge)-1):
        #     #         f.write(self.pathListMerge[i])
        #     # tempPath.open("w")  
        #     with open(pathName+"\\File_Merger_List.txt", 'a') as fileWriter:
        #         fileWriter.write("Invalid File Format : \n\n\n")

        #         for i in range(0,len(self.invalidFileNames)-1):
        #             fileWriter.write(self.invalidFileNames[i]+'\n')
        #         fileWriter.write("\n\n\n")
        #         fileWriter.write("Valid Files Selected : \n\n\n")
        #         for i in range(0,len(self.pathListMerge)-1):
        #             fileWriter.write(self.pathListMerge[i]+'\n')
        #     # with open(pathName+"\\mergeFile.txt", 'r') as fd:
        #     #     print(fd.read())
        #         # fd.write(f'\n{name}')
            

        # except :
        #     print("Creation Failed")
        # # print(self.pathListMerge)

    def createMergeFile(pathName,pathList=[]):
        Path.touch(pathName+"\\File_Merger_Merged_File.txt",exist_ok=True)
        with open(pathName+"\\File_Merger_Merged_File.txt", 'a',encoding="utf8") as fileWriter:
           for i in range(0,len(pathList)-1):
                with open(pathList[i], 'r',encoding="utf8") as fileReader:
                    fileWriter.write(fileReader.read()+'\n\n\n')
            # with open(pathName+"\\mergeFile.txt", 'r') as fd:
            #     print(fd.read())
                # fd.write(f'\n{name}')

#To be continued, write the script to move the not in format file to another location
#Generate a report
#Generate an error log

FileBuildMerger(pathName="D:\\DBA UPGRADE\\CI CD\\Final")

# FileBuildMerger.createMergeFile(pathName="D:\\DBA UPGRADE\\CI CD\\Final", pathList=["D:\\DBA UPGRADE\\CI CD\\Final\\1_Absence\\1_3.5\\1_ALTERSCRIPT_[SSHR(LEAVE)]_Version_9.1916.0_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\1_Absence\\1_3.5\\2_ALTERSCRIPT_[SSHR(Leave))]_Version_9.1917.0_to_Version_9.5000.0_SQL.sql",

# "D:\\DBA UPGRADE\\CI CD\\Final\\1_Absence\\2_4.5\\1_ALTERSCRIPT_[Absence]_Version_9.1000.0_to_Version_9.1000.214_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\1_Absence\\2_4.5\\2_ALTERSCRIPT_[Absence]_Version_9.1000.215_to_Version_9.1000.272_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\1_Absence\\2_4.5\\3_ALTERSCRIPT_[Absence]_Version_9.1001.0_to_Version_9.1299.0_SQL.sql",

# "D:\\DBA UPGRADE\\CI CD\\Final\\2_ALTERSCRIPT_[EHRMV9]_Version_9.6000.1_to_Version_9.6000.202_SQL.sql",

# "D:\\DBA UPGRADE\\CI CD\\Final\\2_Workflow\\1_3.5\\1_ALTERSCRIPT_[Workflow]_Version_9.1000.0_to_Version_9.5000.0_SQL.sql",

# "D:\\DBA UPGRADE\\CI CD\\Final\\2_Workflow\\2_4.5\\1_AlterScript_WFV5_Version_9.1000.0_to_Version_9.1325.0_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\2_Workflow\\2_4.5\\2_ALTERSCRIPT_[WorkflowV9]_Version_9.1326.0_to_Version_9.1713.0_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\2_Workflow\\2_4.5\\3_ALTERSCRIPT_[WorkflowV9]_Version_9.1714.0_to_Version_9.5000.0_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\2_Workflow\\2_4.5\\14_ALTERSCRIPT_[WorkflowV9]_Version_9.5001.0_to_Version_9.6000.0_SQL.sql",

# "D:\\DBA UPGRADE\\CI CD\\Final\\3_Absence\\1_4.5\\10_ALTERSCRIPT_[Absence]_Version_9.5001.0_to_Version_9.6000.0_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\3_Absence\\1_4.5\\4_ALTERSCRIPT_[Absence]_Version_9.1300.0_to_Version_9.2067.0_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\3_Absence\\1_4.5\\5_ALTERSCRIPT_[Absence]_Version_9.2068.0_to_Version_9.2189.0_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\3_Absence\\1_4.5\\6_ALTERSCRIPT_[Absence]_Version_9.2190.0_to_Version_9.2238.0_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\3_Absence\\1_4.5\\7_ALTERSCRIPT_[Absence]_Version_9.2239.0_to_Version_9.2392.0_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\3_Absence\\1_4.5\\8_ALTERSCRIPT_[Absence]_Version_9.2393.0_to_Version_9.2482.0_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\3_Absence\\1_4.5\\9_ALTERSCRIPT_[Absence]_Version_9.2483.0_to_Version_9.5000.0_SQL.sql",

# "D:\\DBA UPGRADE\\CI CD\\Final\\3_Absence\\2_3.5\\1_ALTERSCRIPT_[SSHR(Leave))]_Version_9.5001.0_to_Version_9.6000.0_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\3_Absence\\2_3.5\\2_ALTERSCRIPT_[SSHR(Leave))]_Version_9.6001.0_to_Version_9.6000.44_SQL.sql",

# "D:\\DBA UPGRADE\\CI CD\\Final\\Adhoc_Report\\1_ALTERSCRIPT_[Add-Hoc-Reporting]_Version_9.0001.0_to_Version_9.1658.0_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\Adhoc_Report\\2_ALTERSCRIPT_[Add-Hoc-Reporting]_Version_9.1659.0_to_Version_9.5000.0_SQL.sql",

# "D:\\DBA UPGRADE\\CI CD\\Final\\benefit\\1_ALTERSCRIPT_[BenifitMgtV9]_Version_9.1000.0_to_Version_9.1450.0_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\benefit\\2_ALTERSCRIPT_[BenifitMgt]_Version_9.1451.0_to_Version_9.1502.0_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\benefit\\3_ALTERSCRIPT_[BenifitMgt]_Version_9.1503.0_to_Version_9.1660.0_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\benefit\\4_ALTERSCRIPT_[BenifitMgt]_Version_9.1661.0_to_Version_9.2147.0_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\benefit\\5_ALTERSCRIPT_[BenifitMgt]_Version_9.2148.0_to_Version_9.6000.0_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\benefit\\6_ALTERSCRIPT_[BenifitMgt]_Version_9.6001.0_to_Version_9.6000.34_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\payroll\\1_Web Payroll\\1_ALTERSCRIPT_[Web_Payroll]_Version_9.1000.87_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\payroll\\1_Web Payroll\\2_ALTERSCRIPT_[Web_Payroll]_Version_9.1000.88_to_Version_9.1000.169_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\payroll\\1_Web Payroll\\3_ALTERSCRIPT_[Web_Payroll]_Version_9.1000.169_to_Version_9.1000.209_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\payroll\\1_Web Payroll\\4_AlterScript_[WebPay]_Version_9.1000.210_to_Version_9.1000.231_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\payroll\\1_Web Payroll\\5_AlterScript_[WebPay]_Version_9.1000.232_to_Version_9.1000.235_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\payroll\\1_Web Payroll\\6_AlterScript_[WebPay]_Version_9.1000.236_to_Version_9.1000.250_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\payroll\\1_Web Payroll\\7_AlterScript_[WebPay]_Version_9.1000.251_to_Version_9.1000.420_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\payroll\\1_Web Payroll\\8_AlterScript_Webpayroll_Version_9.1000.1_to_Version_9.1528.0_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\payroll\\2_Web Loan\\1_ALTERSCRIPT_[WebLoan]_Version_9.1000.0_to_Version_9.1346.0_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\payroll\\2_Web Loan\\2_ALTERSCRIPT_[WebLoan]_Version_9.1347.0_to_Version_9.1540.0_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\payroll\\2_Web Loan\\3_ALTERSCRIPT_[WebLoan]_Version_9.1541.0_to_Version_9.1655.0_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\payroll\\2_Web Loan\\4_ALTERSCRIPT_[WebLoan]_Version_9.1656.0_to_Version_9.2020.0_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\payroll\\2_Web Loan\\5_ALTERSCRIPT_[WebLoan]_Version_9.2021.0_to_Version_9.2279.0_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\payroll\\2_Web Loan\\6_ALTERSCRIPT_[WebLoan]_Version_9.2280.0_to_Version_9.5000.0_SQL.sql",

# "D:\\DBA UPGRADE\\CI CD\\Final\\payroll\\3_Web Payroll\\9_AlterScript_[WebPay]_Version_9.1529.0_to_Version_9.5000.0_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\payroll\\3_Web Payroll\\10_AlterScript_[WebPay]_Version_9.2665.0_to_Version_9.6000.0_SQL.sql",

# "D:\\DBA UPGRADE\\CI CD\\Final\\payroll\\4_adding_v9\\19_[Web_Payroll_AddingV9]_Version_9.1770.0_to_Version_9.6000.0_SQL.sql",

# "D:\\DBA UPGRADE\\CI CD\\Final\\payroll\\5_Web_Loan\\1_ALTERSCRIPT_[WebLoan]_Version_9.5000.0_to_Version_9.5000.35_SQL.sql",

# "D:\\DBA UPGRADE\\CI CD\\Final\\payroll\\6_Web_Loan_api\\1_ALTERSCRIPT_[WebLoanAPIV48]_Version_9.5116.0_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\payroll\\6_Web_Loan_api\\2_ALTERSCRIPT_[WebLoanAPIV48]_Version_9.5117.0_to_Version_9.6000.0_SQL.sql",

# "D:\\DBA UPGRADE\\CI CD\\Final\\payroll\\7_payroll\\1_AlterScript_[WebPay]_Version_9.6000.0_to_Version_9.6000.54_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\payroll\\7_payroll\\2_AlterScript_[WebPay]_Version_9.6000.55_to_Version_9.6000.55_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\payroll\\7_payroll\\3_AlterScript_[WebPay]_Version_9.6000.56_to_Version_9.6000.70_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\payroll\\7_payroll\\4_AlterScript_[WebPay]_Version_9.6000.71_to_Version_9.6000.101_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\payroll\\7_payroll\\5_AlterScript_[WebPay]_Version_9.6000.102_to_Version_9.6000.102_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\payroll\\7_payroll\\6_AlterScript_[WebPay]_Version_9.6000.102_to_Version_9.6000.105_SQL.sql",

# "D:\\DBA UPGRADE\\CI CD\\Final\\payroll\\8_globalpay\\1_AlterScript_[GlobalPay(96000200RC)]_Version_9.6000.0_to_Version_9.6000.80_SQL.sql",

# "D:\\DBA UPGRADE\\CI CD\\Final\\payroll\\9_loan\\1_ALTERSCRIPT_[WebLoan]_Version_9.6000.0_to_Version_9.6000.53_SQL.sql",

# "D:\\DBA UPGRADE\\CI CD\\Final\\recruitment_and_eim\\1_EIM\\Eim Admin\\1_AlterScript_[EIM]_Version_9.1000.1_to_Version_9.1000.77_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\recruitment_and_eim\\1_EIM\\Eim Admin\\2_AlterScript_[EIM]_Version_9.1000.78_to_Version_9.1000.137_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\recruitment_and_eim\\1_EIM\\Eim Admin\\3_AlterScript_[EIM]_Version_9.1000.138_to_Version_9.1000.160_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\recruitment_and_eim\\1_EIM\\Eim Admin\\4_ALTERSCRIPT_[EIM]_Version_9.1000.0_to_Version_9.1993.0_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\recruitment_and_eim\\1_EIM\\Eim Admin\\5_AlterScript_[EIM]_Version_9.1994.0_to_Version_9.2363.0_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\recruitment_and_eim\\1_EIM\\Eim Admin\\6_AlterScript_[EIM]_Version_9.2183.0_to_Version_9.5000.0_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\recruitment_and_eim\\1_EIM\\Eim Admin\\7_AlterScript_[EIM]_Version_9.5001.0_to_Version_9.6000.0_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\recruitment_and_eim\\1_EIM\\Eim Admin\\8_AlterScript_[EIM]_Version_9.6000.1_to_Version_9.6000.69_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\recruitment_and_eim\\1_EIM\\EIM V9\\1_AlterScript_EIM_Version_9.1000.1_to_Version_9.1000.48_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\recruitment_and_eim\\1_EIM\\EIM V9\\2_ALTERSCRIPT_[EIM]_Version_9.1000.49_to_Version_9.1000.73_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\recruitment_and_eim\\1_EIM\\EIM V9\\3_ALTERSCRIPT_[EIMV9]_Version_9.1000.74_to_Version_9.1000.78_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\recruitment_and_eim\\1_EIM\\EIM V9\\4_ALTERSCRIPT_[EIMV9]_Version_9.1000.79_to_Version_9.1000.90_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\recruitment_and_eim\\1_EIM\\EIM V9\\5_AlterScript_[EIMV9]_Version_9.1001.0_to_Version_9.2364.0_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\recruitment_and_eim\\1_EIM\\EIM V9\\6_AlterScript_[EIMV9]_Version_9.2365.0_to_Version_9.5000.0_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\recruitment_and_eim\\1_EIM\\EIM V9\\7_ALTERSCRIPT_[EIMV9]_Version_9.5001.0_to_Version_9.6000.0_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\recruitment_and_eim\\1_EIM\\EIM V9\\8_ALTERSCRIPT_[EIMV9]_Version_9.6000.1_to_Version_9.6000.60_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\recruitment_and_eim\\1_EIM\\EIM V9\\9_ALTERSCRIPT_[EIMV9]_Version_9.6000.61_to_Version_9.6000.93_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\recruitment_and_eim\\2_RecruitmentV9\\1_AlterScript_RecruitmentV9_Version_9.1000.0_to_Version_9.1000.26_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\recruitment_and_eim\\2_RecruitmentV9\\2_ALTERSCRIPT_[RecruitmentV9]_Version_9.1000.0_to_Version_9.1332.0_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\recruitment_and_eim\\2_RecruitmentV9\\3_ALTERSCRIPT_[RecruitmentV9]_Version_9.1333.0_to_Version_9.2005.0_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\recruitment_and_eim\\2_RecruitmentV9\\4_ALTERSCRIPT_[RecruitmentV9]_Version_9.2006.0_to_Version_9.5000.0_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\recruitment_and_eim\\2_RecruitmentV9\\5_ALTERSCRIPT_[RecruitmentV9]_Version_9.3742.0_to_Version_9.6000.0_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\recruitment_and_eim\\2_RecruitmentV9\\6_ALTERSCRIPT_[RecruitmentV9_9_6000_200RC]_Version_9.6000.28_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\recruitment_and_eim\\2_RecruitmentV9\\7_ALTERSCRIPT_[RecruitmentV9_9_6000_200RC]_Version_9.6000.29_to_Version_9.6000.100_SQL.sql",

# "D:\\DBA UPGRADE\\CI CD\\Final\\TNA\\1_Attendance V3.5\\1_ALTERSCRIPT_[Attendance]_Version_9.1000.1_to_Version_9.1000.97_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\TNA\\1_Attendance V3.5\\2_ALTERSCRIPT_[Attendance]_Version_9.1000.98_to_Version_9.1000.124_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\TNA\\1_Attendance V3.5\\3_ALTERSCRIPT_[Attendance]_Version_9.1000.125_to_Version_9.1000.138_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\TNA\\1_Attendance V3.5\\4_ALTERSCRIPT_[Attendance]_Version_9.1000.138_to_Version_9.1000.141_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\TNA\\1_Attendance V3.5\\5_ALTERSCRIPT_[Attendance]_Version_9.1000.142_to_Version_9.1000.169_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\TNA\\1_Attendance V3.5\\6_ALTERSCRIPT_[Attendance]_Version_9.1000.170_to_Version_9.1000.173_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\TNA\\1_Attendance V3.5\\7_ALTERSCRIPT_[Attendance]_Version_9.1000.174_to_Version_9.1000.221_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\TNA\\1_Attendance V3.5\\8_ALTERSCRIPT_[Attendance]_Version_9.1000.222_to_Version_9.1000.253_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\TNA\\1_Attendance V3.5\\9_ALTERSCRIPT_[Attendance]_Version_9.1000.254_to_Version_9.1000.262_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\TNA\\1_Attendance V3.5\\10_ALTERSCRIPT_[Attendance]_Version_9.1000.263_to_Version_9.1000.269_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\TNA\\1_Attendance V3.5\\11_ALTERSCRIPT_[Attendance]_Version_9.1000.270_to_Version_9.1000.284_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\TNA\\1_Attendance V3.5\\12_ALTERSCRIPT_[Attendance]_Version_9.1000.285_to_Version_9.1000.317_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\TNA\\1_Attendance V3.5\\13_ALTERSCRIPT_[Attendance]_Version_9.1000.318_to_Version_9.1000.355_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\TNA\\1_Attendance V3.5\\14_ALTERSCRIPT_[Attendance]_Version_9.1000.356_to_Version_9.1000.359_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\TNA\\1_Attendance V3.5\\15_ALTERSCRIPT_[Attendance]_Version_9.1000.360_to_Version_9.1000.361_SQL.sql",

# "D:\\DBA UPGRADE\\CI CD\\Final\\TNA\\2_Attendance V4.5\\1_ALTERSCRIPT_[Attendance]_Version_9.1000.1_to_Version_9.1000.170_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\TNA\\2_Attendance V4.5\\2_ALTERSCRIPT_[Attendance]_Version_9.1000.171_to_Version_9.1000.184_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\TNA\\2_Attendance V4.5\\3_ALTERSCRIPT_[Attendance]_Version_9.1000.185_to_Version_9.1000.244_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\TNA\\2_Attendance V4.5\\4_ALTERSCRIPT_[Attendance]_Version_9.1000.245_to_Version_9.1000.248_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\TNA\\2_Attendance V4.5\\5_ALTERSCRIPT_[Attendance]_Version_9.1000.249_to_Version_9.1000.252_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\TNA\\2_Attendance V4.5\\6_ALTERSCRIPT_[Attendance]_Version_9.1000.253_to_Version_9.1000.280_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\TNA\\2_Attendance V4.5\\7_ALTERSCRIPT_[Attendance]_Version_9.1000.290_to_Version_9.1000.290_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\TNA\\2_Attendance V4.5\\8_ALTERSCRIPT_[Attendance]_Version_9.1000.291_to_Version_9.1000.295_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\TNA\\2_Attendance V4.5\\9_ALTERSCRIPT_[Attendance]_Version_9.1000.296_to_Version_9.1000.308_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\TNA\\2_Attendance V4.5\\10_ALTERSCRIPT_[Attendance]_Version_9.1000.309_to_Version_9.1000.312_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\TNA\\2_Attendance V4.5\\11_ALTERSCRIPT_[Attendance]_Version_9.1000.313_to_Version_9.1000.322_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\TNA\\2_Attendance V4.5\\12_ALTERSCRIPT_[Attendance]_Version_9.1000.323_to_Version_9.1000.351_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\TNA\\2_Attendance V4.5\\13_ALTERSCRIPT_[Attendance]_Version_9.1000.352_to_Version_9.1000.377_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\TNA\\2_Attendance V4.5\\14_ALTERSCRIPT_[Attendance]_Version_9.1000.378_to_Version_9.1000.407_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\TNA\\2_Attendance V4.5\\15_ALTERSCRIPT_[Attendance]_Version_9.1000.408_to_Version_9.1000.411_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\TNA\\2_Attendance V4.5\\16_ALTERSCRIPT_[Attendance]_Version_9.1000.432_to_Version_9.1000.438_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\TNA\\2_Attendance V4.5\\17_ALTERSCRIPT_[Attendance]_Version_9.1000.439_to_Version_9.1000.457_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\TNA\\2_Attendance V4.5\\18_ALTERSCRIPT_[Attendance]_Version_9.1000.458_to_Version_9.1000.469_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\TNA\\2_Attendance V4.5\\19_ALTERSCRIPT_[Attendance]_Version_9.1000.470_to_Version_9.1000.470_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\TNA\\2_Attendance V4.5\\19i_46_ALTERSCRIPT_[Attendance]_Version_9.1000.471_to_Version_9.1000.500_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\TNA\\2_Attendance V4.5\\19ii_47_ALTERSCRIPT_[Attendance]_Version_9.1000.501_to_Version_9.1000.506_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\TNA\\2_Attendance V4.5\\19iii_48_ALTERSCRIPT_[Attendance]_Version_9.1000.507_to_Version_9.1000.514_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\TNA\\2_Attendance V4.5\\20_ALTERSCRIPT_[Attendance]_Version_9.1000.471_to_Version_9.5000.0_SQL.sql",

# "D:\\DBA UPGRADE\\CI CD\\Final\\TNA\\3_Attendance V3.5\\16_ALTERSCRIPT_[Attendance]_Version_9.1000.362_to_Version_9.1000.368_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\TNA\\3_Attendance V3.5\\17_ALTERSCRIPT_[Attendance]_Version_9.1000.369_to_Version_9.1000.374_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\TNA\\3_Attendance V3.5\\18_ALTERSCRIPT_[Attendance]_Version_9.1000.375_to_Version_9.1000.376_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\TNA\\3_Attendance V3.5\\19_ALTERSCRIPT_[Attendance]_Version_9.1000.377_to_Version_9.1000.379_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\TNA\\3_Attendance V3.5\\20_ALTERSCRIPT_[Attendance]_Version_9.1000.380_to_Version_9.1000.406_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\TNA\\3_Attendance V3.5\\21_ALTERSCRIPT_[Attendance]_Version_9.1000.389_to_Version_9.1000.418_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\TNA\\3_Attendance V3.5\\22_ALTERSCRIPT_[Attendance]_Version_9.1000.419_to_Version_9.1000.421_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\TNA\\3_Attendance V3.5\\23_ALTERSCRIPT_[Attendance]_Version_9.1000.422_to_Version_9.1000.476_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\TNA\\4_TNA_V96000\\1_V3.5\\1_ALTERSCRIPT_[Attendance]_Version_9.1086.0_to_Version_9.6000.0_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\TNA\\4_TNA_V96000\\2_V4.5\\2_ALTERSCRIPT_[Attendance]_Version_9.3574.0_to_Version_9.6000.0_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\TNA\\5_TNAV35_9_6000_200\\1_ALTERSCRIPT_[Attendance]_Version_9.6000.57_SQL.sql",
# "D:\\DBA UPGRADE\\CI CD\\Final\\TNA\\6_TNAV45_9_6000_200\\1_ALTERSCRIPT_[Attendance]_Version_9.6000.0_to_Version_9.6000.56_SQL.sql"])