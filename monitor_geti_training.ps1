param(
    [string]$OutputPath = (Join-Path ([Environment]::GetFolderPath("Desktop")) "geti-training-utilization.csv"),
    [int]$IntervalSeconds = 5
)

    $processOutputPath = [IO.Path]::Combine(
        [IO.Path]::GetDirectoryName($OutputPath),
        ([IO.Path]::GetFileNameWithoutExtension($OutputPath) + "-processes.csv")
    )
$outputDirectory = Split-Path -Parent $OutputPath
if ($outputDirectory) {
    New-Item -ItemType Directory -Force -Path $outputDirectory | Out-Null
}

"Timestamp,CPU_Percent,Available_RAM_MB,Pagefile_Percent,Disk_Bytes_PerSec" |
    Set-Content -Path $OutputPath

    "Timestamp,ProcessName,PID,CPU_Percent,WorkingSet_MB,PrivateMemory_MB,Handles,Threads" |
        Set-Content -Path $processOutputPath

Write-Host "Logging system utilization to $OutputPath"
    Write-Host "Logging process utilization to $processOutputPath"
Write-Host "Sampling every $IntervalSeconds seconds. Press Ctrl+C to stop."

    $logicalProcessorCount = [Environment]::ProcessorCount
    $previousProcessCpu = @{}

try {
    while ($true) {
        $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        $cpu = (Get-Counter '\Processor(_Total)\% Processor Time').CounterSamples.CookedValue
        $ram = (Get-Counter '\Memory\Available MBytes').CounterSamples.CookedValue
        $pagefile = (Get-Counter '\Paging File(_Total)\% Usage').CounterSamples.CookedValue
        $disk = (Get-Counter '\PhysicalDisk(_Total)\Disk Bytes/sec').CounterSamples.CookedValue

        "$timestamp,$([math]::Round($cpu,1)),$([math]::Round($ram,1)),$([math]::Round($pagefile,1)),$([math]::Round($disk,1))" |
            Add-Content -Path $OutputPath

        Start-Sleep -Seconds $IntervalSeconds

        foreach ($process in Get-Process) {
            try {
                $currentCpu = $process.TotalProcessorTime.TotalSeconds
                $cpuPercent = 0
                if ($previousProcessCpu.ContainsKey($process.Id)) {
                    $cpuPercent = (($currentCpu - $previousProcessCpu[$process.Id]) / $IntervalSeconds) * 100 / $logicalProcessorCount
                }

                $processRow = [PSCustomObject]@{
                    Timestamp = $timestamp
                    ProcessName = $process.ProcessName
                    PID = $process.Id
                    CPU_Percent = [math]::Round([math]::Max(0, $cpuPercent), 1)
                    WorkingSet_MB = [math]::Round($process.WorkingSet64 / 1MB, 1)
                    PrivateMemory_MB = [math]::Round($process.PrivateMemorySize64 / 1MB, 1)
                    Handles = $process.HandleCount
                    Threads = $process.Threads.Count
                }
                $processRow | ConvertTo-Csv -NoTypeInformation | Select-Object -Skip 1 |
                    Add-Content -Path $processOutputPath
                $previousProcessCpu[$process.Id] = $currentCpu
            }
            catch {
                continue
            }
        }
    }
}
finally {
    Write-Host "Utilization logging stopped. System CSV saved to $OutputPath"
    Write-Host "Process CSV saved to $processOutputPath"
}
