# Paths
$destination = "C:\Users\eddie\OneDrive\Documents\GitHub\ibm_imperial_qc\group_code"
$source = "C:\Users\eddie\OneDrive\Documents\GitHub\Team9-IBMQuantumAIMachine"

# Clear destination folder
Write-Host "Clearing out $destination ..."
Remove-Item "$destination\*" -Recurse -Force -ErrorAction SilentlyContinue

# Create destination folder if it doesn't exist
if (-not (Test-Path $destination)) {
    New-Item -ItemType Directory -Path $destination | Out-Null
}

# Copy everything *except* the .git folder
Write-Host "Copying contents from $source to $destination (excluding .git)..."
Get-ChildItem -Path $source -Recurse -Force |
    Where-Object { $_.FullName -notmatch '\\\.git($|\\)' } |
    ForEach-Object {
        $relativePath = $_.FullName.Substring($source.Length)
        $targetPath = Join-Path $destination $relativePath
        if ($_.PSIsContainer) {
            if (-not (Test-Path $targetPath)) {
                New-Item -ItemType Directory -Path $targetPath | Out-Null
            }
        } else {
            Copy-Item -Path $_.FullName -Destination $targetPath -Force
        }
    }

Write-Host "Sync complete (without .git)."
