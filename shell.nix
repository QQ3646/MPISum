{ pkgs ? import <nixpkgs> {} }:
pkgs.mkShell {
  packages = [ pkgs.cmake pkgs.gcc pkgs.gdb pkgs.openmpi pkgs.python313Packages.mpi4py pkgs.python313Packages.numpy ];
}

Proc  | Lang  | Time (sec)
--------------------------------
1     | C++   | 0.054938
1     | Py    | 0.017687
--------------------------------
2     | C++   | 0.027673
2     | Py    | 0.014881
--------------------------------
4     | C++   | 0.014980
4     | Py    | 0.015212
--------------------------------
8     | C++   | 0.015185
8     | Py    | 0.015586
--------------------------------