%global projectUrl https://github.com/simulationcraft/simc
%global version %(echo "$(date +%Y%m%d)")
%global arch %(test $(rpm -E%?_arch) = x86_64 && echo "x64" || echo "ia32")
%global srcdir %{_builddir}/simulationcraft-gui
%global srcbuilddir %{srcdir}/build
%global outputDir %{_builddir}/simulationcraft-gui-%{version}-out

Name:    simulationcraft-gui
Version: %{version}
Release: 1%{dist}
Summary: SimulationCraft is a tool to explore combat mechanics in the popular MMO RPG World of Warcraft (tm).

Group:   Amusements/Games/Tools
License: GPLv3
URL:     %{projectUrl}

Patch0: gui-sc-to-install.patch

BuildRequires: git
BuildRequires: cmake
BuildRequires: qt-devel
BuildRequires: qt5-qtbase-devel
BuildRequires: libcurl-devel
BuildRequires: pkgconfig

Requires: libcurl
Requires: simulationcraft-cli
Requires: qt5-qtwebengine-devel

%description
It is a multi-player event driven simulator written in C++ that models player character damage-per-second in various raiding and dungeon scenarios.

%prep
# Clone the sources
if ! [ -d %{srcdir}/.git ]; then
  git clone --depth 1 %{url}.git %{srcdir}
fi
pushd %{srcdir}
  # Delete a possible previous build dir
  if [ -d "%{srcbuilddir}" ]; then
    rm -rf build
  fi

  # Reset the git status
  git reset --hard
  git fetch --all

  # Apply patches
  patch -p1 -i %{P:0}
popd

%build
export CFLAGS="%{optflags}"
export CXXFLAGS="%{optflags}"
export PREFIX="/usr"

mkdir -p %{srcbuilddir}
pushd %{srcbuilddir}
  cmake ../ -DCMAKE_BUILD_TYPE=Release -DSC_TO_INSTALL=1
  make -j$(cat /proc/cpuinfo|grep processor|wc -l)
popd

%install
# Variables
outBinDir="%{buildroot}%{_bindir}"
outAppsDir="%{buildroot}%{_datarootdir}/applications"
outShareDir="%{buildroot}%{_datarootdir}/SimulationCraft/SimulationCraft"

execFiles="qt/SimulationCraft"
guiFiles="Welcome.html Welcome.png"

# Create output dirs
install -v -d -m 0755 "${outBinDir}"
install -v -d -m 0755 "${outAppsDir}"
install -v -d -m 0755 "${outShareDir}"

# Exec files
for execFile in $execFiles ; do
	install -v -m 0755 "%{srcbuilddir}/$execFile" "${outBinDir}"
done

# GUI files
for guiFile in $guiFiles ; do
  install -v -m 644 "%{srcbuilddir}/qt/${guiFile}" "${outShareDir}/${guiFile}"
done

# Desktop file
install -v -m 644 "%{_sourcedir}/SimulationCraft.desktop" "${outAppsDir}/SimulationCraft.desktop"

# Icon file
install -v -m 644 "%{srcdir}/qt/icon/SimulationCraft.xpm" "${outShareDir}/SimulationCraft.xpm"

find $RPM_BUILD_ROOT -not -type d -printf "%%%attr(%%m,root,root) %%p\n" | sed -e "s|$RPM_BUILD_ROOT||g" > %{_tmppath}/%{name}_contents.txt

%files -f %{_tmppath}/%{name}_contents.txt
