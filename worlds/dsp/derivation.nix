{ lib, python3Packages }:
with python3Packages;
buildPythonApplication {
  pname = "dsp.apworld";
  version = "0.20";

  propagatedBuildInputs = [ ];

  src = ./.;
}