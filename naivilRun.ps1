Param([Parameter(Mandatory=$True)][string]$filename)

Write-Host $filename

if (Test-Path $filename){
    if(Test-Path $filename".build")
        {rm .\$filename".build"
        New-Item $filename".build" -ItemType Directory}
    .\venv\Scripts\activate
    python.exe main.py $filename
    Get-ChildItem | Out-Null
    cd .\mainTemplate
    cargo run > $null
    rustc --emit=llvm-ir .\src\main.rs > $null
    cd ..
    cp .\mainTemplate\main.ll .\$filename".build"\
    cp .\mainTemplate\target\debug\mainTemplate.exe .\$filename".build"\$filename".exe"
    $stopwatch = New-Object System.Diagnostics.Stopwatch
    $stopwatch.Start()
    $exe = ".\"+$filename+".build\"+$filename+".exe"
    & $exe
    Write-Host $exe
    $stopwatch.Stop()
    $stopwatch
    deactivate
}