import os#,abc
import glob
import re
from operator import itemgetter
from itertools import groupby
import sys
import datetime
from collections import defaultdict

split_unique_str="%_f2s8y9_d" # this could be anything

def find_digits(sn):
    '''
    returns tuple (first , last) occurence of the seq of digits that are at the very end of file name file_03_001.jpg (001 is found, 03 is filename identifier)

    '''
    try:
        s=sn.rsplit(".",1)[0] # no extension
        ext_l = len( sn.rsplit(".",1)[1] ) + 1
    except: # no extension
        s=sn
        ext_l=0
    ## let's search from  the end
    s = s[::-1] # reverse the str
    p = re.compile('\d')
    # find the first occurence
    res = p.search(s)
    if not res: return ()
    first = res.start()
    digit = [ s[first] ]
    next_ = first + 1 #next

    while(True):
        if s[next_].isdigit():
            digit.append(s[ next_ ])
            next_ += 1
        else: break
    return ( - (first+len( digit )) -ext_l, - first - ext_l  )

class Sequel(object):

    def __init__(self,path):
        if os.path.isdir(path):
            self.path = path
        else:
            raise NotADirectoryError(path)

    def del_seq(self):
        raise NotImplementedError
    def rename_seq(self):
        raise NotImplementedError
    def add_metadata(self,filename):
        '''
        returns a tuple with  file as metadata
        (base, extension, mtime, size,ranges)
        '''
        basename = os.path.basename(filename)
        if os.path.isfile(filename):
            fileType = basename.rsplit(".",1)[-1] # extension
            if fileType == basename:
                fileType=''
            fileCTime=os.path.getmtime(filename)
            fileSize=int(os.path.getsize(filename))
            data= (basename,fileType,fileCTime,fileSize,"")
            return data
        else: return (basename,"dir", "","","") # for directories just the type of the node

    def get(self):
        '''
        main processing func
        '''
        contents = glob.glob(self.path+"/*")       #and recognizing the sequences for grouping
        files=[]
        files_with_digits=[]
        dirs=[]
        listSeqs=[]
        the_countable={}
        for i in contents:
            basename = os.path.basename(i)
            if os.path.isdir(i):
                dirs.append( self.add_metadata(i))
            else:
                zyfry=find_digits(i)
                if zyfry :
                    f,l = zyfry
                    if l == 0: #ends with number
                        split_by_digits=basename.rsplit( basename [ f: ] , 1)
                    else:
                        split_by_digits=basename.rsplit( basename [ f:l ] , 1)

                    temp_fileName = split_by_digits[0] + split_unique_str + split_by_digits[1]
                    the_countable[basename]=temp_fileName

                else:
                    files.append(self.add_metadata(i))
        # build dictionary
        res = defaultdict(list)

        for key, val in sorted(the_countable.items()):
            res[val].append(key)

        final_dict={}
        for key, val in dict(res).items():

            before_and_after = key.split(split_unique_str)
            #print (before_and_after)
            before =  len ( before_and_after[0] )
            after =  len ( before_and_after[-1] )
            numbers_tuples = []
            if after == 0:
                numbers_tuples = [(int(i[before:]), len(i[before:] ) ) for i in val]
            else:
                numbers_tuples = [(int(i[before:-after]), len(i[before:-after] ) ) for i in val]
            final_dict[key] = numbers_tuples

        final_dict_final = {}
        for key, values in final_dict.items():
            # check if gaps
            list_a=[]
            vs=sorted([v[0] for v in values])
            min_z_fill = min([v[1] for v in values])
            for k, g in groupby( enumerate(vs), lambda x: x[1]-x[0]):
                list_a.append(list( map( itemgetter(1), g)))
            final_dict_final[key] = (list_a,min_z_fill) # pack [name mask] = (framesNumbers_lists, zfill)

        for key, values in final_dict_final.items():
            min_d = min([min(i) for i in values[0]])
            max_d = max([max(i) for i in values[0]])
            ping_filename  = os.path.join(self.path, key.replace( split_unique_str, str(min_d).zfill(values[1]) ))
            basename,fileType,fileCTime,fileSize,ranges = self.add_metadata( ping_filename )
            total_num = sum(len(x) for x in values[0])
            if total_num < 2:
                files.append( (basename, fileType,fileCTime,fileSize,"" ) )
            else:
                build_name = key.replace( split_unique_str, "%" + str(values[1]).zfill(2)+"d" )
                mi =  list(map( min, values[0]) )
                ma =  list(map( max, values[0]) )
                ranges = ",".join ( [str(i)+"-"+str(a) if not i==a else str(i) for i,a in list(zip( mi, ma))]  ) # gives 1-7, 9, 12-15, 18-23 ...
                files.append( (build_name, fileType,fileCTime,fileSize,ranges ) )
        return files
