
for file in "d140g1234".split():
    fname = '%s.txt' % file
    fnew = '%s-new.txt'  % file

    f = open(fname,'r').read()
    f2 = f.replace('\t','  ')
    f3 = f2.replace('\r','\n')

    open(fnew,'w').write(f3)
    print "Created ",fnew

