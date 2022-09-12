echo off
set arg1=%1
set arg2=%2
shift
shift
if "%arg2%" == "python" ( GOTO No1 )
if "%arg2%" == "unittest" ( GOTO No2 )
GOTO End1

:No1
    python -m src.__init__
GOTO End1
:No2
    python -m unittest test/
GOTO End1

:End1
ECHO "File Ended"