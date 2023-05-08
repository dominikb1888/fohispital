{ pkgs ? import <nixpkgs> {} }:

let
  pythonEnv = with pkgs.python310Packages; [
    # Data Science Basics
    ipython
    jupyter
    fastapi
    uvicorn
    redis

    (
    buildPythonPackage rec {
      pname = "fhir.resources";
      version = "7.0.0";
      src = fetchPypi {
        inherit pname version;
        sha256 = "202d443c81066e063c6f1762b18a9680750db9f4772de5183ed20f0622ac7026";
      };
      doCheck = false;
      propagatedBuildInputs = [
          pytest-runner
          pydantic
          email-validator
      ];
    }
    )

  ];

in pkgs.mkShell {
  buildInputs = with pkgs; [
    pythonEnv
    redis
    # keep this line if you use bash
    pkgs.bashInteractive
  ];
}
