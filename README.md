#mini-pascal-compiler

Implementación de un compilador para el lenguaje minipascal [MOD]. Fines educativos. - UTP


##USO
Un programa de minipascal esta comprendido por una o más funciones.

**Ejemplo de una función**
```
FUN foo( arg:INT )
BEGIN
  PRINT( "Hello World" )
END
```

**En general**
```
FUN <nombre funcion> ( <argumento0:type>, <argumento1:type>,... ,<argumentoN:type> )
  <var0>:<type>;
  <varN>:<type>;
BEGIN
  <sentence0>;
  <sentence1>;
  <sentenceN>
END
```

Cada sentencia finaliza con un punto y coma a excepción de la última sentencia.
**Ejemplo**
```
FUN main() 
 n:int;
 BEGIN
  WHILE i<n-1 do
  BEGIN
    WRITE(v[i]); 
    PRINT(" ");
  END;
  WRITE(v[i]);
  PRINT("Éxito\n")
END
```

## Sentencias de Niveles Inferiores
Las sentencias IF y WHILE, requieren definición de sentencias de un nivel más bajo.

**Ejemplo Sentencia de segundo nivel:**
```
FUN foo( arg:INT )
BEGIN
  WHILE arg < 3  DO
    PRINT( "Hello World" )
END
```

```
FUN foo( arg:INT )
BEGIN
  IF arg > 0 THEN
    PRINT ( "Hello world" )
  ELSE
    PRINT ( "Arg no es mayor que cero" )
END
```

```
FUN foo( arg:INT )
BEGIN
  IF arg > 0 THEN
    PRINT ( "Hello world" )
  ELSE
    PRINT ( "Arg no es mayor que cero" );
  WRITE( arg )
END
```

Ejemplo Sentencias de niveles inferiores.
```
FUN foo( arg:INT )
BEGIN
  WHILE arg < 3  DO
  BEGIN
    PRINT( "Hello World" );
    arg := arg + 1;
    ( ... )
    PRINT( "Ultima linea sin punto y coma" )
  END
END
```

```
FUN foo( arg:INT )
BEGIN
  WHILE arg < 3  DO
  BEGIN    
    arg := arg + 1;
    PRINT( "Ultima linea sin punto y coma" )
  END;
  PRINT( "Hello World" );  
END
```

```
FUN foo( arg:INT )
BEGIN
  IF arg > 0 THEN
  BEGIN
    arg := 1;
    PRINT ( "Hello world" )
  END
  ELSE
  BEGIN
    arg := 0;
    PRINT ( "Arg no es mayor que cero" )
  END;
  WRITE( arg )
END
```

#Autores
Jonathan Alvarez Gonzalez @jonaAlvarezG
Daniel Bernal @tamarindoDN

**Universidad Tecnológica de Pereira**
Ingieria en Sistemas y Computación
IS744 - Compiladores

#Recursos

* https://github.com/jhonber/mPASCAL
* http://mundogeek.net/archivos/2008/04/09/python-expresiones-regulares/
* http://stackoverflow.com/questions/419163/what-does-if-name-main-do
* http://rgruet.free.fr/

#GitHub

https://github.com/jonalvarezg/mini-pascal-compiler.git
