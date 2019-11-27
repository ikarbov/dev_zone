#!/usr/bin/python3
__author__ = 'Keith Hoyle, Snowflake Computing'
import sys, _SnoCon as sc
"""
Usage: 
   cd /Users/khoyle/Documents/workspace/venv/zzSnoCon/
   python3 5SnoConProcedures.py -c oracle -f javascript -i /Users/khoyle/Desktop/PRG/Extract_Product_KPI.sql -o /Users/khoyle/Desktop/PRG/Extract_Product_KPI.js
   python3 5SnoConProcedures.py -c oracle -f javascript -i /Users/khoyle/Desktop/PRG/PRG_LOAD_MKT_LDR_AVAIL_v1_2.sql -o /Users/khoyle/Desktop/PRG/PRG_LOAD_MKT_LDR_AVAIL_v1_2.js
   python3 5SnoConProcedures.py -c teradata -f javascript -i /Users/khoyle/Desktop/ALM_FID_RST_WB_VM_CLIENT.sh -o /Users/khoyle/Desktop/ALM_FID_RST_WB_VM_CLIENT.js
"""

################################################################################################
# Main routine ...........................................................................................
if __name__ == "__main__":
   srcConnector = 'SnoConProcedures'
   sc.init(sys.argv[1:], srcConnector)
   pData = ''
   inFile_txt = sc.inFile_txt(sc.inFile)

   # Process file...
   procs = inFile_txt.lower().split(sc.getSrcKeyWord('Procedure End')) 
   i = 1
   for proc in procs :
      proc = proc.replace(sc.getSrcKeyWord('Procedure Begin'),     sc.getTgtKeyWord('Single-Line Comment') + sc.getSrcKeyWord('Procedure Begin'))
      proc = proc.replace(sc.getSrcKeyWord('Procedure Begin Alt'), sc.getTgtKeyWord('Single-Line Comment') + sc.getSrcKeyWord('Procedure Begin Alt'))
      if i == 0 and 'begin' not in proc: #beginning comments, ignore for now...
         continue
      if len(proc.strip()) == 0 : #ending comments, ignore for now...
         continue
      pData, procName = sc.convertProc(proc, srcConnector)
      procName = procName[0:procName.find('\n')]
      
      if procName.lower() == 'anon_block' :
         procName = procName + '_' + str(i)
       # Output results...
      if sc.outFile != '' :
         oFile = sc.outFile.replace('.PY', '').replace('.py', '').replace('.JS', '').replace('.js', '') + '_' + str(i)
         if sc.cdFormat == 'javascript' :
            oFile = oFile + '.js'
         else :
            oFile = oFile + '.py'
         with open(oFile, "w+") as outputFile:
            outputFile.write(pData)
            outputFile.close()
         print('- Saved ' + oFile + '.')
      else :
         print(pData + '\n################################################################################################')
      i+=1
   print('Done! Converted ' + sc.inFile + ' to ' + sc.cdFormat + '.')
   sys.exit()
