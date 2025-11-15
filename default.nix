{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.stdenv
    pkgs.git
    pkgs.wget
    pkgs.bash
  ];

  shellHook = ''
    set -e

    echo "🔧 Starting conda environment (Miniforge) inside nix-shell…"

    # Detect host CPU architecture (arm64 vs x86_64)
    ARCH="$(uname -m)"
    if [ "$ARCH" = "arm64" ] || [ "$ARCH" = "aarch64" ]; then
      INSTALLER_URL="https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-MacOSX-arm64.sh"
    else
      INSTALLER_URL="https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-MacOSX-x86_64.sh"
    fi

    # Install Miniforge locally in the project directory (not system-wide)
    if [ ! -d ".miniforge" ]; then
      echo "Downloading Miniforge for architecture: $ARCH…"
      wget -q "$INSTALLER_URL" -O miniforge.sh
      bash miniforge.sh -b -p "$(pwd)/.miniforge"
      rm miniforge.sh
    fi

    # Check if Miniforge installation looks valid
    if [ -f ".miniforge/etc/profile.d/conda.sh" ]; then
      # Add conda binaries to PATH
      export PATH="$(pwd)/.miniforge/bin:$PATH"

      # Load conda into the current shell
      . ".miniforge/etc/profile.d/conda.sh"

      ENV_NAME="c-zlib-demo"
      ENV_DIR="$(pwd)/.miniforge/envs/$ENV_NAME"

      echo "🔧 Ensuring project conda environment '$ENV_NAME' exists…"

      if [ ! -d "$ENV_DIR" ]; then
        echo "Creating conda environment '$ENV_NAME' from environment.yml…"
        conda env create -f environment.yml
      else
        echo "Updating existing conda environment '$ENV_NAME' from environment.yml…"
        conda env update -f environment.yml --prune
      fi

      echo "🔧 Activating project conda environment…"
      conda activate "$ENV_NAME"

      echo "🔧 Installing conda-lock inside Conda environment…"
      conda install -y -c conda-forge conda-lock

      echo "✅ conda-lock is ready. Example:"
      echo "   conda-lock -f environment.yml -p linux-64 -p osx-64"

    else
      echo "⚠️ Miniforge installation seems to have failed."
      echo "   Try: rm -rf .miniforge && nix-shell"
    fi
  '';
}
