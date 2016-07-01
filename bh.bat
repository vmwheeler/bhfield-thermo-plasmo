@echo off
@echo run bhfield and paraview
rem examples - use "" to allow more than 9 args
rem bh "100 1.064 0.500 0.600 41 -2.0 2.0 1 0.0 0.0 41 -2.0 2.0 nanoshell 1.0"
rem bh "100 1.064 0.500 0.600 41 -2.0 2.0 1 0.0 0.0 41 -2.0 2.0 other     1.0 1.3205 1.53413 0.0 0.267505 7.21541"

setlocal
rem !!! set 3 dirs here !!!
set bhdir=C:\bhfield-121002\windows
set pydir=C:\bhfield-121002\vtkutils
set pvdir=C:\Program Files (x86)\ParaView 3.14.1\bin


set bhfield="%bhdir%\bhfield-arp-db.exe"
set xyz2vtk=python "%pydir%\xyz2vtk.py"
set vtk2pv="%pvdir%\pvpython.exe" "%pydir%\vtk2pv.pv.py"

mkdir %1
cd %1

if "%2" == "skip_bhfield" goto vtk
if "%2" == "vtk2pv" goto vtk2pv

%bhfield% %~1

if "%2" == "skip_vtk" goto end

:vtk

@echo dat to vtk

%xyz2vtk% "xyzs(abs[Ec]^2)" E_*.dat
%xyz2vtk% "xyzs(Uabs)"   U_*.dat
%xyz2vtk% "xyzv(E-real)v(E-imag)" V_*Ereim.dat
%xyz2vtk% "xyzv(H-real)v(H-imag)" V_*Hreim.dat
%xyz2vtk% "xyzv(E-major)v(E-minor)s(E-ellipt)s(E-azim)s(E-phi)s(E-angh)s(E-hand)" V_*Eelli.dat
%xyz2vtk% "xyzv(H-major)v(H-minor)s(H-ellipt)s(H-azim)s(H-phi)s(EH-phi-dif)s(H-angh)s(H-hand)" V_*Helli.dat
%xyz2vtk% "xyzv(S)s(EH-angle)s(I)s(Iplane)dds(divS3)s(Uabs)d" V_*Poynt.dat

mkdir dat
mkdir vtk
move /Y *.dat dat
move /Y *.vtk vtk

:vtk2pv

@echo vtk to pv scripts

%vtk2pv%

mkdir pv
mkdir img
move /Y *.pv.py pv
move /Y .\vtk\*.png img

:end

cd ..
endlocal
