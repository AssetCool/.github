param([switch]$DryRun)

$ORG = "AssetCool"  # org login/slug
$gh  = "C:\Program Files\GitHub CLI\gh.exe"

$labels = @(
  @{
    Name  = "epic"
    Color = "b7510d"
    Desc  = "A multi-sprint outcome delivered through multiple Features"
  },
  @{
    Name  = "feature"
    Color = "0a2eef"
    Desc  = "A deliverable slice of an Epic (or standalone) that can be shipped"
  },
  @{
    Name  = "task"
    Color = "e6d0bf"
    Desc  = "A concrete unit of implementation work (sub-issue of a Feature)"
  }
)

& $gh repo list $ORG --limit 1000 --private --json nameWithOwner --jq '.[].nameWithOwner' |
ForEach-Object {
  $REPO = $_

  foreach ($l in $labels) {
    $name  = $l.Name
    $color = $l.Color
    $desc  = $l.Desc

    # Check if label exists
    & $gh api "/repos/$REPO/labels/$name" *> $null
    if ($LASTEXITCODE -eq 0) {
      Write-Host "SKIP  $REPO (label '$name' exists)"
      continue
    }

    if ($DryRun) {
      Write-Host "[DRY RUN] ADD   $REPO (would create label '$name')"
      continue
    }

    Write-Host "ADD   $REPO (creating label '$name')"
    & $gh api -X POST "/repos/$REPO/labels" -f name="$name" -f color="$color" -f description="$desc"

    if ($LASTEXITCODE -ne 0) {
      Write-Host "FAIL  $REPO (could not create label '$name' - likely no access / token scope / SSO)"
    }
  }
}
