Name:       perl-URI
Summary:    A Perl module implementing URI parsing and manipulation
Version:    1.54
Release:    1
Group:      Development/Libraries
License:    GPL+ or Artistic
BuildArch:  noarch
URL:        http://search.cpan.org/dist/URI/
Source0:    %{name}-%{version}.tar.bz2
Requires:   perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildRequires:  perl(MIME::Base64)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More)


%description
This module implements the URI class. Objects of this class represent
"Uniform Resource Identifier references" as specified in RFC 2396 (and
updated by RFC 2732).


%prep
%setup

chmod 644 uri-test

%build

if test -f Makefile.PL; then
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?jobs:-j%jobs}
else
%{__perl} Build.PL  --installdirs vendor
./Build
fi

%install
rm -rf %{buildroot}
if test -f Makefile.PL; then
make pure_install PERL_INSTALL_ROOT=%{buildroot}
else
./Build install --installdirs vendor
fi
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'
find %{buildroot} -type f -name '*.bs' -empty -exec rm -f {} ';'
%{_fixperms} %{buildroot}/*

chmod -R u+w $RPM_BUILD_ROOT/*

for file in Changes; do
iconv -f iso-8859-1 -t utf-8 < "$file" > "${file}_"
mv -f "${file}_" "$file"
done


%check
make test

%files
%defattr(-,root,root,-)
%doc Changes README uri-test
%{perl_vendorlib}/URI*
#%doc %{_mandir}/man3/*.3*
