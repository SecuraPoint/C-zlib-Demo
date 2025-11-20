# C zlib Demo
A C repository for demonstration. It uses zlib as dependency. Packages are managed with conda and conda-forge.

## Local development
Use nix-shell to start dev environment.
```bash
nix-shell
```

### Compile project
Run to compile and start the project
```bash
# Start nix shell
nix-shell

# Make the project
cd src
make

# Start the project
./main
```

### Create conda-lock.yml file
Use conda-lock to create lock file.
```bash
conda-lock -f environment.yml -p osx-64 -p linux-64
```

### Create ABOUT Files
The ABOUT files are used as a meta data transfer mechanism. They are scanned by scancode toolkit (Scancode.io). Their content is recognized as packages in Scancode.io as well as DejaCode. Therefore, they are created by a helper python script. This script is called within the ci-pipeline as well. It creates the required about files through parsing information from the _conda-lock.yml_. It has to be executed in order to facilitate the SCA scan:
1. Generate _conda-lock.yml_
2. Generate ABOUT files
3. Run SCA scan with scancode toolkit

Generate the ABOUT files as follows
```bash
# Give the path to the conda-lock.yml. <outdir> is optional. <codebase version> should be replaced with the current version identifier of this codebase.
python ./conda_lock_to_about.py path/to/conda-lock.yml <outdir> <codebase version>

# For example:
python ./conda_lock_to_about.py conda-lock.yml about/ 1.2.4
```


## Push a new version
Do the following steps to push a new version, which triggers a ScanCode.io scan.
```bash
# run nix shell to start local environment
nix-shell

# recreate conda-lock.yml
conda-lock -f environment.yml -p osx-64 -p linux-64

# commit and push
git commit -m "Some message"
git push

# add a tag and push it. Strict use of semantic versioning to trigger pipeline#
git tag v1.0.x
git push origin v1.0.X
```

## Relevant knowledge

### Valid PURL format for conda-forge
This is a valid PURL for conda-forge: `pkg:conda/zlib@1.3.1?channel=conda-forge&subdir=linux-64&build=hb9d3cd8_2&type=conda`. It results in a derived (constructed by scancode) download URL of this format: `https://conda.anaconda.org/conda-forge/linux-64/zlib-1.3.1-hb9d3cd8_2.conda`
