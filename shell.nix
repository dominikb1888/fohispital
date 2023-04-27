{ pkgs ? import <nixpkgs> {} }:

let
  pythonEnv = with pkgs.python310Packages; [
    # Data Science Basics
    ipython
    jupyter
    fastapi
    uvicorn

    (
    buildPythonPackage rec {
      pname = "fhir.resources";
      version = "6.5.0";
      src = fetchPypi {
        inherit pname version;
        sha256 = "1d02ff2547e5b6323543c8ce9916e0c9e5536847b3b2171acb1f51a86efba16e";
      };
      doCheck = false;
      propagatedBuildInputs = [
          pytest-runner
          pydantic
      ];
    }
    )

  ];

in pkgs.mkShell {
  buildInputs = with pkgs; [
    pythonEnv
    poetry
    # keep this line if you use bash
    pkgs.bashInteractive
  ];
}
