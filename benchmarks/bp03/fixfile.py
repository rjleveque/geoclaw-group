import os

files = """d100g124       d140g1234      d61g1234
           d120g124       d149g124       d80g1234    d189g1234""".split()

for file in files:
    fname = '%s.txt' % file
    fnew = '%s-new.txt'  % file
    outfile = open(fnew,'w')

    f = open(fname,'r').read()
    #f2 = f.replace('\t','  ')
    #f3 = f2.replace('\r','\n')
    #open(fnew,'w').write(f3)

    lines = f.split('\r')
    for line in lines[1:]:
        tokens = line.split('\t')
        if len(tokens) <= 1:
            print "blank line skipped"
        else:
            if tokens[0]=='': 
                it = 1
            else:
                it = 0
            try:
                t = float(tokens[it])
                #print "t = ",t
            except:
                print "*** tokens: ",tokens
                print "*** Error in converting to float: ",tokens[1]
                print "*** line: ",line
                raise Exception()
            outstring = ""
            for token in tokens[it:]:
                outstring += token.rjust(15)
            if t <= 5.0:
                outfile.write(outstring + '\n')
            else:
                break

    outfile.close()

    print "Created ",fnew

