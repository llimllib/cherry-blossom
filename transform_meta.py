import os, glob, re
META_RE = re.compile(r'^<!-- ?([ \w]+): ?([\w ,.:\+\/-]+)-->')
for f in glob.glob('./entries/*.txt'):
    fin = file(f)
    lines = fin.readlines()
    fin.close()
    for line in lines:
        r = META_RE.match(line)
        if r:
            metakey, val = [x.strip() for x in r.groups()]
            lines.insert(1, "#%s %s\n" % (metakey, val))
            lines.remove(line)

    fout = file(f, 'w')
    for line in lines:
        fout.write(line)
