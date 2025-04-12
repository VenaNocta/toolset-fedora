# OATH via PAM

**PAM:**

```bash
dnf install pam_oath
```

## Secure Cockpit

To enable MFA for all admin users change the `/etc/pam.d/cockpit` config file to enclude following lines before the password validation:

```
auth    [default=1 success=ignore]  pam_succeed_if.so user ingroup wheel
auth    requisite                   pam_oath.so alwaysok usersfile=${HOME}/.ssh/oath_secret window=30 digits=6
```

## User Setup

Use the script ... if you want to be able to show the token you can install the oathtool:

```bash
dnf install oathtool
```

