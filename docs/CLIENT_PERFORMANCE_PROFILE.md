# VKPack Client Performance Profile

VKPack is intentionally large. The client profile now uses a high-memory Java 21 setup, but the important bit is this: more RAM only helps if Java and the pack can use it without turning garbage collection into the new bottleneck.

## Current Modrinth App Override

The live VKPack profile was updated in Modrinth App's local launcher database:

- Max heap: `51200 MB` (`50 GB`)
- Initial heap: `-Xms16G`
- Collector: ZGC with generational mode
- Soft heap target: `40G`
- CPU target: `-XX:ActiveProcessorCount=17`

The machine reports `20` logical processors, so `17` is the closest practical 85 percent target. This does not make Minecraft's single game thread magically use 17 cores. It tells Java's GC/compiler/worker sizing to treat 17 logical processors as available.

## JVM Args

```text
-Dfml.readTimeout=240
-Xms16G
-XX:+UseZGC
-XX:+ZGenerational
-XX:SoftMaxHeapSize=40G
-XX:ActiveProcessorCount=17
-XX:+ParallelRefProcEnabled
-XX:+DisableExplicitGC
-XX:+PerfDisableSharedMem
-Dsun.rmi.dgc.server.gcInterval=2147483646
-Dsun.rmi.dgc.client.gcInterval=2147483646
```

## Reapply The Profile

From the repo root on Windows:

```powershell
python tools/apply_client_performance_profile.py
```

The script backs up Modrinth's `app.db` first, then updates the `VKPack` instance launch override.

## Why The Client Can Still Lag

The latest crash/log pass did not look like a clean out-of-memory failure. The biggest offenders were JEI and recipe registration problems:

- missing `cataclysm_spellbooks:technomancy_power` upgrade-orb registry data,
- Electrodynamics JEI pseudo-recipe errors,
- Malum/Undergarden JEI recipe type mismatch,
- long JEI plugin registration stalls.

This pass also caps Sophisticated JEI Index backpack scanning and moves several fragile JEI plugins onto ModernFix's main-thread loading path. That may cost a little startup speed, but it should reduce crashy async behavior.