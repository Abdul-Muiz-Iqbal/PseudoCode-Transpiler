# PseudoCode-Transpiler
A Python CLI Tool that allows you to transpile pseudocode into python code.

## Current Status
- This project will be updated as soon as I learn more pseudocode. This is meant as a boon for those who are learning pseudocode so that
they may check their logic by running the actual code.

## Error Handling
- Currently, this does not handle any errors and any mistake made in the pseudocode will cause an exception in python. This will later on be  
fixed and meaningful error messages will be given during the compilation phase. Runtime errors however, mostly will not be converted to pseudocode errors and  
will remain python exceptions.

## Usage
- `psu /file/path/ -p` This transpiles the file to a python script
- `psu /file/path/` -c This compiles the generated python file into an exe

## Requirements
- Python >= 3.*
- PyInstaller >= 4.*

## Disclaimer
- As pseudocode is a non standard way of writing algorithms, the syntax you learnt may be different from what this interprets.  
This transpiler follows syntax specifications from a school course as such, your mileage may vary.

## Thanks
- Special thanks to [@aliazam](https://www.github.com/aliazam) who joked that something like this would contradict the very reason pseudocode was made; to be non standard
