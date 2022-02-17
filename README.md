# pdv
Python/Kivy sistema de punto de venta

# Crear Ejecutable en Windows

### PyInstaller 3.1+ 
```
pip install --upgrade pyinstaller
```


### Crea folder donde se guardara la aplicación
```
mkdir nomb_folder
```

### Entra a ese folder en tu terminal
```
cd nomb_folder
```


### Ejecutar siguiente instrucción
```
python -m PyInstaller --name pdv_nombre camino-a-projecto\pdv\main.py
```

### Abrir el archivo .spec y dentro de este escribir al inicio:
```
from kivy_deps import sdl2, glew
```

### Dentro del mismo archivo, buscar y modificar COLLECT:
```
coll = COLLECT(exe, Tree('camino-a-projecto\\pdv\\'),
               a.binaries,
               a.zipfiles,
               a.datas,
               *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
               strip=False,
               upx=True,
               name='pdv_nombre')
```

Si no quieres que la consola (cmd) aparezca cuando ejecutes la app, cambia console de True a False
```
exe = EXE(pyz,
          # otras líneas,
          console=False,
          # otras líneas)
```


### Ejecutar siguiente instrucción
```
python -m PyInstaller pdv_nombre.spec
```

### El ejecutable se encontrara en:
```
nomb_folder/dist/pdv_nombre/app.exe
```



