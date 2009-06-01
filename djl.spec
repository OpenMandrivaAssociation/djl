Name:       djl
Version:    1.2.14
Release:    %mkrel 1
Summary:    A game manager inspired by Steam from Valve software
License:    GPLv3+
Group:      Games/Other
URL:        http://djl-linux.org/
Source0:    http://en.djl-linux.org/maj_djl/archives/%{name}-%{version}.tar.gz
Patch0:	    djl-1.2.11-path.patch
Patch1:	    djl-1.2.12-hide-add-menu-entry-button.patch
BuildRequires:	imagemagick
Requires:   python-qt4 >= 4
Requires:   python >= 2.5, python < 3
BuildArch:  noarch
BuildRoot:  %{_tmppath}/%{name}-%{version}

%description
djl is an open-source (GPL licensed) game manager written in Python for the
GNU/Linux Operating System, inspired by Valve's Steam software for Windows.

It makes it possible to download, install (via a repository) and remove a 
large number of games placed in a subdirectory in an absolutely invisible
way (but without dealing with any dependencies).
It can also execute .desktop shortcuts located in another directory (this way,
it's possible to launch games which were already installed).

Several games are available in the repository. Anyone can submit new games to 
developers via a web page (http://djl.jeuxlinux.fr/djl_addgame_en.php).

%prep
%setup -q -n %name
%patch0 -p0 -b .path
%patch1 -p0 -b .no-add-desktop-file-button
rm djl/.eric4project/ -Rf
rm -f djl/libs/test_ws.py #unneeded
mv djl/Journal_en.txt djl/Journal.txt .
chmod a-x COPYING
chmod a-x Journal_en.txt
chmod a-x Journal.txt

%build

%install
rm -rf %{buildroot}
install -d -m 755 %{buildroot}%{_gamesdatadir}/djl
cp -pr djl/* %{buildroot}%{_gamesdatadir}/djl
install -d -m 755 %{buildroot}%{_gamesbindir}
install -m 755 djl.sh %{buildroot}%{_gamesbindir}/djl

mkdir -p %{buildroot}%{_liconsdir}
mkdir -p %{buildroot}%{_iconsdir}
mkdir -p %{buildroot}%{_miconsdir}
convert -resize 48x48 djl/icone.png %{buildroot}%{_liconsdir}/%{name}.png
convert -resize 32x32 djl/icone.png %{buildroot}%{_iconsdir}/%{name}.png
convert -resize 16x16 djl/icone.png %{buildroot}%{_miconsdir}/%{name}.png

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=DJL
Comment=Game manager with lots of games available
Exec=%{_gamesbindir}/djl
Icon=%{name}
Terminal=false
Type=Application
Categories=Game;
EOF

%find_lang %{name}

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post
%update_menus
%endif

%if %mdkversion < 200900
%postun
%update_menus
%endif

%files -f %{name}.lang
%defattr(-,root,root)
%doc COPYING LIESMICH LISEZMOI README Journal.txt Journal_en.txt
%{_gamesbindir}/djl
%{_gamesdatadir}/djl
%{_datadir}/applications/mandriva-%{name}.desktop 
%{_iconsdir}/*
