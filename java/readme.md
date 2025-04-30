# Java Alternatives

Since the Fedora 42 move, RedHat stopped supporting older java versions. Therefore we are now required to install them from Temurin, <ins>which is fine</ins>, **but** Temurin does not provide all the alternatives paths that we have grown to rely on! - so this is what to packages herein provide

## Build-JRE

```bash
rpmbuild --build-in-place -bb temurin-8-jre-alternatives-1-1.spec
```

## Build-JDK

```bash
rpmbuild --build-in-place -bb temurin-8-jdk-alternatives-1-1.spec
```

