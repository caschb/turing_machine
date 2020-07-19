# Turing Machine
This is a Turing Machine implementation using Python.

To use the deterministic Turing Machine run:
```
python main.py <config_file> <initial_strings_file> [-q]
```

To use the multitape Turing Machin run:
```
python main.py <config_file> <initial_strings_file> -t mtkc [-q]
```

Deterministic Turing Machine sample configurations and data:
```
datos_prueba/increment.txt -- configuration file
datos_prueba/increment_vals.txt -- data file

datos_prueba/mttarea2.txt -- configuration file
datos_prueba/mttarea2-acepta.txt -- data file
datos_prueba/mttarea2-prueba.txt -- data file
datos_prueba/mttarea2-rechaza.txt -- data file
```

Multitape Turing Machine sample configurations and data:
```
datos_prueba/mtkcintas-palin.txt -- configuration file
datos_prueba/mtkcintas-palin-strings.txt -- data file
```

Team:
1. Christian Asch B40703
2. Christian Rodríguez B76595
3. Jostin Álvarez B70374

Universidad de Costa Rica. CI-0132.
