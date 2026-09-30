#!/usr/bin/env python3
"""Validate real sibling checkouts before asking Xcode to build the workspace."""
import json
from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT / 'MaxLab.xcworkspace'
seen_ids = set()
apps = set()
for reference in ET.parse(WORKSPACE / 'contents.xcworkspacedata').getroot():
    location = reference.attrib['location']
    assert location.startswith('group:'), location
    project = (ROOT / location.removeprefix('group:')).resolve()
    assert project.is_dir() and project.suffix == '.xcodeproj', project
    data = json.loads(subprocess.check_output(['plutil', '-convert', 'json', '-o', '-', str(project / 'project.pbxproj')]))
    objects = data['objects']
    assert not seen_ids.intersection(objects), f'Duplicate project IDs in {project}'
    seen_ids.update(objects)
    project_object = objects[data['rootObject']]
    source_root = project.parent
    visited = set()

    def visit(identifier, parent):
        obj = objects[identifier]
        visited.add(identifier)
        tree = obj.get('sourceTree', '<group>')
        if tree == 'BUILT_PRODUCTS_DIR':
            return
        assert tree in ('<group>', 'SOURCE_ROOT'), (identifier, tree)
        base = source_root if tree == 'SOURCE_ROOT' else parent
        path = base / obj.get('path', '')
        if obj['isa'] == 'PBXFileReference':
            assert (path.is_dir() if obj.get('lastKnownFileType') == 'folder.assetcatalog' else path.is_file()), f'Broken file reference: {path}'
            current = source_root
            for part in path.relative_to(source_root).parts:
                assert part in {entry.name for entry in current.iterdir()}, f'Wrong path case: {path}'
                current /= part
        for child in obj.get('children', []):
            visit(child, path)

    visit(project_object['mainGroup'], source_root)
    for identifier, obj in objects.items():
        if obj['isa'] == 'PBXFileReference':
            assert identifier in visited, f'Orphaned navigator reference: {obj}'
        if obj['isa'] == 'XCSwiftPackageProductDependency':
            assert obj.get('package') in project_object['packageReferences'], obj
    app = project.stem
    scheme = ET.parse(project / 'xcshareddata/xcschemes' / f'{app}.xcscheme')
    for ref in scheme.iter('BuildableReference'):
        assert ref.attrib['ReferencedContainer'] == f'container:{app}.xcodeproj'
        target = objects[ref.attrib['BlueprintIdentifier']]
        assert target['isa'] == 'PBXNativeTarget'
        assert target['name'] == ref.attrib['BlueprintName']
    apps.add(app)
assert apps == {'Gamefy', 'Reset', 'MaxLab', 'PhotoVeil'}, apps
print('Workspace file references, unique project IDs, package bindings and shared schemes are valid.')
