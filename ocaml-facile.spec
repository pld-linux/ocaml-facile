#
# Conditional build:
%bcond_without	ocaml_opt	# skip building native optimized binaries (bytecode is always built)

# not yet available on x32 (ocaml 4.02.1), update when upstream will support it
%ifnarch %{ix86} %{x8664} arm aarch64 ppc sparc sparcv9
%undefine	with_ocaml_opt
%endif

Summary:	Functional Constraint Library implemented in Objective Caml
Name:		ocaml-facile
Version:	1.1.3
Release:	3
License:	LGPL
Group:		Libraries
Source0:	http://opti.recherche.enac.fr/facile/distrib/facile-%{version}.tar.gz
# Source0-md5:	172c4fbea636a8fa575b988390639d8d
Patch0:		opt.patch
URL:		http://www.recherche.enac.fr/opti/facile/
BuildRequires:	ocaml >= 3.02
%requires_eq	ocaml-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		debug_package	%{nil}
%if %{without ocaml_opt}
%define		no_install_post_strip	1
# no opt means no native binary, stripping bytecode breaks such programs
%define		_enable_debug_packages	0
%endif

%description
FaCiLe is a constraint programming library on integer and integer set
finite domains written in OCaml. It offers all usual facilities to
create and manipulate finite domain variables, arithmetic expressions
and constraints (possibly non-linear), built-in global constraints
(difference, cardinality, sorting etc.) and search and optimization
goals. FaCiLe allows as well to build easily user-defined constraints
and goals (including recursive ones), making pervasive use of OCaml
higher-order functionals to provide a simple and flexible interface
for the user. As FaCiLe is an OCaml library and not "yet another
language", the user benefits from type inference and strong typing
discipline, high level of abstraction, modules and objects system, as
well as native code compilation efficiency, garbage collection and
replay debugger, all features of OCaml (among many others) that allow
to prototype and experiment quickly: modeling, data processing and
interface are implemented with the same powerful and efficient
language. For a more complete description, you may consult the preface
and foreword of the online documentation

%prep
%setup -q -n facile-%{version}
%patch0 -p1

%build
# use ./configure because of 'Unknown option "LDFLAGS=-Wl,--as-needed -Wl,-z,relro -Wl,-z,-combreloc "
./configure

%{__make} -C src all %{?with_ocaml_opt:opt} \
	CC="%{__cc} %{rpmcflags} -fPIC"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/facile

install src/facile.cmi src/facile.cma $RPM_BUILD_ROOT%{_libdir}/ocaml/facile
%if %{with ocaml_opt}
install src/facile.cmxa src/facile.a $RPM_BUILD_ROOT%{_libdir}/ocaml/facile
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE README
%dir %{_libdir}/ocaml/facile
%{_libdir}/ocaml/facile/*.cma
%{_libdir}/ocaml/facile/*.cmi
%if %{with ocaml_opt}
%{_libdir}/ocaml/facile/*.a
%{_libdir}/ocaml/facile/*.cmxa
%endif
