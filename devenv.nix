{ pkgs, ... }: {
  languages.python.enable = true;

  packages = with pkgs.python3Packages;
    [
      httpx
      pydantic
      beautifulsoup4
      lxml
      pillow
      numpy
      pandas
    ];

  enterShell = ''
    echo \"Hello from devenv!\"
  '';

  # files = { 
  #   .env = { text = \"KEY=VALUE\" };
  # };

  # See full reference at https://devenv.sh/reference/options/
}

