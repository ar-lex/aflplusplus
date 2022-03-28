%global afl_helper_path %{_libdir}/afl
#Because option -fstack-clash-protection was added in clang11.
%global optflags %(echo %{optflags} | sed -e "s|-fstack-clash-protection||g")

Name:          aflplusplus
Summary:       Practical, instrumentation-driven fuzzer for binary formats
Version:       4.00c
Release:       1
License:       ASL 2.0
URL:           https://github.com/AFLplusplus/AFLplusplus
Source0:       %{name}-%{version}.tar.bz2
Patch1:        0001-Fix-sed-args.patch
Provides:      %{name}-fuzz = %{version}-%{release}

BuildRequires: clang
BuildRequires: llvm-devel
BuildRequires: gmp-devel
BuildRequires: gcc
BuildRequires: gcc-plugin-devel
BuildRequires: make
BuildRequires: gnu-sed
BuildRequires: python3-devel
BuildRequires: zlib-devel

%description
American fuzzy lop uses a novel type of compile-time instrumentation
and genetic algorithms to automatically discover clean, interesting
test cases that trigger new internal states in the targeted
binary. This substantially improves the functional coverage for the
fuzzed code. The compact synthesized corpuses produced by the tool are
also useful for seeding other, more labor- or resource-intensive
testing regimes down the road.

Compared to other instrumented fuzzers, afl-fuzz is designed to be
practical: it has a modest performance overhead, uses a variety of
highly effective fuzzing strategies, requires essentially no
configuration, and seamlessly handles complex, real-world use cases -
say, common image parsing or file compression libraries.


%package compillers
Summary:       Clang and gcc support for %{name}
Requires:      clang
Requires:      gcc gcc-plugin-devel


%description compillers
This subpackage contains clang and gcc support for
%{name}.

The code in this package allows you to instrument programs for AFL using
true compiler-level instrumentation, instead of the more crude
assembly-level rewriting approach taken by afl-gcc and afl-clang.

%package tests
Summary:       Testcases for ${name}

%description tests
This subpackage contains testcases for %{name}.

%prep
%autosetup -p1 -n %{name}-%{version}/upstream

%build
%make_build \
  AFL_NO_X86=1 \
  PREFIX="%{_prefix}" \
  HELPER_PATH="%{afl_helper_path}" \
  source-only

%install
export AFL_NO_X86=1
export PREFIX="%{_prefix}"
export HELPER_PATH="%{afl_helper_path}"
%make_install
rm -rf %{_docdir}/afl
rm -rf %{_mandir}/man8



%files
%{_bindir}/afl-analyze
%{_bindir}/afl-fuzz
%{_bindir}/afl-plot
%{_bindir}/afl-showmap
%{_bindir}/afl-tmin
%{_bindir}/afl-cmin*
%{_bindir}/afl-gotcpu
%{_bindir}/afl-whatsup
%{_bindir}/afl-persistent-config
%{_bindir}/afl-system-config
%{_datadir}/afl/dictionaries/*

%files compillers
%{_bindir}/afl-c++
%{_bindir}/afl-cc
%{_bindir}/afl-clang
%{_bindir}/afl-clang++
%{_bindir}/afl-clang-fast
%{_bindir}/afl-clang-fast++
%{_bindir}/afl-g++
%{_bindir}/afl-gcc
%{_bindir}/afl-gcc-fast
%{_bindir}/afl-g++-fast
%{afl_helper_path}

%files tests
%{_datadir}/afl/testcases
