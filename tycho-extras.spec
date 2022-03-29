%global xmvn_libdir %(realpath $(dirname $(readlink -f $(which xmvn)))/../lib)
Name:                tycho-extras
Version:             1.3.0
Release:             3
Summary:             Additional plugins for Tycho
License:             EPL-1.0
URL:                 http://eclipse.org/tycho/
Source0:             http://git.eclipse.org/c/tycho/org.eclipse.tycho.extras.git/snapshot/org.eclipse.tycho.extras-tycho-extras-%{version}.tar.xz
Patch0:              %{name}-fix-build.patch
Patch1:              fix-xmvn-pomless-builddep.patch
Patch2:              tycho-extras-use-custom-resolver.patch
BuildArch:           noarch
ExcludeArch:         s390 %{arm} %{ix86}
BuildRequires:       maven-local mvn(io.takari.polyglot:polyglot-common)
BuildRequires:       mvn(org.apache.commons:commons-lang3) mvn(org.apache.maven:maven-archiver)
BuildRequires:       mvn(org.apache.maven:maven-core) mvn(org.apache.maven:maven-model)
BuildRequires:       mvn(org.apache.maven:maven-model-builder)
BuildRequires:       mvn(org.apache.maven:maven-plugin-api)
BuildRequires:       mvn(org.apache.maven.plugins:maven-plugin-plugin)
BuildRequires:       mvn(org.apache.maven.plugins:maven-source-plugin)
BuildRequires:       mvn(org.apache.maven.plugin-tools:maven-plugin-annotations)
BuildRequires:       mvn(org.codehaus.plexus:plexus-component-metadata)
BuildRequires:       mvn(org.eclipse.jgit:org.eclipse.jgit)
BuildRequires:       mvn(org.eclipse.sisu:org.eclipse.sisu.plexus)
BuildRequires:       mvn(org.eclipse.tycho:org.eclipse.tycho.core.shared)
BuildRequires:       mvn(org.eclipse.tycho:org.eclipse.tycho.p2.resolver.shared)
BuildRequires:       mvn(org.eclipse.tycho:sisu-equinox-launching) mvn(org.eclipse.tycho:tycho-core)
BuildRequires:       mvn(org.eclipse.tycho:tycho-p2-facade)
BuildRequires:       mvn(org.eclipse.tycho:tycho-packaging-plugin)
BuildRequires:       mvn(org.fedoraproject.p2:org.fedoraproject.p2)
%description
A small set of plugins that work with Tycho to provide additional functionality
when building projects of an OSGi nature.

%package javadoc
Summary:             Java docs for %{name}
%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n org.eclipse.tycho.extras-tycho-extras-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%pom_remove_plugin :maven-site-plugin
%pom_remove_plugin org.eclipse.m2e:lifecycle-mapping
%pom_remove_plugin org.sonatype.plugins:maven-properties-plugin tycho-p2-extras-plugin
%pom_remove_dep org.apache.maven:apache-maven tycho-p2-extras-plugin
%pom_add_dep org.fedoraproject.p2:org.fedoraproject.p2 tycho-eclipserun-plugin/pom.xml
%mvn_alias :{*} org.eclipse.tycho:@1

%build
%mvn_build -f

%install
%mvn_install
install -d -m 755 %{buildroot}%{xmvn_libdir}/ext/
ln -s %{_javadir}/%{name}/tycho-pomless.jar %{buildroot}%{xmvn_libdir}/ext/
ln -s %{_javadir}/tesla-polyglot/polyglot-common.jar %{buildroot}%{xmvn_libdir}/ext/

%files -f .mfiles
%{xmvn_libdir}/ext/*

%files javadoc -f .mfiles-javadoc

%changelog
* Sat Apr 2 2022 xiaoqianlv <xiaoqian@nj.iscas.ac.cn> - 1.3.0-3
- fix build fail

* Sun Sep 13 2020 yanan li <liyanan032@huawei.com> - 1.3.0-2
- fix build fail

* Wed Aug 19 2020 maminjie <maminjie1@huawei.com> - 1.3.0-1
- package init
