# Java Alternatives

Since Fedora 42 moved stopped supporting older java versions we are required to install them from Temurin, which is fine, **but** Temurin does not provide all the alternatives paths that we have grown to rely on! - so this is what to packages herein provide

## Build-JRE

```bash
rpmbuild --build-in-place -bb temurin-8-jre-alternatives-1-1.spec
```

## Build-JDK

```bash
rpmbuild --build-in-place -bb temurin-8-jdk-alternatives-1-1.spec
```

