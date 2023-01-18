* Define Windows "DNS hostnames" that refer to the "WSL IP address" (dynamic)

* WHY? To be able to use DNS hostnames e.g. in a browser that maps to the (dynamic) "WSL IP address".
  * NOTE: The "WSL IP address" changes between each shutdown of WSL.

** Prevent auto-generation of `/etc/hosts` by Windows

* => Add the following to `/etc/wsl.conf`:

```bash
  [network]
  generateHosts = false
```

* Restart WSL, run from Powershell: `$ wsl --shutdown`

** ALTERNATIVE 1: Use "localhost" or "127.0.0.1" from Windows

* One can use "localhost" or "127.0.0.1" to access WSL from Windows (e.g. a browser).

** ALTERNATIVE 2: Use the "WSL2 Host" service

* Repo: <https://github.com/shayne/go-wsl2-host>
  * "Automatically update your Windows hosts file with the WSL2 VM IP address"
  
* TASK: Maps "Windows hostnames" to the volatile "WSL IP address"
  * Service writes mappings into the Windows "hosts" file.
  * NOTE: The "WSL IP address" changes after: `$ wsl --shutdown` (and probably after each Windows restart)

* NOTE: Windows "DNS hostnames" are mapped to "IP addresses" in file: `C:\Windows\System32\Drivers\etc\hosts`

* USEFUL: To get WSL's current IP address, run: `> wsl hostname -I` in Powershell.

* INSTALL "wsl2host" service on Windows:
  * Download the latest "wsl2host.exe": 
    * <https://github.com/shayne/go-wsl2-host/releases/tag/v0.3.5>
  * Move it to `c:\temp\`
 
  * Install it from an elevated PowerShell: `> .\wsl2host.exe install`
  * It asks for user and password (can be fixed later)

* Fix the login of the "WSL2 Host" service:
  * Open the "Services" application in Windows.
  * Open Properties of the "WS2 Host" service. 
  * Set "Logon" to "Use Local System account instead".
    * NB! Your local logged on user needs to have rights to run Local Services.
  * Stop and Start the service.

* Generate the mapping to "ubuntu.wsl" in the Windows "hosts" file
  * From elevated Powershell run: `.\wsl2host.exe debug`
  * Press "Ctrl+C" (stops it).
  * Check if the mapping has been added to Windows "hosts" file:
    * `172.22.206.86 ubuntu.wsl    * managed by wsl2-host`

* Finally: Verify that the "WSL2 Host" service is working by running `$ ping ubuntu.wsl`

* DEBUGGING:
  * If the line was not added it might help to run: `.\wsl2host.exe start`
  * ALso make sure these 2 lines are not commented out in the "hosts" file:
  
    ```bash
      127.0.0.1       localhost
      ::1             localhost
    ```

## ALIASES: Map Windows "DNS hostnames" to the "WSL IP address"

* NiCE: Aliases is supported by the "WSL2 Host" service.

* NOTE: Needed because "aliases" (host to host mappings) are NOT allowed in the Windows "hosts" file.

* See solution here: <https://github.com/shayne/go-wsl2-host>
* Specifying aliases that point to your WSL2 VM IP. 

* => In WSL create the `~/.wsl2hosts` file.
* Add only 1 line where alle "alias" hostnames are space separated, e.g.:
  * `some.client.local my-app.local ubuntu.wsl`
* NOTE: DO not use comments (#) in the file!!

* The mappings from  `~/.wsl2hosts` will be automatically added to the Windows "hosts" file. Typically: 
  * NOTE: Probably needs a restart of the "WSL2 Host" service.

* => Typical lines added to `C:\Windows\System32\Drivers\etc\hosts`:

  ```bash
  172.22.206.86 ubuntu.wsl    * managed by wsl2-host
  172.22.206.86 mp3converter.com    * alias: Ubuntu; managed by wsl2-host
  172.22.206.86 rabbitmq-manager.com    * alias: Ubuntu; managed by wsl2-host
  ```