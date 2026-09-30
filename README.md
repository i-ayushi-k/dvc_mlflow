# Diabetes Dataset — DVC Tutorial/Example

This project applies the exact workflow from the supplied `DVCtutorial.docx`
and `DVCexample.docx` to `data/diabetes.csv`.

Dataset:
- 995 rows
- Columns: glucose, bloodpressure, diabetes

## 0. Open this folder in VS Code

Open the `diabetes-dvc-project` folder in VS Code.

## 1. Install DVC (one time)

In PowerShell:

```powershell
pip install dvc
dvc --version
git --version
```

## 2. Required initialization sequence

The tutorial says to initialize Git first, then DVC, then commit the setup.

```powershell
git init
dvc init
git add .dvc .gitignore
git commit -m "Initialize DVC"
```

If Git asks for your identity:

```powershell
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

Then repeat the commit.

## 3. Version 1 — track the original diabetes dataset

The supplied dataset is already in:

```text
data/diabetes.csv
```

Run:

```powershell
dvc add data/diabetes.csv
```

This creates:

```text
data/diabetes.csv.dvc
```

and updates `.gitignore`.

Now commit the DVC pointer, exactly like the tutorial/example:

```powershell
git add data/diabetes.csv.dvc .gitignore
git commit -m "Add initial diabetes dataset"
git tag -a "v1.0" -m "Diabetes dataset version 1.0"
```

You can verify:

```powershell
git status
dvc status
```

## 4. Version 2 — update the dataset

For this demonstration, we keep all 995 original observations and columns,
but deterministically reorder the rows. This changes the file contents without
inventing or deleting observations, so DVC creates a new data version.

Run:

```powershell
python scripts/make_version2.py
```

Then update DVC tracking:

```powershell
dvc add data/diabetes.csv
```

Commit the new DVC pointer:

```powershell
git add data/diabetes.csv.dvc
git commit -m "Update diabetes dataset to version 2"
git tag -a "v2.0" -m "Diabetes dataset version 2.0"
```

Check:

```powershell
dvc status
git log --oneline --decorate --all
git tag
```

## 5. Switch back to Version 1

This is the "double checkout" from the tutorial:

### Step A — switch Git metadata

```powershell
git checkout v1.0
```

### Step B — sync the actual dataset using DVC

```powershell
dvc checkout
```

Now `data/diabetes.csv` is the Version 1 dataset again.

## 6. Switch forward to Version 2

```powershell
git checkout v2.0
dvc checkout
```

Now the working dataset is Version 2.

## 7. Optional: local DVC remote

The example explains that DVC can store data in external storage. For a
classroom demonstration, a local folder can be used instead of S3/GCS.

Create a remote:

```powershell
mkdir ..\dvc-storage
dvc remote add -d localremote ..\dvc-storage
git add .dvc/config
git commit -m "Configure local DVC remote"
```

Push:

```powershell
dvc push
```

Pull later:

```powershell
dvc pull
```

## Core idea

Git versions the small `.dvc` pointer file.

DVC versions the actual dataset.

So the workflow is:

```text
Original diabetes.csv
        |
        v
   dvc add
        |
        v
diabetes.csv.dvc  ---> DVC cache
        |
        v
   git commit
        |
        v
      v1.0
        |
   modify dataset
        |
        v
   dvc add again
        |
        v
new diabetes.csv.dvc
        |
        v
   git commit
        |
        v
      v2.0
        |
        v
git checkout v1.0
        |
        v
  dvc checkout
        |
        v
Version 1 dataset restored
```
