import os,sys,datetime,argparse
import lsequels

def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)

def print_table(lists):
    # calc widths to print nicely
    name_width =   max( [len(i[0]) for i in lists] )+1
    ranges_width = min(max( [len(i[-1]) for i in lists] ), 25)
    size_width =   max(max( [len(str(i[-2])) for i in lists] ),4)
    timeformat = '%Y-%m-%d %H:%M:%S'
    time_width = len(timeformat)
    header = f"{'':{name_width}}|{'ranges':{ranges_width}}|{'type':8}|{'size':{size_width}}|{'time':{time_width}}"

    print (header)
    #total_width =name_width+ranges_width+ size_width+
    print ("-"*(len(header)+4  ))
    for (build_name, fileType, fileCTime,fileSize, ranges ) in lists:
        #truncate ranges
        ranges = ranges[ : ranges_width ]
        timeformat = '%Y-%m-%d %H:%M:%S'
        time_width = len(timeformat)
        ts=datetime.datetime.utcfromtimestamp(fileCTime).strftime('%Y-%m-%d %H:%M:%S')
        line = f"{build_name:{name_width}}|{ranges:{ranges_width}}|{fileType:8}|{fileSize:{size_width}}|{ts:{time_width}}"
        print (line)

#run just as a program expecting --dir as a parm for listing its contents

def main():
    parser = argparse.ArgumentParser(description='Specify directory for subsequences...')
    parser.add_argument('--dir', type=dir_path)
    args = parser.parse_args()

    subSeq = lsequels.Sequel(args.dir)
    lists=subSeq.get()
    print_table(lists)

if __name__=="__main__":
    main()
