{ pkgs ? import <nixpkgs> {} }:
pkgs.mkShell {
  packages = [ pkgs.cmake pkgs.gcc pkgs.gdb pkgs.openmpi pkgs.python313Packages.mpi4py pkgs.python313Packages.numpy ];
}