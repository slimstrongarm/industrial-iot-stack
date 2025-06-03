#!/usr/bin/expect -f
# SSH and run Docker investigation

set timeout 30
set password "LocalAccount"

spawn ssh localaccount@100.94.84.126

expect {
    "password:" {
        send "$password\r"
        expect {
            ">" {
                # We're in Windows CMD/PowerShell
                send "bash\r"
                expect "$"
            }
            "$" {
                # We're already in bash
            }
        }
    }
}

# Now run our investigation commands
send "echo '🔍 Docker & WSL Investigation'\r"
expect "$"

send "echo ''\r"
expect "$"

send "echo '📊 Checking Docker...'\r"
expect "$"

send "docker --version 2>/dev/null || echo 'Docker CLI not found'\r"
expect "$"

send "echo ''\r"
expect "$"

send "echo '🐧 Checking WSL...'\r"
expect "$"

send "wsl -l -v 2>/dev/null || cmd.exe /c 'wsl -l -v' 2>/dev/null || echo 'WSL not accessible'\r"
expect "$"

send "echo ''\r"
expect "$"

send "echo '🏃 Docker Status:'\r"
expect "$"

send "docker ps 2>/dev/null || echo 'Docker daemon not accessible'\r"
expect "$"

send "exit\r"
expect eof