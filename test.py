from devtools.linux import lxrun
a = lxrun('dmidecode', err=True)
print(a)
