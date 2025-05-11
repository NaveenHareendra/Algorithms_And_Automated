import pandas as pd
from pathlib import Path
import os

class ScriptGen:
    def __init__(self):
        self.SQLScriptGenerator();

    def SQLScriptGenerator(self):
        result = pd.read_excel(io="D://Work//Automations//Excel_Reader//data.xlsx", header=None, index_col=0)
        query ="select obj.name, col.name \n" \
        "from sys.columns col \n" \
        "inner join sys.objects obj ON obj.object_id = col.object_id \n" \
        "where obj.name in ("

        countQuery ="\n\nselect @availableObjects=COUNT(*) from sys.objects obj 	\nwhere obj.name in ("

        tempTableInsert = "INSERT INTO #tableName(nameOfTable)\nValues" 
                        
        # print()
        for tableName in result.index[0:(result.index.size-1)]:
            while tableName[0]==' ':
                tableName=tableName[1:len(tableName)]

            while tableName[len(tableName)-1]==' ':
                tableName=tableName[0:len(tableName)-1]

            while tableName[len(tableName)-1]=='\n':
                tableName=tableName[0:len(tableName)-1]

            while tableName[0]=='\n':
                tableName=tableName[1:len(tableName)]

            if tableName[len(tableName)-1]!=',':
                query+="'"+tableName+"',\n";
                countQuery+="'"+tableName+"',\n";
                tempTableInsert+="('"+tableName+"'),\n";
            else:
                # print(tableName)
                # print(f'corrected {tableName[0:len(tableName)-1]}')
                query+="'"+tableName[0:len(tableName)-1]+"',\n";
                tempTableInsert+="('"+tableName[0:len(tableName)-1]+"'),\n";
                countQuery+="'"+tableName[0:len(tableName)-1]+"',\n";
        
        tableName =result.index[result.index.size-1]

        if tableName[len(tableName)-1]!=',':
            query+=f"'{tableName}')"
            tempTableInsert+="('"+tableName+"')\n";
            countQuery+=f"'{tableName}')"
        else:
            query+=f"'{tableName[0:len(tableName)-1]}')"
            tempTableInsert+="('"+tableName[0:len(tableName)-1]+"')\n";
            countQuery+=f"'{tableName[0:len(tableName)-1]}')"

        query+="\nand obj.schema_id=(select schema_id from sys.schemas where name='<Replace>')"
        countQuery+="\nand obj.schema_id=(select schema_id from sys.schemas where name='<Replace>')"
        self.GenerateSQLFile(query, tempTableInsert,countQuery);
        print("\nFile succesfully created check Script_PreparedFROMEXCEL.sql file...\n")
        
    
    def GenerateSQLFile(self, selectQuery, InsertQuery,countQuery):
        tempTableScriptCreate ="BEGIN\n\n"\
        "declare @availableObjects smallint\n\n"\
        "drop table if exists #tableName;\n\n"\
        "create table #tableName(\n nameOfTable varchar(30) \n);\n\n"

        invalidTablePrintScript=	"DECLARE @tableNameVar varchar(50)\n"\
	"DECLARE tableNameCursor  CURSOR FOR select nameOfTable  from #tableName \n OPEN tableNameCursor\nFETCH NEXT FROM tableNameCursor INTO @tableNameVar \n"\
	"WHILE @@FETCH_STATUS = 0  \nBEGIN  	\n\nIF NOT EXISTS(select 1 from sys.objects obj where name =@tableNameVar and obj.schema_id=(select schema_id from sys.schemas where name='<DBUserId>')) BEGIN\n	" \
    " PRINT 'Table is not available at the Database: '+@tableNameVar\nEND;\n  FETCH NEXT FROM tableNameCursor INTO @tableNameVar\n  end;\n  close tableNameCursor\n  deallocate tableNameCursor;\n\n";
        
        pathName=""
        pathName +=str(Path(__file__).parent.absolute())
        Path.touch(pathName+"\\Script_PreparedFROMEXCEL.sql",exist_ok=True)
        with open(pathName+"\\Script_PreparedFROMEXCEL.sql", 'w',encoding="utf8") as fileWriter:
           fileWriter.write('-------------------------------------------------- Script File --------------------------------------------------\n\n\n')
           fileWriter.write(tempTableScriptCreate);
           print("~ Writing SQL select Query\n");
           fileWriter.write(InsertQuery+"\n\n")
           fileWriter.write(invalidTablePrintScript);
           print("~ Writing other queries\n");
           fileWriter.write(countQuery+"\n\nPRINT 'Available object count: '+convert(varchar(30),@availableObjects)\n\n")        
           print("~ Writing SQL temp table insert Query\n");
           fileWriter.write(selectQuery)
           fileWriter.write("END;\nGO\n")
           
if __name__ == "__main__":
    ScriptGen();