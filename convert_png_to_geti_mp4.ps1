Add-Type -AssemblyName System.Windows.Forms

$ffmpeg = Get-Command ffmpeg -ErrorAction SilentlyContinue
if (-not $ffmpeg) {
    [System.Windows.Forms.MessageBox]::Show(
        "FFmpeg was not found on this computer. Install FFmpeg and add it to PATH, then run this script again.",
        "FFmpeg Required",
        [System.Windows.Forms.MessageBoxButtons]::OK,
        [System.Windows.Forms.MessageBoxIcon]::Error
    ) | Out-Null
    exit 1
}

$inputDialog = New-Object System.Windows.Forms.OpenFileDialog
$inputDialog.Title = "Select the PNG image to convert"
$inputDialog.Filter = "PNG images (*.png)|*.png"
$inputDialog.Multiselect = $false

if ($inputDialog.ShowDialog() -ne [System.Windows.Forms.DialogResult]::OK) {
    exit 0
}

$outputDialog = New-Object System.Windows.Forms.FolderBrowserDialog
$outputDialog.Description = "Select the folder for the Geti MP4 test video"

if ($outputDialog.ShowDialog() -ne [System.Windows.Forms.DialogResult]::OK) {
    exit 0
}

$inputPath = $inputDialog.FileName
$outputDirectory = $outputDialog.SelectedPath
$baseName = [IO.Path]::GetFileNameWithoutExtension($inputPath)
$outputPath = Join-Path $outputDirectory "${baseName}_geti_test.mp4"
$counter = 1

while (Test-Path -LiteralPath $outputPath) {
    $outputPath = Join-Path $outputDirectory "${baseName}_geti_test_$counter.mp4"
    $counter++
}

Write-Host "Creating a 10-second, 30-FPS MP4 for Geti..."
& $ffmpeg.Source -y -loop 1 -framerate 30 -i $inputPath -t 10 -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" -c:v libx264 -pix_fmt yuv420p -r 30 $outputPath

if ($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath $outputPath)) {
    [System.Windows.Forms.MessageBox]::Show(
        "FFmpeg could not create the MP4. Review the PowerShell output for details.",
        "Conversion Failed",
        [System.Windows.Forms.MessageBoxButtons]::OK,
        [System.Windows.Forms.MessageBoxIcon]::Error
    ) | Out-Null
    exit 1
}

Write-Host "Created: $outputPath"
[System.Windows.Forms.MessageBox]::Show(
    "Created Geti test video:`n$outputPath",
    "Conversion Complete",
    [System.Windows.Forms.MessageBoxButtons]::OK,
    [System.Windows.Forms.MessageBoxIcon]::Information
) | Out-Null