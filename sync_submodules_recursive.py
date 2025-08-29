#!/usr/bin/env python3
import subprocess, os, sys

def run(cmd, cwd=None, check=True):
    print(f"$ {cmd}  (cwd={cwd or os.getcwd()})")
    p = subprocess.run(cmd, cwd=cwd, shell=True,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                       text=True)
    if check and p.returncode != 0:
        print(p.stderr, file=sys.stderr)
        sys.exit(p.returncode)
    return p.stdout.strip()

def get_submodule_paths():
    """
    Lista todos los submódulos de forma recursiva.
    git submodule status --recursive incluye hijos a todos los niveles.
    """
    out = run("git submodule status --recursive")
    paths = []
    for line in out.splitlines():
        parts = line.strip().split()
        if len(parts) >= 2:
            paths.append(parts[1])
    return paths

def commit_and_push_submodule(path):
    try:
        run("git add .", cwd=path)
        run('git commit -m "chore: sync local changes in submodule"', cwd=path)
        run("git push", cwd=path)
    except SystemExit:
        print(f"  [info] no hay cambios para push en {path}")

def update_parent_pointers(submodules):
    for path in submodules:
        run(f"git add {path}")
    status = run("git status --porcelain")
    if status:
        run('git commit -m "chore: update submodule pointers"')
        run("git push")
    else:
        print("  [info] no hay punteros de submódulo para actualizar en el repo padre")

def main():
    submodules = get_submodule_paths()
    if not submodules:
        print("No se detectaron submódulos.")
        sys.exit(0)

    # 1) Commit+push en todos los submódulos (y sub-sub-…)
    for path in submodules:
        commit_and_push_submodule(path)

    # 2) Actualizar punteros en el repo raíz
    update_parent_pointers(submodules)
    print("✅ ¡Todos los submódulos sincronizados y punteros actualizados!")

if __name__ == "__main__":
    main()
