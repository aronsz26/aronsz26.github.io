# aronsz26 Repo

Jailbreak repo for my tweaks. Add it to Sileo or Zebra:

```
https://aronsz26.github.io/
```

## Tweaks

- [LockScreenRestore](https://github.com/aronsz26/LockScreenRestore): the iOS 15 lock screen, back on iOS 16 (rootless)

## Adding a release

1. Copy the new `.deb` into `debs/`.
2. Run `python3 update_repo.py` to rebuild `Packages` and `Release`.
3. Commit and push.
