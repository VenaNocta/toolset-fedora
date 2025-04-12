# OATH via PAM

**PAM:**

```bash
dnf install pam_oath
```

## Secure Cockpit

To enable MFA for all admin users change the `/etc/pam.d/cockpit` config file to enclude following lines **after** the password validation:

```
auth    [default=1 success=ignore]  pam_succeed_if.so user ingroup wheel
auth    requisite                   pam_oath.so usersfile=/home/${USER}/.ssh/oath_secret window=30 digits=6
```

## User Setup

The script requires `qrencode` to display a scanable code.

```bash
dnf install qrencode
```

If you want to be able to show the token you can install the `oathtool`.

```bash
dnf install oathtool
```

