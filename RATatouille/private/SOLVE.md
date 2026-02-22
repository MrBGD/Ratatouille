RATatouille

Q1:The malware verifies if it was launched with a specific secret argument. If the argument is missing, it relaunches itself using that key to hide its execution. What is the value of this argument? 
Answer: HCPrMNUTufgxpxMSH

Q2:To evade analysis, the malware checks for specific hardware to ensure it is running on a real victim's machine. What Disk Model and Drive Letter does it check for? Format: "disk_model, drive_letter:"
Answer: WDS100T2B0A, F:

Q3:Provide the list of strings the malware searches for to detect if it is running inside a Virtual Machine. Format: "string1 string2"
Answer: QEMU DADY VirtualBox BOCHS_ BXPC___

Q4:The loader uses AES encryption to unpack the payload. Provide the Key, the IV (in Base64), and the Cipher Mode used. Format: "key IV mode"
Answer: XPtZOUHY5OeenWFPBw1yCsPCGanSXRbZFoEprI16QF8= FRxUQwvJ84LwrFZMYH8pPg== CBC

Q5:The malware achieves persistence or stores its configuration in the Windows Registry. What is the full Registry path used?
Answer: HKLM:\SOFTWARE\OOhhhm=

Q6:In the deobfuscated PowerShell script, what is the original name of the function responsible for loading the final .NET payload into memory? 
Answer: Acwq


Dupa ce ti ai creat o masina virtuala, cu un IDE sau orice text editor(spre ex sublime), si deschizi fisierul o sa observi pe prima linie un @echo off urmat de o tona de stringuri random asf si la final un payload imens.
Ultimul payload nu te atingi de el, il poti ignora chiar sterge, acolo sunt alte 3 sampleuri de malware dropate de scriptul obvuscat, asa ca ai grija. 

Daca analizezi prima parte din fisier ai sa observi niste stringuri care iau valoarile {'s','e','t'}
dupa ce le dai replace all codul prinde usor usor forma. 

Pe urma incepi sa observi ca fiecare instructie set contine un prim string random si apoi cate 3 exact la fel. acele 3 stringuri trebuiesc sterse ca sa ramai cu o instructie clean unde fiecare string primeste o valoare diferita. 
set "ybSlHVTKzh%UKFYJUsuigkBCjUfnelOqOJWbRCdsLXjUBAPyjkCfos%=%UKFYJUsuigkBCjUfnelOqOJWbRCdsLXjUBAPyjkCfos%=%UKFYJUsuigkBCjUfnelOqOJWbRCdsLXjUBAPyjkCfos%" devine set "ybSlHVTKzh==" unde "ybSlHVTKzh" are valoare =. le pastrezi asa cum sunt, te vor ajuta sa decodezi niste payloaduri mai tarziu.

La fel, mai sunt instructiun set unde caractere cu caractere sunt imprastiate printre "garbage" sunt forma %string%. este important sa le elimini folosind un regex de tipul: %[a-zA-Z0-9_]{<val>,}% unde <val> poate sa fie o valoare +20, sau depinde in functie de cate mare sau mic mai este garbageul. INSA FOARTE IMPORTANT, LEGAT DE URMATOAREA FAZA:
A 2 chestie importanta e sa observi ca sunt anumite lini unde instructiunea set este lipsa. aceleasi sunt piesele principale din payloadul final. trebuiesc luate separat SI SALVATE INTR UN FISIER NOU, in aceeasi ordine ca in malware, ai nevoie sa le regrupezi cu set-urile curate. DACA DAI REGEX CU INSTRUCTIUNILE PIERZI INTREGUL PAYLOAD DEOARECE IL IA CA GARBAGE.

Next, dupa ce ai curatat intructiunile set, trebuie sa grupezi fiecare chunck de set cu ceea ce ai obtinut anterior si intr-un fisier .bat, iei chunk cu chunk si ii salvezi output ul. EX: 


```
@echo off
setlocal EnableDelayedExpansion

set "pcZSBETvygCuFpibPhZsI=n"
set "qJJssEVOxDgTCvvRUCQIq=x"
<continuare comenzi set>

echo "!AnWNulONQkXxHHPkSSxdWe!!FYdDMQpenWUmsRAxojSHd!!baoxPwiKFUPfsUkaNzYj!!wkDKocoWwbjLXNdfxHFV!!CfZZyeUcyoGibCYy!!RUovjKBHNgaacPdl!!IGiWfWRprDFkIHSLMk<restul_stringului>!SBKbayPRMpuzzJzcSbxKGzS!" > test.txt
```


ALT LUCRU IMPORTANT. LA STRINGURILE SALVATE ANTERIOR TREBUIE DAT REPLACE LA % CU !, altfel nu iti va functiona si risti sa "executi" acea functie/payload


daca ai facut corect, la final primul chucnk trebuie sa iti afiseze asta:

```
@echo off

"if "" neq "HCPrMNUTufgxpxMSH" ( if /i "C:<redacted>" neq "C:<redacted>\" powershell -windowstyle hidden -command "Start-Process -FilePath 'C:<redacted>\<nume>.bat' -ArgumentList 'HCPrMNUTufgxpxMSH' -WindowStyle Hidden" & exit )" 
```

dupa ce se repeta pt fiecare chunk (cred merge si o automatizare, i haven`t tried), la final ai tot codul de powershell deobfuscat.

urmeaza part2 cu malware ul dropat de loader.