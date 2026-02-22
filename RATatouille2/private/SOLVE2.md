

Q1: The malware uses a specific prefix for its Registry keys and file paths to hide them from the user and system tools (Stealth Mode). What is this prefix?
    $nya

Q2: This stealth technique is based on a well-known open-source Rootkit project. Provide the opensource link to the original malware is based on.
    https://github.com/bytecode77/r77-rootkit

Q3: The malware drops a malicious binary that masquerades as a legitimate system driver to blend in. What is the filename and extension of this dropped file?  filename.extension
    ACPIx86.sys

Q4: In which Registry Key path does the malware store the configuration for the files it is hiding?
    HKEY_LOCAL_MACHINE\SOFTWARE\$nya-config\paths

Q5: What is the specific family name of this malware?
    Onimai


https://www.virustotal.com/gui/file/711694573dc5f812f09e0cfe70437b1fceceace3644e316559ddc15af7695506/behavior

https://app.any.run/tasks/0d1eacad-c683-4d4b-b591-915cb2d3f5b7

https://hybrid-analysis.com/sample/711694573dc5f812f09e0cfe70437b1fceceace3644e316559ddc15af7695506/692f6204644820301701c3a6

https://hunt.io/malware-families/onimai

https://www.securonix.com/blog/analyzing-obscurebat-threat-actors-lure-victims-into-executing-malicious-batch-scripts-to-deploy-stealthy-rootkits/

```

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
#comanda de sus este executata separat in powershell pentru a avea acces la a rula scriptul de mai jos.


function Decrypt-AES($Base64Input) {
    $AesObject = [System.Security.Cryptography.Aes]::Create()
    $AesObject.Mode = [System.Security.Cryptography.CipherMode]::CBC
    $AesObject.Padding = [System.Security.Cryptography.PaddingMode]::PKCS7
    $AesObject.Key = [System.Convert]::FromBase64String("XPtZOUHY5OeenWFPBw1yCsPCGanSXRbZFoEprI16QF8=")
    $AesObject.IV  = [System.Convert]::FromBase64String("FRxUQwvJ84LwrFZMYH8pPg==")
    $Decryptor = $AesObject.CreateDecryptor()
    $DecryptedBytes = $Decryptor.TransformFinalBlock($Base64Input, 0, $Base64Input.Length)
    $Decryptor.Dispose()
    $AesObject.Dispose()
    return $DecryptedBytes
}

function Decompress-GZip($CompressedBytes) {
    $InputStream = New-Object System.IO.MemoryStream(,$CompressedBytes)
    $OutputStream = New-Object System.IO.MemoryStream
    $GZipStream = New-Object System.IO.Compression.GZipStream($InputStream, [System.IO.Compression.CompressionMode]::Decompress)
    $GZipStream.CopyTo($OutputStream)
    $GZipStream.Dispose()
    $InputStream.Dispose()
    $OutputStream.Dispose()
    return $OutputStream.ToArray()
}

$SourceFile = "<fisierul_ce_contine_ultimu_payload>" 
if (-not (Test-Path $SourceFile)) {
    Write-Error "Could not find $SourceFile"
    exit
}

Write-Host "Reading $SourceFile..." -ForegroundColor Cyan
$FileContent = [System.IO.File]::ReadAllText($SourceFile)
$PayloadRaw = $null
foreach ($Line in $FileContent -split [Environment]::NewLine) {
    if ($Line.StartsWith('AYWeD')) {
        $PayloadRaw = $Line.Substring(5) 
            break
    }
}

if (-not $PayloadRaw) {
    Write-Error "Could not find the payload marker 'AYWeD' in the file."
    exit
}

$PayloadParts = $PayloadRaw -split '\\'
Write-Host "Found $( $PayloadParts.Count ) payload stages." -ForegroundColor Cyan

for ($i = 0; $i -lt $PayloadParts.Count; $i++) {
    Write-Host "Processing Stage $($i + 1)..." -NoNewline
    
    try {
        $CleanString = $PayloadParts[$i].Replace("#", "/").Replace("@", "A")
        $Bytes = [System.Convert]::FromBase64String($CleanString)
        $Decrypted = Decrypt-AES $Bytes
        $FinalBytes = Decompress-GZip $Decrypted
        $OutputFile = "Stage$($i + 1).bin"
        [System.IO.File]::WriteAllBytes($OutputFile, $FinalBytes)
        Write-Host " Saved to $OutputFile" -ForegroundColor Green
    }
    catch {
        Write-Host " Failed!" -ForegroundColor Red
        Write-Error $_
    }
}

Write-Host "`nExtraction Complete." -ForegroundColor Yellow
```