#!/usr/bin/env python3
"""Inspect GLB v2 JSON metadata without executing content or decoding geometry."""
import argparse
import json
import struct
from pathlib import Path


def inspect(path):
    data = Path(path).read_bytes()
    if len(data) < 12:
        raise ValueError('File is shorter than a GLB header')
    magic, version, length = struct.unpack_from('<4sII', data)
    if magic != b'glTF' or version != 2 or length != len(data):
        raise ValueError('Expected GLB v2 with a matching declared file length')
    offset, document = 12, None
    while offset < length:
        if offset + 8 > length:
            raise ValueError('Truncated chunk header')
        size, kind = struct.unpack_from('<II', data, offset)
        offset += 8
        if size % 4 or offset + size > length:
            raise ValueError('Invalid chunk alignment or truncated chunk')
        if kind == 0x4E4F534A:
            if document is not None:
                raise ValueError('Multiple JSON chunks')
            document = json.loads(data[offset:offset + size].decode('utf-8').rstrip(' \x00'))
        offset += size
    if not isinstance(document, dict):
        raise ValueError('Missing GLB JSON object')
    nodes = document.get('nodes', [])
    return {
        'file': str(Path(path).resolve()), 'bytes': length,
        'extensions_required': document.get('extensionsRequired', []),
        'extensions_used': document.get('extensionsUsed', []),
        'nodes': [{'index': i, **{key: n[key] for key in
                  ('name', 'mesh', 'children', 'matrix', 'translation', 'rotation', 'scale')
                  if key in n}} for i, n in enumerate(nodes)],
        'mesh_count': len(document.get('meshes', [])),
        'accessor_declared_bounds': [{'index': i, 'type': a.get('type'),
                                     'min': a.get('min'), 'max': a.get('max')}
                                    for i, a in enumerate(document.get('accessors', []))
                                    if 'min' in a or 'max' in a],
        'external_resources': [v['uri'] for key in ('buffers', 'images')
                               for v in document.get(key, []) if 'uri' in v],
        'limitations': ['Metadata only: no compressed geometry decoding, world-space bounds, semantic part identification, or factual construction verification.'],
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file')
    args = parser.parse_args()
    try:
        print(json.dumps(inspect(args.file), indent=2))
    except (ValueError, OSError, UnicodeError, struct.error) as error:
        parser.exit(1, f'GLB inspection failed: {error}\n')
