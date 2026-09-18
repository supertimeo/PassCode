; Inno Setup script for PassCode

#define MyAppName "PassCode"
#define MyAppVersion "0.1.0"
#define MyAppPublisher "PassCode"
#define MyAppExeName "PassCode.exe"
#define MyWatcherExeName "PassCode_Watcher.exe"

[Setup]
AppId={{7A5B8C9D-1234-5678-9ABC-DEF012345678}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
; Installation dans le profil utilisateur (pas Program Files) et sans
; élévation admin : si le setup demandait l'admin et que l'utilisateur
; élève avec un compte différent du sien (cas classique sur certains PC),
; HKEY_CURRENT_USER pointerait vers le compte administrateur au lieu de
; celui de l'utilisateur normal, et le registre Run resterait vide pour
; ce dernier. En installant "lowest privilege" dans {localappdata}, on
; garantit que HKEY_CURRENT_USER correspond toujours au bon utilisateur.
DefaultDirName={localappdata}\Programs\{#MyAppName}
PrivilegesRequired=lowest
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
SetupIconFile=..\assets\PassCode_icon.ico
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
Name: "startup_unlock"; Description: "Lancer PassCode a chaque deverrouillage de session"; GroupDescription: "Options de demarrage:"; Flags: unchecked

[Files]
Source: "..\dist\PassCode\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\dist\PassCode_Watcher.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Code]
const
  RUN_REG_PATH = 'Software\Microsoft\Windows\CurrentVersion\Run';

procedure KillWatcherProcess;
var
  ResultCode: Integer;
begin
  Exec(ExpandConstant('{cmd}'), '/c taskkill /IM {#MyWatcherExeName} /F >nul 2>&1', '',
    SW_HIDE, ewWaitUntilTerminated, ResultCode);
end;

procedure RemoveOldScheduledTask;
var
  ResultCode: Integer;
begin
  { Nettoyage d'une éventuelle tâche planifiée créée par une ancienne version }
  Exec(ExpandConstant('{cmd}'), '/c schtasks /delete /tn PassCode /f >nul 2>&1', '',
    SW_HIDE, ewWaitUntilTerminated, ResultCode);
end;

procedure WriteRunEntryOrWarn(const ValueName, ExePath: String);
begin
  if not RegWriteStringValue(HKEY_CURRENT_USER, RUN_REG_PATH, ValueName, ExePath) then
    MsgBox('Impossible d''inscrire "' + ValueName + '" au démarrage automatique ' +
      '(clé de registre HKCU\' + RUN_REG_PATH + ').' + #13#10#13#10 +
      'L''application devra être lancée manuellement.', mbError, MB_OK);
end;

procedure CurStepChanged(CurStep: TSetupStep);
var
  ExePath, WatcherPath: String;
  ResultCode: Integer;
begin
  if CurStep = ssPostInstall then
  begin
    ExePath := ExpandConstant('{app}\{#MyAppExeName}');
    WatcherPath := ExpandConstant('{app}\{#MyWatcherExeName}');

    RemoveOldScheduledTask();
    KillWatcherProcess();
    RegDeleteValue(HKEY_CURRENT_USER, RUN_REG_PATH, 'PassCode');
    RegDeleteValue(HKEY_CURRENT_USER, RUN_REG_PATH, 'PassCode_Watcher');

    if IsTaskSelected('startup_boot') then
    begin
      { Démarrage: registre Run lance PassCode directement }
      WriteRunEntryOrWarn('PassCode', ExePath);
    end
    else if IsTaskSelected('startup_unlock') then
    begin
      { Déverrouillage: registre Run lance à la fois PassCode (pour le tout
        premier démarrage/ouverture de session) et le watcher (pour les
        déverrouillages suivants). Le watcher surveille nativement
        l'événement de déverrouillage de session
        (WTSRegisterSessionNotification) pour lancer PassCode à chaque fois.
        Plus fiable que le Task Scheduler, qui perd son trigger silencieusement
        quand le token de session interactive expire.
        Le watcher ignore lui-même les événements reçus dans les toutes
        premières secondes suivant son lancement (période de grâce), pour ne
        pas lancer PassCode en doublon si Windows envoie un faux événement de
        déverrouillage juste après le login. }
      WriteRunEntryOrWarn('PassCode', ExePath);
      WriteRunEntryOrWarn('PassCode_Watcher', WatcherPath);

      if not Exec(WatcherPath, '', '', SW_HIDE, ewNoWait, ResultCode) then
        MsgBox('Impossible de démarrer le watcher de déverrouillage immédiatement.' + #13#10 +
          'Il se lancera automatiquement à la prochaine ouverture de session.', mbInformation, MB_OK);
    end;
  end;
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
begin
  if CurUninstallStep = usPostUninstall then
  begin
    KillWatcherProcess();
    RemoveOldScheduledTask();
    RegDeleteValue(HKEY_CURRENT_USER, RUN_REG_PATH, 'PassCode');
    RegDeleteValue(HKEY_CURRENT_USER, RUN_REG_PATH, 'PassCode_Watcher');
  end;
end;
