import sys
import os.path
import mpasparse
import mpasgen
# lee el archivo que entra por linea de comando y nombra el archivo de salida
filename = sys.argv[1]
outname = os.path.splitext(filename)[0] + ".s"
# Abre archivo
f = open(filename)
data = f.read()
f.close()

top = mpasparse.parse(data)
mpasparse.dump_tree( top )


if top:
    outf = open(outname,"w")
    mpasgen.generate(outf,top)
    outf.close()
