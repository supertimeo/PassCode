; Inno Setup script for PassCode

#define MyAppName "PassCode"
#define MyAppVersion "0.1.0"
#define MyAppPublisher "PassCode"
#define MyAppExeName "PassCode.exe"

[Setup]
AppId={{7A5B8C9D-1234-5678-9ABC-DEF012345678}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
Compression=zip
SolidCompression=yes
WizardStyle=modern
UninstallDisplayIcon={app}\{#MyAppExeName}
OutputBaseFilename=PassCode-Setup
OutputDir=..\dist

[Languages]
Name: "french"; MessagesFile: "compiler:Languages\French.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "startup_boot"; Description: "Lancer PassCode au demarrage du PC"; GroupDescription: "Options de demarrage:"; Flags: unchecked

[Files]
Source: "..\dist\PassCode.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\assets\*"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\configs\*"; DestDir: "{app}\configs"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Code]
procedure CurStepChanged(CurStep: TSetupStep);
var
  RegPath: String;
  ExePath: String;
begin
  if CurStep = ssPostInstall then
  begin
    RegPath := 'Software\Microsoft\Windows\CurrentVersion\Run';
    ExePath := ExpandConstant('{app}\{#MyAppExeName}');

    if IsTaskSelected('startup_boot') then
    begin
      RegWriteStringValue(HKEY_CURRENT_USER, RegPath, 'PassCode', ExePath);
    end
    else
    begin
      RegDeleteValue(HKEY_CURRENT_USER, RegPath, 'PassCode');
    end;
  end;
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
var
  RegPath: String;
begin
  if CurUninstallStep = usPostUninstall then
  begin
    RegPath := 'Software\Microsoft\Windows\CurrentVersion\Run';
    RegDeleteValue(HKEY_CURRENT_USER, RegPath, 'PassCode');
  end;
end;
