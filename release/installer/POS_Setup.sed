[Version]
Class=IEXPRESS
SEDVersion=3

[Options]
PackagePurpose=InstallApp
ShowInstallProgramWindow=1
HideExtractAnimation=1
UseLongFileName=1
InsideCompressed=1
CAB_FixedSize=0
CAB_ResvCodeSigning=0
RebootMode=N
InstallPrompt=%InstallPrompt%
DisplayLicense=%DisplayLicense%
FinishMessage=%FinishMessage%
TargetName=%TargetName%
FriendlyName=%FriendlyName%
AppLaunched=%AppLaunched%
PostInstallCmd=<None>
AdminQuietInstCmd=
UserQuietInstCmd=
SourceFiles=SourceFiles
SelfDelete=0

[Strings]
InstallPrompt=
DisplayLicense=
FinishMessage=
TargetName=c:\Users\aprek\Desktop\FAST FOOD APP\release\POS_Setup.exe
FriendlyName=NSA Fast Food POS Update 1.2.1
AppLaunched=install_update.bat
FILE0="install_update.bat"
FILE1="payload.zip"
FILE2="uninstall.bat"

[SourceFiles]
SourceFiles0=c:\Users\aprek\Desktop\FAST FOOD APP\release\installer\

[SourceFiles0]
%FILE0%=
%FILE1%=
%FILE2%=