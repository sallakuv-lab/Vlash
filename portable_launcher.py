from __future__ import annotations

import os
import runpy
import sys
from pathlib import Path, PureWindowsPath

# Static imports keep the complete offline runtime inside the PyInstaller folder.
# They live in an uncalled helper so importing this module for tests does not
# require those Windows packages to exist on the build-orchestration host.
def _bundle_dependencies() -> None:
    import pygame  # noqa: F401
    import OpenGL.GL  # noqa: F401
    import OpenGL.GLU  # noqa: F401
    import PIL  # noqa: F401
    import cryptography  # noqa: F401
    import fitz  # noqa: F401
    import openpyxl  # noqa: F401
    import docx  # noqa: F401
    import reportlab  # noqa: F401
    import tkinterdnd2  # noqa: F401
    import extract_msg  # noqa: F401
    import win32com.client  # noqa: F401
    import tkcalendar  # noqa: F401
    import playsound3  # noqa: F401
    import simpleaudio  # noqa: F401
    try:
        import playsound  # noqa: F401
    except Exception:
        pass


APP_FILENAME = "Orione_Fix11.pyw"


def app_path_for(executable: Path) -> Path:
    raw = str(executable)
    if "\\" in raw and "/" not in raw:
        return Path(str(PureWindowsPath(raw).with_name(APP_FILENAME)))
    return executable.with_name(APP_FILENAME)


def _show_missing_app(path: Path) -> None:
    try:
        import tkinter as tk
        from tkinter import messagebox
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(
            "Orione Fix11",
            f"File principale non trovato:\n{path}\n\n"
            "Mantieni Orione.exe e Orione_Fix11.pyw nella stessa cartella.",
            parent=root,
        )
        root.destroy()
    except Exception:
        pass


def main() -> int:
    exe = Path(sys.executable).resolve()
    app = app_path_for(exe)
    if not app.is_file():
        _show_missing_app(app)
        return 2
    root = exe.parent
    os.chdir(root)
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    # sys.argv is deliberately preserved. Orione uses flags such as
    # --orion-engine and --statgraf-engine when the frozen executable relaunches
    # itself for the OpenGL child processes.
    runpy.run_path(str(app), run_name="__main__")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
