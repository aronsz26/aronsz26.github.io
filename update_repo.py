#!/usr/bin/env python3
# Rebuilds the repo index (Packages, Release) from the .deb files in debs/.
# Usage: python3 update_repo.py   (after copying a new .deb into debs/)
import bz2, gzip, hashlib, io, lzma, os, subprocess, tarfile, time

ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)

def control_of(deb):
    names = subprocess.run(['ar', 't', deb], capture_output=True, text=True, check=True).stdout.split()
    member = next(n for n in names if n.startswith('control.tar'))
    data = subprocess.run(['ar', 'p', deb, member], capture_output=True, check=True).stdout
    if member.endswith('.zst'):
        data = subprocess.run(['zstd', '-dc'], input=data, capture_output=True, check=True).stdout
    with tarfile.open(fileobj=io.BytesIO(data)) as tar:
        f = next(m for m in tar.getmembers() if os.path.basename(m.name) == 'control')
        return tar.extractfile(f).read().decode().strip()

entries = []
for name in sorted(os.listdir('debs')):
    if not name.endswith('.deb'):
        continue
    path = os.path.join('debs', name)
    raw = open(path, 'rb').read()
    entries.append('\n'.join([
        control_of(path),
        f'Filename: ./{path}',
        f'Size: {len(raw)}',
        f'MD5sum: {hashlib.md5(raw).hexdigest()}',
        f'SHA1: {hashlib.sha1(raw).hexdigest()}',
        f'SHA256: {hashlib.sha256(raw).hexdigest()}',
    ]))
packages = ('\n\n'.join(entries) + '\n').encode()

files = {'Packages': packages, 'Packages.gz': gzip.compress(packages, mtime=0),
         'Packages.bz2': bz2.compress(packages), 'Packages.xz': lzma.compress(packages)}
for name, data in files.items():
    open(name, 'wb').write(data)

release = [
    'Origin: aronsz26', 'Label: aronsz26', 'Suite: stable', 'Version: 1.0', 'Codename: ios',
    'Architectures: iphoneos-arm64 iphoneos-arm', 'Components: main', 'Description: Tweaks by aronsz26',
    'Date: ' + time.strftime('%a, %d %b %Y %H:%M:%S UTC', time.gmtime()),
]
for label, algo in [('MD5Sum', hashlib.md5), ('SHA1', hashlib.sha1), ('SHA256', hashlib.sha256)]:
    release.append(f'{label}:')
    for name, data in files.items():
        release.append(f' {algo(data).hexdigest()} {len(data)} {name}')
open('Release', 'w').write('\n'.join(release) + '\n')
print(f'{len(entries)} package(s) indexed')
