{ pkgs }: {
  deps = [
    pkgs.python311
    pkgs.nodejs_22
    pkgs.libGL
    pkgs.glib
  ];
  env.LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [ pkgs.libGL pkgs.glib ];
}
