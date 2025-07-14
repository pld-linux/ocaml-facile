#
# Conditional build:
%bcond_without	ocaml_opt	# native optimized binaries (bytecode is always built)

# not yet available on x32 (ocaml 4.02.1), update when upstream will support it
%ifnarch %{ix86} %{x8664} %{arm} aarch64 ppc sparc sparcv9
%undefine	with_ocaml_opt
%endif

Summary:	Functional Constraint Library implemented in Objective Caml
Summary(pl.UTF-8):	Biblioteka ograniczeń funkcyjnych dla OCamla
Name:		ocaml-facile
Version:	1.1.3
Release:	4
License:	LGPL v2.1+
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
language.

%description -l pl.UTF-8
FaCiLe to biblioteka programowania ograniczeń na liczbach całkowitych
i skończonych zbiorach liczb całkowitych. Funkcjonalność obejmuje
tworzenie i operowanie na zmiennych skończonych, wyrażenia i stałe
arytmetyczne (także nieliniowe), wbudowane ograniczenia (różnica,
liczność, sortowanie itp.) oraz szukanie i optymalizację celu. FaCiLe
pozwala także łatwo tworzyć zdefiniowane przez użytkownika
ograniczenia i cele (w tym rekurencyjne), wszędzie wykorzystując
ocamlowe funkcje wyższego rzędu, aby udostępnić użytkownikowi
prosty i elastyczny interfejs. Jako że FaCiLe jest biblioteką dla
OCamla, a nie innego języka, użytkownik korzysta z wywodzenia typów i
silnego typowania, wysokopoziomowej abstrakcji, systemu modułów i
obiektów, a także wydajności kompilowania do kodu natywnego,
odśmiecania i debuggera - wszystkich cehc OCamla, które pozwalają
szybko prototypować i eksperymentować: modelowanie, przetwarzanie
danych i interfejs są zaimplementowane w tym samym potężnym i wydajnym
języku.

%package devel
Summary:	Functional Constraint Library implemented in Objective Caml - development part
Summary(pl.UTF-8):	Biblioteka ograniczeń funkcyjnych dla OCamla - część programistyczna
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%requires_eq	ocaml

%description devel
This package contains files needed to develop OCaml programs using
FaCiLe library.

%description devel -l pl.UTF-8
Pakiet ten zawiera pliki niezbędne do tworzenia programów w OCamlu
używających biblioteki FaCiLe.

%prep
%setup -q -n facile-%{version}
%patch -P0 -p1

%build
# not autoconf configure
./configure

%{__make} -C src all %{?with_ocaml_opt:opt} \
	CC="%{__cc} %{rpmcflags} -fPIC"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/facile

cp -p src/facile.cmi src/facile.cma $RPM_BUILD_ROOT%{_libdir}/ocaml/facile
%if %{with ocaml_opt}
cp -p src/facile.cmxa src/facile.a $RPM_BUILD_ROOT%{_libdir}/ocaml/facile
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE README
%dir %{_libdir}/ocaml/facile
%{_libdir}/ocaml/facile/*.cma

%files devel
%defattr(644,root,root,755)
%{_libdir}/ocaml/facile/*.cmi
%if %{with ocaml_opt}
%{_libdir}/ocaml/facile/*.a
%{_libdir}/ocaml/facile/*.cmxa
%endif
