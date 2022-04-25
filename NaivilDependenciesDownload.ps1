
# Source file location
$rust = 'https://static.rust-lang.org/rustup/dist/x86_64-pc-windows-msvc/rustup-init.exe'
$python= 'https://www.python.org/ftp/python/3.11.0/python-3.11.0a7-amd64.exe'

$FolderName = "requisite-packages"
if (Test-Path $FolderName) {
   Write-Host "Folder Exists" 
}
else
{
    New-Item $FolderName -ItemType Directory
    Write-Host "requisite-packages Folder Created successfully"
}

if (Test-Path $FolderName\rustup-init.exe){
    Write-Host "Rust setup already exists!"    
}else
{
    
    Invoke-WebRequest -Uri $rust -OutFile $FolderName\rustup-init.exe
}

if (Test-Path $FolderName\python-3.11.0a7-amd64.exe){
    Write-Host "Python setup already exists!"    
}else
{
    Invoke-WebRequest -Uri $python -OutFile $FolderName\python-3.11.0a7-amd64.exe
}

if (Test-Path "C:\Users\$env:username\AppData\Local\Programs\Python\Python311\"){
    Set-Alias -Name python -Value "C:\Users\$env:username\AppData\Local\Programs\Python\Python311\python.exe"
    python -m venv tvenv
    .\tvenv\Scripts\activate
    pip install rply anytree 
}else{
    Write-Host "INSTALLING PYTHON"
    .\requisite-packages\"python-3.11.0a7-amd64.exe"
    Set-Alias -Name python -Value "C:\Users\$env:username\AppData\Local\Programs\Python\Python311\python.exe"
    python -m venv tvenv
    .\tvenv\Scripts\activate
    pip install rply anytree 
}

if (Test-Path -Path "C:\Users\Mihai\.cargo\bin"){
    Write-Host "Rust already installed!"
    cargo new mainTemplate
    cd .\mainTemplate
    cargo add num

}else{
    Write-Host "Please install Rust"
    .\requisite-packages\rustup-init.exe
    cargo new mainTemplate
    cd .\mainTemplate
    cargo add num
    
    
}
 

