%global origin          openjdk
%global origin_nice     OpenJDK
%global java_version    17
%global pkg_type        jre
%global priority        1161
Name:           temurin-%{java_version}-%{pkg_type}-alternatives
Version:        1
Release:        1
Summary:        Java Alternatives for Java Temurin %{java_version} (%{pkg_type})

License:        https://www.apache.org/licenses/LICENSE-2.0
URL:            https://github.com/VenaNocta/toolset-fedora/java
BuildRequires:  ( coreutils or coreutils-single )
Requires:       temurin-%{java_version}-%{pkg_type}
Requires:       alternatives


# disable rpmbuild features
#%global debug_package %{nil}
#%define __arch_install_post %{nil}
#%define __os_install_post %{nil}
%define _build_id_links none

%description
Provides Alternatives paths for Java Temurin %{java_version} (%{pkg_type})

###############################################################################

%global compatiblename         temurin-%{java_version}-%{pkg_type}
%global java_version_full      %{java_version}
%define uniquejavadocdir()     %{expand:%{compatiblename}-%{java_version_full}-%{release}}

# Standard JPackage directories and symbolic links.
%define sdkdir()        %{expand:%{compatiblename}}
%define jredir()        %{expand:%{sdkdir -- %{?1}}}

%define sdkbindir()     %{expand:%{_jvmdir}/%{sdkdir -- %{?1}}/bin}
%define jrebindir()     %{expand:%{_jvmdir}/%{jredir -- %{?1}}/bin}

%global family                 %{compatiblename}.%{_arch}
%global family_noarch          %{compatiblename}

###############################################################################

%define save_alternatives() %{expand:
  # warning! alternatives are localised!
  # LANG=en_US.UTF-8  alternatives --display java | head
  function nonLocalisedAlternativesDisplayOfKey() {
    LANG=en_US.UTF-8 alternatives --display "$KEY"
  }
  function headOfAbove() {
    nonLocalisedAlternativesDisplayOfKey | head -n $1
  }
  KEY="%{?1}"
  LOCAL_LINK="%{?2}"
  FAMILY="%{?3}"
  rm -f %{_localstatedir}/lib/rpm-state/"$KEY"_$FAMILY > /dev/null
  if nonLocalisedAlternativesDisplayOfKey > /dev/null ; then
      if headOfAbove 1 | grep -q manual ; then
        if headOfAbove 2 | tail -n 1 | grep -q %{compatiblename} ; then
           headOfAbove 2  > %{_localstatedir}/lib/rpm-state/"$KEY"_"$FAMILY"
        fi
      fi
  fi
}

%define save_and_remove_alternatives() %{expand:
  if [ "x$debug"  == "xtrue" ] ; then
    set -x
  fi
  upgrade1_uninstal0=%{?3}
  if [ "0$upgrade1_uninstal0" -gt 0 ] ; then # removal of this condition will cause persistence between uninstall
    %{save_alternatives %{?1} %{?2} %{?4}}
  fi
  alternatives --remove  "%{?1}" "%{?2}"
}

%define set_if_needed_alternatives() %{expand:
  KEY="%{?1}"
  FAMILY="%{?2}"
  ALTERNATIVES_FILE="%{_localstatedir}/lib/rpm-state/$KEY"_"$FAMILY"
  if [ -e  "$ALTERNATIVES_FILE" ] ; then
    rm "$ALTERNATIVES_FILE"
    alternatives --set $KEY $FAMILY
  fi
}

%define alternatives_java_install() %{expand:
if [ "x$debug"  == "xtrue" ] ; then
  set -x
fi
PRIORITY=%{priority}
if [ "%{?1}" == %{debug_suffix} ]; then
  let PRIORITY=PRIORITY-1
fi


key=java
key_path=%{sdkbindir -- %{?1}}/java
alternatives \\
  --add-follower $key $key_path \\
    %{_jvmdir}/jre jre %{_jvmdir}/%{jredir -- %{?1}}

for X in %{origin} %{java_version_full} ; do
  key=jre_"$X"
  alternatives --install %{_jvmdir}/jre-"$X" $key %{_jvmdir}/%{jredir -- %{?1}} $PRIORITY --family %{family}
  %{set_if_needed_alternatives $key %{family}}
done

key=jre_%{java_version_full}_%{origin}
alternatives --install %{_jvmdir}/jre-%{java_version_full}-%{origin} $key %{_jvmdir}/%{jredir -- %{?1}} $PRIORITY  --family %{family}
%{set_if_needed_alternatives $key %{family}}
}

%define alternatives_javac_install() %{expand:
if [ "x$debug"  == "xtrue" ] ; then
  set -x
fi
PRIORITY=%{priority}
if [ "%{?1}" == %{debug_suffix} ]; then
  let PRIORITY=PRIORITY-1
fi

key=javac
key_path=%{sdkbindir -- %{?1}}/javac
alternatives \\
  --add-follower $key $key_path \\
    %{_jvmdir}/java java_sdk %{_jvmdir}/%{sdkdir -- %{?1}}

for X in %{origin} %{java_version_full} ; do
  key=java_sdk_"$X"
  alternatives --install %{_jvmdir}/java-"$X" $key %{_jvmdir}/%{sdkdir -- %{?1}} $PRIORITY  --family %{family}
  %{set_if_needed_alternatives  $key %{family}}
done

key=java_sdk_%{java_version_full}_%{origin}
alternatives --install %{_jvmdir}/java-%{java_version_full}-%{origin} $key %{_jvmdir}/%{sdkdir -- %{?1}} $PRIORITY  --family %{family}
%{set_if_needed_alternatives  $key %{family}}
}

%define alternatives_javadoc_install() %{expand:
if [ "x$debug"  == "xtrue" ] ; then
  set -x
fi
PRIORITY=%{priority}
if [ "%{?1}" == %{debug_suffix} ]; then
  let PRIORITY=PRIORITY-1
fi

key=javadocdir
alternatives --install %{_javadocdir}/java $key %{_javadocdir}/%{uniquejavadocdir -- %{?1}}/api $PRIORITY  --family %{family_noarch}
%{set_if_needed_alternatives  $key %{family_noarch}}
exit 0
}

%define alternatives_javadoczip_install() %{expand:
if [ "x$debug"  == "xtrue" ] ; then
  set -x
fi
PRIORITY=%{priority}
if [ "%{?1}" == %{debug_suffix} ]; then
  let PRIORITY=PRIORITY-1
fi
key=javadoczip
alternatives --install %{_javadocdir}/java-zip $key %{_javadocdir}/%{uniquejavadocdir -- %{?1}}.zip $PRIORITY  --family %{family_noarch}
%{set_if_needed_alternatives  $key %{family_noarch}}
exit 0
}

###############################################################################

%define postun_headless() %{expand:
  if [ "x$debug"  == "xtrue" ] ; then
    set -x
  fi
  post_state=$1 # from postun, https://docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/#_syntax
  %{save_and_remove_alternatives  jre_%{origin} %{_jvmdir}/%{jredir -- %{?1}} $post_state %{family}}
  %{save_and_remove_alternatives  jre_%{java_version_full} %{_jvmdir}/%{jredir -- %{?1}} $post_state %{family}}
  %{save_and_remove_alternatives  jre_%{java_version_full}_%{origin} %{_jvmdir}/%{jredir -- %{?1}} $post_state %{family}}
}

%define postun_devel() %{expand:
  if [ "x$debug"  == "xtrue" ] ; then
    set -x
  fi
  post_state=$1 # from postun, https://docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/#_syntax
  %{save_and_remove_alternatives  java_sdk_%{origin} %{_jvmdir}/%{sdkdir -- %{?1}} $post_state %{family}}
  %{save_and_remove_alternatives  java_sdk_%{java_version_full} %{_jvmdir}/%{sdkdir -- %{?1}} $post_state %{family}}
  %{save_and_remove_alternatives  java_sdk_%{java_version_full}_%{origin} %{_jvmdir}/%{sdkdir -- %{?1}} $post_state %{family}}
exit 0
}

%define postun_javadoc() %{expand:
if [ "x$debug"  == "xtrue" ] ; then
  set -x
fi
  post_state=$1 # from postun, https://docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/#_syntax
  %{save_and_remove_alternatives  javadocdir  %{_javadocdir}/%{uniquejavadocdir -- %{?1}}/api $post_state %{family_noarch}}
exit 0
}

%define postun_javadoc_zip() %{expand:
  if [ "x$debug"  == "xtrue" ] ; then
    set -x
  fi
  post_state=$1 # from postun, https://docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/#_syntax
  %{save_and_remove_alternatives  javadoczip  %{_javadocdir}/%{uniquejavadocdir -- %{?1}}.zip $post_state %{family_noarch}}
  %{save_and_remove_alternatives  javadoczip_%{origin}  %{_javadocdir}/%{uniquejavadocdir -- %{?1}}.zip $post_state %{family_noarch}}
  %{save_and_remove_alternatives  javadoczip_%{java_version_full}  %{_javadocdir}/%{uniquejavadocdir -- %{?1}}.zip $post_state %{family_noarch}}
  %{save_and_remove_alternatives  javadoczip_%{java_version_full}_%{origin}  %{_javadocdir}/%{uniquejavadocdir -- %{?1}}.zip $post_state %{family_noarch}}
exit 0
}

###############################################################################

%posttrans
%{alternatives_java_install %{nil}}
%if "%{pkg_type}" == "jdk"
  %{alternatives_javac_install %{nil}}
%endif

%postun
%{postun_headless %{nil}}
%if "%{pkg_type}" == "jdk"
  %{postun_devel %{nil}}
%endif

#%posttrans javadoc
#%{alternatives_javadoc_install %{nil}}

#%postun javadoc
#%{postun_javadoc %{nil}}

#%posttrans javadoc-zip
#%{alternatives_javadoczip_install %{nil}}

#%postun javadoc-zip
#%{postun_javadoc_zip %{nil}}

%files

%changelog
* Wed Apr 30 2025 VenaNocta <venanocta@gmail.com> - 20250430
- added well known alternative paths

