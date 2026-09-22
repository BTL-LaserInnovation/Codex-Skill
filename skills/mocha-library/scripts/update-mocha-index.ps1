[CmdletBinding()]
param(
    [string]$OutputDirectory = (Join-Path $PSScriptRoot '..\references')
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Get-MochaRoot {
    $strMochaRoot = $env:PathMocha
    if (-not $strMochaRoot) {
        $strMochaRoot = [Environment]::GetEnvironmentVariable('PathMocha', 'User')
    }
    if (-not $strMochaRoot) {
        $strMochaRoot = [Environment]::GetEnvironmentVariable('PathMocha', 'Machine')
    }
    if (-not $strMochaRoot) {
        throw 'PathMocha is not set in the process, User, or Machine environment.'
    }

    $strResolvedRoot = [IO.Path]::GetFullPath($strMochaRoot).TrimEnd('\\')
    foreach ($strRequiredPath in @('include', 'src', 'all.sln')) {
        if (-not (Test-Path -LiteralPath (Join-Path $strResolvedRoot $strRequiredPath))) {
            throw "PathMocha does not contain the expected path: $strRequiredPath"
        }
    }
    return $strResolvedRoot
}

function Get-RelativePath([string]$strRoot, [string]$strPath) {
    return $strPath.Substring($strRoot.Length).TrimStart('\\').Replace('\\', '/')
}

function ConvertTo-ComponentId([string]$strValue) {
    $strId = $strValue.ToLowerInvariant() -replace '[^a-z0-9]+', '-'
    return $strId.Trim('-')
}

$strMochaRoot = Get-MochaRoot
$strOutputDirectory = [IO.Path]::GetFullPath($OutputDirectory)
New-Item -ItemType Directory -Force -Path $strOutputDirectory | Out-Null

$arrComponents = [System.Collections.Generic.List[object]]::new()
$arrRelationships = [System.Collections.Generic.List[object]]::new()
$arrFlows = [System.Collections.Generic.List[object]]::new()
$mapProjectIds = @{}

$arrComponents.Add([ordered]@{
    id = 'mocha-solution'; name = 'Mocha Solution'; kind = 'project'
    files = @('all.sln', 'common.props'); responsibilities = @('Primary Visual Studio solution and shared build properties')
})
$arrComponents.Add([ordered]@{
    id = 'public-headers'; name = 'Public Headers'; kind = 'library'
    files = @('include'); responsibilities = @('Public MFC/C++ contracts grouped by module')
})
$arrComponents.Add([ordered]@{
    id = 'project-sources'; name = 'Project Sources'; kind = 'module'
    files = @('src'); responsibilities = @('Visual C++ project implementations')
})
$arrComponents.Add([ordered]@{
    id = 'reusable-libraries'; name = 'Reusable Libraries'; kind = 'library'
    files = @('lib', 'lib.static'); responsibilities = @('Built and static library outputs')
})

$mapArea = [ordered]@{
    'mfc-utilities' = @{ name = 'MFC Utilities'; files = @('include/misc', 'include/QMisc', 'src/misc', 'src/MessageToolWnd') }
    'vision-processing' = @{ name = 'Vision Processing'; files = @('include/FrameGrabber', 'src/FrameGrabber', 'src/ImageProcessor', 'src/Vision') }
    'device-integration' = @{ name = 'Device Integration'; files = @('include/PLC', 'src/HSMS', 'src/Scanner', 'src/PLCLinker') }
    'geometry-3d' = @{ name = 'Geometry and 3D'; files = @('include/Shape', 'include/xMathUtil', 'src/Shape', 'src/3DCloudView') }
}
foreach ($objArea in $mapArea.GetEnumerator()) {
    $arrComponents.Add([ordered]@{
        id = $objArea.Key; name = $objArea.Value.name; kind = 'module'; files = $objArea.Value.files
        responsibilities = @('High-level reusable Mocha subsystem')
    })
}

$arrHeaderDirectories = Get-ChildItem -LiteralPath (Join-Path $strMochaRoot 'include') -Directory | Sort-Object Name
foreach ($objDirectory in $arrHeaderDirectories) {
    $arrFiles = Get-ChildItem -LiteralPath $objDirectory.FullName -Recurse -File |
        Where-Object { $_.Extension -in @('.h', '.hpp', '.cpp', '.cxx') } |
        ForEach-Object { Get-RelativePath $strMochaRoot $_.FullName }
    $strComponentId = "public-$(ConvertTo-ComponentId $objDirectory.Name)"
    $arrComponents.Add([ordered]@{
        id = $strComponentId; name = "Public $($objDirectory.Name)"; kind = 'library'; files = @($arrFiles)
        responsibilities = @('Public headers and colocated source for this module')
    })
    $arrRelationships.Add([ordered]@{
        from = 'public-headers'; to = $strComponentId; kind = 'contains'; label = 'module contracts'
        evidence = @((Get-RelativePath $strMochaRoot $objDirectory.FullName))
    })
}

$arrProjectFiles = Get-ChildItem -LiteralPath (Join-Path $strMochaRoot 'src') -Recurse -File -Filter '*.vcxproj' | Sort-Object FullName
foreach ($objProjectFile in $arrProjectFiles) {
    $strRelativeProjectPath = Get-RelativePath $strMochaRoot $objProjectFile.FullName
    $strProjectId = "project-$(ConvertTo-ComponentId $strRelativeProjectPath.Replace('.vcxproj', ''))"
    $mapProjectIds[$objProjectFile.FullName.ToLowerInvariant()] = $strProjectId
    $strProjectContent = Get-Content -Raw -LiteralPath $objProjectFile.FullName
    $objTypeMatch = [regex]::Match($strProjectContent, '<ConfigurationType>(?<type>[^<]+)</ConfigurationType>')
    $strConfigurationType = if ($objTypeMatch.Success) { $objTypeMatch.Groups['type'].Value } else { 'Unknown' }
    $arrComponents.Add([ordered]@{
        id = $strProjectId; name = [IO.Path]::GetFileNameWithoutExtension($objProjectFile.Name); kind = 'module'
        files = @($strRelativeProjectPath); symbols = @($strConfigurationType)
        responsibilities = @('Visual C++ project implementation')
    })
    $arrRelationships.Add([ordered]@{
        from = 'mocha-solution'; to = $strProjectId; kind = 'builds'; label = $strConfigurationType
        evidence = @('all.sln', $strRelativeProjectPath)
    })
    $arrRelationships.Add([ordered]@{
        from = $strProjectId; to = 'reusable-libraries'; kind = 'produces'; label = 'library or runtime output'
        evidence = @($strRelativeProjectPath)
    })
}

foreach ($objProjectFile in $arrProjectFiles) {
    $strSourceProjectId = $mapProjectIds[$objProjectFile.FullName.ToLowerInvariant()]
    $strProjectContent = Get-Content -Raw -LiteralPath $objProjectFile.FullName
    foreach ($objMatch in [regex]::Matches($strProjectContent, '<ProjectReference Include="(?<path>[^"]+)"')) {
        $strReferencedPath = [IO.Path]::GetFullPath((Join-Path $objProjectFile.DirectoryName $objMatch.Groups['path'].Value))
        $strTargetProjectId = $mapProjectIds[$strReferencedPath.ToLowerInvariant()]
        if ($strTargetProjectId) {
            $arrRelationships.Add([ordered]@{
                from = $strSourceProjectId; to = $strTargetProjectId; kind = 'uses'; label = 'project reference'
                evidence = @((Get-RelativePath $strMochaRoot $objProjectFile.FullName))
            })
        }
    }
}

$arrLibraryFiles = @(
    Get-ChildItem -LiteralPath (Join-Path $strMochaRoot 'lib') -Recurse -File -Filter '*.lib'
    Get-ChildItem -LiteralPath (Join-Path $strMochaRoot 'lib.static') -Recurse -File -Filter '*.lib'
) | Sort-Object FullName | ForEach-Object { Get-RelativePath $strMochaRoot $_.FullName }
$arrComponents.Add([ordered]@{
    id = 'library-files'; name = 'Available Library Files'; kind = 'library'; files = @($arrLibraryFiles)
    responsibilities = @('Concrete .lib files available for target-project integration')
})
$arrRelationships.Add([ordered]@{
    from = 'reusable-libraries'; to = 'library-files'; kind = 'contains'; label = 'built artifacts'
    evidence = @('lib', 'lib.static')
})

$arrFlows.Add([ordered]@{
    id = 'reuse-discovery'; kind = 'control'
    steps = @('public-headers', 'project-sources', 'mocha-solution', 'reusable-libraries')
})

$objIndex = [ordered]@{
    schemaVersion = '1.0'
    updatedAt = [DateTime]::UtcNow.ToString('o')
    source = [ordered]@{ diagram = 'mocha-library.mmd'; scope = 'external-repository:PathMocha'; notes = 'File paths are relative to the current PathMocha root.' }
    components = @($arrComponents)
    relationships = @($arrRelationships)
    flows = @($arrFlows)
    changeNote = 'Generated from the current PathMocha library for fast MFC/C++ reuse discovery.'
}

$strIndexPath = Join-Path $strOutputDirectory 'mocha-library.index.json'
$objIndex | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $strIndexPath -Encoding utf8

$strUpdatedAt = $objIndex.updatedAt
$strDiagram = @"
%% schemaVersion: 1.0; updatedAt: $strUpdatedAt; index: mocha-library.index.json
flowchart LR
    mocha-solution["mocha-solution<br/>all.sln"]
    public-headers["public-headers<br/>include"]
    project-sources["project-sources<br/>src"]
    reusable-libraries["reusable-libraries<br/>lib + lib.static"]
    mfc-utilities["mfc-utilities<br/>misc, QMisc"]
    vision-processing["vision-processing<br/>Vision, FrameGrabber"]
    device-integration["device-integration<br/>PLC, HSMS, Scanner"]
    geometry-3d["geometry-3d<br/>Shape, xMathUtil, 3D"]

    mocha-solution -->|builds| project-sources
    public-headers -->|contracts| mfc-utilities
    public-headers -->|contracts| vision-processing
    public-headers -->|contracts| device-integration
    public-headers -->|contracts| geometry-3d
    project-sources -->|implements| mfc-utilities
    project-sources -->|implements| vision-processing
    project-sources -->|implements| device-integration
    project-sources -->|implements| geometry-3d
    mfc-utilities -->|outputs| reusable-libraries
    vision-processing -->|outputs| reusable-libraries
    device-integration -->|outputs| reusable-libraries
    geometry-3d -->|outputs| reusable-libraries
"@
Set-Content -LiteralPath (Join-Path $strOutputDirectory 'mocha-library.mmd') -Value $strDiagram -Encoding utf8

Write-Host "Generated $strIndexPath"
Write-Host "Generated $(Join-Path $strOutputDirectory 'mocha-library.mmd')"
