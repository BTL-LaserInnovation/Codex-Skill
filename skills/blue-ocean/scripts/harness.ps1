# Thin Windows PowerShell 5.1 / PowerShell 7 entry point; arguments match harness.py.
# Example: .\harness.ps1 status --project-root D:\Projects\Product
$ErrorActionPreference = 'Stop'
$scriptPath = Join-Path $PSScriptRoot 'harness.py'
& python $scriptPath @args
exit $LASTEXITCODE
