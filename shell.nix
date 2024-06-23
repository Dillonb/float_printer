{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    python312Full
    python312Packages.termcolor
  ];
}
