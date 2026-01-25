{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs";
  };

  outputs = { nixpkgs, ... }:
    let
      forAllSystems = nixpkgs.lib.genAttrs [ "aarch64-linux" "x86_64-linux" ];
    in
    {
      devShells = forAllSystems (system: {
        default = pkgs.mkShell {
          packages = [
            python3
          ];
        };
      });


    };
}