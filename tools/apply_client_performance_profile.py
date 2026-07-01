#!/usr/bin/env python3
"""Apply VKPack's high-memory client launch profile to Modrinth App.

This edits Modrinth's local SQLite launcher database. It makes a SQLite backup
first, then sets the VKPack instance to a 50 GB max heap and Java 21/ZGC flags.
"""
from __future__ import annotations

import argparse
import json
import os
import sqlite3
import time
from pathlib import Path

VKPACK_EXTRA_ARGS = [
    '-Dfml.readTimeout=240',
    '-Xms16G',
    '-XX:+UseZGC',
    '-XX:+ZGenerational',
    '-XX:SoftMaxHeapSize=40G',
    '-XX:ActiveProcessorCount=17',
    '-XX:+ParallelRefProcEnabled',
    '-XX:+DisableExplicitGC',
    '-XX:+PerfDisableSharedMem',
    '-Dsun.rmi.dgc.server.gcInterval=2147483646',
    '-Dsun.rmi.dgc.client.gcInterval=2147483646',
]


def default_app_db() -> Path:
    appdata = os.environ.get('APPDATA')
    if not appdata:
        raise SystemExit('APPDATA is not set; pass --app-db explicitly.')
    return Path(appdata) / 'ModrinthApp' / 'app.db'


def backup_database(app_db: Path) -> Path:
    backup_dir = app_db.parent / 'db-backups' / ('vkpack-client-perf-' + time.strftime('%Y%m%d-%H%M%S'))
    backup_dir.mkdir(parents=True, exist_ok=True)
    source = sqlite3.connect(str(app_db))
    backup = sqlite3.connect(str(backup_dir / 'app.db'))
    source.backup(backup)
    backup.close()
    source.close()
    return backup_dir / 'app.db'


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--app-db', type=Path, default=default_app_db())
    parser.add_argument('--instance-name', default='VKPack')
    parser.add_argument('--max-memory-mb', type=int, default=51200)
    parser.add_argument('--global-default-memory-mb', type=int, default=16384)
    args = parser.parse_args()

    app_db = args.app_db.resolve()
    if not app_db.exists():
        raise SystemExit(f'Modrinth App database not found: {app_db}')

    backup_path = backup_database(app_db)

    con = sqlite3.connect(str(app_db))
    con.execute('pragma busy_timeout=10000')
    row = con.execute(
        """
        select o.instance_id, json(o.overrides)
        from instance_launch_overrides o
        join instances i on i.id = o.instance_id
        where i.name = ?
        """,
        (args.instance_name,),
    ).fetchone()
    if not row:
        raise SystemExit(f'Instance launch overrides not found for {args.instance_name!r}')

    instance_id, overrides_json = row
    overrides = json.loads(overrides_json)
    overrides['extra_launch_args'] = VKPACK_EXTRA_ARGS
    overrides['memory'] = {'maximum': args.max_memory_mb}
    overrides.setdefault('hooks', {'pre_launch': None, 'wrapper': None, 'post_exit': None})

    con.execute(
        'update instance_launch_overrides set overrides=jsonb(?) where instance_id=?',
        (json.dumps(overrides, separators=(',', ':')), instance_id),
    )
    con.execute('update settings set mc_memory_max=? where id=0', (args.global_default_memory_mb,))
    con.commit()

    print(f'Backup written: {backup_path}')
    print(f'Updated instance: {args.instance_name} ({instance_id})')
    print(f'Max memory: {args.max_memory_mb} MB')
    print('Extra launch args:')
    for item in VKPACK_EXTRA_ARGS:
        print(f'  {item}')
    con.close()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())