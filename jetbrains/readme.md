# Repackaging JetBrains

This folder contains the scripts and resulting `.spec` files for repackaging the JetBrains Products for Linux (`.rpm` files).
All scripts in this folder are build for Admins to streamline product rollout on an organizational level.

Just to clarify, all patches made upon repackaging are exclusively done to modularize the products,
they however do **not remove** the **requirement of a valid license**!

## Basic Patches

**Patch: `$IDE_HOME`**

The `$IDE_HOME` override has been added to the startup script and by default it is set to `/usr/lib64/jetbrains/<product>-<version>` which is the location where the product will be installed.

**Patch: `$VM_OPTIONS_FILE`**

The `<product>64.vmoptions` file has been moved to `/etc/jetbrains/<product>64.vmoptions`,
the new path is configured via `$VM_OPTIONS_FILE`.

The location of the `.vmoptions` file has been moved so that admins have the base settings of all JetBrains products in `/etc/jetbrains/`.

**Patch: `$PHPSTORM_JDK`**

The `$PHPSTORM_JDK` override option has been added to the startup script.

With this option an admin can change with which Java Runtime the product is executed.

Furthermore, JetBrain's Java Runtime is packaged in an extra `<product>-<version>-jbr` package,
which will be preferred over the default Java Runtime when installed.


## Notes

### PHPStorm : DevContainer

In `phpstorm-pro` version `2024.3.5-1` you can start and connect to devcontainers via **Podman**,
using **compose with `Dockerfile`s** **without having the jbr installed**.

In the later versions until version `2025.2.4-1` **this does not work at all**.

In `phpstorm-pro` version `2025.2.4-1`, if you want to use this feature the **jbr package must be installed**.

