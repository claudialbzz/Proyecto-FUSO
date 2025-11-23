import sys


archivo=sys.argv[1]
n=int(sys.argv[2])
archivo_salida=sys.argv[3]

e=open(archivo,"r")
s=open(archivo_salida,"w")

dic_usuarios={}
for l in e:
    l=l.strip().split()
    if l[0] in dic_usuarios:
        dic_usuarios[l[0]]+=1
    else:
        dic_usuarios[l[0]]=0


for _ in range(n):
    maximo=0
    usuario_max=-1
    for usuario in dic_usuarios.keys():
        if dic_usuarios[usuario]>maximo:
            maximo=dic_usuarios[usuario]
            usuario_max=usuario
            dic_usuarios[usuario]=0
    s.write(f"{usuario_max}  {maximo}\n")

e.close()
s.close()

