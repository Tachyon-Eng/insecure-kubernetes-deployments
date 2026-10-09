FROM ubuntu:jammy


RUN \
    apt-get update && \
    apt-get install -y wget apt-transport-https software-properties-common lsb-core && \
    wget -q "https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/packages-microsoft-prod.deb" && \
    dpkg -i packages-microsoft-prod.deb && \
    rm packages-microsoft-prod.deb && \
    apt-get update && \
    apt-get install -y powershell


RUN \
    apt-get install -y sudo make kmod gcc nmap clang iproute2 curl


RUN \
    pwsh -Command "IEX (IWR 'https://raw.githubusercontent.com/redcanaryco/invoke-atomicredteam/v2.0.0.0/install-atomicredteam.ps1' -UseBasicParsing); Install-AtomicRedTeam -getAtomics"


RUN \
    mkdir -p /root/.config/powershell && \
    echo 'Import-Module "/root/AtomicRedTeam/invoke-atomicredteam/Invoke-AtomicRedTeam.psd1" -Force' > /root/.config/powershell/profile.ps1

CMD ["sleep", "infinity"]
