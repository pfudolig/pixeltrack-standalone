import datetime
logfile = '/data2/user/pfudolig/pixeltrack-standalone/test.txt'
timestamp = datetime.datetime.now()

with open(logfile,"a") as myfile:
    myfile.write('\n')
    myfile.write(str(timestamp))
    myfile.write('\n')
    myfile.write('\t somethign soemthgsfn')
    myfile.write('\n')
    myfile.write('\t ehellow owlrd')

for i in range (3):
    with open(logfile,"a") as myfile:
        myfile.write('\n')
        myfile.write(str(timestamp))
        myfile.write('\n')
        myfile.write('\t somethign soemthgsfn')
        myfile.write('\n')
        myfile.write('\t ehellow owlrd')