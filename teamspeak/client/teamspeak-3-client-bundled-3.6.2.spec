Name:           teamspeak-3-client-bundled
Version:        3.6.2
Release:        1
ExclusiveArch:  x86_64
Obsoletes:      %{name} <= %{version}
Summary:        TeamSpeak repackaged for RPM based systems

License:        TeamSpeak License
URL:            https://teamspeak.com/en/downloads/#client
Source0:        %{name}-%{version}.tar.xz

AutoReqProv:    no
BuildRequires:  pxz
BuildRequires:  sed

%description

%prep
rm -rf %{_builddir}/%{name}-%{version}/
mkdir -p %{_builddir}/%{name}-%{version}
pushd %{_builddir}/%{name}-%{version}
tar -xf %{_sourcedir}/%{name}-%{version}.tar.xz
popd

%define _ts_path /teamspeak/client-v3
%install
rm -rf %{buildroot}
# copy files to target
pushd  %{_builddir}/%{name}-%{version}
mkdir -p %{buildroot}%{_bindir}/
# update install location
sed -i -r 'h;s/[^#]*//1;x;s/#.*//;s/"\$\(dirname "\$\(readlink -f "\$\{BASH_SOURCE\[0\]\}"\)"\)"/\/usr\/lib64\/teamspeak\/client-v3\//g;G;s/(.*)\n/\1/' ts3client
cp -n  ts3client                         %{buildroot}%{_bindir}/
mkdir -p %{buildroot}%{_libdir}%{_ts_path}/
cp -n  LICENSE.txt                       %{buildroot}%{_libdir}%{_ts_path}/
cp -n  CHANGELOG                         %{buildroot}%{_libdir}%{_ts_path}/
cp -n  error_report                      %{buildroot}%{_libdir}%{_ts_path}/
cp -n  *.so*                             %{buildroot}%{_libdir}%{_ts_path}/
cp -n  openglblacklist.json              %{buildroot}%{_libdir}%{_ts_path}/
cp -n  package_inst                      %{buildroot}%{_libdir}%{_ts_path}/
cp -n  qt.conf                           %{buildroot}%{_libdir}%{_ts_path}/
cp -n  QtWebEngineProcess                %{buildroot}%{_libdir}%{_ts_path}/
cp -n  ts3client_linux_amd64             %{buildroot}%{_libdir}%{_ts_path}/
cp -n  update                            %{buildroot}%{_libdir}%{_ts_path}/
cp -nr gfx/                              %{buildroot}%{_libdir}%{_ts_path}/
cp -nr html/                             %{buildroot}%{_libdir}%{_ts_path}/
cp -nr iconengines/                      %{buildroot}%{_libdir}%{_ts_path}/
cp -nr imageformats/                     %{buildroot}%{_libdir}%{_ts_path}/
cp -nr platforms/                        %{buildroot}%{_libdir}%{_ts_path}/
cp -nr qtwebengine_locales/              %{buildroot}%{_libdir}%{_ts_path}/
cp -nr resources/                        %{buildroot}%{_libdir}%{_ts_path}/
cp -nr sound/                            %{buildroot}%{_libdir}%{_ts_path}/
cp -nr soundbackends/                    %{buildroot}%{_libdir}%{_ts_path}/
cp -nr sqldrivers/                       %{buildroot}%{_libdir}%{_ts_path}/
cp -nr styles/                           %{buildroot}%{_libdir}%{_ts_path}/
cp -nr translations/                     %{buildroot}%{_libdir}%{_ts_path}/
cp -nr xcbglintegrations/                %{buildroot}%{_libdir}%{_ts_path}/
mkdir -p %{buildroot}%{_datadir}/applications/
cp -n  com.teamspeak.client-v3.desktop %{buildroot}%{_datadir}/applications/
popd
# stop the toolkit from doing other stuff
exit 0

%clean
rm -rf %{buildroot}

%files
%{_datadir}/applications/com.teamspeak.client-v3.desktop
%{_bindir}/ts3client
%{_libdir}/%{_ts_path}/

%changelog
===============================================================================
                        TeamSpeak 3 - Client Changelog
                       Copyright TeamSpeak Systems GmbH
                          https://www.teamspeak.com
===============================================================================
   + Added feature or noticeable improvement
   - Bug fix or something removed
   * Changed or Information
   ! Important - Take note!
===============================================================================

=== Client Release 3.6.2 - 21 Sep 2023
- Fix Asus PCIe cards issue
- Fix a client crash

=== Client Release 3.6.1 - 24 Jul 2023
- Fix chat being disabled when 'Open channel chat automatically' is enabled
- Fix chat input placeholder becoming normal text
- Fix crash on MacOS with certain virtual sound cards & aggregate devices
- Fix crash on Linux with non-AVX CPUs
- Fix crash on Windows 32bit client
* Update OpenSSL to 1.1.1u
* Please note, we recommend using the 64bit client on Windows 64bit.

=== Client Release 3.6.0 - 14 Jun 2023
! Plugin API increased to 26 as workaround for Qt update incompatibility
+ Added option to automatically select channel chat tabs after connecting to a
  TeamSpeak Server.
+ Added support for OS dark mode stylesheet extensions (<style>_darkmode.qss).
  This also supports platform specific extensions (<style>_mac_darkmode.qss).
* Improved overall compatibility with TeamSpeak Server version 5 and newer.
* Tweaked icons based on user feedback.
* myTeamSpeak sync now utilizes push service instead of polling periodically.
* Certain Microsoft specific URL schemes will no longer considered to be valid
  when using [URL] bbCode tags.
* Additional Linux dependencies:
  sudo apt install libxcb-xinerama0 libatomic1 pulseaudio fontconfig
                libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-render-util0
                libxcb-xkb1 libxkbcommon-x11-0
- Disabled server list browser
- Fixed a crash on macOS versions 11.3 and newer.
- Fixed an issue with duplicate names for cached badge icons.
- Fixed an issue where channel groups were not shown in client context menus
  when an inherited group has been set.

=== Client Release 3.5.6 - 25 Nov 2020
! TeamSpeak is going back to the roots remembering its core values. Big thanks
  to our community and our users for your trust and continued support. We would
  be nothing without you!
! Updated Plugin API version to 25.
+ Added option to hide server/channel group icons in client context menus.
+ Added option to show inaccessible server/channel groups in client context
  menus as requested in our community forums.
+ Added options for IT administrators to lock user settings in an enterprise
  environment. This can be achieved by either launching the client with the
  new -locksettings commandline parameter or by placing a settings.lock file 
  in the TeamSpeak config/installation directory.
+ Added -configname commandline parameter, which can be used to specifiy a
  distinct name for your user settings in combination with -localconfig on
  Windows (example: -localconfig -configname=test).
* Updated UI with our new logo.

=== Client Release 3.5.5 - 04 Nov 2020
- Fixed crash in the comfort noise algorithm
- Fixed crash in audio processing (reported by Stefan Schiller aka scryh)

=== Client Release 3.5.3 - 07 May 2020
- Fixed a client freeze
- Fixed an issue that could reset a talking client's AGC state
- Fixed crashes reported by crashdumps

=== Client Release 3.5.2 - 02 Apr 2020
- Fixed crashes reported by crashdumps.

=== Client Release 3.5.1 - 23 Mar 2020
* Fixed a crash on startup
* Disabled playback AGC for clients sending from an Opus Music channel

=== Client Release 3.5.0 - 19 Mar 2020
! Updated Plugin API version to 24.
+ Added new voice activity detection modes (Automatic, Volume Gate, Hybrid).
+ Added automatic voice volume leveling option in playback settings.
+ Added typing attenuation feature to try to reduce the sounds made by typing.
+ Added comfort noise feature to add synthetic background noise to fill the 
  artificial silence while being connected to a TeamSpeak Server.
+ Added optional -connect commandline parameter to specify an address for 
  auto-connecting on startup (example: -connect=voice.teamspeak.com). Some
  additional parameters can be used to provide more details (-pw, -nickname, 
  -channel, -channelid, -channelpw, -newtab, -mytsid, -showqueryclients, 
  -capture, -playback, -hotkeys).
+ Added support for upcoming TeamSpeak Server releases using a PostgreSQL
  database backend.
+ Added hotkeys to assign, revoke or toggle specific server groups based on 
  current group memberships (e.g. mute clients in a specific raid group).
+ Added volume toolbox widget for quick access to microphone volume gate,
  overall and individual client volume levels.
+ Added convenience variables and options to infoframe templates.
+ Added active badge showcase to client infoframe templates.
+ Added design option to show/hide client badges in server tree.
+ Added server/channel group icons to client context menus.
* Moved server/channel group IDs to tooltips in permission settings.
* Improved client context menu to filter inaccessible groups and permission
  related tools.
* Improved echo cancellation and noise reduction systems.
* Improved error handing for multi-track recording.
* Infoframe templates now support "??" modifier for variables to prevent their
  value from being shown so they can be used conditionally to determine whether
  or not a specific line should be hidden (e.g. %%??CLIENT_FLAG_AWAY%%).
* Remote icon list is now sorted by upload date/time rather than icon ID.
* Qt color roles can now be customized in themes (e.g. for hyperlinks).
- Removed AGC from audio capture settings in favour of playback AGC.
- Fixed a bug where mutli-track recordings could cause a crash when clients
  join or leave your channel.
- Fixed a bug where multi-track recordings were not saved on server shutdown.
- Fixed a bug where custom displaynames for clients were shown in infoframe
  even when it was equal to the nickname of the client in view.
- Fixed a bug where default capture/playback profiles could not be switched.
- Fixed a bug where deactivated plugins were loaded when launching the client.
- Fixed crashes reported by crashdumps.

=== Client Release 3.3.2 - 26 Aug 2019
- Fixed a crash when calling specific plugin API functions reported by t4styy.

=== Client Release 3.3.1 - 25 Aug 2019
! Updated settings.db version to 9.
+ Added optional -configname commandline parameter to specify a custom name for 
  the settings folder. Note that this parameter needs to be used in combination
  with -localconfig on Windows (default: config).
+ Added support for channel/client permission hints to enable/disable specific 
  UI actions. Note, that this feature requires TeamSpeak Server version 3.10.0 
  or later.
* Improved settings database performance.
- Fixed a bug where the same badge icon was displayed multiple times for the
  same client.
- Fixed a bug where the infoframe did not update when the selected client left
  the server.
- Fixed a crash in Qt framework when receiving specific Unicode characters.
- Fixed a freeze problem in bookmarks manager.

=== Client Release 3.3.0 - 18 Jun 2019
! Updated Qt framework to 5.12 LTS releases.
! Updated Opus codec to version 1.3 to introduce lots of quality improvements,
  new features, and bug fixes.
! This version of the TeamSpeak Client requires macOS 10.12 (Sierra) or later.
! The HTML style tag is no longer supported in infoframe templates. All addon
  authors should use the <stylename>_chat.qss file for CSS style definitions
  instead.
! Updated Plugin API version to 23.
* Increased size limit for text messages to 8 KiB.
* Updated easy-permission templates to use Opus instead of Speex/CELT codecs.
* Spacer tags in channel names will now be omitted in infoframe templates.
* Improved pagination support for banlist and clientdblist for plugin API.
+ Added additional variables to infoframe templates.
+ Implemented multi-select for clients in the servertree.
+ Implemented multi-track recording feature, to allow recording each client's 
  audio stream independently.
+ Added support for signed badges to prevent usage of fake data. Note, that
  this feature requires TeamSpeak Server version 3.8.0 or later.
+ Added support for URL tagging in incoming text messages.
+ Added support for myTeamSpeak ID bans in virtual server banlist.
+ Added support for Windows tiles. Thanks to our user RandomHost for providing
  the material.
+ Added support for updated license types (Gamer, Commercial, Sponsorship).
+ Added invoker data for onPluginCommandEvent(). Note, that server-side support
  for this API change will be introduced with TeamSpeak Server version 3.9.0.
- Fixed a freeze in easy-permission settings when switching between different
  templates.
- Fixed a bug where default profiles could be deleted in settings.
- Fixed crashes reported by crashdumps.

=== Client Release 3.2.5 - 17 Apr 2019
- Fixed Qt security vulnerability.

=== Client Release 3.2.3 - 01 Oct 2018
- Fixed a crash in audio playback.
  Thanks to our user Seebi for the great report!

=== Client Release 3.2.2 - 17 Sep 2018
! Fixed client freeze when plugins are using voice callbacks.
! Cancel myTeamSpeak ID validation if there is no encryption key present.
- Fixed problems with myTeamSpeak ID update.
- Fixed Sync state handling if encryption was not set up.
- myTeamSpeak ID is now properly updated after using sync fallback.

=== Client Release 3.2.1 - 14 Aug 2018
! Improved connecting to myTeamSpeak service

=== Client Release 3.2.0 - 13 Aug 2018
! Dropped support for pre 3.1.0 TeamSpeak servers.
+ Introducing myTeamSpeak integrations for Twitch. Link your Twitch account
  with your myTeamSpeak account and enjoy special benefits on TeamSpeak
  servers of your subscribed Twitch streamers. This requires sending along
  your myTeamSpeak ID, enabling the server to check if your account is
  subscribed to the Streamer.
+ improved server tree performance.
- fixed bug where the client show the wrong client info if the client loads
  multiple icons
- Various myTeamSpeak Sync bug fixes and improvements.
- Client does not show a myTeamspeak ID error anymore when connecting to a pre
  3.3.0 server.
- minor fix in myTeamSpeak ID creation if requested by multiple clients.
+ Added proper error handling for integrations if the TeamSpeak server has a 
  huge time difference.
- Server integration cache is updated properly even if the integration was
  deleted and added again while connected.
- Fixed problem assigning the desired groups when logging in to an account
  while connected to a TeamSpeak server.
- Updated handling in myTeamSpeak options tab in case of connection issues.
- Fixed sorting of groups in server integration drop down box.
- Privilege key error dialog now only appears once when using an invalid key.
+ Improved server integration management dialog. Does not resize to the
  content anymore.
- Fixed german translation.
- Fixed behavior where the client didn't show an error message if a problem
  occurs while manipulating server integrations.
- Made styling for server integration management dialog possible.
- Fixed crash that occures when the client request the Twitch subscription
  status.
- Fixed error where the client does not handle a myTeamSpeakID update properly.
* Smaller updates in connection initialisation handling.

=== Client Release 3.1.10 - 09 Jun 2018
+ Introducing our new TeamSpeak Logo.

=== Client Release 3.1.9 - 04 May 2018
- Windows: Notify if microphone access is denied due to privacy settings
- Linux: Fix scrollwheel triggering mouse4/5

=== Client Release 3.1.8 - 22 Jan 2018
- Fixed disconnect on invalid connection info data.
- Fixed macOS application bundle which caused the client to not start on
  case-sensitive file systems.
- Hardened Linux startscript to better find installed SSL certificates. If no
  SSL certificates are found, don't crash the client on start but show
  meaningful error message (but we still cannot run without SSL certificates).
- Fixed critical messagebox very early in the startup process, which tried to
  load an icon before the zip archive was initialized.
- Fixed to badges parser which failed to limit shown badges to three with
  invalid input.
- Fixed creating bookmark folders in bookmarks manager.

=== Client Release 3.1.7 - 13 Dec 2017
* Added setting in Options/Design to disable tree tooltips as requested by user
  feedback. Tooltips are enabled by default.
* Added contextmenu to move bookmarks and identities between synchronized and
  local lists as usability improvement for sight-impaired users.
* Updated license agreement in installers.
* Various internal changes for our new server accounting system.
* Added support for percent-encoded server nicknames in ts3server:// links,
  invite dialog and chat.
* Use more reliable timestamp server for Windows code signing certificate.
* Refactored server nickname check and discard/apply behaviour in virtual
  server edit dialog.
* Overhauled TSDNS code to better integrate new server nicknames into the
  existing resolve process.
- Fixed rare possibility to lose synchronized items when myTeamSpeak server
  gets unresponsive.
- Fixed subscribe mode producing errors when connecting to servers where your
  subscription abilities are limited by permissions.
- Fixed empty license text in about dialog for non-german/english languages.
- Fixed possible rare crash when exiting the application on all platforms.
- Fixed possible crash on macOS in hotkey detection code.
- Fixed client freeze when trying to resolve a server nickname and backend
  is unavailable or slow.
- Fixed crash in bookmarks dialog found in crashdumps.

=== Client Release 3.1.6 - 16 Aug 2017
! Added Server Nicknames feature. Register a server nickname on the
  myTeamSpeak.com webpage to let users easily connect to your TS3 server.
! Added support for new server property and permission, which allows you to
  enter registered server nicknames as server property to display it to all
  users on this server.
* Support for new black/graylist backend.
* Support for new server license features.
* Don't spam "failed to connect to myteamspeak server" notifications. Show
  it once after client start and then again only in intervals of 6 hours.
- Windows sound backend overhaul continued.
- Fixed crashes reported by crashdumps

=== Client Release 3.1.5 - 20 Jul 2017
! This is the last release with support for Windows Vista
+ Added possibility to overwrite Qt style icons with custom iconpacks
+ Added tooltips over client and channel items in server tree
+ Added support for SVG Tiny 1.2 (static only, no animations) icons. Most 
  icons are no longer hardcoded to fixed size 16x16.
+ Replaced included default_mono and default_colored iconpacks with SVG icons.
  Iconpacks with PNG icons are still supported, so existing third-party
  iconpacks continue to work. We encourage third-party iconpack authors to
  update their iconpacks with SVG icons.
+ Overhauled icons in most windows for improved support for high dpi monitors.
* Updated Qt to 5.6.2 on Windows and macOS
* Updated Visual Studio C++ runtime on Windows to 14.0.24215 (MSVC 2015-3)
* New default style for infoframe based on "Improved Default" by Sven Paulsen.
* Removed old default/modern/classic styles.
* Rewrote translation mechanism for infoframe styles. Translations now come
  from lagos_xx.qm and are filled by C++, so multiple language templates are
  no longer necessary. However, for legacy style support, language templates
  will be loaded with priority. So if e.g. clientinfo_de.tpl exists, it will
  be used. If not, clientinfo.tpl is loaded, which should contain the new
  translatable placeholders.
* Updater no longer downloads banner from server, banner is now hardcoded in
  executable. Dynamic banners currently not needed.
- Addon management UI now properly shows state when plugins failed to
  initialize.
- Multiple minor fixes to recently overhauled hotkey system
- Fixed infinite password dialog in file browser when using cancel
- Multiple minor filetransfer fixes
- Uninstaller now automatically closes the client instead of showing dialog.
- Fixed some wrong icon names in default iconpacks, which caused these icons
  to be loaded from fallback default.zip.
- Automatically clean null icons from icon cache when updating from 3.1.4
  to 3.1.5 client. 3.1.4 might have downloaded SVGs which it cannot use, which
  caused creation of an empty icon file.
- Fixed package installer crash on Windows 32-bit OS.
- Fixed length check in various nickname input fields. Trim whitespaces before
  calculating length when doing validity checks.
- Added bandaids for misbehaving audio drivers on Windows
- Fixed possible Windows soundbackend crash reported by crashdumps
- Fixed possible spontaneous crash during client runtime

=== Client Release 3.1.4.2 - 28 Jun 2017 
! This is the last release with support for Windows Vista
! Preparation release for 3.1.5:
  Fixed possible issue when updating to future client release 3.1.5 would abort
  with a timeout error when downloading and installing the Microsoft
  redistributable installer for MSVC 2015 Update 3.
- Fixed package installer crash on Windows 32-bit OS.

=== Client Release 3.1.4.1 - 01 Mai 2017
* Automatically close TeamSpeak client on uninstall. Only show warning dialog
  if client has not closed within 5 seconds
- Fixed silent install in Windows installer

=== Client Release 3.1.4 - 13 Apr 2017
+ Angle is now the default OpenGL renderer to workaround issues with the latest
  NVidia driver update.
+ Added new commandline parameter --force-opengl-desktop, which would force the
  old default renderer
- Fixes to recently overhauled windows soundbackend

=== Client Release 3.1.3 - 23 Mar 2017
* ClientQuery plugin is now managed by the online addon system
- Fix several hotkeys not binding properly
- Fixed rare crash in Windows Audio backend
- Fixed rare crash on exit

=== Client Release 3.1.2 - 16 Mar 2017
+ Added new hotkey setting to use this hotkey only in the current server tab.
* (experimental) added command line arguments to let users with broken gfx
  drivers force using Angle DirectX backend or software rendering:
  --force-opengl-angle --force-opengl-soft
* Control plugin is now managed by the online addon system
* Various improvements to Overwolf integration.
* Minor update to license agreement logic to avoid showing a new license text
  when users are not required to re-accept the license.
* Windows Audio Session (WASAPI) sound backend improvements.
* Readded possibility to use ts3server links with token and addbookmark
  parameters, which got lost with sync changes in 3.1. Instead of storing a
  token in the bookmark as pre-3.1, the token is locally stored in a file
  and used the first time a connection is established via the added bookmark.
  Such tokens will not be synchronized via myTeamSpeak.
- Improved text in error reporter to make more clear what we are going to
  upload.
- Updated some permission help texts
- Fixed incorrect channel password being used on automatic reconnect.
- Fixed bookmarks manager drag&drop where autoconnect bookmarks lost their
  bold state.
- Fixed order of autoconnect bookmarks to behave again like in pre-3.1 clients
- Fixed package installer failing on package.ini files encoded with UTF-8-BOM.
- TSDNS deprecated dialog is now a message in the server tab.
- Fixes to sync status display in statusbar.
- Minor fixes to myTeamSpeak recovery key behaviour, don't allow using a
  recovery key after logging out of myTeamSpeak account.
- Fixed myTeamSpeak item collision dialog to no longer try to solve a
  collision while the item has already been deleted.
- Multiple improvements and fixes to new hotkey backend introduced in 3.1.1
- Minor fixes to file browser introduced with recent filetransfer rewrite.

=== Client Release 3.1.1.1 - 21 Feb 2017
! Fixed possible crash on OS X

=== Client Release 3.1.1 - 10 Feb 2017
! Plugin API version updated to 22. Version 21 plugins will continue to work.
+ New hotkey backend
  + New Plugin API to allow plugins to "provide" new hotkey input
  + Mouse Button 4 and 5 support on Linux
  + Improved cross-platform keyboard key mapping to better handle keys 
    on non US keyboards
  - Fixed a bug that would cause the client to lose the ability 
    to handle hotkeys on Mac after an update using the built-in updater
  ! Hotkeys created using Client 3.1.1 are not compatible with 3.1.0.1 or below
  ! Moved Gamepad and Joystick support from the client to a plugin. This plugin
    is available in myTeamSpeak and will be automatically installed.
+ Improvements to Windows Audio Session sound backend
* Added some informative tooltips and dialogs to myTeamSpeak dialogs, trying to
  explain what "Stay logged in on this computer" and "Synchronization" features
  do, as this apparently caused some user confusion.
* Changed behavior in myTeamSpeak options page. Apply settings immediately
  instead of waiting for Apply/Ok click.
* Added openglblacklist.json trying to workaround broken OpenGL drivers of
  some graphic cards, forcing software renderer mode.
* Added help texts to sync item collision dialogs to explain how a collision
  happened and how to resolve it.
- TSDNS fixes to workaround issues with broken routers. Using Google DNS
  servers as fallback.
- Fixed channel subscriptions of non-existant channels bloating bookmark sync
  data. Bookmarks will auto-cleanup themselves on connect.
- Open external links in online addons browser widget in external browser.
- Limit channel auto-subscription to 500 channels to avoid exceeding maximum
  server packet size.
- Fixed filetransfer from password-protected channels.
- Fixed updater UAC detection on Windows.
- Treat empty profiles in plugin API guiConnect function as "use default
  profiles", fixing issue in Overwolf apps.
- Reimplemented plugin API call getBookmarkList, added demo code to test plugin
- Fixed crash in plugin API sendFile function when passing a nullptr as return
  code.
- Fixed opening the recovery key dialog from statusbar icon when sync data
  failed to decrypt.
- Increased settings.db version to 7 due to new hotkey backend.
- Fixed various crashes found through the crashdump upload system.
- Fixed third icon in badges setup dialog not showing the proper badge.
- Various fixes to importing pre-3.1 hotkeys.
- Fixed certain unicode characters in bookmark nickname to trigger the "unsaved
  changes" dialog even if there was no change. Closing the bookmarks dialog
  with "Ok" once will fix existing bookmarks.
- Fixed clearing cache during a running client session breaking badges.
- Fixed server- and clientlog filter list breaking on entries including
  linebreaks.
- Fixed port being ignored in bookmarks using IPv6 addresses.
- Added "Cancel" button to myTeamSpeak account setup dialog.
- Fixed pressing escape not deleting the key in a hotkey dialog created by
  the plugin API requestHotkeyDialog.
- Fixed a crash in the ClientQuery Plugin.
- When a style is uninstalled, the client now switches back to default.
- When a soundpack is uninstalled, the combobox for selection is now updated
  properly.
- Sound packs can now use relative paths again to reference to default sound
  pack files
- Default sound pack gets updated immediately upon installation through addon
  browser.
- Addons are now sorted by name in the addon options

=== Client Release 3.1.0.1 - 12 Jan 2017
! Fixed crash at startup on Windows Vista

=== Client Release 3.1 15 - Dec 2016
+ Added support for myTeamSpeak. Signing up for a myTeamSpeak account will
  allow you to synchronize your bookmarks, identities, hotkeys, whisper lists
  and channel subscriptions. Upcoming myTeamSpeak features will include addons
  synchronization, addons update management, and more.
+ Added IPv6 support
+ Filetransfer backend rewritten
+ New improved echo cancellation implementation
+ Addons now install into user directory by default, where no UAC is required
  unless using a portable installation.
+ All backend for bookmarks, identities, hotkeys, whisperlists, subscriptions,
  addons etc. rewritten, using new storage system across all devices.
+ New implementation of TSDNS. Important change: The client now only looks for
  a TSDNS server on a toplevel SRV record. For server name a.b.c.d.e the client
  will only search for a TSDNS server with a SRV record named _tsdns._tcp.d.e
+ Added russian and japanese translations.
+ Upgraded C++ runtime to Visual Studio 2015. Added support to install the
  Microsoft C++ runtime package on demand during update process.
+ Added whisperlist import/export to textfile, see contextmenu on the
  synchronized/local lists in whisperlists dialog. Requested by users for
  easier sharing of complex whisperlist setups.
+ Added badges system. Redeem a code to receive special badges. Configure which
  of these badges should be shown in the client. See Options / MyTeamSpeak page
+ Added -safemode commandline parameter to skip loading any plugins.
+ Added check for injected Ad-Aware dll which may crash the TeamSpeak client.
! In recent OS X versions, hotkeys may stop working after using the built-in
  updater. When installing from a disk image, they work fine. We are currently
  evaluating this issue.
  If you are an OS X user and require hotkeys, consider using the disk image
  installer instead of the updater.
! TSDNS now uses the list https://publicsuffix.org/list/public_suffix_list.dat
  to determine at what level the client should query for a TSDNS server. It
  will pick the domain 1 level below the domains on that list. For example: for
  a.b.c.co.uk it will pick c.co.uk since co.uk is on that list.
* Do not consider a teredo tunnel as a routable ipv6 address. If there is no
  other routable ipv6 address, this means the client will not try to resolve
  ipv6 addresses.
* Submenus temporarily removed from Self menu on OS X until we find a
  workaround for Qt 5.6.1 issue with submenus not updating properly.
* Overhauled Windows sound backend.
* Plugins can now load dynamic libraries from a subfolder with same name as
  plugin library (Windows only).
- Added missing 16x16_myts_account.png to "Origin" iconpack (gfx/default.zip)

=== Client Release 3.0.19.4 - 18 Jul 2016
! Last release supporting Windows XP.
* Overwolf rebranding, open Overwolf webpage instead of running the installer.

=== Client Release 3.0.19.3 - 23 Jun 2016
- Another fix for client freeze on malicious input

=== Client Release 3.0.19.2 - 22 Jun 2016
- Fixed infinite loop when clicking on malicious channels/clients/server items
  in the tree
- Updated polish translation

=== Client Release 3.0.19.1 - 25 Apr 2016
+ Added polish and portugese translations
+ Added support for graylisted servers
- Fixed possible crash on weird unicode characters

=== Client Release 3.0.19 - 01 Apr 2016
+ Added pre- and postinstall conditions to Updater to allow running custom
  commands before or after an update. Will be used to install the new
  Visual Studio 2015 C++ runtime for next release.
+ Added French and Spanish translations
* OS X client now uses Apple Transport Security instead of OpenSSL
* Updated Lua runtime in Lua plugin
* New features window now has an expire timeout to prevent opening outdated
  news when doing a fresh install.
- Fixed possible crash on Linux 64-bit when receiving invalid network packages
- Fixed banners send with "Cache-Control" HTTP resonse header
- Fixed slow loading banners being shown after disconnecting from server
- Fixed possible freeze when loading lots of channel images
- Updated included libpng
- Updated included openssl
- Fixed master volume slider not updating properly when using multiple playback
  profiles
- Prevent displaying locale images in bbCode IMG tags
- Don't collect channelid:// URLs in Url catcher
- Fixed freeze with many images in channel description
- Fixed ban presets showing invalid preset items
- Fixed avatar display when uploading a new avatar with different dimensions
- Fixed external links in About / License
- Fixed possible Qt crash when downloading from Http sources
- Removed server IP display in server and client connection info dialogs
- Removed setup wizard, replaced with a simple dialog to let users enter a
  default nickname. To be expanded in a future release.
- Fixes to hotkey events in plugin SDK

=== Client Release 3.0.18.2 - 23 Oct 2015
! Further hardened security fix from 3.0.18.1. Remote images are now stored in
  single directory by hash, instead of subfolders.
+ Added external link warning to opening URLs from within URL Catcher
* Updated include folders in plugin SDK for recent code restructuring
* On entering an unsubscribed channel, scan all clients for CLIENT_TALK_REQUEST
  and preset that value to avoid getting the notification sound when clicking
  on that client later.
- Fixed unclickable Download Folder label in Filebrowser dialog.
- Fixed PTT delay not getting properly saved and restored.
- Replaced wrong clear filter icon in permissions overview dialog.

=== Client Release 3.0.18.1 - 10 Oct 2015
! Hotfix release to fix security vulnerability

=== Client Release 3.0.18 - 23 Sep 2015
+ Updated to Qt 5.5.0 for improved Windows 10 compatibility and to fix a crash
  seen in client 3.0.17
+ Added option to always prevent poke dialog as quick workaround after GamesCom
  feedback. See Options/Applications/Never Show Poke Dialog. This may be
  removed again when a more final solution is implemented.
+ Added warning dialog when opening hyperlinks to external pages.
+ Added cw.png to countries flags
* Updated bundled Overwolf installer
- Fixed address field on connect dialog to accept ts3server:// links again,
  a bug introduced with 3.0.17 release.
- No contextmenu in clients list of server groups dialog when the currently
  selected group is not a regular group.
- Fixed Windows 8.1 and 10 detection in new statistics gathering in 3.0.17.
- Updated some icons and banners where outdated logo was shown.
- Prevent uploading URL shortcuts on Windows to prevent a client freeze.
- Corrected a few typos in permissions help texts.

=== Client Release 3.0.17 - 04 Aug 2015
+ Added automatic crashdump upload, replacing the old manual upload to the
  forum. In case of a crash, a report tool will show and ask the user if the
  dump should automatically be uploaded to our servers.
+ Collect and send anonymous statistics about users hardware and operating
  system to us for internal decisions (which hardware and OS version needs to
  be supported etc.). Disabled by default, user will be asked by a dialog the
  first time if he agrees to send the data. Decision can be changed later in
  Options/Application/Anonymous Statistics. What exactly is being sent is
  displayed in the client log. If agreed, data is sent once per month. Users on
  beta channel always send the data.
+ Added multilingual license agreement dialog due to legal requirements.
+ Added multilingual newsticker with support dynamic update periods.
+ Multilingual Windows installer.
+ Iconpacks default_colored_2014 and default_mono_2014 updated. Some icons
  were overhauled and some new were added.
+ OS X: Added support for GateKeeper Version 2 signatures for OS X 10.9 and
  above.
+ Added more icon names to settings.ini.
+ Improved support for high resolution Retina displays.
+ Added dialog to restart client after changing iconpack or language.
+ Added taskbar flashing on incoming chat message.
* Updated Windows C++ runtime to version 120.
* Updated to Qt 5.4.1 
- Fixed URL capture when emoticon replacement is enabled. The emoticon :/ was
  replaced inside hyperlinks (http://) and thus ruined the link. Also fixed
  clientid:// and channelid:// links, which were affected by the same problem.
- Fixed scaling of various images.
- Fixed possible crashes related to filetransfer.
- Changed appearance of poke dialog when client is minimized, hidden or behind
  a fullscreen application.
- Fixed crash with rotating users in 3D sound.
- Fixed possible crash with some bluetooth controllers.
- Fixed searching server tree for customname and nickname.
- Fixed sending offline messages to multiple users.
- Fixed issue with chat partner disconnecting.
- Fixed special character treatment in TSDNS resolver.
- Fixed various issues with URL tagging.
- Reworked UTF 8 conversion backend.
- Fixed possible crash with invalid texts in virtual server settings dialog.
- Removed appscanner plugin due to questionable usefulness

=== Client Release 3.0.16 - 06 Aug 2014
+ Added two new iconpacks, one as new default. When using the old default
  iconpack, it will be changed to the new default once. Old iconpack is
  still included for people who prefer it.
+ Added new modern theme, but do not set as default automatically.
* Updated template files to use the new icon syntax.
* Added plugin_sdk.html to install directory, pointing to the current download
  location.
- Fixed possible issue with control DLL plugin and recent Overwolf release.

=== Client Release 3.0.15.1 - 14 Jul 2014
- Fixed possible client freeze with url tags.
- Fixed possible client freeze with huge images.
- Images (both remote and ts3image) with width or height > 4000 px are now
  refused and no longer displayed in the channel description.
- Magnet urls are now allowed.
- Limited number of caught URLs to 10 per chat message.
- Adjustments to teamspeak control plugin for better Overwolf compatibility.

=== Client Release 3.0.15 - 23 Jun 2014
+ Overhauled update system. General goals are to reduce download size and allow
  the updater to update itself before updating the client.
+ Two-step update ensures that the updater can update itself before updating
  the TeamSpeak client. This way we can deploy changes to the updater more 
  quickly.
+ Updater copies itself to temp folder and then runs from there, thus we no
  longer have issues with the updater not being able to update files because they
  are currently used by the system.
+ Added binary patching to the updater for a faster and much smaller download
+ Compressed update files with lzma instead of gzip to further reduce size
+ Added update channel selection to Options dialog (Applications page) to make
  it easier to switch to beta channel. No more update.ini editing required.
+ URLs will now be written into their own database named urls.db. The old urls.dat
  will be converted and deleted. If the converter finds a broken url in the
  urls.dat, the file will be discarded and a clean database will be created.
* Simplified Updater UI, removed some useless functions (Start/Changelog)
* Updated bundled Overwolf installer
* Multiple fixes and improvements to bbCode parser from 3.0.14.
* Updated openssl to 1.0.1h
- Removed pluginsdk.zip from installer and updater. It is available again from
  our downloads page (http://teamspeak.com?page=downloads).
- Removed mirrors.ini, mirrors are no longer being used.
- Fixed broken date and time displays (bans, temp passwords, messages, logs
  etc). This was an oversight when switching from Qt 4 to 5.
- Fixed currently typing pen in chat not showing to other users.
- Fixed delay after applying changes in some pages of the Options dialog,
  especially noticeable in Applications page.
- Fixed adding bans not working with some Unicode characters in nicknames.
- Fixed some tooltips which changed with Qt5.
- Fixed temporary passwords table header which broke with Qt5.
- Fixed disabling max user spinboxes in channel edit dialog.
- Fixed icon scaling when loading from folder.
- Removed icon when moving a spacer.
- The profile and whisperlist name is now limited to 60 characters.
- Fixed an icon in filebrowser.
- Fixed website invitation for OSX.
- Fixed ts3link if a file or a folder name contains whitespace.
- Fixed client freeze and lag when loading chat history.
- Fixed permission table header which broke with Qt5.
- Fixed package installer which broke with Qt5.
- Fixed timestamp field in chat. Some digits were interpreted wrong.
- Fixed package installer. Some addons could not be uncompressed.
- Fixed quotation marks surrounding news ticker in updater on Linux and OS X

=== Client Release 3.0.14 - 14 Mar 2014
+ Updated to Qt 5.2.1. Updated compilers, runtime and third party libraries.
  This includes a multitude of changes to the TeamSpeak client to ensure
  transition from Qt 4 to 5. This is a major update under the hood.
+ Iconpacks can now be provided as a zip file. See gfx/default.zip
  Old folders gfx/default and gfx/countries will be emptied on update.
  Custom iconpacks are still supported. Icons in extracted folders take
  priority over zip archives if both exist.
  Note: Plugin authors have to provide their own icons.
+ The plugin SDK is now distributed as zip archive in pluginsdk.zip. The old
  pluginsdk folder is no longer updated, original files will be automatically
  deleted on update.
+ Added https support, so the client can now load and display remote icons from
  https pages. A https server banner will work after the next server release.
* Distribute Windows runtime as DLLs in TeamSpeak installation root instead of
  using vcredist package. This is a temporary solution until the updater is
  able to run a downloaded vcredist package post-update if required.
* Unused Qt 4 libraries will be deleted by the updater when the updater starts
  (so not immediately on first update, as the old updater still requires Qt 4).
* Memory usage and overall performance optimizations.
* Plugin API increased to 20. Plugins depending on Qt 4.8 have to be updated.
* Plugin API: Added isDown parameter to requestHotkeyInputDialog function to
  support PTT key bindings. Note: It's in the pluginsdk.zip now!
* Prevent client from connecting to ports > 65535.
* Missing icons will be shown as a blue bordered icon with a number.
* Inform users when a recording client joins or leaves your channel.
* Permissions window allows to set b_channel_join_ignore_password for server
  groups, channel groups and clients.
* "Install Overwolf" checkbox in Windows is now remotely controlled by Overwolf
  server. If down or not reachable, defaults to disabled.
* Cache animated avatars/banners to lower hard disk access.
* On Linux the system tray icon is now hidden by default due to incompatibilities
  with Qt and freedesktop tray icon standards. It can be activated in the
  options.
* Privilege key window supports Multi-select for copy to clipboard action.
* Improved integration with Overwolf for their latest 2014-02-03 release.
* Moved chat format buttons from mainwindow into the chat input contextmenu.
  These actions will now add bbCode tags to the text instead of using a very
  basic WYSIWYG approach, which is too dependant on Qt CSS formatting risking
  to break on any Qt update.
* Automatically format *bold* and _underline_ in received chat messages.
- Fixed joystick/gamepad button count.
- Fixed renaming profiles.
- Fixed saving preset messages.
- Removed "Hide in taskbar" option
- Removed "Use double click to activate" option, tray icon activation is now
  using the platform standard behavior (double click on Windows, single click
  on other platforms)
- Fixed an undefined file transfer status when transfer starts.
- Fixed a possible file transfer crash when transfer starts.
- Updated emoticons display which can now show more icons at once.
- Fixed showing a blank main window when minimizing/maximizing the window
  quickly.
- PTT key in capture profile is only shown from default hotkey profile.
- Show error message on missing sound files.
- Fixed possible crash when deleting a profile.
- Fixed possible animated avatar freeze.
- Fixed rare crash when increasing identity security level.
- Fixed client name format in client banned message
- Fixed wrong notification ID in channel created event

=== Client Release 3.0.13.1 - 24 Oct 2013
+ Fixed possible crash in appscanner plugin when receiving invalid plugin
  commands via serverquery or fake plugins.
* Ignore "Hide TeamSpeak in Taskbar" option when being started from Overwolf
  while in a fullscreen game, as this may minimize the game.
* Added Ctrl+W shortcut to close server tab
* Self menu mnemonic changed from s to e to avoid collision with _S_ettings
- Appscanner plugin no longer requests autoload.
- Fixed UI display issue with delete delay in edit channel deialog when
  b_channel_modify_temp_delete_delay is not set.

=== Client Release 3.0.13 - 01 Oct 2013
+ Added support for channel delay feature in server 3.0.10. This allows to set
  a delay in seconds after which temporary channels will be deleted after the
  last client has left. To configure a virtualserver default, set the delay in
  the virtualserver edit dialog. Or configure per channel in the channel edit
  dialog. Channel templates were adjusted to show the delete delay and a count-
  down until the channel is removed.
+ Added search field in customize toolbar dialog.
+ Added display of filetransfer progress in taskbar (Windows 7 and above).
* Removed deprecated Direct Input hotkey system, meanwhile replaced by the
  "Default" hotkey system.
- Fixed assigning hotkey when key was mapped or deactivated via "ScanCode Map".
- Fixed avatar animation when an animated gif will be set after a jpg.
- Fix for Overwolf integration, avoid getting back to desktop when TeamSpeak
  is started by Overwolf in-game and immediately a dialog opens.

=== Client Release 3.0.12 - 09 Sep 2013
+ Integrated Overwolf Overlay.
  Windows: Overwolf can now be installed and started from the TeamSpeak client
  via menu and toolbar actions. Bundled Overwolf mini installer in TeamSpeak
  autoupdate and installer, which downloads the actual Overwolf installer.
  All platforms: Added Overwolf icon in TeamSpeak tree to indicate clients
  running Overwolf (can be disabled in Options/Design). These icons require
  TeamSpeak Server 3.0.9 or later.
+ Included TeamSpeak control plugin. This is part of a project offering the
  possibility to control TeamSpeak from another application running on the same
  computer, similar to the clientquery plugin. Currently Windows only. More
  detailed information will be available in the near future.
* Removed the overlay plugin from TeamSpeak installer and autoupdate, so future
  updates to the overlay plugin no longer depend on a TeamSpeak release. The
  overlay plugin is available and maintained on the authors webpage:
  http://ts3overlay.r-dev.de/
* Direct Input Hotkey is now automatically changed to "Default" in preparation
  to removing Direct Input in a later release. While you can manually switch it
  back to Direct Input again, we don't recommend to do so.
- Fixed possible crash in direct input hotkey system.
- Fixed infinite file access caused by animated images.
- Fixed possible crash in client/server log highlight dialog.
- Fixed issue running 32 bit Linux client on systems without SSE2 CPU support.

=== Client Release 3.0.11.1 - 06 Aug 2013
- Fixed possible crash in hotkey system on client startup
- Fixed dependencies on newer glibc versions
- Plugin API: Fixed ts3plugin_onHotkeyRecordedEvent not being called

=== Client Release 3.0.11 - 31 Jul 2013
! Changed the platform string for the Mac OsX platform from "Mac" to "OS X"
+ Added (Windows only) hotkey support for multiple USB devices. If we cannot
  get the USB device name from the system, we will try to read it from a local
  file. Please notice usb.ids in root folder. You can always overwrite it with
  the latest version from http://www.linux-usb.org/usb.ids.
+ The chat- and poke messages are now styleable too. Please notice the
  default_chat.qss in styles/ folder for example. The default_chat.qss is also
  the fallback if <stylename>_chat.qss does not exist.
+ Added "Classic" theme for users who want the old chat color scheme back.
+ Protection against DOS attacks was added to server 3.0.8. Added required
  counterpart of this functionality to the client. Server 3.0.8 requires
  client 3.0.11 to connect.
+ Added C++ runtime libraries to Linux deployment
* Reworked URLs storage hopefully fixing crash on loading corrupt data file.
  Stored URLs from previous versions will expire.
* Autoexpire URLs after 180 days.
* Plugin API: printMessage and printMessageToCurrentTab are now executed in
  the GUI thread, fixing a crash in the Arma plugin.
* Added "Channel" to Receive/Sent Poke notification. New default for both
  is server + channel + client.
* Added confirmation when deleting an Identity via the remove button.
* Automatically close "ban client" and "serverquery login" dialogs when
  disconnecting.
* Added limit of 40 characters in phonetic nickname field in channel dialog.
* Added character limit to name field in server/channel copy dialog.
* Added copying Server IP to clipboard from server connectioninfo dialog.
* Added a dialog to make sure the user will be informed about old USB device
  hotkeys. They have to be newly assigned once.
* Changed default chat notification settings for outgoing pokes.
* Changed default settings for neutral contacts, no custom name anymore.
* Added rootIsDecorated to remove collapse indicator on root item to stylesheet
* Added to client template: CLIENT_VERSION_SHORT, CLIENT_CONNECTED_SINCE
* Added to channel template: CHANNEL_VOICE_DATA_ENCRYPTED_FLAG
* Added to server template: SERVER_VERSION_SHORT
* Added that info frame loads the <style>_chat.qss
- Fixed issue with outgoing poke display when user has special characters in
  in his nickname and the poke contains an URL.
- Removed Collected URLs item from the tray menu.
- Fixed some custom nickname displays which were not shown correctly (chat,
  poke and whisper history).
- Fixed UTF-8 display of country tooltips (e.g. Cura�ao), added bl.png for
  Saint Barth�lemy.
- Fixed "Make current channel default" in bookmarks dialog which didn't work
  properly after adding this bookmark while already being connected.
- Fixed wrong connection count for new bookmarks (was 1 after creation even
  if we didn't connect yet).
- Fixed vanishing port number from bookmark address field.
- Fixed issue with chat pen displaying chat partner is typing when he was
  just interacting with the tab.
- Fixed webserver list freezing when webserver is not reachable.
- Fixed wrong "Apply/Discard" dialog when changing option pages.
- Plugin API: Callbacks are now called properly on requestFileList
- Fixed issues with highlight and filter in server log dialog.
- Fixed offline message subject which will no longer send newlines.
- Fixed that http:// is now the default scheme when missing in poke- or
  hostmessage dialog.
- Fixed stylesheet helper hotkey which now shows the correct object names.
- Fixed the translation of some hotkey descriptions.
- Fixed server messages which had an additional whitespace at the beginning.
- Fixed quoting of channel- and user links.
- Fixed pasting a newline character which now is prevented at several places.
- Fixed discarding mouse buttons at hotkey system "Keyboard & Mouse Only". If
  you don't need discarding, "Default" is the better choice and also more
  flexible.
- Fixed unusable sound devices in osx
- Fixed default Downloads folder on Linux, no longer download to home dir.

=== Client Release 3.0.10.1 - 04 Apr 2013
+ Fixed gatekeeper signature error starting the 3.0.10 client on Mac OS X
* Updater will in addition to renaming updated DLLs and exe also move them
  to a folder "old" to avoid Qt loading the old plugin DLLs.
* Export missing requestClientEditDescription to Lua
+ Added some context menu entries into whisper history
- Stereo recording in DirectSound works properly now
- Recording from sources with more than 2 channels should downmix properly to 
  2 channels now (in stead of just using the first 2 channels)
- Adjusted default position of windows when opened for the first time when the
  position has not yet been stored.
- Added more default languages to the Mac OS X app bundle affecting the Mac
  menu, which is independant from Qt translation files. All language folders
  are now ignored by gatekeeper, so they can be safely manually added.
- Fixed Upload button of IconView dialog on Mac OS X
- Removed warning spam message on Mac OS X when connecting to a TSDNS server.
- Fixed tooltip for United Kingdom
- Fixed possible crash in Add-Hotkey dialog
- Fixed crash when right-clicking on the background area of notification
  options.
- Do not replace "-" with "&minus;" in hostmessage dialog.
- Adjusted package installer to work properly if plugins do not follow the
  recommended name scheme of _win32.dll and _win64.dll
- Fixed possible crash when deleting profiles.
- Fixed encoding when invitation contains channel password with spaces.

=== Client Release 3.0.10 27 - Feb 2013
+ Added Opus voice and music codecs. Requires server 3.0.7 or later.
  Please note that Opus Music is not intended for general voice chat and no
  preprocessing is done when opus music is used. This means that AGC, noise
  suppression, echo cancellation etc. do not work when using Opus music.
* Updated Qt to 4.8.3 for improved Windows 8 compatibility.
* Overhauled Audio tab of channel edit dialog for new Opus Codec
* Updated client to use new permission list format as used by server 3.0.7
* Restore size and position of Complains List and Permission Overview windows.
  Changed base class of both from QDialog to QWidget.
* Added guiConnect, createBookmark, getPermissionIDByName and
  getClientNeededPermission to Lua API
* Tweaked length checks in various text fields for client and channelname.
* A spacer without a name will now be shown as an empty line.
* If a playback- or capture profile was renamed or deleted every hotkey
  depending on this profile will be adjusted.
* Changed hotkey dialog category spacer alignment to left.
* Client template can now show the update channel used by other clients.
* New option to autostart TeamSpeak on Windows startup.
* Added optional "server_uid=<suid>" parameter to ts3server links. If an
  existing bookmark with the same server UID found, the bookmarks settings
  will be used for the connection.
* Added context menu to notifications to select which sounds are important.
  The setting is global for all sound packs.
* Added context menu entry in server list to copy server address to clipboard.
* Added "Move Client to own Channel" in client context menu. 
* Added notification icon to status bar if client has unread offline messages.
* Added TS3_CONFIG_DIR environment variable to overwrite location of config
  directory.
* Adjusted default size of some windows to adjust better to small and very
  large monitor resolutions.
* Added message for outgoing pokes. Can be configured in Notifications Options.
* Overhauled Tabs look on Mac OS X via default_mac.qss stylesheet.
* ts3server links are again caught for the Collected URLs
* Added confirmation when resetting custom toolbar settings to default
* Don't show server update dialog while running a fullscreen application
- Fixed upload/download slots if one slot was set to 0.
- Fixed closing hotkey dialog even though keep open was enabled.
- Fixed copy and paste client text.
- Fixed client window sizes which now depend on the screen resolution when
  opening for the first time.
- Fixed converting 3D sound positions into db.
- Fixed offline message parsing error if message was empty.
- Fixed that hotkey push button always adds in "all" hotkey profiles instead
  of the selected one.
- Fixed resizing and centering smaller gif icons to 16x16.
- Fixed that the setup wizard only configures the default hotkey profile and
  when having more than one hotkey profile a hint on the welcome page will be
  shown as a reminder.
- Fixed bb-code of server host message when message contains newlines.
- Fixed editing a hotkey but assigning the same action.
- Fixed a direct input hotkey issue when pushing two buttons at once on
  different devices.
- Fixed stuck PTT button when releasing the mouse.
- Fixed "Edit bookmark" contextmenu in bookmarks menu.
- Fixed some ts3server links issues when using cid parameter.
- Setup wizard now always uses the Standard hotkey profile in case when
  multiple hotkey profiles exist.
- Fixed UTF-8 characters in URL catcher
- Fixed possible crash sending a poke to a meanwhile disconnected client
- Fixed local mute/unmute hotkeys
- Fixed passing onClientIDsEvent and onClientIDsFinishedEvent to Plugin API
- Fixed crash when deleting a playback profile
- Fixed crash when no default sound device is present
- Fixed previously renamed onCustom3dRolloffCalculationClientEvent and
  ts3plugin_onCustom3dRolloffCalculationWaveEvent functions in test plugin.

=== Client Release 3.0.9.2 - 29 Oct 2012
- Reverted running privileged behaviour which was changed for 3.0.9 and causes
  hotkeys not working with games running as administrator.
- Fixed writing whisper group targets.

=== Client Release 3.0.9.1 - 25 Oct 2012
+ Added button in notifications to set all bookmark soundpacks to "default".
- Fixed converter setting "default" instead of "default female voice" so old
  bookmarks use soundpack in notifications.

=== Client Release 3.0.9 - 23 Oct 2012
+ Changed the storage format of the configuration files to a SQLite database.
  Conversion is done automatically the first time the client is started, all
  affected files will be moved to a backup folder.
+ Increased Plugin API version to 19
+ Added setClientVolumeModifier to plugin API. Min/Max volume is -50.0 to +20.0
+ Added getClientNeededPermission and getPermissionIDByName to plugin API
+ Added missing plugin API parameters for onUpdateClientEvent
+ Added parsing of channel id "cid=xyz" from invitation link. If you also give
  a channel name parameter the channel id gets priority.
  e.g. http://www.teamspeak.com/invite/voice.teamspeak.com/?cid=xyz
+ Added channel/client search in active server tree with STRG+F but only if
  the server tree has the focus. Otherwise it is the ordinary chat search.
+ Added hotkey switch to previous/next channel (channel family).
+ Added hotkey switch to previous/next channel (same level).
+ Added hotkey request talk power.
+ Added hotkey revoke all and grant next user talk power.
+ Added revoke talk power by double clicking the tree icon.
+ Added revoke talk power and revoke all and grant next user talk power toolbar
  action.
+ Added host message preview button which shows the formatted message in a
  tooltip.
+ Added Hotkey Gamepad and Joystick compatibility for RAW and Direct Input.
  Existing Direct Input hotkeys will be converted to Raw Input once Direct
  Input is activated. Existing Raw Input hotkeys cannot be converted so they
  have to be reassigned.
+ Added date and time to server log ("*** Log begins...").
+ Added bookmarkmanager context menu "sort by name".
* After deleting an offline message the next message will be selected.
* Moved possible existing serverquery authlogin and authpassword from 
  ts3clientui_qt.conf to ts3clientui_qt.secrets.conf.
* Added Made in Germany icon in About dialog.
* Chat character counter always located left of newsticker.
* Client drag&drop improvements.
* Added -silent commandline parameter to package installer.
* Package installer stores installed add-ons in addons.ini
* Modified tree behaviour to avoid scrolling up/down constantly on crowded
  servers.
* Modified chat scrolling behaviour to keep the chat textoutput in place when
  new messages arrive while being scrolled up or having text selected.
* Added [hr] bbCode support to channel description.
* Added save and restore last ban reason when banning a client.
* Added offline subject and message character limit.
* When dropping many files into chat line the drop text will be just cut off at
  the end because of the chat line limit. When dropping many files into chat
  history and the message length would fit into two separate lines, the drop
  will be accepted. If the drop text is too long it will be ignored.
* Small icons will get extended and centered to at least 16x16.
* Added license display to server info (SERVER_LICENSE for template)
* Extended logging for querying TSDNS SRV records.
- Fixed context menu in channel description edit.
- Fixed HTML entities in plain chat log.
- Fixed embedding local server banner URL in [IMG] tags is no longer necessary.
  Just drop an image from file filebrowser or type a valid ts3image:// link.
- Fixed connecting to server via ts3server:// link or invitation if link
  contains a channel name.
- Fixed a reply offline message coloring issue.
- Fixed hotkey compatibility issue with keys "M" and "N".
- Fixed hotkey issue with "keyboard & mouse only" (no keys were captured).
- Fixed display of resized animated banner.
- Fixed possibily blocking ban dialog time display.
- Don't allow negative ban times.
- Fixed icon viewer grid size, which could be broken after uploading icons
  which don't have the standard size of 16x16.
- Updated b_client_is_sticky permission help text.
- Fixed unicode usage of updater uncompression tool.
- Fixed servericon not updating properly in chat tab.
- Removed legacy VAD option from capture options.
- Clear temporary statusbar message when typing chats, the max characters
  counter could overlap with tempoary help texts.
- Fixed possible crash when using the -nohotkeys parameter.
- Removed built-in serverquery Window. Future server versions do not support
  this anymore.
- Fixed max input length calculation for channel description and offine
  messages when using unicode and escaped characters.
- Fixed group sorting in channel groups of client dialog.
- Fixed saving sort column and sort order in offline messages dialog.
- Fixed that channel description editor only shows plain text.
- Fixed plugin enable/disable checkbox at plastique style.
- Fixed joining servers default channel if bookmarks default channel is full.
- Fixed copying text from info frame if text is formatted with [list] tag.
- Fixed background when dragging files from file browser.
- The offline message dialog can be opened once per server and will act on the
  servers state.
- Fixed upload/download state after resuming a transfer interrupted by error.
- Fixed transfer state after resuming an interrupted transfer and also the
  transferred size.
  
=== Client Release 3.0.8.1 - 30 Jul 2012
+ Increased Plugin API version to 18:
  Added returnCode to flushChannelCreate|Update, changed type of permissionID
  parameters from anyID to unsigned int.
+ Mono sounds can now also be sent to just left and right (stereo) speakers.
  This is now the default setting. Select "Mono to surround" in playback
  options to get the old behaviour.
* Changing the bantime dropdown no longer adjusts the time.
* Added contextmenu to copy client version from About dialog to clipboard.
* Added SERVER_ICON, CHANNEL_ICON and CLIENT_ICON variables to info templates.
* Enable scrollbuttons on Mac tabs to avoid the window resizing when too many
  chat tabs open.
* Added Isle of Man country flag.
- Fixed possible crash when clicking on ts3server:// links with a default
  channel specified.
- Fixed banlist sorting which did not apply properly after searching.
- Reverted plain/text mimetype for client items drag&drop. Needs some more work
  on lineedits first to implement this properly.

=== Client Release 3.0.8 - 16 Jul 2012
+ Added support for SRV records when resolving domain names. Format for a SRV
  record for a TS3 server is: 
  "_ts3._udp.name TTL IN SRV priority weight port target"
  It is also possible to add a SRV record for a TSDNS server for a domain, the
  format for this is:
  "_tsdns._tcp.name TTL IN SRV priority weight port target"
  The priority when resolving is: (1) _ts3 SRV record, (2) _tsdns SRV record,
  (3) TSDNS, (4) DNS
+ Added local server banner via filetransfer.
+ Added showing the chat line limit and its typed chars.
+ Added check of containing files before deleting a channel.
+ Added after assigning a hotkey the lockable key like NUM_LOCK etc. will be
  switched back to its previous state.
+ Added notification channel deleted/edited "by the server". Please note the
  two added keys CHANNEL_DELETED_BY_SERVER and CHANNEL_EDITED_OTHER_BY_SERVER
  in settings.ini. Addon Sound Packs can add them too.
+ Added custom "block receiving whisper" button for toolbar.
+ Added activate/deactivate/toggle hotkeys to block receiving whispers.
+ Mac OS X: Added Apple Developer ID certificate for gatekeeper in upcoming
  Mountain Lion release.
* Clients can now be dragged from chat log.
* Enable drag&drop from "List All Clients" again. Drag applies to the selected
  client.
* Save last sorting of "List All Clients" list. Apply sorting whenever new
  clients arrive after clicking the "More" button. Nicknames are now sorted
  case-insensitive.
* Show invoker if client description was edited by another client.
* Support bbCode in ts3plugin_infoData text
* Package installer only autoactivates styles if a qss file is present.
- Fixed "RenderDeviceContext" logging on Windows.
- Overhauled Delete Avatar mechanism to trigger more reliable when avatar was
  deleted by another user.
- Some typo fixes in English and German texts.
- Fixed voice test no longer ignores "vad over ptt".
- Fixed strange behavior when hammering PTT during voice test.
- Fixed changing enable/disable delayPTT and its delay value during voice test.
- Fixed using "Keyboard & Mouse" hotkey system with Synergy.
- Fixed chat line issue when opening menu e.g. via ALT+S.
- Fixed an issue with the filetransfer slots could get over the maximum of 10.
- Fixed crash when parsing a corrupt urls.dat (thanks to torzsi for the file).
  Please note: urls.dat is now called caught_urls.dat and because it got a new
  internal format, the old one will be deleted after convertion.
- Fixed displaying wrong default channel group in channelgroup permissions.
- Fixed a memory leak, which could increase memory usage drastically when
  running the client for a very long time.
- Fixed filter clear button in server/client logviews, cleaned up layouts.
- Fixed chat line edit char counter which now counts also unicode characters,
  so the displayed characters can be different from the counter.
  
=== Client Release 3.0.7 - 21 Jun 2012
! Plugin API changed to 17
+ Added away hotkey with away message.
+ Added toolbar buttons set and delete for avatars.
+ Added saving of ban duration for presets.
+ Added [noparse]...[/noparse] tags for chat to prevent text in between beeing
  replaced with emoticons. Note: It's strict so both tags have to be found!
+ Exported temporary password functions to Plugin API
+ New getClientDisplayname function in Plugin API (client name including custom
  nickname, as configured in the contacts)
+ Added special return value of -2 to Plugin init function. See test plugin for
  details. This return value should only be used in very rare situations.
+ Added two(windows only) additional hotkey systems for keyboard and mouse for
  testing. The RawInput system can also handle joysticks and gamepads. Existing
  hotkeys will be backed up and converted to make them also usable for the new
  systems.
+ Added dialog when trying to send a server chat without permission.
+ Added new channel description preview (work in progress) which is a
  replacement for the WYSIWYG editor.
+ Added "Enter Chat Message..." info text to chat field.
+ Added context menu to ban out of complainlist.
+ Added hotkeys to activate/deactivate/toggle 3D sound.
+ Added close Tab on middle mouse button.
+ Added readable error message if send to channel chat fails due to permission.
+ Added possibility to use custom country flag icons: If the folder
  gfx/customCountries exists, country icons will be loaded from this folder,
  otherwise as before from gfx/countries. gfx/customCountries won't be over-
  written again from updater.
* Styles can now change the color of the newsticker text, see Bluesky style for
  an example.
* Style authors: Chat line "Enter chat message" color now can be overwritten.
  See existing default.qss style for example.
* Swapped skip/negated column in permission overview so it's the same order as
  in the permissions tree.
* Request to start createfileassoc.exe to add .ts3_addon etc. file associations
  to the registry can now be skipped with "Ignore" button.
* Mac OS X: Migrated config location from ~/.ts3client to ~/Library/Application
  Support/TeamSpeak 3. The folder will automatically be moved the first time
  TeamSpeak starts, if the old folder exists and the new folder does not exist.
* Warn user when connecting to a server and the server UID has changed in
  comparison to the stored value in the bookmark.
* Compress command packets to reduce network traffic (voice and filetransfer
  will not be affected)
- Running createfileassoc.exe will restore file associations to original if the
  user had changed them manually in Windows explorer.
- Fixed copy to clipboard ts3file:// link tagging.
- Fixed some whisperlist dialog issues.
- Fixed some issues when deleting animated avatars.
- Empty banner files will be automatically removed so the client can retry
  downloading the banner.
- Fixed creating empty registry key in HKCU\Software on client start.
- Install path in package installer can now be manually edited.
- Tweaked package installer window size, was too small on Mac OS X.
- Package installer now asks if the installed addon should be activated.
  Requires to restart TeamSpeak client to actually activate the addon.
- Fixed crash when using stylesheet helper hotkey on its own tooltip.
- Volume control plugin has been removed for now, there are too many issues
  for too many users. The updater will automatically delete the DLL.
- Improved subscribe and local mute functions called by Plugins, they will
  now do exactly the same like triggering the action via client UI.
- Fixed comboboxes in connect dialog and bookmarks which returned invalid
  text when elided (including the "...", which resulted in invalid identities
  or profiles).
- Fixed disabling "Rename" and "Delete" contextmenu in server-/channelgroup
  permission windows. Requires server 3.0.6 or above.
- Fixed disabling the servergroup menuitems in a clients contextmenu, checking
  own i_group_member_add_power against each i_group_needed_member_add_power.
- Fixed default value of "Play only important sounds when muted" dropdown in
  the notifications setup.
- Disable all elements in the permissions window on anti-flood error to avoid
  leaving the permissions in an invalid state. The user needs to wait some
  seconds and then klick "Reload" to refresh dialog.
- Mac: Fixed crash when releasing a dragged tree item after disconnecting.
- Fixed client ignoring force-ptt permission when connecting to a server
  without capture profile.
- Fixed away message in tree not checking the "Ignore away message" setting
  from contacts manager.
- Not possible to send empty complains anymore.
- Fixed an issue when marking multiple offline messages as unread.
- Fixed appending wrong server chat log.
- Fixed checking folder entries on existing before opening otherwise it will be
  reset to default home dir.
- Fixed channel description preview close.
- Fixed setting channel description which was wrong on sub channels.
- Fixed messing up radioboxes in capture setup when creating new profiles.
- Fixed extracting URLs on history messages broken by &nbsp; spaces.

=== Client Release 3.0.6 - 20 Apr 2012
+ Added temporary server passwords, see contextmenu on server. Temporary
  passwords are valid for a specified period of time and work in addition to
  the permanent server password. The server requires a permanent passwords
  set, else temporary passwords have no effect. Needs server 3.0.3 or above.
+ Plugin API updated to 16
+ Added context menu "Paste & Send" in chat line.
+ The away message is now shown beside nickname.
+ Added multiselection for "Permissions > Channel Groups > Clients", the DEL
  key works too.
+ Added ban reason sorting.
+ Added line markers for each chat line. Can be disabled via chat display
  context menu (default is enabled).
+ Added ability to delete other clients avatar if b_client_avatar_delete_other
  is set. Requires server 3.0.3 or above.
+ Removed the confusing soundpack "None".
+ Added animated gif support for avatar and channel description. Can be
  toggled in Settings->Options->Design (default is enabled).
+ Added new permission b_client_request_talker, this allows clients to
  request talk power. Requires server 3.0.3 or above.
+ Added news browser, meant to point users to new features in the client.
* Added name of the user who granted talk power to the message: "Talk power
  granted by X".
* Utilities (update, error_report and package_installer) are now dynamically
  translatable.
* Plugin API changes: Added setPluginMenuEnabled, requestClientIDs,
  onClientIDsEvent, onClientIDsFinishedEvent. Removed pluginEvent and
  getAPIVersion. Removed plugin_events.h header.
* Added plugin hotkeys, see test plugin for details
* Added version string to uninstall registry entries for display in Windows
  deinstall system control panel.
* Phonetic name can now be pre- defined per identiy but still be overwritten in
  every bookmark.
* ts3server:// links can now be entered into the Connect dialog. Values from
  this link will overwrite existing values from the dialog.
* Collected URLs are now saved in binary file instead of ini, much faster.
* Display server/channel group icons in group list of permissions window.
* All clients list can now also be searched by client unique identifier.
- Fixed contextmenu in chat on ts3server links
- Fixed opening the privilege key dialog without having the permission to see
  the key list and also then, all created keys will be shown until the dialog
  has been closed or list has been reloaded.
- Minor UI overhaul of privilege key list and add dialog.
- Fixed adding a custom ban even without the permission to list. When adding a
  ban a dialog will show if the ban could be inserted.
- Empty ban list no longer shows "Insufficient permissions to view bans"
- Fixed opening URLs with different char encoding e.g. ISO 8859-1 (Latin-1) 
  having '%F6' instead of '�' in filename.
- Fixed opening text chat from a received poke on correct server.
- Fixed no colors in multiline messages.
- Fixed invitation if privilege key contains a plus sign.
- Fixed special HTML characters (<, > etc) getting lost in chat history
- Fixed special HTML characters in client description
- Clear old server log when connecting to a new server in the server log view
- Changed behaviour of the last tabs close button.
- Fixed broken avatar template values.
- Fixed poke message size limit when message includes URL(s).
- Fixed writing and reading chatlog history. Please backup or delete old chat
  logs to start clean or you might feel some strange delay.
- Fixed bookmarks manager reporting unsaved changes.
- Fixed copying nicknames from chat if they contain whitespaces.
- Removed some repetitive settings from options dialog which are also
  accessible via contextmenus in the client mainwindow.
- Adjusted client for anti-flood settings fix for server version 3.0.3.
- Fixed an assert with animated images.
- Removed animation of group icons.
- Sorting of server- and channelgroups should behave the same even with
  identical sortID everywhere in the client.
- Added Delete keyboard shortcut to subscriptions dialog to remove entries
- Volume control plugin overhaul
- Fixed possibly invalid grant value displayed in permission overhaul
- Removed "Export to PDF" in permission overhaul
- Cleaned up client, channel and server info templates. Added list of all
  replacable variables to templates so user can easily restore the removed
  information with own templates.
- Removed clientID column from all-clients list
- Fixed banners not reloading anymore when the image was not available.
- Fixed bookmark drag&drop issues on Mac.
- Fixed crash when trying to send an offline message via fake link.
- Fixed copy and paste when text contains an image object.
- Fixed saving first-start-bookmark for not using hotkeys on a temporary uuid.
- Fixed hotkey toggle/activate/deactivate plugin.
- Fixed minor issues using animated gifs.
- Added workaround for G35 sound driver issue (voice only on right site)

=== Client Release 3.0.5 - 15 Feb 2012
* Caps Lock now available as hotkey on Mac
* Minor bookmarks manager layout overhaul
* Adjusted Linux runscript to work better with KDE
- Fixed misbehaving "More" button in All Clients List
- Fixed possible crash when connecting to server
- Fixed chat input field when switching chat tabs and text was selected
- Disable "Show ServerQuery Clients" when adding a bookmark via a ts3server://
  link with "addbookmark=<label>".
- Use nickname of default identity when connecting via ts3server://
- Hide empty global "Plugins" menu when no plugin creates a global menuitem.
- Display bookmark name in server tab, bookmark name was previously ignored.
- Fixed detecting changes in bookmarks manager with new serverquery and
  soundpack settings.
- Add bookmark from ts3server link as last item on first level of the tree
  instead of subitem of the last folder.
- Calling requestFileList in plugins no longer opens file browser window in
  client (note plugins should use return codes to implement this properly).
- Updater: When autostarting the client, keep the start button disabled to
  avoid starting the client multiple times.
- Escape "&" in bookmark labels when shown in menu
- Fixed issues banning visible client when ban power was set by channel group.
- Fixed anti-flood message printed in wrong tab
- Fixed chat tab notification markers when switching between multiple servers.
- Newsticker performance improvements.
- Fixed possible crash when clicking toolbar buttons while switching servers.
- When clicking ts3server links with addbookmark=<label>, request adding new
  bookmark if the specified label does not yet exist.

=== Client Release 3.0.3 - 20 Jan 2012
! Updated plugins API to 15
+ Improved ban list, now shown as a table. Added sorting and filtering. Right-
  click on table header to configure which table columns to show.
+ Plugin API: Added function banclientdbid. Added new parameter lastNickName to
  onBanListEvent.
+ Plugin API: Added parameter clientUniqueIdentity to onClientChatClosedEvent
  and onClientChatComposingEvent.
+ Added custom plugin menus (global menu, channel and client contextmenus), so
  plugins can add menuitems to the TS3 client and receive events when the item
  is clicked. See the test plugin for details about implementing own menus.
  The Lua plugin also allows own menus.
+ Allow editing channel groups of a user in "Channel groups of Client" dialog.
+ Added button to remove all channel groups with a single click from a client
  in "Channel groups of Client" dialog.
+ Windows uninstaller optionally deletes all configuration files. Added new
  page to uninstaller where user can control this (default: do not delete).
+ Added option to clear cache on exit (Options - Security)
+ Added "Edit bookmark" to bookmarks popup menu
+ Added option to change also the nickname in connected bookmark when renamed
  oneself.
* Mac: Added Cmd+W shortcut to minimize main window
* Avatar images will be resized when uploading, to users can select a larger
  image and have TeamSpeak scale it down automatically.
* Permission tabs for channel, client and channelclient permissions are now
  disabled instead of being removed when the permission to list that type
  is missing.
* Improved behaviour of channel permissions dialog when permissions failed to
  be applied.
* Show server query clients is no longer a global option but for each server
  tab, based on a bookmark. A temporary toggle can be added by customizing the
  toolbar. Please update your bookmark. We do not convert the old setting!
* Because of now having all TS3 supported bbCodes usable in WYSIWYG editor, the
  bbCode [SIZE=+3] is just still in for convenient. Please use a fixed value
  like [SIZE=10] to have more possibilities.
* Newsticker allows to click on individual HTML links.
* Added link to Applications folder and background image to Mac disk image.
* Print memory usage to client log for testing purpose.
- Channel chat tab can no longer be closed.
- Hide "Error requesting ping" error log when disconnected (in this case it's
  not really an error).
- Hide statusbar text when mouse leaves chat text window to avoid sticky
  statusbar messages from hyperlinks.
- Fixed broken HTML in delete client confirmation dialog from List all Clients
  window when client nickname had special HTML characters like < >
- Fn key on Macbooks now recognized as hotkey
- Fixed contextmenu of bookmark menuitems when items were in subfolders
- Save channel subscriptions per server and client UID (before only per server)
- Fixed hotkey BringToFront when client was minimized.
- Fixed preventing baloontips when running a fullscreen application.
- Fixed composing and close-chat events which got previously broken.
- Fixed autoreconnecting in password-protected channel.
- Properly register packet installer file associations on Mac in the case of
  old Mac clients getting updated (worked when installing from dmg).
- Fixes and performance improvements for fetching and caching remote icons in
  channel description.
- Fixed invalid "Not connected" display in G15 plugin when closing another
  server tab.
- Removed option to configure chat history buffer size. Just use 20 lines.

=== Client Release 3.0.2 - 16 Nov 2011
! Updated plugins API to 14
+ Added individual handling of soundpacks per servertab.
+ Added that dropping a file from File Browser into an offline message will
  create a ts3file:// link. A few minor bbCodes are now usable too.
+ Added "close all but this" for chat tabs.
+ Added two notifications CLIENT_RENAMED_BY_YOU and CLIENT_RENAMED_BY_OTHER
  which were also included in our default soundpacks.
* Exported new function getClientLibVersionNumber to plugins API
* Changed paramaters of onServerLogEvent and onServerLogFinishedEvent in
  plugins API and Lua plugin scripts.
* Updated server log dialog to support new improved server logging.
* More detailed client logging for connection attempts.
* Crashdump dialogs lets you open the folder to the dump file instead of just
  copying the filename.
* Banner requests now consider the HTTP header "Cache-Control: no-cache".
* Updater autostarts client after successful update
* Improved connection quality information in statusbar.
* Added news ticker to client and updater.
* Last ban time remembered and restored when opening ban dialog the next time.
* Mac: Mainwindow splitter no longer collapsible as workaround for Qt issue.
- Fixed client issue when connected with multiple tabs and overwriting a file
  in filebrowser of inactive tab.
- Fixed some default_speech sound file issues. Some special sound files pointed
  to old targets.
- Fixed not respecting the i_group_sort_id for server/channel groups in virtual
  server edit dialog.
- Fixed some line breaks for copy & paste from chatlog.
- Fixed client can write in another opened chatab.
- Fixed showing false drop indicator frame after moving a channel spacer.
- Fixed showing "invalid client id" in "out of view" detection.
- Fixed renaming the channel tab if another channel gets a new name.
- Fixed false report "offline message sent" when permissions are insufficient.
- Fixed showing found receipients in autocompleter in "new offlinemessage"
  dialog. The search is triggered if receipient is not in the contact list.
- Fixed hiding clients system tray context menu when clicking outside.
- Fixed copying channel edit dialog description to clipboard. New Lines are no
  longer stripped off.
- Fixed whisper lamp shining blue instead red if whisper hotkey was pressed
  again before release delay was reached.
- Added missing whisper settings to contact defaults dialog.
- Bookmark folders no longer collapse when dragging & dropping.
- Added small delay when searching in the All-clients list window to prevent
  spamming the server with search requests.
- Fixed bug in tree drag&drop which made is possible to drag a wrong client
  into a channel.
- Fixed: Notifications marked as important were not saved to soundpacks.
- Fixed assert when editing "special" notifications.
- Various improvements and fixes to sound backends.
- Fixed display of b_client_skip_channelgroup_permissions in permission
  overview when skip flag was set on channel.
- Channels no longer collapse after moving when a client is moved inside.
- Fixed bookmark manager identity dropdown box misbehaving when default
  identity is not the first in the identity list.
  
=== Client Release 3.0.1 - 12 Aug 2011
* On machines that have a center speaker (like surround 5.1 and surround 7.1)
  changed the output channels for 1 channel sound to front left+right speakers
  (was center speaker). This fixes issues for people who have no center speaker
  connected even though their sound card is configured for surround sound.
- Fixed "Assertion channels==0".
- Fixed UTF-8 usage in plugins API, stylesheets, package installer, soundpacks
  and updater.
- Fix sound issue on Mac for unknown/mono sound output devices
- Fix assert in recordeditor when clientplugins modified captured sound data
- clientquery: Fix issue where no ERROR_ok was returned when running
  clientupdate
- clientquery: Documentation tweaks
- Fixed possible crash with tsdns resolve
- Fixed bug where ptt stayed active when whispering on a second tab

=== Client Release 3.0.0 - 05 Aug 2011
! Increased plugin API version to 13
+ Multiple improvements to Voice Latency (= the time it takes before what you
  say is heard by others). Among these also a tweak to the Voice Activity
  Detection which makes VAD slightly less accurate but removes 20ms of latency.
  The old VAD behavior is still available as "Legacy Voice Activation
  Detection" in capture settings.
+ Added "connectbookmark=<bookmarkUuid>" commandline parameter.
+ Changed the custom nickname character limit (no whitespaces), minimum 1 and
  maximum 30 characters.
+ Added getServerVersion, isWhispering and isReceivingWhisper to plugin API.
+ Added getAvatar and onAvatarUpdated to plugin API. See test plugin for usage.
+ Added that Push-To-Talk delay also affects Push-To-Whisper and whisper reply.
+ Showing a notice if a bookmark has "unresolved" properties to remind about
  who is using the defaults temporarily.
+ The keyboard-search in servertree has been improved. Holding down SHIFT while
  typing a character to search backwards. Custom nickname has priority.
+ Many new commands added to clientquery interface
* If a timeout occurs while enumerating direct input devices, a dialog shows
  which devices have been found so far. It might will help find the problem.
* SPECIAL_3D_TEST and SPECIAL_SOUND_TEST are always attempted to play from 
  default soundpack, even when "no sounds" is configured.
- Fixed bug that could lead to corrupted sound being played back when the
  latency factor slider was set to values > 1.
- Fixed when switching to playback profile with a slash in its name a new
  profile was created.
- Fixed whisper list hotkeys, individual use of "on key down/release".
- Fixed that servernames in subscriptions dialog will be updated.
- Fixed downloads when target dir is not writable (e.g. CD, DVD etc).
- Fixed HotKey Run Plugin commands with length above 1024 will be truncated.
  
=== Client Release 3.0.0-rc2 - 08 Jun 2011
+ Added banner resize mode to virtualserver settings.
+ Channel context menu "unsubscribe from channel family" is available as soon
  as any subchannel is subscribed.
+ "Set Avatar" now is disabled without permission.
+ Added package installer for easy plugins/styles/soundpacks etc. one-click
  installations.
* Plugin authors note: requestChannelSubscribe and requestChannelUnsubscribe
  now take an array of channelIDs as parameter instead of a single channelID.
* Exchanged default soundpack with male and female soundpacks.
* Added soundpack page to setup wizard to select one of male or female.
* Select and scroll to own client after connecting.
* Fixed switching a fullscreen game to desktop when client is minimized and
  showing the "warn while muted", the "entering moderated channel", the 
  "force push-to-talk" or the "maximum amount of clients reached" dialog.
* Client and server log windows now save and restore log level checkbox states.
* Added "Debug" checkbox to control debug output in client log window.
* Added "Delete" to channel permission to set i_channel_needed_delete_power.
* Plugin API: Added returnCode parameter to sendPluginCommand
- Support for international domain names readded.
- Removed validation of input text from connection connect and bookmark
  address field, so that every address can be used.
- Fixed possible crash in AppScanner plugin with Umlauts.
- Added a missing separator within an invitation.
- Moved rest of the sounds into soundpack for more customized handling.
- Fixed that poke dialog no longer opens when nickname was changed.
- Changed the Push-To-Talk tooltip lines which were displayed in wrong order.
- Fixed displaying port when connected via invitation.
- Fixed errordisplay when family subscriptions on channels fail.
- Fixed dropping images from filebrowser into channel description when
  connected on multiple servers.
- Fixed context menu to copy offlinemessage text.
- Limited the last mentioned URLs in systemtray context menu to 10.
- Fixed that image-descriptions near avatar are sometimes written over the edge
- Image in channel description was broken when overwritten with same name.
- Fixed that offline messages throws a warning when recipient wasn't found on
  the server.
- Don't save empty subscribed channels list when quickly disconnecting again
  from a server, loosing the subscribed channels.
- Fixed problem when binding hotkeys while joysticks were active that "pressed"
  a button constantly. 
- Fixed that TeamSpeak does not start as a result of broken input device
  drivers. If detected TeamSpeak will at least start without usable hotkeys.
- Fixed ts3server:// links being overwritten by autoconnect bookmarks when a
  bookmark for the linked server already exists.
- Windows installer no longer allows installing the 64-bit client on 32-bit
  operating systems.
- Fixed flickering of hoster button when special no-cache http flag is used.

=== Client Release 3.0.0-rc1 - 10 May 2011
! Updated CELT codec. Due to codec bitstream incompatibility you can only
  communicate with new clients in channels using the CELT codec. Old clients
  will either sound weird/corrupt, or (on newer servers) will not be heard.
! Increased plugin API version to 11
! Style authors should adjust SERVER_PORT in their serverinfo.tpl, see the
  existing template within the default style.
+ Removed fmod sound system
+ Added a new default sound pack
+ Added new "easy permission" dialogue for easier configuration of permissions
+ Added text format toolbar and WYSIWYG edit mode to channel description
  tear-off editor.
+ Added TSDNS support, see documentation on the TSDNS server release, which
  is bundled with future TS server releases. Connecting to servers for the
  first time via hostname can be slower than before in some circumstances.
+ Added delay of one second to server-side client search in "All clients"
  dialog before search can be used again to avoid spamming the server.
+ Added horizontal scrollbars to channel group dialogs
+ Added dialog to manage server subscription modes to Options - Applications
+ Removed option "Show smilies", now every chat context menu sets globally.
+ Added hotkey "Stylesheet helper" which helps us and stylesheet authors to
  show the needed information from under cursor widget. Additionally it will
  set the given stylesheet e.g. background: blue; for highlight.
+ Added "F1" keyboard shortcut to open permissions help window.
+ To avoid confusion, a notice in the advanced permissions tree informs the
  the user when b_client_skip_channelgroup_permissions is enabled.
+ Added information dialog when Automatic Speech Detection changes to
  Push-to-talk or vice versa due to b_client_force_push_to_talk.
+ Added button to chat options page to change chat default font.
+ TTS (Text To Speech) on Windows now uses the correct playback device.
+ TTS (Text To Speech) volume on Windows can now be adjusted via playback
  sound pack volume slider.
+ Channel create/edit dialog now allows to set some channel specific permission
+ Added option to virtual server dialog to disable weblist reporting
+ In filetransfer view, a slot and speed limitation can be set directly. The
  minimum speed limit is at least 5 KiB.
+ Fixed making a passworded channel to default channel. Note: If a channel was
  made to a default channel it cannot just be switched back. Make another
  channel default instead - see also tooltip.
+ Showing information message when trying to delete the default channel.
* Updated to Qt 4.7.2
* Playback options: Voice volume slider now requires a click to "Apply", so
  both sliders now behave identical.
* Overhauled ban dialogs.
* Overhauled webserver list layout.
* Print more detailed message when a channel/client/server icon wasn't found.
* Testing voice in the capture device option page will now use the default
  playback profile instead of the currently selected profile.
* Capture Mode and -Device can be changed during an active voice test.
* Hoster button now works with php scripts serving images, it is not longer
  required to directly link to image files.
  link to image files 
* The file transfer bandwidth limit takes influence of the available slots.
  Each slot should have at least 5 KiB/s, 2 slots 10 KiB/s etc.
* Updated layout of channel settings dialog
* Capture- and Playback devices will be checked for validity and existence 
  on device change or when the connection is initiated.
* "Start/Stop rotation" have been removed from 3D item context menu entries.
* The invitation dialog will be closed when client gets disconnected.
* Glance button no longer toggles global option, instead toggle the subscribe
  subscribe state for individual server tabs. State is saved and restored per
  server unique id over client restart.
* Removed option "Mute microphone when locking", now always active.
* Enabled text chat to ServerQuery clients. Inform user that a ServerQuery
  needs to register for private text messages to receive private chats.
* To reduce server load, when applying easy permissions send all permissions
  in one step. This makes marking UI elements red when the permissions could
  not be applied unfortunately impossible, so this feature was removed for now.
* Show only one permissions help window per permissions dialog, not one per tab
* Implemented more Lua functions, see testmodule/demo.lua. Lua plugin now
  registers for plugin commands so they can be used from Lua scripts.
* More/Less button state saved and restored for connect, bookmarks and virtual
  server edit dialogs.
* Plugin filename suffixes are removed for pluginCommand usage. Currently
  removed suffixes are: _win32, _win64, _linux_x86, _linux_amd64, _x86, _amd64,
  _32, _64, _mac, _i386, _ppc
* Added settings dialog to Lua plugin to allow enabling or disabling Lua
  script modules, replacing the old mechanism with the text file in the Lua
  plugin directory.
* "/lua run <function>" now supports running functions from modules using
  "/lua run <module>.<function>". Adjusted testmodule to the new beheaviour.
* Port fields removed from connect and bookmark dialogs. Instead the syntax
  <hostname>:<port> is used.
* Overhauled permissions help widget
* Display in client info frame if a channel group was inherited from an upper
  channel.
* Clients contextmenu offers to set inherited channel groups if applicable on
  current subchannel.
* Overhauled appscanner plugin settings
* Overhauled contextmenus in permissions window
* Adjusted eliding channel names in sort-after dropdown box in channel edit
  dialog
* Overhauled context menus in filetransfer view
* URL Catcher only writes new captured URLs on client quit
* Added tooltip help texts when creating channel spacer
* Allow drag&drop from clients list into client permission lineedit
* Removed now unused callback onVoiceRecordDataEvent from plugin API
* Serverconnectioninfo window remembers position
* Fixed client lag when renaming contacts in huge contact list
* Setup wizard overhauled
- Fixed possible assertion on incoming chats.
- Virtual server weblist checkbox disabled on missing permission on newer
  servers.
- Fixed possible crash in G15 plugin when pressing the "Chan" button while
  disconnected.
- Fixed VolumeControl plugin to close settings dialog when deactivating plugin
  via hotkey.
- Fixed that an unchecked transfer speed limit means unlimited.
- Fixed server tabs not switching playback/capture devices properly when only
  the mode was changed.
- Fixed appscanner plugin handling client data when server was restarted.
- Calling plugin functions requestFileList and requestPermissionOverview no
  longer open the FileBrowser or PermissionOverview dialogs within the client.
  Added returnCode parameter to onFileListEvent and onPermissionOverviewEvent,
  so plugins can also check if the callbacks were caused by an own request.
- "Test Voice" stops as soon as the microphone will be activated
- Fixed subscribe-all freezing the client for several seconds on big servers.
- Playing notifications test sound now uses the TS3 default playback profile
  instead of the system default device and uses the wave file volume modifier.
- Remember selected item in notifications tree when switching sound packs.
- Fixed default settings for contacts manager being saved to wrong config file.
- Fixed disconnect not stopping autoreconnect properly during IP lookup.
- Fixed caught URLs "times mentioned" numeric sorting.
- The whisper history context menu got a few more entries.
- Fixed an offline message issue when a contact changed his nickname while
  typing an offline message.
- Fixed using "one time privilege key" after improving security level when
  connecting to server.
- Fixed that channel chat tab name could be wrong after reconnect.
- Fixed several widget height issues on netbooks.
- Limit amount of remembered client log messages to 500.
- Fixed client log view losing text format when clicking the Clear button.
- Don't open chat tab on double-click for ServerQuery clients.
- Fixed showing Device-Changed-Notification when playback or capture mode has
  been reset to default during sound system convertion.
- Automatically select top group after deleting a server- or channelgroup
- Fixed hotkey when editing/renaming "switch to channel", reported by user in
  forum
- Channel spacer weren't shown in "switch to channel" list.
- Fixed bad apply/discard check on Options Download page, which always reported
  to have changed with an empty config file.
- To resolve issues with some webservers, no longer append ?suid=<server uid>
  to banner URLs.
- Fixed reloading privilege key list after creating invitation.
- Fixed virtualserver edit dialog having "Banner gfx URL" and "URL" fields in
  wrong order.
- Double-click on Grant column in advanced permission tree will add the grant
  permission instead of the normal permission if permission was assigned yet.
- Check matching client unique identifier when opening a contextmenu from chat.
- Fixed playing connected sound after dialog about unfinished filetransfer was
  closed.
- Removed showing "???" when download gets larger than listed. For example,
  when resuming an upload, while another one is downloading.
- Fixed notifications test sounds not playing when playback device was set
  to "Automatically use best mode" and "Default" device.
- Activating capture device of the server tab which previously owned the
  capture device when applying capture options, instead of activating the
  most-right server tab.
- Disable chat tabs when autoreconnecting after server connection was lost.
- Don't disable chat input field anymore when the chat partner is not
  connected to ensure offline messages can be sent and the chat text can
  be still accessed.
- When a client with an active chat tab disconnects and another visible client
  with the same client unique ID is available, reassign the chat tab to the
  other client ID to continue the chat.
- When continuing to chat with the same client UID after reconnecting to
  another server, reusing the existing chat tab.
- Fixed that a filetransfer hangs in waiting status, when file is in use.
- Return key to enter a channel will now ignore autorepeat, so the action
  triggers only once when the key is pressed down.
- Fixed filetransfer context menu "open folder" on queue item.
- Fixed showing "Transfer Completed" as tray message when cancelled.
- Fixed an issue when download contains subfolders
- Don't show the "ID not found" dialog when adding a client to a server- or
  channelgroup fails on insufficient permissions error.
- Adjusted search behaviour for permissions to find both the permission name
  and description, independent of which of them is currently displayed.
- Group sort ID now used in comboboxes in whisper and privilege key dialogs.
- Fixed printMessage plugin function with channel target.
- Couple of filetransfer fixes like: progress sorting, up-/download texts,
  filetransfer view show once...
- Fixed that playback- and capture devices only were checked when connected
- Fixed that context menu on user in channel groups appears twice
- Default font family for chat was shown wrong.
- Fixed displaying ":0" when connecting to IP.
- Fixed possible crash when autoreconnecting on a server which was previously
  connected to using an IP.
- Fixed password parameter when inviting a buddy
- Fixed no more triggering close/reopen capture devices when just changing
  PreProcessorConfigValues like voice activation state, echo cancelling etc.
- Fixed playing sound "file transfer complete" when canceling while using
  bandwidth limiter.
- No custom contextmenu when clicking on Windows titlebar
- Fixed language selection box in application options page
- Fixed showing the creation date of files in file transfer overwrite dialog.
- Added selection page for overlay and volumecontrol plugins to setup wizard,
  added check to open bookmarks/serverlist/Get own server webpage to last
  wizard page.
- Ignore ts3file:// links in URLCatcher
- If the currently used capture profile gets deleted, the default capture
  profile will be set on all connected servers using this profile.
- Fixed display of newly downloaded icons in icon viewer
 
=== Client Release 3.0.0-beta37 - 21 Dec 2010
! Plugin API version increased to 9. Added possibility to use return codes
  with plugins to associate server errors with ts3 function calls from
  individual plugins. See the test plugin for implementation details.
! Soundpack creators take note, the ${clientType} variable now expands to
  "blocked_user" instead of "foe" for consistency reasons.
! The maximum amount of simultaneous tranfers is now 10 (5 upload/5 download).
+ Added function requestInfoUpdate to plugin API to allow plugins to request
  updating the info area of the specified item if this is the currently
  displayed item in the info area.
+ Added option "Enable Detect speech while using Push-To-Talk"
+ Added "Quota" tab to client connection info dialog to display monthly
  filetransfer quota statistics.
+ Added that clients can be added via unique-/database id and dropped from
  server tree or contacts into permissions -> channel groups -> clients.
+ Added "Whisper lists" button to whisper options as alternative way to open
  the whisper lists dialog.
+ Channel descriptions can now be formatted using the BB-Code [LIST] tag. Also
  supported is [LIST=x] where x is one of "1, i, I, a, A".
+ Add search field to servergroups permissions window.
+ Added "Skip" and "SkipAll" for filetransfers
+ Filebrowser shows current available dirs and files
+ Added "Delete client" to contextmenu in "All clients" dialog for deleting
  offline clients directlry from the clients database list.
+ Added dialog with a "Don't show again" checkbox when entering a moderated
  channel to inform the user how to request talk power.
+ Added links to add-ons webpage to multiple places in the client.
+ Hotkeys now have an own config named hotkeys.ini. Existing hotkeys will be
  extracted to the new config file at client startup and only accessed there.
  This makes it easier to share hotkey configurations.
+ All contacs have been extracted to own config named contacts.ini
+ Added a message popup when server update is available but server hasn't been
  updated for at least seven days.
+ Added information dialog when warn-when-muted sound is played for the first
  time telling the user what this sound means and give him a chance to disable
  the feature.
* Changed hotkey to focus channel widget from Shift-Backspace to Alt-Return.
* Permission overview contextmenu item is now dependant on either
  b_client_permissionoverview_own or b_client_permissionoverview_view for own
  client and b_client_permissionoverview_view for other clients.
* Permission overview now shows grant permission in a new column of the
  corresponding permission instead of an own line.
* The search field in the "All clients" dialog now searches directly on the
  server instead of the local results. So no need to hit "More" multiple times
  until all clients are received before searching anymore.
* When uploading/downloading an existing file, the dialog shows filesize and
  file creationdate.
* Permission filter text and state of the granted-only checkbox are now saved
  and restored per permission tab.
* Changed behavior of clicking a ts3server:// link including "addbookmark".
  Now choose between "Do nothing", "Bookmark only" and "Bookmark and Connect".
* New more detailed soundpack entries for server/channelgroup assigned actions.
* Permissions tree now displays group icon and the show-group-name permission
  as icon and text instead of the raw permission value.
* When kicked or banned from the server, only one or neither sound file will
  be played, depending on which notification is activated.
* Behaviour of glance button changed: Now toggles between "Subscribe to all
  channels" and "Subscribe to current and previously subscribed channels"
  option. Current channel subscribe state is saved to disc and restored next
  client restart. If "Subscribe to all channels" is selected, newly created
  channels are automatically subscribed.
* The Hotkey "Bring Client to Front" will no longer minimize a full screen game
- Fixed chat logging when multiple servertabs are trying to log into the
  same logfile.
- When forcing to start a second client with "-nosingleinstance", the second
  instance will log chats to avoid having multiple clients write to the same
  file producing invalid HTML.
- Fixed dropping files to upload on filebrowsers tool buttons. Dropping there
  is not available from the outside like desktop, explorer etc. Inside the
  filebrowser, items can still be dropped to root or the according levels up.
- When adding a user twice to a server group, don't open the buddy-invite
  dialog occuring when a client is unknown on this server.
- Reload server/channelgroups when b_serverinstance_modify_templates or
  b_serverinstance_modify_querygroup have changed.
- Whisper lists in whisper dialog can now be changed using cursor keys.
- Fixed source file being deleted from view when drag&drop operation in
  filebrowser failed.
- Overhauled layout of offline messages dialogs, added Ctrl+N and Ctrl+R
  keyboard shortcuts for "New" and "Reply" actions.
- Fixed filetransfer playing error sound twice if file not found
- Fixed filetransfer request to overwrite/resume/abort files
- Fixed date/time format in filebrowser, urlcatcher, clientdebuglog and
  client log, which wasn't system dependent
- Remove write-only file property before deleting local avatar to avoid the
  "Failed to remove existing local avatar copy" error message.
- Fixed filetransfer progressbar display on windows when using classic theme
- Fixed playing filetransfer complete sound once per download
- Removed option "Only play sound when all of my transfers have been completed"
- Fixed assertion when editing a channel or channelclient permission and
  channels were created, moved or deleted.
- Fix the "warn when talking while muted" function: It should now only occure
  if you have only a mic mute set - and it works with Push-To-Talk now.
- Fixed sorting in filebrowser, alphabetic order wasn't always respected
- Fixed pasting files or folders containg "=" in name from filebrowser
- Fixed crash when transferring files simultaneous
- Fixed starting updater located in a directory with unicode characters
- Fixed resetting filebrowsers window state when refreshing directory
- Fixed filebrowser could throw "database empty result set" when transferring
  recursive and by that end up in a broken/invalid paths.
- Fixed format options were taken over to other tabs.
- Fixed an issue, when clicking invitation but starting TeamSpeak for the
  first time.
- Fixed "Server groups dialog" menuitem in client contextmenu being enabled on
  hotkey even if the client lacks i_group_member_add_power.
- Added Save/Discard/Abort dialog to bookmarks manager when closing the dialog
  while bookmarks are modified.

=== Client Release 3.0.0-beta36 - 08 Nov 2010
+ Added Shift-Backspace keyboard shortcut to focus the channeltree for easier
  screenreader usage. Adjusted spoken accessible names in the mainwindow and
  further improved tab focus behaviour.
+ Activate, Deactivate and Toggle PTT hotkeys have been moved to category 
  Microphone and renamed to "Local Mic Mute" which is now more meanigful
- Fixed whisper reply hotkey which was mixed up when assigned via whisper list
  dialog.
- Fixed missing window title of setup wizard on Linux
- Restored previous chat line input focus behaviour if selecting clients or
  channels in the tree or a chat tab using the mouse. If using keyboard
  navigation, the chat input is not focused to avoid interfering with
  accessibility support.
- Fixed possible crash when permission window was automatically closed on
  server shutdown but dialogs or contextmenus were still open.
- Fixed a bug where VAD cannot be used when Toggle PTT was manually added
- Fixed "Toggle Speaker Mute" und "Toggle Microphone Mute" in setup wizard
- Fixed hotkeys configured in setup wizard not being set properly
- Fixed assertion when adding Hotkey-/Capture- or Playback Profile hotkey
- Adjusted input validator of permissions tree
- Channel commander action can now be added to toolbar
- Sort ID now considered for server groups order in permissions overview.
- Fixed iconpath when IconPack entry is missing in the config file.
- Overhauled volumecontrol plugin.

=== Client Release 3.0.0-beta35 - 27 Oct 2010
* Automatically removing "mailto:" when copying an email address
* Adjusted tab focus behaviour of client main window for easier keyboard
  navigation using a screenreader.
+ Added Shift-Enter keyboard shortcut to focus the chat input line.
- Fixed appscanner no longer crashes the client when apps.ini is broken
- Fixed bbCode autotagging issues when channel description or chat text
  contains bbCode-tag
- Fixed avatar could be set on wrong tab
! beta34 skipped

=== Client Release 3.0.0-beta33 - 25 Oct 2010 (never released in stable branch)
* Added a bookmarks label character limit
+ Because of a hotkey search includes bookmarks and channels, it was rather
  slow on big servers. The search pattern now must have at least 3 characters.
+ Added Hotkey converter extension to fix a possible crash which can be caused
  by invalid or old hotkeys.
- Fixed requesting avatar with 2 connections and same identity
- Fixed Push-To-Talk hotkey in "Test Voice" and also "Delay releasing PTT"
- Fixed disabled sounds when optionspage was closed just with "Cancel"
- Fixed some issues when adding a push-to-talk key manually via hotkey setup
  but still using vad
- Server- and channelgroups can now be sorted by setting the new permission
  i_group_sort_id. If not set or set to zero, the group ID is considered for
  sorting.
- Support for new permission i_group_show_name_in_tree: Set to 1 to display
  the group name before the client name inside the tree. Set to 2 to display
  group name behing client name. Set to 0 to ignore (same as not set).
- Fixed expand/collapse indicator not showing when dragging folders in
  bookmarks manager.
- Fixed possible crash when deactivating the G15 plugin. Updated Logitech SDK
  to version 3.06. Users running Logitech 2.x drivers should update their
  G15 drivers.
- Fixed selecting first group when opening the permissions window

=== Client Release 3.0.0-beta32 - 12 Oct 2010
* Hotkey dialog got an overhaul and available hotkeys are more categorized
* Changed that DEL key, when holding down in treeview is no longer autorepeated
  if deleting a channel or kicking a client
* Respect our min/max size when creating or editing "Change Nickname" hotkey
+ Added that a whisper reply hotkey can be assigned in whisper list dialog
- Fixed some loading issue, when image will be renamed in filebrowser but used
  in channel description
- Fixed moving files from one filebrowser to another, when both are from same
  server and also same channel (means same file), then moving is prevented.
- Fixed showing error message when banned uid was not found by the server
- Fixed push-to-talk hotkey where PTT could be activated though VAD is chosen
- When switching chat tabs while writing a message, all used WYSIWYG textformat
  options will be translated to bbCode
- Fixed a crash when hostmessage dialog was OK-clicked when server tab was
  already closed
- Fixed deactivated buttons when filebrowser folder is empty
- Fixed client icon file not found errors after deleting an icon from offline
  user which will occur when icon is no longer in cache. Requesting the icon is
  now blocked until client reconnects.
- Fixed bbCode URLs in Hostmessage dialog again which was deactivated by work
  on poke dialog context menu
- Fixed possible crash on exit when whisper history widget has been opened.
- Handle "database empty result set" server message when opening the servers
  icon view dialog without any icons available.
- Fixed selecting own client after connecting, which was broken in certain
  circumstances (subscribe all or glance active, but missing subscribe
  permissions).

=== Client Release 3.0.0-beta31 - 27 Sep 2010
* Handle server error when client version is too old for this server by telling
  the user why the connection failed and offer an automatic client update.
* User context menu in poke dialog now opens by clicking mouse left or right
* When opening a filebrowser dialog and its geometry is beyond desktop, it will
  be moved to the upper left corner to not get lost.
+ Added clientquery- sendtextmessage will open chattab when partner not in view
+ Added that complains can be removed with DEL- key and also forced when
  holding SHIFT- key (will suppress the confirmation dialog)
- Fixed "database empty result" when entering empty directory
- Fixed "database empty result" when client-/server group has no permission set
- Fixed opening empty filebrowser
- Fixed two clicks needed to deactivate glancebutton if subscribed to channel
  with clients inside
- Fixed possible broken filetransfer stats at the end when overwriting files
- Fixed that playback- and hotkey profile can't be activated on active tab via
  self menu when tab didn't get activated by mouse click
- Fixed bbCode URLs in Hostmessage dialog, which were not clickable
- Fixed showing an empty complain list when removing fails
- Fixed a minor issue with 'drag & drop' in Bookmarks Manager
- Fixed identities with "Umlauts" which weren't converted correctly
- Fixed "Connection Info" menuitem in "Self" menu being deactivated when online
  and activated when offline. Fixed possible crash when closing client with
  connectioninfo dialogs open.
- Reworked application shutdown mechanism to avoid corrupt configuration files

=== Client Release 3.0.0-beta30 - 21 Sep 2010
+ Support sending and receiving unencrypted voice data. Added options to the
  create/edit channel dialog and to the virtual server edit dialog where this
  behavior can be configured. Only available on server beta29 and higher.
+ Support for ts3server:// on Mac OS X
* Changed keyboard shortcut for webserverlist from Ctr+W to Ctrl+Alt+S, as
  Ctrl+W can collide with the standard window close shortcut.
* Changed the behavior of user context menu in poke dialog
* Permissions tree now includes permissions with grant power only when the
  "Show granted only" checkbox is enabled.
- Fixed edit box for clientname could be larger than predefined
- Fixed possible crash when server stops and permissions window is open.
  Permissions subdialogs (add/delete/copy group) are now non-modal.
- Identities were trimmed on load
- Renaming in treeview will no longer be interrupted when poke dialog or new
  message tab opens
- Connect hotkey now only works if disconnected or previous connection has
  completed to avoid starting multiple connection attempts at the same time.
- Adjusted path to clientquery docs on Mac OS X.
- Fixed logging capture- and playback device name.
- Fixed plugin loading when pathname contains non-standard characters.
- Revertes changed to application path detection in beta29, so starting the
  client from a webbrowser via ts3server:// link works again properly.
- Rename also the existing "ConnectTo" hotkeys when bookmark was renamed
- Fixed offline message cache which could return wrong messages
- Fixed size of host message dialog if it is a short message
- Removed check for i_ft_file_browse_power when opening the filebrowser
  window, as this check is inaccurate as the value for i_ft_needed_file_
  browse_power is unknown to the client.
- Fixed plugin dialog displaying wrong information for unloaded (wrong API
  version etc.) plugins.

=== Client Release 3.0.0-beta29 - 10 Sep 2010
- Fixed opening an empty banlist
- Fixed not writing logs and accessing sounds or plugins when path contains an
  apostrophe
- Fixed selecting channel and server group items in 3D setup with same id

=== Client Release 3.0.0-beta28 - 08 Sep 2010
! The way certain text message characters are escaped was changed, servers
  below beta28 will not be able to correctly display some text messages
! Plugin API version increased to 8
+ Added new plugin called ClientQuery which acts similar to the server query
  functionality, but can only be accessed via localhost (Port 25639). It is
  enabled by default and is useful to add TS3 related information into third
  party applications

+ Added getServerConnectInfo, getChannelConnectInfo, getChannelVariableAsUint64
  and setChannelVariableAsUInt64 functions for plugins, see the test plugin as
  example how to use them.
+ Added ts3plugin_requestAutoload to plugins API to let plugins request to be
  automatically loaded on client start, unless the user has manually disabled
  the plugin.
+ Added "Copy Nickname to clipboard" context menu to "List All Clients" dialog
+ When editing ban entries of another users fail, a messagebox shows that a
  modified copy will be inserted instead
+ Rewrote the updater it now also has a banner as an appreciation to the
  companies that provide bandwidth and servers
* Some minor offline message text-tweaks which makes it more email alike
* Added an improvement to highlight a bookmark item, if nickname has an
  invalid length
* More improvements of server groups priority in 3D setup when a client has
  multiple server groups (particularly add and delete)
* Improved priority of server groups in 3D setup 
* Plugin dialog now displays all plugins which failed to load including an
  error message.
- Fixed playing sound "error" when filetransfer fails instead of "complete"
- Fixed collapsing permissions list when insufficient permission modify power
- Renamed mute microphone keybind for clarity
- Added hotkey "Activate Microphone (current tab)"
- Fixed missing error sound when connection to server fails
- Fixed that self menu could set hardware mute on wrong tab
- Fixed possible crash when reconnecting to a server while permissions dialog
  is still open
- Fixed wrong flickering tray icon after server shutdown
- Fixed sound and description when connection to server failed
- Fixed using master volume when restoring client volume
- Fixed client names with special characters, which could end up in "????"
  in offline message context menu (left-click)
- Fixed wrong icon after server shutdown
- Fixed drop file on a file in same filebrowser caused an empty line
- Fixed deactivate Priority Speaker, which didn't work sometimes
- Fixed visibility of "Offline Message Dialog" when opened via context menu
- Fixed ban list buttons
- Plugins API: Fixed sendPluginCommand function.
- Added client-side check when loading nicknames from bookmarks or last used
  entry of connectdialog to prevent non-printable unicode characters.
- Overhauled chatline cursor backup to restore cursor position on tab change.
- Handle modal-quit message on servers with 0 max slots
- Fixed string issue in whisper dialog when groupname contained html
- Fixed that string "invalid" was out of bounds in capture sound setup dialog
  when combobox had an invalid capture device
- Fixed filebrowser Drag&Drop from channel to channel on a file, we assume
  current path instead of a denied symbol
- Fixed channelinfo template description field didn't use the hole width
- Fixed sending Offline Messages to a disconnected chatpartner via context menu
  could end up in "Premature end of document"
- Fixed some hotkeys did't respect different server tabs
- Text tweak for warn-when-muted
- Fixed parsing ts3server links with Unicode nicknames, channels etc.
- Fixed whisper dialog not displaying the correct server or channel group when
  reopening the dialog.
- Permission check for Create-Subchannel contextmenu adjusted.
- Added "ts3server://host:port" as alternative syntax to
  "ts3server://host?port=<port>". If both are given, "port=<port"> takes
  precedence.
- Fixed always-on-top feature being lost after minimize to tray.
- Fixed autoreconnect after standby to rejoin the previous channel.
- Replace outgoing &nbsp; with whitespace instead of incoming text. Fixed
  replacement using UTF-8 0xC2 0xA0 instead of ASCII 0xA0
- Added workaround to avoid assertion when connecting to server.
- Removed log spam when checking channelcommander icon.
- Fixed UTF-8 conversion error at client start
- Fixed contextmenu operating on wrong table index when sorting the table
- Close bookmark contextmenu when selecting an action
- Plugin printMessage functions did not convert utf-8 strings properly
- Updated permission texts, translation fixes
- Reduced maximum lines to reload chat history to 1000.
- Mac: Fixed problem that lead to jpg and gif images not being displayed
- Fixed collapsing permissions list when insufficient permission modify power
- Fixed crash when using "mute output on all servers"

=== Client Release 3.0.0-beta26 - 10 Aug 2010
- Fixed local unmute when client was muted by plugin.
+ Added "Copy permission name" contextmenu to permission overview.
+ Added tooltip information to each entry in the webserver list.
* Changed default webserver list table, city and create channels columns are by
  default hidden, max clients and current clients joined into one column.
+ Added contextmenu to webserver list table to enable or disable table columns.
- Tab close button never gets focus to avoid accidential closing of server tab.
- Fixed client info HTML templates showing the application scanner line even
  if disabled.
- Fixed grant permissions now being displayed properly in permissions tree.
- Adjusted password and can-create-channels filter in webserver list window to
  make the behaviour more obvious.
  Hide full/empty servers filter and users filter no longer exclusive.

=== Client Release 3.0.0-beta25 - 06 Aug 2010
! Updated plugin API version to 7
+ Plugins can now add a line to the server/channel/client info frame by
  implementing ts3plugin_infoTitle, ts3plugin_infoData, ts3plugin_freeMemory.
  See the test plugin for details how to use this feature. This feature is
  optional, plugins can opt not to implement the new functions.
  Added new field PLUGIN_INFO_DATA to html templates to add the plugin info.
+ Some contact-actions can now be added to customized toolbar:
  Add as Friend, Add as Blocked, Remove from Contacts
- Fixed possible crash on Linux when attempting to load a Qt style.
- Fixed right aligned and centered spacers could have a wrong position when the
  deleted channel had a huge name
- Fixed wrong servergroup positioning-priority in 3D setup 
- Fixed that selected client in 3D setup points to a wrong server group
- Fixed crash when opening options dialog when Application/StatusDisplay config
  setting is missing.
- Offline messages handling for escaped separators and also accept NUM- ENTER
- Fixed another error message when creating an invitation
- Fixed deleting server group in 3D setup
- Tweaked offline messages again to add targets via autocompleter, combobox or
  just writing in. Suggesting new approach - open for discussion. (WIP)
- Easy permissions work-in-progress
- Server tree elide and icon position tweaks 
- Server tree now shows a horizontal scroll bar if necessary
- Fixed opening the whisper list window which could lead to not being able to
  assign a hotkey
- Fixed filename in filebrowser cannot be seen
- Fixed renaming a file in filebrowser and using a huge filename
- Fixed empty filebrowser (detailed view) header now has a fixed size
- Fixed an error message when creating an invitation without having permission
  to open the privilege key list
+ Added hotkey to request Channel Commander
* Overhauled offline messages
  + Removed the receiver list from the offline messages dialog and inserted a
    button to add receivers to new/reply message dialog
  - Fixed display of unread messages
  + Scroll through messages with the up/down arrow keys
* 3D Sound improvements
  - Fixed crash on deleting item when channel- and serverGroupID are the same
  - When entering channel, a still existing uid's properties were overwritten
  - Respecting clients which are whispering 
  - Fixed testsound was only played when item was moved by mouse down on client
    icon, not on client name
  + All known entries for current channel can be shown via context menu (WIP)
  - Fixed apply button didn't always enable when it should
 
=== Client Release 3.0.0-beta23 - 02 Aug 2010
- Fixed critical error when switching into a channel with a serverquery client
  immediately after connecting to the server.
- Updated German translation, several typo fixes
- Closing client with opened and changed 3D setup caused Discard/Cancel/Apply
  which blocks client from quitting.
- Fixed wrong count of unread offline messages
- Fixed typo when exporting identities
- Fixed token generation for server groups when channel groups was previously
  selected.
* Added required plugin API field to plugin dialog.
* Updated server/channel/client info HTML templates
- Fixed Windows not accepting banner URLs with a ":" within.
- Fixed the 3D listener position could be set though 3D was disabled
- Fixed whiper list hotkey rollback deleted too much
- Fixed 3D setup apply button does not always enable on position change
+ Added a warning when exporting identities
- Fixed closing 3D setup Discard/Cancel/Apply could be requested twice
- Inform Mac users about enabling assistive devices, but show only once.
- Fixed channel chat tab doesn't update channelname when channel was changed
- Added search paths "gfx" and "iconpath", usable by HTML templates and style-
  sheets. e.g. "gfx:countries/fr.png or "iconpath:16x16_about.png"
  Iconpath will by dynamically set to the current iconpack path.
- Save and restore last 3D dialog window position
- Do not show whisper history window while a fullscreen application is running.
- Enable and disable 3D sound didn't work properly
- Temporary 3D settings no longer get lost when clicking apply
- Discard/Cancel/Apply when 3D setup has changes and dialog close was requested
- All positions in 3D setup will be resetted when dialog is just closed
* Replaced end of chat history marker as QTextEdit has a problem displaying
  <hr> properly.
- Fixed channel and client chat not reloading properly when connecting to a
  different server on the same tab.
+ Added country display for clients to the info area and optional in the tree.
  Displaying flags in the tree is disabled by default and can be toggled in the
  Designs options page.
- Fixed a bug where 3D ini was cleared completely instead of current server uid
- Positions in 3D setup will also be saved when 3D sound is not enabled
- Fixed enabling 3D caused some sort of lag
- Fixed avatar not reloading properly when connecting twice to the same server.
- Fixed channel description images not updating properly.
+ Added context menu to delete an item at select client in 3D setup
- A couple of 3D setup bugfixes when positioning the items
+ Added "Activate Microphone" to servertab contextmenu.
- Fixed options dialog not opening properly from the invalid playback/capture
  device warning dialog on login or from whisper history window.
+ In 3D setup, the 3D positions of clients can be arranged for server- and
  channel groups or also for channel commanders
- Fixed filetransfer crash when download folder does not exist and the file
  will be transferred to $HomeDir but the file is already there.
! Support for dynamic loading of third-party Lua scripts. Scripts should be
  put into subdirectory of plugins/lua_plugin and must have a file init.lua.
  For details see the example testmodule.
  File custom.lua was moved to testmodule/demo.lua
! Plugin API version increased to 6, added getDirectories() helper function.
- Autosubscribe on login will not overwrite expand channel settings
- Updater now only shows the messagebox warning about still running client when
  starting manually. If starting automatically, silently wait until the client
  has quit.
- Fixed Delete-group shortcut using focus of complete permissions windows.
- Adjusted whisper reply to support multiple whisper reply keys via multiple
  hotkey profiles.
- Fixed whisper replies creating "ghost" profiles in hotkey setup dialog.
- Fixed that channel spacer can cause a client crash 
- Fixed server and channel group menus adding empty menus at the end  
- Connect dialog now accepts empty port fields, in this case the default port
  is used.
- (Un)subscribing channel family will include the parent channel on which the
  action was triggered.
! New mechanism to locate files from within qss files using the "url" command:
  Instead of "styles/<my_style>/<my_file>" use "styles:<my_style>/<my_file>".
  Check default.qss and bluesky.qss as example. This change is required so the
  images are found when starting the client using a non-standard working
  directory.
+ Added "center selected" to setup 3D
- Added optional new channel commander icon displayed as client icon instead of
  replacement lamp. The behaviour can be changed in Options/Design.
- Removed client-side checks for b_virtualserver_servergroup_list and
+ Reply to an offline message has been improved
+ Fixed delete multiple offline messages
- Removed client-side checks for  b_virtualserver_servergroup_list and
  b_virtualserver_channelgroup_list, those permissions were meant for
  ServerQuery usage.
  Menuitem for opening the channelgroups of client dialog now checks
  b_virtualserver_channelgroup_client_list instead.
+ Offline messages new/reply window will save and restore its geometry
+ Offline messages are sorted by date (default)
+ Added options from MainWindow context menu to Option Dialog
- Added notice to chat and client log when own client description was changed.
- Fixed quotes in hotmessage dialog.
- Fixed unread offline messages count could be wrong
- Fixed offline messages reply window didn't open
+ Added 'DEL' key to delete offline messages
+ Offline messages can be marked as read/unread
+ Added server name in title of offline messages window
- Fixed banlist adds nickname into ban after clicking reload
+ Added "Find client in channel tree" to client contextmenu in text chat (only
  available if channel of client is subscribed)
- Fixed offline ban adds nickname
+ Overhaul of the offline messages sorting abilities
+ Added options from ServerStatusWidget to Option Dialog 
- Fixed deleting all identities at once 
- Whisper history widget updates entries when client changed its nickname
- Fixed offline message reply can get sender wrong 
- Fixed receiving whisper not being properly block when sender was added or
  removed from contacts.
- Fixed microphone can't be activated on active tab when capture profile was
  edited 
- Added options dialog to customizable toolbar
- Lua plugin: Removed some unused or non-useful callbacks from ts3events.lua
- Fixed problem when closing the last tab via "X" while "close all but this"
  isn't ready yet. The tabs were no longer able to play sounds.
- Fixed that G15-Plugin affect main-toolbar/taskbar icon 
- Unmute clients when they come into view and were previously muted but
  meanwhile been deleted from contacts.
- Fixed that lua affect main-toolbar/taskbar icon 
- Fixed closing client volume window which did not properly reset to the old
  volume.
- When hovering icons in server tree, the tooltips have to be displayed escaped
* Apply local muted state from contacts list when receiving a whisper
* Attempt to apply volume modifier from contacts list when receiving a whisper,
  however this can currently be only applied when the whispering client is
  visible
- Fixed that collected URLs search filter is case-insensitive
- Fixed collected URLs date sorting
- Fixed host button disappearing when another tabs disconnect/reconnect
- Fixed copy privilege key to clipboard which was limited to key column
- Fixed downloading subfolders via filebrowser where files ended in wrong path
+ Added new default_vista.qss to fix the bookmark manager toolbar buttons hover
  for Windows XP
- Disabled toolbar client actions on ServerQuery clients
- Disable identity security spinbox while improve operation is in progress
- Fixed tab order for offline messages dialogs
- Fixed whisper to Groups will reset to default settings in the whisper list 
+ Added context menu "ban" in client database list viewer 
* -localconfig and -homeconfig commandline parameters now only available on
  Windows.
- Fixed Qt style other than default not loading properly on Linux.
- Properly select new group after adding new server/channel permission group
- Pass UTF-8 strings from and to plugin.
- Depending on the different webbrowsers, a ts3server link could have a "/" 
  behind the host part after crop, which lead to "Unable to resolve ..."
- Fixed invitation link with a channelpass was not build correct 
+ The 'DEL' key can now be used to delete a whisper list
- Fixed that "Away on this server" depends on amount of servers 
- Fixed permission confirm-delete-group-dialog group name
- Fixed another crash when removing a whisper list
- Whisper history window now longer automatically raises, interferred with
  fullscreen games.
- Fixed editing a hotkey could probably crash if action type is "none"
+ When using an invitation, its url will be written to client log (scp request)
- Whisper dialog got a rework and does not longer contain tabs (WIP)
- Fixed a bug in whisper dialog, where comboboxes are not cleared when
  selecting another server
- We now use a slightly different approach to handle file browser drag and
  drop. If some users still can't drag and drop into file browser, a warning
  text will be added to clientlog
- New lines in welcome message from server are now respected by client
- Fixed some typos in whisper dialog
- Fixed showing a previously selected identity when identity changes while
  bookmark manager is still open
- Fixed drawing a spacer as subchannel where its name should be shown as text
- Fixed bad whitespace characters when passing chat messages to plugins
- Don't include template and serverquery groups in client server/channelgroup
  context menu
* Display filename if automatic (icons, images etc.) filetransfer failed
+ Added serverlist to connections menu displaying a list of registered servers
- There was a typo at the special spacers. It has to be -.. instead of --.
  To have them all again: "---,...,-.-,___,-.."
- Removed Mac TTS assert which might fire when exiting the client 
- Close permissions window when disconnecting from server
- Fixed banner reappearing from cache when a banner got deleted and previously
  an interval was defined.
* stop_talking.wav soundfile moved from soundpack to global sounds location
- Fixed duplicate clients in servergroup permissions window
+ Collected URLs now also search for "Mentioned By"
* Added reload button in Privileges Key Manager 
* Changing the nickname in the contacts manager now requires a Return or click
  on the apply button (the green arrow) to apply the changes, to avoid sorting
  the list with every typed character.
* The server/channel groups in "add privileges key" are now sorted
+ Added context menu entry on server/channel groups to create a privilege key
+ Added permission help window  to permissions window to view information about
  the currently selected permission. Also allows searching over all permissions
  name, description and information. Right-click on the search result list
  to find the selected permission in the permissions tree.
* Prevent empty identity name in Identity Manager. Empty identity names would
  force bookmarks to use the default identity.
* An identity which is still connected to a server can no longer be removed
+ Added right-click contextmenu to bookmarks. Behaviour on a bookmark menuitem
  is: Left click = connect, middle click = connect in new tab, right click =
  open contextmenu.
+ If adding a client via permissions to servergroup fails, you will be asked to
  create an invitation.
* Show window close button in Mac setup wizard
* Rewrote ts3server:// parser to handle some special cases like '?', '\' or '&'
  in the link parameters. Note: If you have a '&' or '\' in a channel name,
  it needs to be escaped as '\&' or '\\' or be converted in percent encoding
  like automatically done by the Invite Buddy dialog.
- Fixed a few more translation issues with hotkey setup
* Changed contacts manager sort order: Friends first, then blocked, last
  neutral. Within each type sort alphabetically.
- Added new notification settings for playing sounds while output muted
- Fixed switching sort clients above/below channels options while connected
- Fixed selection issue in contacts manager when editing nicknames, thanks to
  -{HGH}-GEN.Skylab for the report
- Automatically close permission tabs when reconnecting to a server and the
  required permissions are missing
+ Bookmarks now realize change or deletion of identity
+ Added individual (optional) phonetic nickname to contacts, overwriting
  existing clients phonetic nickname.
* Contacts manager UI overhaul
- Close clients list window when the associated servertab gets closed to avoid
  a possible crash.
- Fixed a case when client window won't show up 
- Added invite buddy redirection
- Fixed autoreconnect to current channel instead of default channel if current
  channel was renamed in the meantime
- Fixed self-activating VAD when just switching through the options settings

  while whispering
- Prevent edit channel and create subchannel dialog to be opened for the same
  channel at the same time
- Changed the little whisper indicator from blue to red
- Bookmarks, which autoconnect on startup are now shown bold
- Fixed many fields which were wrong interpreted when containing html
- Previously html- escaped server/channel groups have to be displayed unescaped
- Added limitation for Away Preset Name

=== Client Release 3.0.0-beta22 - 09 Jun 2010
- Server and channel groups in permission dialog are now sorted by group_id.
- Fixed nickname and identityname in statusbar, if both are visible at the same
  time and both contain html-tags.
- Nickname label in connection info will only show plain text
- Fixed Delete shortcut in permission groups list
- Removed ServerQuery group type when adding channel groups
- Strip html-tags from server/channel group names
- Fixed linux drag and drop in whisper dialog
- Check invalid server password error on connect and offer user a dialog to
  enter a new password
- Disable standard codec slider when all codec/quality/latency sliders are
  also disabled
- Support for new channel description view power permissions
- Offline messages do now reply more like e-mails 
- Fixed mirror selection of updater
- Typo and text corrections, updated German translation
- Fixed use of current identity name in statusbar. If an identiy was removed
  but still used inside a bookmark, the old instead of default name was shown.
- Fixed channel edit trying to change codec or latency when those were reduced
  due to permissions.
- Enabled dialog to ask for joining the servers default channel when maximum of
  "max family clients" is reached.
- No longer playing away notification when joining a server as "away".
- Client was able to send an offline message to server.
- Fixed G15 plugin which did not detect connections properly.
- It is no longer possible to paste newlines into server/channel groups.
- The identity name now has the same length limitation as a nickanme.
- Fix bug in filetransfer where after a failed transfer a 0 byte file would
  remain on the receiver end
- Mac: Fix issue that resulted in an outdated version of our updater being
  used
- Linux: start scripts should now handle when they are executed from a 
  different location than in the client installation path
+ When using globally away on a server tab, new clients will join and set their
  status also to away afterwards.
+ Added context menu to copy client uids to clipboard when listing all clients.

=== Client Release 3.0.0-beta21 - 01 Jun 2010
! Due to changes in the voice packet layout you require a server >= beta23 to
  be able to communicate via voice
! Plugins API: Added isReceivedWhisper parameter to onTalkStatusChangeEvent,
  increased plugins api version to 5.
! New whisper list system. Old lists are no longer valid. Please setup whisper
  lists and hotkeys again. Whisper setup was moved from Options to own dialog
  (see Tools menu). Instead of saving into common config file whisper lists
  are now located in seperate file whisper.ini.
  Who is allowed to whisper to you can now be configured in the new Whisper
  options page. Either allow or deny all, or configure indiviual clients via
  contacts manager.
+ Added high latency / low bandwidth codec option. View the new latency factor
  slider to channel create/edit dialog.
+ Added new easy to use codec setup slider. Experts can still configure things
  individually
+ Added option to sort clients above or below channels due to popular demand.
  See "Design" options page for the setting. Default is the new behaviour.
+ Linux: Native Pulse Audio Support is available and will be used in "Use best"
  mode automatically when available.
- Windows Vista and Windows 7 now default to WASAPI when "Use best" is
  selected (Previous default was direct sound)
* The quick access list in whisper dialog now always stays visible.
- Fixed some UTF8 display issues in hotkey setup.
* Banner code overhaul, fixing a possible crash when connecting to multiple
  servers with activated banner.
- Fixed possible crash in hotkey dialog
- Prevent message loop when server restarts and client is outdated.
- Fixed wrong status messages when halt filetransfer.
- Fixed toggle "Push To Talk".
* The searchfield does no longer contain a clear button. 
+ Added singleinstance check to updater
- Fixed wrong tree icon when connecting while talking
- Fixed wrong tab icon initially after connection but before talking
- When adding new serverquery scripts to the library, increment the name in the
  form of "New script", "New script_1", etc.
+ If we detect that a hotkey with the mode "activate" or "deactivate" is about
  to be added, we will provide the opposite key.
* Show custom nicknames of contacts in chatlog when custom nicknames are set to
  use for this contact in the contacts manager.
- Fixed Switch to Server hotkeys
- No whisper with missing talk power
+ Added a log- warning when disconnect from a server with active filetransfer.
- Fixed away button was toggled on the wrong tab.
* Icons in server tree will no longer overlap the server-/channel-/ clientname.
- Fixed chat history when containing a new line (broken formatoptions).
+ Added Invite buddy dialog to autocreate a ts3server or http link to your
  current TeamSpeak 3 server, see Tools menu
* Added channel spacers: Use "[?Spacer#]Text" to add one. Where "?" can
  be an alignment (r = right, c = center, l = left). If "*" is used, all chars
  after the spacer-tag will be repeated until the whole line is filled. Change
  "#" to get an unique channel name, the value doesn't matter.
  Example: [cSpacer0]a centered text, [rSpacer1]a right aligned text. 
  Check also the five special spacer: "---,...,-.-,___,--.".
* Set permissions of secrets config file to 0x600 on Linux and Mac
+ Added icon button to channel edit dialog
* Windows 7 Thai font displayed properly.
- Fixed hotkey setup in setup wizard.
- Permissions overview adjusted for server change: Skip flag now skips channel,
  channelgroup permissions.
* Added the amount of reserved slots in servers info frame
- Fixed a possible crash when disconnect while upload is in progress.
* Replaced "Serverinfo available in X seconds" in info frame with a simple
  "Refresh", which is inactive during the 5 seconds delay.
  Stylesheet authors need to adjust their serverinfo.tpl file:
  SERVER_UPDATE_AVAILABLE_IN_SECS -> SERVER_REFRESH_INACTIVE
  SERVER_UPDATE_AVAILABLE_NOW -> SERVER_REFRESH_ACTIVE
  Use default style serverinfo.tpl as example.
+ Added ping and packetloss to serverconnection info
* When trying to delete unsubscribed channels with clients inside, give user
  option to force delete the channel.
- Fixed Always-on-top option so it works after client restart. You might need
  to enable it once again in the options dialog if you want to use the feature.
- Fixed rare crash when clicking in the chat history.
+ Added reserved slots in virtual server edit.
* New mechanism to check if another instance of the client is already running.
- Fixed more hotkey translation issues
- Fixed disconnect hotkey translation issue
- In Privilege Key Manager, keys can also be copied as an invitation 
- Fixed a few typos (thanks to SgTRWE).
- Showing the server group name inside message box when about to leave.
- Muted icon takes precedence over whisper icon

- Fixed channel/server group submenus not properly checking groups
- Fixed chat history buffer trimming
- Fixed the VAD Slider behaviour
- Added missing tooltip for an enabled master volume widget.
- Changed strings "Token" to "Privilege Key"
- Changed the toggle quick access icon in whisper list dialog.
- Fix filetransfer percentage, which could end up far above 100%
+ Using a token will always show a MessageBox.
- Fixed filebrowser drag&drop files or folder with ] inside.
+ Added whisper icon to display clients currently whispering (thanks to
  DarkCode for the icon)
* Awakening from sleep mode works alot better now but the user has to
  reactivate the capture profile manually. 
- Ignore  "database empty result set" when querying empty client permissions.
- G15 plugin: Fixed clients talking display disappearing from display.
* Updated apps.ini
- The changed icon appears red, when max clients is reached or is 0.
- English text corrections, thanks to ZeroTKA
- Updated TS3 logo image shown in about dialog.
- Fixed empty lines in trayicon tooltip.
* Added contextmenu to channelgroup clients dialog to remove displayed clients.
- Fixed switching hotkey profiles. Activating another hotkey profile is no
  problem at all. Deactivating any profile switches all hotkeys completely off
  and can only be reactivated via context menu!
+ The assigned hotkey profile(s) will now be shown in whisper dialog.
* Changed the directory label in filebrowser so it no longer uses a HTML link.
  Stylesheet authors can now access the label via QLabel#directoryLabel
- Fixed "test voice" lamp.
- Fixed the away button, which didn't show pressed when going globally away,
  using a preset.
- Fixed banlist invoker name wasn't shown when nickname contains an html-tag.
- Fixed Mac button text colors with Aqua style in bookmarks dialog.
- Fixed Mac text formatting in virtual server edit dialog.
- No contextmenu on server update available links
- Bluesky updates and fixes.
- Fixed possible assert in permissions widget when icon viewer is open.
- Hotkey message box "Overlapping hotkey detected..." was shown too often.
- Added minimum header width to some table and tree headers.
- Changed serverinfo update text: Update available -> Serverinfo available.

=== Client Release 3.0.0-beta20 - 13 Apr 2010
- Adjusted default TTS CLIENT_SWITCHED_FROM_CURRENT_CHANNEL_STAYS and
  CLIENT_SWITCHED_FROM_CURRENT_CHANNEL_DISAPPEARS, channelname is the new
  channel, not the old.
* The connection info does no longer scale up an avatar if its size is smaller
  than 80 pixel. Avatars are only scaled down when necessary.
- Stop the server info update timer when disconnecting.
- Fixed percent encoded bookmark label from ts3server:// links.
- Enabled chat contextmenu for serverquery clients again, apparently used by
  people regarding to forum.
* Updated apps.ini
* Translation updates and some minor text adjustments.
- Fixed a case where an existing chat tab wasn't reused, when the disconnected
  chat partner rejoins a just subscribed channel.
- Fixed host button icon URL in Edit Virtual Server disabled when no permission
- Fixed using hotkeys when running as administrator
- Fixed vanishing of "set server/channel groups" context menu, if an entry was
  added or deleted.
+ "Set server/channel group" context menu entries have been separated into
  "More..." sub menus every 15 entries.
* Bluesky update for tree selection and hover
+ Don't play notification sounds when playback device is muted. Behaviour can
  be configured in the Notifications Options page, default enabled.
+ Some contact manager tweaks to have a nicer look with stylesheets.
+ Added contact manager tooltips which shows the complete row.
+ Changing a server group does now look like changing a channel group. To
  change multiple groups, use the dialog (the old way) at the top of the menu.
- Fixed entering channel after renaming and applying with Return or Enter key.
* Added "DEL" key to remove entries in identity manager. 
* Added a default channel chat message when chat was newly created.
- Fixed a case where chattab names could end up empty.
* Inserted checks to detect bad characters in filenames for upload.
- Fixed checkbox in ban editing dialog, to use regular expressions or not.

=== Client Release 3.0.0-beta19 - 31 Mar 2010
- Updater fixes so updating Qt libraries works properly. Wait 2 seconds before
  autostarting update so the client can close first. Updater no longer closes
  when update is finished when it was started from the TS3 client.
- Fixed scrollbar in server icon view.
- Strip whitespaces from port when pasting ip:port into connect dialog.
* Updated apps.ini

=== Client Release 3.0.0-beta18 - 30 Mar 2010
! Qt version updated to 4.6.2. Stylesheets might need to be checked for
  compatibility issues. Translators should update to Linguist from Qt 4.6.2.
  Plugin authors using Qt need to recompile their plugins with Qt 4.6.2.
+ Support for Jaws screen reader. Feedback on this and accessibility support
  in general would be appreciated.
* Use Return or Enter key as shortcut to switch into selected channel (should
  be easier for people using screenreaders)
+ Added support to fetch images from ftp servers. It can be anonymous (if the
  server supports it) and login users as well. Use the ftp- syntax e.g.
  "ftp://your.server/image.png" or "ftp://gfx:gfy@your.server/image.png".
  Be aware that the login part of URLs might is visible if someone opens the
  virtual server edit dialog.  
* Added update countdown in server info on the right
- Fixed message indicator when client rejoins chat
- Fixed overwriting recursive uploads caused crash
- Fixed possible crash when disconnecting from server with banner
- Fixed to poke dialog which would in some situations not be properly updated.
* Added delay to reload/older/newer buttons in serverlog to avoid blocking the
  server with log request spam.
* Renamed User volume modifier dialog restore button
- Fixed downloads from a link which always used the first matching tab. Could
  lead to a dead end when tab had no permission while the actual tab did.
+ Added new hotkey "Disconnect from all servers"
* Added list of all clients on the current server, see Permissions menu.
  Clients can be dragged into the servergroups client list (even if offline).
- Fixed filetransfer asking for password, when downloading from a link.
* Print standard permission error message when failing file rename or delete
* Added new edit field in virtual server dialog to set an URL for the hoster
  button icon. If unset, the default icon is used.
* Changed "Edit Virtual Server" shortcut to Ctrl+Alt+S as the old shortcut
  interfered with entering the Euro sign.
- Updater: Start runscript on Linux when update finished. Make Linux 64-bit
  binary executable after download.
- Fixed crash when running the setup wizard while current servertab has no
  valid capture device.
- Fixed appearance of expiration, when reason is missing in banlist.
- Fixed possible crash when closing the client with multiple servertabs open.
- Fixed that two different PTT activate on same hotkey profile 
- The hotkey combination warning message was cut off when html- tag was used.
+ Showing avarage transfer speed and runtime at the end of transfer.
- Fixed filetransfer speed label flickering
+ Added new download option "Only play sound when all transfers are ready"
+ Ongoing filetransfers can be saved before quit and also resumed after
  reconnect to the server. A messagebox will appear to ask for decision.
- Fix: Clients can now be dropped to servergroup from all server tabs with same
  unique identifier, but no longer from different servers as before.
* Drag&drop clients to servergroups disabled for default groups or when client
  already exists.
* Use Delete key to delete selected permission group or client (depending on
  which widget has focus).
* Automatically select added permission groups for convenience.
- Fixed linebreaks in server hostmessage
- Fixed broken linebreaks in channel description
+ Fixed hotkey "Connect to Server (current tab)". Now it only blocks reconnects
  and no longer connects to other servers on current tab.
+ Filetransfer got many bugfixes and improvements.
* Moved some hardcoded stylesheets out to default.qss. Added default_linux.qss
- Fixed memleak caused by appscanner
* Update visible clients in tree when group icons have changed instead of
  waiting until the tree updates on mouse movement.
* Channel groups per client dialog can now display channel groups of offline
  clients. Added "Display Channel Groups of Client" to Permissions menu in
  addition of the existing client contextmenu (just opening on "empty" client
  instead of the selected one).
* Print some more meaningful message after using a token.
* Updated German translation.
- "Display Channel Groups" action in client contextmenu is disabled when
   b_virtualserver_channelgroup_list is missing.
* Added hostname, IP and port fields to server connectioninfo dialog.
* Added copy buttons to server and client connectioninfo, replacing the old
  somewhat hidden contextmenu.
* Save and restore size of new channelgroup dialogs
* Exported ts3Functions.startVoiceRecording and ts3Functions.stopVoiceRecording
  to plugins. Plugin API version increased to 4, bundled plugins upgraded.
* Upload of remote icons is now queued, so it's possible to upload a whole
  directory of icons in one step.
* Updated default TTS soundpack, adding ${servername} to more entries
- Fixed that an offline ban is no longer bypassed by a simple rename
* Added to plugin SDK: onCustomCaptureDeviceCloseEvent,
  onCustomPlaybackDeviceCloseEvent, onFMODChannelCreatedEvent
* Adjust toolbar buttons on the fly when switching servers or current item.
* Properly handle whitespaces in ts3server channel names, e.g.:
  ts3server://voice.teamspeak.com?&channel=This Is A Channel With Spaces
* Sort servergroups in contextmenu dialog in the same order as in the
  servergroups permissions widget (by ID).
- No more "database empty result set" when listing channelgroups of client but
  the client is not a member of any channelgroup
- Fixed server chat was being blocked by contacts list.
- Fixed accidently broken expand/collapse subchannels in channel contextmenu.
* Overhauled Setup Wizard texts.
- Fixed Umlaut in clientinfo_de.tpl
* Added link to video tutorials webpage in Help menu
* Server icons dialog remembers and restores its size.
- Restore custom server icon on chat tab when switching between servers.
- Fixed client templates after deleting server groups.
* Client checks new PERMISSION_b_client_modify_own_description to allow
  changing the own description only.
- Fixed servergroup dialog items not (de)activating properly when changing a
  group or someone else changed your groups.
* Added "All files" to identity export dialog, enforce .ini suffix for exported
  identities

=== Client Release 3.0.0-beta17 - 09 Mar 2010
* Automatically lay out icons in server icon viewer on resize
+ Added popup menu to icon button of virtual server dialog to remove the icon.
* Close virtual server dialog when disconnecting.
* Bluesky style updates for new UI elements.
- Chat autoscroll fixes when using multiline chat input.
- Fixed logfile management of chat logging.
+ Added overview to display all clients within a channelgroup for each channel,
  see new button and contextmenu in channelgroup permissions window.
+ Added overview to display all channelgroups of a client, see new contextmenu
  entry on client menu (permissions submenu).
* Updated German translation.
* Disable password field in channel edit dialog for default channel
- Update other servertab icons if connection failed (banned, invalid password)
- Disable servergroups client contextmenu if permission is not given
  (b_virtualserver_servergroup_list).
- Fixed bug when unsubscribing a channel manually while glance is active.
- Properly display '&' characters in tab names properly
* Show a more detailed explanation when trying to remove priority speaker via
  contextmenu and the permission was not set as channel client permission. The
  contextmenu can only handle channel client priority speaker permission.
* Disable permissions tree for client and channel-client permissions when no or
  an invalid client is selected.
- DNS lookup failure won't stop autoreconnecting anymore.
+ Use recently implemented remote server icon for bookmarks.
- Fixed reappearing toolbar when window reappears from tray and the toolbar was
  previously disabled.
- Fixed invalid whisper targets with whisperlists.
* Virtual server edit dialog now honors b_virtualserver_modify_icon_id (Icon)
  and b_virtualserver_modify_name (phonetic nickname).
* Overhauled server groups edit dialog.
- Client honors max chat size and won't send messages which exceed length to
  the server anymore.
- Fixed possible crash when closing server groups dialog.
* Replaced the red questionmark "no icon set" icon with a transparent pixmap.
- When playing test sound in options->playback and switching to another
  section, the sound will stop. If changing mode or device during test sound,
  the "apply"-button will immediately play with the new mode/device.
- Fixed possible crash when closing the client after using the test playback
  device button.
- Context menus no longer affect the next current tree item when the item on
  which the menu was opened is deleted.
- Fixed highlighting wrong server tab after moving it.
- Changed that virtual server edit dialog shows an icon instead of icon_id.
- The server groups dialog does now respond to changes on the server groups.
* Hoster button now will only open ftp://, https:// or http:// URLs. When no
  scheme is given, like "teamspeak.com", http:// is always suggested.
+ Added server phonetic nickname for TTS via ${servername} in settings.ini
* Servergroup icons displayed in servergroup edit dialog.
+ Added icons for server, channels and clients. Server icon is set in the
  virtual server edit dialog. Channel and client icons are set by i_icon_id
  in channel/client permissions.
* Updater now starts update automatically when called from client.

=== Client Release 3.0.0-beta16 - 24 Feb 2010
- Don't drag&drop a tree item on itself
+ Server groups will be updated on the fly
* Minimum updates for Server info is now every 5 seconds.
* Allow b_channel_join_ignore_password for server groups and global client
  permissions only, others make no sense.
- Fixed possible endless loop when entering a password-protected channel with
  b_channel_join_ignore_password set on the channel.
- Fixed edit-channel menuitem when calling from chat context menu.
- Removed confirm close server tab option from Applications page
- Fixed the missing context menus for channels in chatlog
+ New context menu to manage the server groups
* For Windows Vista + Win7, also load <stylesheet>_vista.qss if it exists
* Added option to setup delayed PTT and whisperlist release in capture setup
  page (by default enabled, 0.3 seconds delay)
- Fixed possible crash when opening the customize toolbar window.
- Fixed the Priority Speaker action state, reported by user in forum.
+ Client disconnects from all servers when entering System standby state.
  Reconnect on System resume can be disabled via options (Windows only).
- Fixed crash when a client was assigned to a channel group but its icon
  wasn't in the local cache.
- Fixed alternating row colors in default style when switching the skins.
- Fixed that clients can use "<>" in their nicknames again.
+ Added hotkey "Switch to Server"-tab. If multiple server tabs are open, it
  will be tabbed forward through the servers. Without an opened tab, the hotkey
  does nothing.
- Fixed respecting the port in URL for host banner and channel description
  images.
* Hotkey "Connect to: Server (current tab)" will only be executed, when
  current tab is disconnected. So it does no longer reconnect.
- Fixed that the hoster button jumps left, when master volume is hidden.
- Fixed bug enumerating the server groups in client info template.
- The toolbar now is limited to the width of the main window. Otherwise it
  could get very large when customized with many actions and moved outside the
  main window.  
+ Some new values have been added to the templates.
+ Server groups are also shown in client info.
- Fixed 3D test sound, which shouldn't play without moving a client. This
  includes a fix for looping the sound when closing the dialog.
+ The channel description images can be resized via channel info template to a
  predefined maximum (see channelinfo.tpl).
+ The avatar can be resized via client info template (see clientinfo.tpl).
- Fixed reloading hoster banners, when client has multiple connections to a
  server.
- Fixed the away status when switching back to online again.
- Fixed crash when opening the "Create Channel Dialog" via customized toolbar
  and not connected to a server. 
- Fixed "Mute/Unmute" client actions in customized toolbar which do no longer
  toggle each other.
- Fixed "Request Talk power" and also "Cancel Request Talk Power" in customized
  toolbar. They are always enabled but now act as intended.
- Fixed icon "cancel talk request" at own client in server tree.
- Fixed crash when clicking "Expand/Collapse All" via customized toolbar and
  not connected to any server.
- Fixed crash when trying to ban clients via chat context menu and another user
  was faster banning the same client.
+ Added dialog to clear local disk cache. See "Security" options page.
- Another fix to middle-clicking client to open connection info.
- Adjusted detection of email links. URLs with login names no longer take
  precedence over email, except in the form of e.g. "user@www|ftp.foo.de"
- Adding grant permissions to i_group_icon_id will not open the group icon
  dialog anymore.
* Made the group icon window a QDialog so it opens centered on its parent.
- Client makes use of i_group_max_icon_filesize before uploading the icon
- i_client_max_avatar_filesize value of -1 means unlimited file size.
- When adding bookmarks via menu or ts3server link, add the item as last
  instead of after current item (usually 2nd when the bookmarks window was
  closed, which was annoying)
- Handle error if avatar couldn't get deleted on the server.
- Fixed channel phonetic nickname not getting cleared when removing in the 
  channel edit dialog.
* Strip whitespaces from server label and address when adding to bookmarks
* Added unique identifiers to bookmark folders
- Reverted ServerQuery clear-highlight shortcut back to Escape, Backspace key
  did not work properly.

=== Client Release 3.0.0-beta15 - 08 Feb 2010
- Fixed bug when middle-clicking a client opened own connection info after using
  the Self - Connection Info menuitem once.
- Added nickname in ban info when unique id is set. 
- Max ban time will always be inserted in ban dialog when available.
+ Support for remote server/channelgroup icons in addition to the current
  method. Added dialog to manage remote and view local icons (see server
  contextmenu). Server- and channelgroups permission tabs offers the same
  dialog to select icons when editing i_group_icon_id
  IDs < 1000 are considered to be local files from the current gfx
  directory: group_<id>.png. NOTE: This has changed, the old form of
  servergroup/changroup_<id>.png does no longer exist. Instead there is
  one filename form for all icons now.
  IDs >= 1000 are considered to be the IDs of remote icons.
* Updated German translation
- Fixed possible crash when clearing channel passwords
- The poke dialog does no longer get a higher priority than other dialogs.
- Fixed scrolling tree with PageUp/PageDown and ArrowUp/ArrowDown.
- Fixed that master volume slider works across multiple tabs when these tabs
  have the same activated playback profile.
- Fixed a possible filetransfer crash when cancelling the overwrite question
+ Inserted a chat date marker to show the age of the log entries.
- Fixed loosing the drop location marker when dragging a tree item outside of
  the tree widget.

=== Client Release 3.0.0-beta13 - 02 Feb 2010
* Added automatic scroll to tree when dragging items to the top or lower margin
- Fixed context menu for a downloaded directory.
- Fixed a download bug where the actual channel folder wasn't respected.
- When adding integer permissions and grant permissions, first let the user
  input the value and then send it to the server to avoid sending double data.
- Added button to options to reset all "Are you sure...?" confirmations.
- Added confirmation when setting grant permission to zero.
- Don't ask "You are still connected to..." when closing server tab if you
  actually are not connected
+ Added option "Always stay on top" in application settings (Windows only).
- Fixed "Channel maxclient reached" pop up menu doesn't save answer 
- Refilter permissions tree when "show granted only" is enabled and a
  permission is removed.
* No longer check for "config" directory in installation directory when
  deciding the configuration location
* Added server address and port to last-seen information in contacts
- "User requested talk power" sound only played if user is in own channel
- Fixed wrong TTS channelname with connected sound
+ Added customizable toolbar buttons (most icons are still too small. They will
  be updated with a later release.)
* Updated German translation
- Automatically unmute users when they are removed from contacts list
* Added Edit virtualserver menuitem to Self menu
- Closing edit virtualserver dialog with Escape will also trigger the discard/
  apply dialog
- Fixed possible marking the edit virtual server dialog modified after opening
- Fixed typo in hotkey setup, so "Status change - Deactivate" works again. 
* Individually handle permissions to view server/channel group tabs and display
  notification in the permission and client widget if they cannot be viewed.
* Initialize only those permission tabs for which permission was granted to
  avoid invalid permission error spam.
- Removed -enableallactions commandline option.
- Fixed restoring server and channel groups on reconnect when keeping the
  permissions window open.
- Fixed strange behaviour of toggle microphone hotkey in combination with auto-
  activate microphone when switching server tabs.
* Reload chatlog when connecting to a new server in the same tab
* Tweaked autoscrolling after reloading logs
- Fixed creating hotkeys (no keys were accepted / gray box stayed always open)
* Play talk-power-requested sound only if user has permission to grant it
* Changed serverquery clear highlight button shortcut to Backspace, so Escape
  key is available for closing the window again.
+ Escape always closes hotkey dialog, even if hotkey input doesn't work.
* Allow multiple whitespaces in channel description.
+ Added use of server-, channel- and client info templates. Look into
  the folder styles\default for premade templates, which can be modified
  for different styles and languages.
+ Added server address:port in server info.
- Fixed pasting a text into hotkey rename field.

=== Client Release 3.0.0-beta12 - 20 Jan 2010
! Plugin API version changed to 3
! Lua scripts moved to plugins/lua_plugin/ instead of scripts/
* Copyright label in About dialog can no longer be modified by translations.
  Instead translators can use the PLACEHOLDER label in the about dialog. If
  this feature is not wanted, keep "PLACEHOLDER" as text and the label will
  be hidden.
* Added qParentWidget paramter to ts3plugin_configure function. Use this *only*
  when creating QWidgets or QDialogs as parent widget. Cast it to QDialog before
  using. For other UI libraries ignore this parameter and use the first window
  handle parameter instead.
- Fixed pasting multilines in chatedit
+ Added dialog to join default channel, when favorite default channel is full.
* Added new parameter to plugin function ts3Functions.printMessage
* Added new plugin function ts3Functions.printMessageToCurrentTab
- Removed plugin function ts3Functions.getCurrentChatServerConnectionHandlerID
* Updated bundled apps.ini
- Fixed pasting host:port in bookmarks address field (port of bookmark item was
  not updated properly)
* Windows can now be closed with ESC in addition to existing Ctrl+W shortcut
- Fixed a bug where setup wizard doesn't save the mic option correctly 
* Added input field to connect and bookmark dialog for one-time token.
- Displayed elapsed time in improve identity dialog should no longer overflow.
- Fixed a possible freeze when closing the improve identity dialog while an
  identity upgrade is in progress.
- Text tweaks and German translation updates
- Fixed some strings which didn't appear in the translation
- Fixed toggling capture- and playback profiles 
- Hotkeys can be translated
- Fixed possible crash when using "close-all-but-this" on tabs
* Renamed "Password" to "Server password" in connect and bookmark dialogs to
  avoid confusion this might be a user password.
* Reactivated hotkeys "Bring to front" and "Send to back" (Windows only).
- Fixed possible crash on startup with Windows client
- Fixed handling of b_client_skip_channelgroup_permissions in permissions
  overview dialog
- Fixed bug that denied you to create a channel when you did not have
  the permission b_channel_create_with_sortorder and somebody else created
  a channel while you were filling out the create-channel fields

=== Client Release 3.0.0-beta11 - 18 Jan 2010
! A beta11 client is required to connect to beta13 servers
* Handle "host:port" entries in connect and bookmark dialogs. Automatically
  jump into the port field when typing ":".
* Added "Make current channel default" button to bookmarks manager
* Added ability to drag&drop channels into default channel lineedit in
  bookmarks and connect dialog.
- Autounsubscribe now takes effect when being moved or kicked out of a channel,
  not only when switching oneself.
- Fixed opening filebrowser for a passworded channel, after password is
  entered correctly.
- Added hotkey "Master Volume" to turn "up" and "down".
- Deactivated hotkeys "Bring to front" and "Send to back". Because it didn't
  work as intended.
* Use only one plugin API number instead of major/minor. Plugin authors, please
  check the now single ts3plugin_apiVersion() function in the plugin SDK.
* Exported some missing clientlib_rare function to plugins
- Reset use volume when removing user from contacts list
- Reactivated plugins in setup hotkeys
* Warn user when server version mismatches client version

=== Client Release 3.0.0-beta10 - 10 Jan 2010 (never officially released)
* Added new sound notifications when a user (not own client) requested talk
  power and when own client was granted or revoked talk power.
+ Added hotkeys "Bring to front" and "Send to back"
- Filetransfer somtimes crashed on localhost server
- Broken filetransfers in filetransfer manager can be restarted/resumed
+ Filetransfer downloads from other servers are deactivated for now
* Added check if CPU supports SSE instruction set. If not, TeamSpeak will not
  start. This check can be disabled by passing "-nocpucheck" as commandline
  parameter.
* Let user confirm when cancelling Identities dialog when there are changes.
* Added warning when selecting MODALQUIT hostmessage mode in the virtualserver
  edit dialog
- Removed assert thrown when opening options, reported by user on forum
* More verbose output when .wav files failed to play (especially which file
  was not found). Should help soundpack authors.
- Removed double quotes on channel creation
- Fixed displaying images in channel info
- Escape "]" in ts3file links when drag&dropping from filebrowser into chat
* Updated bundled apps.ini
* Removed some fields from info frame on the right
- The chattab close button didn't appear when the tab was closed and a new
  message arrives on this tab.
* Workaround for the occasionally broken horizontal line after reloaded chat
* Bluesky minor fixes
- Fixed crash in Lua plugin when using "/lua run" without function parameter.
- Prevent chatlog from getting double entries
* Added option to disable muting when locking screen. It is enabled by default.
  (Windows only feature)
* Plugin can now decide if it wants the configure option called from a new
  thread or the Qt GUI thread. See the ts3plugin_offersConfigure() function in
  the plugin SDK for details.
- ServerQuery window: If no login data was given in the "Manual" setting in the
  loginname/password input fields, skip login command instead of sending empty
  strings.
- Token Manager now shows the creation time and also the description.
- A token description can be entered, when adding a token.
- Revert to default soundpack if the soundpack from config file does not exist
- Fixed ASSERT thrown when uploading files with drag&drop on Mac OS X.
- Fixed renaming client or channel. The rename box does no longer get smaller
  than the text if some changes occur in server tree.
- Fixed capture URLs
- Fixed use of bb- codes
* G15 plugin now requests server variables once per minute instead once per
  second to reduce traffic.
* Client no longer requests server variables on login but only on-demand to
  reduce traffic.
- When in filebrowser list- mode are just directories, the header label "Size"
  was cut off when its not default (english) language
- Removed double quotes when edited a channel. Inserted client clickable link
  in "renamed" message
+ Added hotkey "grant next talk power"
- Talk Power can also be granted and cancelled by double clicking the request
  talk power icon
* New ts3server:// parameters:
  - "token=<token>": Will send token to server on connection
  - "addbookmark=<Server label>": Requests to add the link to the users
    bookmarks (with confirmation) with the specified server label instead of
	connecting to the server
* Added confirmation dialog when removing clients from servergroups
* Display group name in the group-delete confirmation dialog
- Disable bookmark autoconnect when starting the client via ts3server:// link
- Fixed splitting escaped channel path string
- Ensure connect-to hotkey is executed only once in current serverview
* Updated plugin.h sample code for C++ compilers
- Fixed possible crash when exiting the client while ServerQuery window is open
- Ensure ServerQuery "quit" is sent only once when closing the window
- The chat timestamp section will no longer be wrapped if someone sends a huge
  text without spaces.
- Stripped out more bb- code to avoid the appearance of urls or images
- Removed double escaping of meta data in clients info
+ Clients can also be banned when they are just gone offline. Click clients
  name at disconnected message.
* Limit various client text input dialogs to server-defined max length.
* Trim whitespaces of client and channel nicknames
* Optimized banner animation code. Added workaround for image files with 0 ms
  animation delay to prevent them eating up all CPU cycles.
- Adjusted add-ban dialog taborder
- Fixed glance button not resetting properly when switching server tabs
- Typo fixes, updated German translation
- Fixed Escape key in Mac hotkey dialog, wasn't detected properly to abort the
  hotkey input
- Fixed hotkey input window sometimes not getting the focus on Mac
* Ensure at least the default hotkey profile is loaded when using voice test,
  else the PTT key might not be available for voice test.
- Fixed possible crash with hotkeys when closing server tabs
- Don't request channel description when subscribing channels with clients
  inside
- Don't spam "Error getting channel from channel names in Action-SwitchTo"
  to client protocol when not connected
* Show custom name from contacts manager even if recording. However, both
  custom and nickname are not shown, text would be too long.
* Windows TTS now only uses one channel instead of five simultaneous voices.
* Added sound warnings when users in your channel start/stop recording and when
  you switch into a channel where users are already recording.
* Show special warnings when deleting template server/channel groups.
* Improved chat autoscroll
- Chat does no longer scroll history when a multiline text was pasted and arrow
  up/down was pressed
- Some chat sections grayed out, where they shouldn't
- When opening a text chat, the tab gets immediatly active
- Fixed hotkey for start-/stop recording
+ Added hotkeys to switch to next/previous channel but be aware, if you change
  too frequently, the server will take antispam measures!
- Various tweaks containing the chat - (history, bb- code, html, saving cursor
  positions)
! Plugin API increased to 2.0, all included plugins updated.
* Added more functions to Lua plugin
* Overhauled Token manager dialog
- Fixed missing template groups when reconnecting to server (force reload from
  cache when needed permissions arrived)
- Fixed grayed out channel chat and setting tabname when changing channel
- Fixed formatting of "/help" output in channel chats
* When automatically subscribing all channels on login, don't spam log with
  subscribe message for each channel, just print one line.
+ Improved chat text selection 
- Fixed that a ban entry gets deleted when its editing fails due to permission
- Fixed chat tab order of server and channel 
- Fixed a crash when 3D Sound is still open and TS3 closes with STRG+Q
* Visibility of toolbar and statusbar is now stored in configuration file.
* Contacts window now stores and restores its geometry. The sector of clients
  will also take the largest possible size.
- Fixed bug with request talk power that could lead to no talk power being
  requested even though the user issued the command
- fix "Assertion "m_pChanClients" failed at
  client\clientlib\serverconnectionhandler.cpp:1196" bug

=== Client Release 3.0.0-beta9 - 31 Dec 2009
+ In client context menu, grant and revoke talk power was separated
- Whisper List can now be set up with identical names. The path will also be
  shown in the list to make clear, which channel is used.
- Prevent showing of bb- or html- code in (meta data) info frame
- Fixed a strange chat tab behavior
- ServerQuery or other clients can no longer take over a chattab, when clientID
  of the recently gone chatpartner matches.
- Fixed that users no longer can display local images in chat.

=== Client Release 3.0.0-beta8 - 29 Dec 2009 ===
- Ignoring "file://" which can start local executables.
- Fixed a bug while whispering and reconnecting
- Fixed bug that could lead to the client sending UDP packets with the
  network interface max capacity. Only systems with a instable system clock
  were affected.
- Fixed small memleak
- Fixed invalid detection of racing/flight device equipment
- Sort clients also by is_talker status in tree view

=== Client Release 3.0.0-beta7 - 25 Dec 2009 ===
* In the virtualserver edit dialog, show a warning when selecting a permanent
  server or channel group as default, as this will remove all users from the
  group.
- Fixed bug with empty serverquery tree items
* Support PHP banner URLs like for example:
  http://www.foo.com/image.php?img=bar.png
- Fixed warn-while-muted setting not loading from config on application start
- Disable autoreconnect on invalid password error to avoid ending in an
  infinite reconnect loop
- ServerQuery can no longer take over a chattab, when clientID of the queryclient
  matches the clientID of a recently gone chatpartner. (wip!)
- Fixed bad mirrors.ini

=== Client Release 3.0.0-beta6 - 23 Dec 2009 ===
- Mac: Fixed path to 3d_test.wav
* Client no longer ignores i_client_serverquery_view_power permission.
* TokenManager: Add Token ComboBoxes now preselect the default groups
* Updated German translation
- Prevent enabling VAD/continuous transmission via options dialog when
  force-push-to-talk permission is set
* Dont raise TS3 windows except filebrowser when dragging a file over any
  client window
* VirtualServerEdit: Save and restore window geometry
* Added error message when creating folder failed
- Fixed possible crash in whisperlistmanager when deleting channels which were
  added to a whisperlist
* Permissions filter now case insensitive
- Fixed handling skip flag in permissions overview
* Display "Forced" in skip column of permissions overwhen when skip is enforced
  via b_client_skip_channelgroup_permission
* Permissions filter now case insensitive
- 3d Sound: TestUsers were no longer multiplied when toggling 3d sound
- Channel edit event did not change the channel phonetic name
- Updater: Added timeout for 5 seconds. Otherwise the updater hangs infinite if
  the update server cannot be reached.
- Middle mouse button didn't work with bookmark submenus
- Run disabled check on menus on server tab change
- Fixed crash with invalid client links
- Fixed all serverconnections being lost if you press a hotkey for Connect to
  Server
- BookmarkManager: Fixed IDs and statistics of duplicated entries.

=== Client Release 3.0.0-beta5 - 22 Dec 2009 ===
* Added "Logs" tab to virtualserver edit dialog to configure server logging.
* When update or blacklist server cannot be reached, print info instead of
  warning log.
* Added confirmation dialog when removing grant permissions
- Whisper List: Some tweaks when the last list was removed
- "Activate microphone automatically" didn't work correctly with PTT
- 3D Sound: Prevent multiple "Cannot disband..."- dialogs
- Filetransfer: Downloading a link does no longer crash
- Don't show the permission error message when closing ServerQuery window
* Added "Join Channel of Client" and "Move Client to own Channel" to context
  menu opened on client in chat log.
- Do not show "Failed to open permissions cache file for reading" message when
  cache file does not exist.
* Fixed checks in virtualserver edit dialog bandwidth and quota fields. Range
  is now from -1 to 2^64 - 1. "-1" means maximum value for convenience.
* Added debug output showing config path when it cannot be saved
* Implemented channel phonetic name. See channel edit dialog to set it.
* Added option to disable middle mouse button shortcuts in tree (See
  Applications options page)
* Bluesky update: Fixed toolbar and toolbar close buttons in bluesky_linux.
  Fixed broken labels in channel 3D sound widget.
* Added default_mac.qss and bluesky_mac.qss to overwrite special Mac app bundle
  paths to the styles directory.
* Add win32/win64 to dump filename
* Added missing apps.ini to installer
* Added new setting to select between "Subscribe to all channels" and
  "Subscribe to current and previously subscribed channels". With the first,
  you will subscribe to all channels on login and stay subscribed when you
  switch channels. While you can unsubscribe channels manually, you will
  resubscribe to all channels on next login again. With the second, you will
  subscribe only to the current channel on login plus any channels subscribed
  in a previous connection to this server. Switching channels will unsubscribe
  you, unless it was a "remembered" subscription.
* Now unused Autosubscribe all and Autounsubscribe checkboxes removed from
  Design options page
- When connecting via ts3server:// link, use default identity, capture,
  playback and hotkey profiles
* Nickname length increased to 30 characters
* Limit phonetics nickname length to 30 characters
* Phonetics nickname simplified. Instead of entering the format phonetic
  alphabet name, just enter the desired name itself, e.g. "Peter", "Ralf".
* Typo fix German translation ("Konflicht").
* Changed German translation for "poke" to "anstupsen".
* Removed detailed settings for warn-when-talking-while-muted, option by
  default on
* Check if notifications sound is enabled for warn-when-muted, automatically
  enable and warn user if sound script is missing
* Added checks to warn-when-muted activation: Not away, not headset muted, not
  disconnected
* Check for update only once per day
- Fixed a possible crash that could occure when the capture device was closed
  (for example when changing devices in local test mode)

=== Client Release 3.0.0-beta2 - 20 Dec 2009 ===
- Fixed a problem where the client could not store some passwords correctly,
  the stored version was always trimmed to only a few characters
- When entering hostnames/ips with trailing or leading spaces this could lead
  to the client not being able to connect. We now ignore trailing and leading
  white space.
- Fixed a crash while destructing tts
- Fixed a crash with hoster banner
- Fixed a problem where the "Glance" button could cause a client assertion to
  fail (which terminated your client).
- fixed possible crash with whisperlist
* Renamed sound packs to better (more descriptive) names
* Replaced the previous default sound pack with a less verbose version
- Play stop talking wav, even in TTS profile 
- Bandwidth limit when edited in virtual server edit dialog now accepts bigger
  values
- Fixed a crash that could occure on connect when connecting with a hostname
  instead of by IP
- Mute headphones now also stops you from sending, since this what casual users
  expect. The functionality to mute only your headphones and still be able to
  transmit will return in a future build.

=== Client Release 3.0.0-beta1 - 19 Dec 2009 ===
* Initial beta release

