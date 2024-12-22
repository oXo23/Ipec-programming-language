@echo off
rem https://github.com/npocmaka/batch.scripts/edit/master/hybrids/iexpress/bat2exeIEXP.bat
if "%~2" equ "" (
    echo usage: %~nx0 batFile.bat target.Exe
    exit /b 1
)

set "target.exe=%__cd__%\%~2"
set "batch_file=%~f1"
set "bat_name=%~nx1"
set "bat_dir=%~dp1"

rem Prompt user for customization
set /p "package_name=Enter package name (e.g., com.mycompany.app): "
set /p "app_name=Enter application name: "
set /p "app_version=Enter application version: "
set /p "app_maker=Enter application maker/source/founder: "

copy /y "%~f0" "%temp%\2exe.sed" >nul

(
    echo()>>"%temp%\2exe.sed"
    echo(AppLaunched=cmd.exe /c "%bat_name%")>>"%temp%\2exe.sed"
    echo(TargetName=%target.exe%)>>"%temp%\2exe.sed"
    echo(FILE0="%bat_name%")>>"%temp%\2exe.sed"
    echo([SourceFiles])>>"%temp%\2exe.sed"
    echo(SourceFiles0=%bat_dir%)>>"%temp%\2exe.sed"
    echo([SourceFiles0])>>"%temp%\2exe.sed"
    echo(%%FILE0%%=)>>"%temp%\2exe.sed"
)

iexpress /n /q /m %temp%\2exe.sed

del /q /f "%temp%\2exe.sed"
exit /b 0

[Version]
Class=IEXPRESS
SEDVersion=3
[Options]
PackagePurpose=InstallApp
ShowInstallProgramWindow=0
HideExtractAnimation=1
UseLongFileName=1
InsideCompressed=0
CAB_FixedSize=0
CAB_ResvCodeSigning=0
RebootMode=N
InstallPrompt=
DisplayLicense=
FinishMessage=
TargetName=%target.exe%
FriendlyName=%app_name%
AppLaunched=%AppLaunched%
PostInstallCmd=<None>
AdminQuietInstCmd=
UserQuietInstCmd=

[Strings]
InstallPrompt=
DisplayLicense=
FinishMessage=
FriendlyName=%app_name%
PostInstallCmd=<None>
AdminQuietInstCmd=
UserQuietInstCmd=
