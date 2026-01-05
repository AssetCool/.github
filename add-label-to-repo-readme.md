# Add Labels to All Org Repos

This PowerShell script adds standard **epic**, **feature**, and **task** GitHub labels to every repository in the `AssetCool` organization using the GitHub CLI.

## Requirements

- PowerShell
- GitHub CLI (`gh`) installed and authenticated (use an access token)
- Maintain access to the target repositories

## Usage

Dry run (no changes made):

```powershell
.\add-label-to-repo -DryRun
```

Apply changes:

```powershell
.\add-label-to-repo
```

## Notes

- Existing labels are skipped
- DryRun shows what would be created without modifying repositories