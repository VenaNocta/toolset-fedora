# Java Alternatives

Since the Fedora 42 move, RedHat stopped supporting older java versions. Therefore we are now required to install them from Temurin, <ins>which is fine</ins>, **but** Temurin does not provide all the alternatives paths that we have grown to rely on! - so this is what the packages here provide

The provided Paths in the `temurin-*-j*-alternatives` packages include:

`<alternatives key>` | `<path>`
---|---
`java_sdk` | `/usr/lib/jvm/java`
`java_sdk_<version>` | `/usr/lib/jvm/java-<version>`
`java_sdk_openjdk` | `/usr/lib/jvm/java-openjdk`
`java_sdk_<version>-openjdk` | `/usr/lib/jvm/java-<version>-openjdk`
`jre` | `/usr/lib/jvm/jre`
`jre_<version>` | `/usr/lib/jvm/jre-<version>`
`jre_openjdk` | `/usr/lib/jvm/jre-openjdk`
`jre_<version>-openjdk` | `/usr/lib/jvm/jre-<version>-openjdk`

## Build-JRE

```bash
rpmbuild --build-in-place -bb temurin-8-jre-alternatives-1-1.spec
```

## Build-JDK

```bash
rpmbuild --build-in-place -bb temurin-8-jdk-alternatives-1-1.spec
```

