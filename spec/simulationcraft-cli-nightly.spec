%global projectUrl https://github.com/simulationcraft/simc
%global version %(echo "$(date +%Y-%m-%d)")
%global arch %(test $(rpm -E%?_arch) = x86_64 && echo "x64" || echo "ia32")
%global srcdir %{_builddir}/simulationcraft-cli
%global srcbuilddir %{srcdir}/build
%global outputDir %{_builddir}/simulationcraft-cli-%{version}-out

Name:    simulationcraft-cli
Version: %{version}
Release: 1%{dist}
Summary: SimulationCraft is a tool to explore combat mechanics in the popular MMO RPG World of Warcraft (tm).

Group:   Amusements/Games/Tools
License: GPLv3
URL:     %{projectUrl}

BuildRequires: git
BuildRequires: cmake
BuildRequires: libcurl-devel
BuildRequires: pkgconfig

Requires: libcurl

%description
It is a multi-player event driven simulator written in C++ that models player character damage-per-second in various raiding and dungeon scenarios.

%prep
# Clone the sources
if ! [ -d %{srcdir}/.git ]; then
  git clone -depth 1 %{url}.git %{srcdir}
fi
pushd %{srcdir}
# Delete a possible previous build dir
# if [ -d "%{srcbuilddir}" ]; then
#   rm -rf build
# fi
# Reset the git status
  git reset --hard
  git fetch --all
popd

%build
export CFLAGS="%{optflags}"
export CXXFLAGS="%{optflags}"

mkdir -p %{srcbuilddir}
pushd %{srcbuilddir}
  cmake ../ -DCMAKE_BUILD_TYPE=Release -DBUILD_GUI=OFF
  make -j$(cat /proc/cpuinfo|grep processor|wc -l)
popd

%install
# Variables
outBinDir="%{buildroot}%{_bindir}"
outShareDir="%{buildroot}%{_datarootdir}/simulationcraft-cli"
outShareProfilesDir="${outShareDir}/profiles"
outShareDocsDir="${outShareDir}/docs"

execFiles="simc"
profileDirs=$(cd "%{srcdir}/profiles" && find . -type d | sed -s 's/\.\///' | grep -v "\.")
profileFiles=$(cd "%{srcdir}/profiles" && find . -type f | sed -s 's/\.\///')

# Create output dirs
install -v -d -m 0755 "${outBinDir}"
install -v -d -m 0755 "${outShareDir}"
install -v -d -m 0755 "${outShareProfilesDir}"
install -v -d -m 0755 "${outShareDocsDir}"

install -v -d -m 0755 "${outShareProfilesDir}"
for profileDir in $profileDirs ; do
	install -v -d -m 0755 "${outShareProfilesDir}/$profileDir"
done

# Exec files
for execFile in $execFiles ; do
	install -v -m 0755 "%{srcbuilddir}/$execFile" "${outBinDir}"
done

# Profile files
for profileFile in $profileFiles ; do
	install -v -m 644 "%{srcdir}/profiles/${profileFile}" "${outShareProfilesDir}/${profileFile}"
done

# Doc files
install -v -m 644 "%{srcdir}/LICENSE" "${outShareDocsDir}/LICENSE"
install -v -m 644 "%{srcdir}/README.md" "${outShareDocsDir}/README.md"

find $RPM_BUILD_ROOT -not -type d -printf "%%%attr(%%m,root,root) %%p\n" | sed -e "s|$RPM_BUILD_ROOT||g" > %{_tmppath}/%{name}_contents.txt

%files -f %{_tmppath}/%{name}_contents.txt
