Name:          AFLplusplus
Version:       3.15a
Release:       1

Summary:       Practical, instrumentation-driven fuzzer for binary formats

License:       ASL 2.0

URL:           https://github.com/AFLplusplus/AFLplusplus
Source0:    %{name}-%{version}.tar.bz2

# For running the tests:
Source1:       hello.c

BuildRequires: clang
BuildRequires: llvm-devel gmp-devel
BuildRequires: gcc gcc-plugin-devel make


%global afl_helper_path %{_libdir}/afl


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


%package fuzz
Summary:       Fuzzer and and auxiliary utilities for %{name}

%description fuzz
This subpackage contains fuzzer and and auxiliary utilities for %{name}.

%package docs
Summary:       Documentation, dictionaries and testcases for %{name}

%description docs
This subpackage contains documentation, dictionaries and testcases for %{name}.


%prep
%setup -q -n %{name}-%{version}/upstream


%build
CFLAGS="%{optflags}" \
AFL_NO_X86=1 \
%{__make} %{?_smp_mflags} \
  PREFIX="%{_prefix}" \
  HELPER_PATH="%{afl_helper_path}" \
  source-only

%install
AFL_NO_X86=1 \
  PREFIX="%{_prefix}" make install \
  HELPER_PATH="%{afl_helper_path}" \
  DESTDIR="$RPM_BUILD_ROOT"

%check
# This just checks that simple programs can be compiled using
# the compiler wrappers.

ln -sf %{SOURCE1} hello.cpp
./afl-gcc-fast %{SOURCE1} -o hello
./hello
./afl-g++-fast hello.cpp -o hello
./hello
./afl-cc %{SOURCE1} -o hello
./hello

%files fuzz
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

%dir %{afl_helper_path}
%{afl_helper_path}/*

%files docs
%doc docs/*
%doc dictionaries/
%doc testcases/

%changelog
