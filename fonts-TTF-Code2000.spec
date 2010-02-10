# NOTE
# according to license we *can* store the .ZIP in distfiles in
# unaltered form, while can't distribute resulting rpm.
#
# Conditional build:
%bcond_with	license_agreement	# generates package
#
%define		base_name	fonts-TTF-Code2000
Summary:	Code2000 Unicode TrueType font
Summary(pl.UTF-8):	Unikodowy font TrueType Code2000
%if %{with license_agreement}
Name:		%{base_name}
%else
Name:		%{base_name}-installer
%endif
%define		_rel	1
Version:	1.171
Release:	%{_rel}%{?with_license_agreement:wla}
License:	Shareware, fee required
Group:		Fonts
%if %{with license_agreement}
Source0:	http://code2000.net/CODE2000.ZIP
# Source0-md5:	1fa4e4b61d7ac0980b038e9260667a77
%else
# Source10 extracted from Source0
Source10:	CODE2000.HTM
Source11:       http://svn.pld-linux.org/svn/license-installer/license-installer.sh
# Source11-md5: 4fb1600353dd57fe088e0b12fb0ecac2
%endif
URL:		http://code2000.net/code2000_page.htm
%if %{with license_agreement}
BuildRequires:	unzip
Requires(post,postun):	fontpostinst
Requires:	%{_fontsdir}/TTF
Requires:	fontpostinst
%else
Requires:	unzip
Requires:	mktemp > 1.5-18
Requires:	rpm-build-tools
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		ttffontsdir	%{_fontsdir}/TTF

%description
Code2000 is a shareware font. It is a Unicode-based font, as are many
modern computer fonts. Code2000 is one of the larger fonts available
and the latest build has over 60000 glyphs.

It relies on font-smoothing (anti-aliasing) for screen display, it
does not contain hinting instructions.

%prep
%if %{with license_agreement}
%setup -q -c
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if !%{with license_agreement}
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/%{base_name}}

sed -e '
	s/@BASE_NAME@/%{base_name}/g
	s/@TARGET_CPU@/%{_target_cpu}/g
	s-@VERSION@-%{version}-g
	s-@RELEASE@-%{release}-g
	s,@SPECFILE@,%{_datadir}/%{base_name}/%{base_name}.spec,g
' %{SOURCE11} > $RPM_BUILD_ROOT%{_bindir}/%{base_name}.install

install %{_specdir}/%{base_name}.spec $RPM_BUILD_ROOT%{_datadir}/%{base_name}
install %{SOURCE10} $RPM_BUILD_ROOT%{_datadir}/%{base_name}

%else
install -d $RPM_BUILD_ROOT%{ttffontsdir}
install *.TTF $RPM_BUILD_ROOT%{ttffontsdir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with license_agreement}
%post
fontpostinst TTF

%postun
fontpostinst TTF

%else
%post
%{_bindir}/%{base_name}.install

echo "
License issues made us not to include inherent files into
this package by default. If you accept the conditions specified
by the font Author in:
%{_datadir}/%{base_name}/CODE2000.HTM
and want to install a real font, then rebuild the package with the
following command:

%{_bindir}/%{base_name}.install --with license_agreement %{_datadir}/%{base_name}/%{base_name}.spec
"
%endif

%files
%defattr(644,root,root,755)
%if %{with license_agreement}
%doc *.HTM
%{ttffontsdir}/*
%else
%attr(755,root,root) %{_bindir}/%{base_name}.install
%{_datadir}/%{base_name}
%endif
