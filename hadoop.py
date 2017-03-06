from sh import git
import sh
import subprocess
def getconfig():
    file_commit=open('./config/temp.txt')
    sh.cd('../hadoop/hadoop')
    commits=file_commit.readlines()
    index=0
    while(index<(len(commits)-1)):
        cur_commit=commits[index][:40]
        par_commit=commits[index+1][:40]
        #get the line, end with java
        diff = subprocess.check_output('git diff '+cur_commit+' '+par_commit+' --numstat|grep java$',shell=True)
        #getSubsystem(diff.split('\n'))
        #getdirectory(diff.split('\n'))
        #getfilename(diff.split('\n'))
        #getaddline(diff.split('\n'))
        #getdeleteline(diff.split('\n'))
        #getlinecode(diff.split('\n'),par_commit)
        #getnumberdev(par_commit,cur_commit)
        getaveragetime(diff.split('\n'),par_commit,cur_commit)
        #print cur_commit+" "+par_commit
        index += 2
'''
list of diff
format:
    122     59      hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/namenode/FSNamesystem.java
    562     0       hadoop-hdfs-project/hadoop-hdfs/src/test/java/org/apache/hadoop/hdfs/server/namenode/TestAuditLoggerWithCommands.java
the root directory name as the subsystem name
'''
def getSubsystem(diffs):
    print "--------------------getSubsystem-----------------------"
    subsystems = set()
    for diff in diffs:
        if(len(diff)==0):
            continue
        path = diff.split("\t")[2]
        subsystem = path.split('/')[0]
        #print subsystem
        subsystems.add(subsystem)
    print  len(subsystems)
'''
the directory name to identify directories
'''
def getdirectory(diffs):
    print "--------------------directory-----------------------"
    directorys = set()
    for diff in diffs:
        if(len(diff)==0):
            continue
        path = diff.split("\t")[2]
        start = len(path.split('/')[0])
        end = path.index(path.split('/')[-1])
        directory=path[start:end]
        #print directory
        directorys.add(directory)
    print  len(directorys)
'''
the file name to identify files
'''
def getfilename(diffs):
    print "--------------------getfilename-----------------------"
    filenames = set()
    for diff in diffs:
        if(len(diff)==0):
            continue
        path = diff.split("\t")[2]
        filename = path.split('/')[-1]
        #print filename
        filenames.add(filename)
    print  len(filenames)
'''
get addline
'''
def getaddline(diffs):
    print "--------------------getaddline-----------------------"
    sum_addline = 0
    for diff in diffs:
        if(len(diff)==0):
            continue
        addline = diff.split("\t")[0]
        sum_addline += int(addline)
    print sum_addline
'''
get deleteline
'''
def getdeleteline(diffs):
    print "--------------------deleteline-----------------------"
    sum_deleteline = 0
    for diff in diffs:
        if(len(diff)==0):
            continue
        deleteline = diff.split("\t")[1]
        sum_deleteline += int(deleteline)
    print sum_deleteline
'''
get line of code before change
'''
def getlinecode(diffs,par_commit):
    print "--------------------getlinecode-----------------------"
    subprocess.check_output('git checkout '+par_commit,shell=True)
    codelines = 0
    for diff in diffs:
        if(len(diff)==0):
            continue
        file = diff.split('\t')[2]
        #call the cloc to caculate the lines of code
        print file
        command = '../../repository/cloc/cloc '+file+'| grep ^Java'
        javacode = subprocess.check_output(command,shell=True)
        codeline = javacode.split(' ')[-1]
        codelines += int(codeline)
    print codelines
'''
get number of developers that changed the modified files
'''
def getnumberdev(par_commit,cur_commit):
    print "--------------------getnumberdev-----------------------"

    number_dev = subprocess.check_output('git shortlog --numbered --summary '+par_commit+'..'+cur_commit+'| wc -l',shell=True)
    print number_dev
'''
get average time internal between the last and the current change
'''
def getaveragetime(diffs,par_commit,cur_commit):
    print "--------------------averagetime-----------------------"
    subprocess.check_output('git checkout '+cur_commit,shell=True)
    for diff in diffs:
        if(len(diff)==0):
            continue
        file = diff.split('\t')[2]
        command='git blame '+par_commit+'..'+cur_commit+' -- '+file
        command+='|awk -F[\')\'] \'{print $2}\' | awk \'{print $1 $2}\' | sort | uniq'
        print command
        time = subprocess.check_output(command,shell=True)
        print time

getconfig()
