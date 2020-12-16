%global version %(echo "$(git rev-parse --short HEAD)")
%global arch %(test $(rpm -E%?_arch) = x86_64 && echo "x64" || echo "ia32")
%global srcdir %{_builddir}/simulationcraft-cli-%{version}
%global outputDir %{_builddir}/simulationcraft-cli-%{version}-out

Name:    simulationcraft-cli
Version: %{version}
Release: 1%{dist}
Summary: SimulationCraft is a tool to explore combat mechanics in the popular MMO RPG World of Warcraft (tm).

Group:   Amusements/Games/Tools
License: GPLv3
URL:     https://github.com/simulationcraft/simc

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
  git clone %{url}.git %{srcdir}
fi
pushd %{srcdir}
# Reset the git status
  git reset --hard
  git fetch --all
  git pull
popd

%build
export CFLAGS="%{optflags}"
export CXXFLAGS="%{optflags}"

mkdir -p %{srcdir}/build
pushd %{srcdir}/build
  cmake ../ -DCMAKE_BUILD_TYPE=Release -DBUILD_GUI=OFF
  make -j$(cat /proc/cpuinfo|grep processor|wc -l)
popd
