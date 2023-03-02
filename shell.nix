{ pkgs ? import <nixpkgs> {} }:

let
  pythonEnv = with pkgs.python310Packages; [
    # Backend
    ipython
    jupyter
    fastapi
    uvicorn

    # FHIR
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

    # Database
    sqlalchemy
    (buildPythonPackage rec {
      pname = "sqlalchemy-json";
      version = "0.5.0";
      src = fetchPypi {
        inherit pname version;
        sha256 = "89f82420dbb6ace0228535506686536f646ee17e2f35a1a810cefbce6d75a649";
      };
      doCheck = false;
      propagatedBuildInputs = [
          sqlalchemy
          six
      ];})


    psycopg2
    # (
    # buildPythonPackage rec {
    #   pname = "sqlmodel";
    #   version = "0.0.8";
    #   src = fetchPypi {
    #     inherit pname version;
    #     sha256 = "3371b4d1ad59d2ffd0c530582c2140b6c06b090b32af9b9c6412986d7b117036";
    #   };
    #   doCheck = false;
    #   propagatedBuildInputs = [
    #       pydantic
    #       sqlalchemy
    #   ];
    # }
    # )
    #
  ];

in pkgs.mkShell {
  buildInputs = with pkgs; [
    pythonEnv
    postgresql
    # keep this line if you use bash
    pkgs.bashInteractive
  ];
}
