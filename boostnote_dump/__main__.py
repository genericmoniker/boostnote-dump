from pathlib import Path
import json
import re
import shutil
import sys
import textwrap
import cson

attach_re = re.compile(r'\(:storage[\\\/][a-f0-9-]+[\\\/](.+)\)')


def usage():
    print('python -m boostnote-dump <boostnote notes dir> <output dir>')


def main():
    if len(sys.argv) != 3:
        usage()
        sys.exit(1)

    boostnote_dir = Path(sys.argv[1])
    output_dir = Path(sys.argv[2])
    notes_dir = output_dir / 'notes'
    notes_dir.mkdir(parents=True, exist_ok=True)
    attach_dir = output_dir / 'attachments'
    attach_dir.mkdir(parents=True, exist_ok=True)

    boostnote_json = json.loads((boostnote_dir / 'boostnote.json').read_text())
    folders = {f['key']: f['name'] for f in boostnote_json['folders']}

    boostnote_notes_dir = boostnote_dir / 'notes'
    for file in boostnote_notes_dir.iterdir():
        print(file, '...', sep='', end='')
        doc = cson.loads(file.read_text(encoding='utf-8'))
        if doc['isTrashed']:
            print('skipped (trash)')
            continue
        if doc['type'] != "MARKDOWN_NOTE":
            print('skipped ', doc['type'])
            continue
        output = metadata(doc, folders)
        output += content(doc)
        path = notes_dir / filename_from_title(doc['title'])
        path.write_text(output, encoding='utf-8')
        print('done')

    boostnote_attach_dir = boostnote_dir / 'attachments'
    for subdir in boostnote_attach_dir.iterdir():
        if subdir.is_dir():
            for file in subdir.iterdir():
                print(file, '...', sep='', end='')
                shutil.copy2(file, attach_dir)
                print('done')


def metadata(doc, folders):
    notebook = ''
    try:
        notebook = 'Notebooks/' + folders[doc.get('folder')]
    except KeyError:
        pass
    tags = doc['tags']
    if notebook:
        tags.append(notebook)
    return textwrap.dedent(
        f"""
        ---
        title: {doc.get('title')}
        created: {doc.get('createdAt')}
        modified: {doc.get('updatedAt')}
        tags: [{', '.join(tags)}]
        pinned: {str(doc.get('isStarred', False)).lower()}
        ---

        """
    ).lstrip()


def content(doc):
    return attach_re.sub(r'(@attachment/\1)', doc['content'])


def filename_from_title(title):
    keepcharacters = (' ', '.', '_')
    return (
        "".join(c for c in title if c.isalnum() or c in keepcharacters).strip()
        + '.md'
    )


if __name__ == "__main__":
    main()
