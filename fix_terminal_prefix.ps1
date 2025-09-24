# PowerShell скрипт для исправления префикса "qс"
# Запустите от имени администратора

Write-Host "🔧 ИСПРАВЛЕНИЕ ПРЕФИКСА 'qс' В ТЕРМИНАЛЕ" -ForegroundColor Green
Write-Host "=" * 50

# Проверяем права администратора
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "❌ Скрипт должен быть запущен от имени администратора!" -ForegroundColor Red
    Write-Host "🔧 Щелкните правой кнопкой на PowerShell и выберите 'Запуск от имени администратора'" -ForegroundColor Yellow
    Read-Host "Нажмите Enter для выхода"
    exit 1
}

Write-Host "✅ Скрипт запущен от имени администратора" -ForegroundColor Green

# Создаем резервную копию профиля PowerShell
$profilePath = $PROFILE
if (Test-Path $profilePath) {
    $backupPath = "$profilePath.backup.$(Get-Date -Format 'yyyyMMdd_HHmmss')"
    Copy-Item $profilePath $backupPath
    Write-Host "✅ Резервная копия профиля создана: $backupPath" -ForegroundColor Green
    
    # Проверяем содержимое профиля
    $content = Get-Content $profilePath -Raw
    if ($content -match 'qс') {
        Write-Host "⚠️ Найден префикс 'qс' в профиле PowerShell" -ForegroundColor Yellow
        $newContent = $content -replace 'qс', ''
        Set-Content $profilePath $newContent -Encoding UTF8
        Write-Host "✅ Префикс 'qс' удален из профиля" -ForegroundColor Green
    } else {
        Write-Host "✅ Префикс 'qс' не найден в профиле" -ForegroundColor Green
    }
} else {
    Write-Host "ℹ️ Профиль PowerShell не существует" -ForegroundColor Cyan
}

# Проверяем переменные окружения
Write-Host "`n🔍 Проверка переменных окружения..." -ForegroundColor Cyan
$envVars = @('PSModulePath', 'PATH', 'PSExecutionPolicyPreference', 'PSExecutionPolicy')
foreach ($var in $envVars) {
    $userValue = [Environment]::GetEnvironmentVariable($var, 'User')
    $machineValue = [Environment]::GetEnvironmentVariable($var, 'Machine')
    
    if ($userValue -and $userValue -match 'qс') {
        Write-Host "⚠️ Найден префикс 'qс' в переменной $var (User)" -ForegroundColor Yellow
        $newValue = $userValue -replace 'qс', ''
        [Environment]::SetEnvironmentVariable($var, $newValue, 'User')
        Write-Host "✅ Переменная $var (User) исправлена" -ForegroundColor Green
    }
    
    if ($machineValue -and $machineValue -match 'qс') {
        Write-Host "⚠️ Найден префикс 'qс' в переменной $var (Machine)" -ForegroundColor Yellow
        $newValue = $machineValue -replace 'qс', ''
        [Environment]::SetEnvironmentVariable($var, $newValue, 'Machine')
        Write-Host "✅ Переменная $var (Machine) исправлена" -ForegroundColor Green
    }
}

# Проверяем реестр
Write-Host "`n🔍 Проверка реестра Windows..." -ForegroundColor Cyan
$regKeys = @(
    'HKCU:\Software\Microsoft\PowerShell',
    'HKLM:\SOFTWARE\Microsoft\PowerShell',
    'HKCU:\Console',
    'HKCU:\Software\Microsoft\Command Processor'
)

foreach ($key in $regKeys) {
    if (Test-Path $key) {
        try {
            $values = Get-ItemProperty -Path $key -ErrorAction SilentlyContinue
            if ($values) {
                $values.PSObject.Properties | ForEach-Object {
                    if ($_.Value -and $_.Value.ToString() -match 'qс') {
                        Write-Host "⚠️ Найден префикс 'qс' в реестре: $key\$($_.Name)" -ForegroundColor Yellow
                        $newValue = $_.Value.ToString() -replace 'qс', ''
                        Set-ItemProperty -Path $key -Name $_.Name -Value $newValue -ErrorAction SilentlyContinue
                        Write-Host "✅ Значение в реестре исправлено" -ForegroundColor Green
                    }
                }
            }
        } catch {
            # Игнорируем ошибки доступа к реестру
        }
    }
}

# Создаем временную защиту - обработчик Enter
Write-Host "`n🛡️ Создание временной защиты..." -ForegroundColor Cyan
$protectionScript = @'
# Временная защита от префикса "qс"
function global:prompt {
    $originalPrompt = "PS $($executionContext.SessionState.Path.CurrentLocation)$('>' * ($nestedPromptLevel + 1)) "
    
    # Проверяем, есть ли префикс "qс" в команде
    $command = (Get-History -Count 1).CommandLine
    if ($command -and $command.StartsWith('qс')) {
        Write-Host "⚠️ Обнаружен префикс 'qс' в команде: $command" -ForegroundColor Yellow
        Write-Host "🔧 Выполняю команду без префикса..." -ForegroundColor Cyan
        $cleanCommand = $command.Substring(2)  # Убираем "qс"
        Invoke-Expression $cleanCommand
        return $originalPrompt
    }
    
    return $originalPrompt
}
'@

$protectionPath = "$env:TEMP\terminal_protection.ps1"
$protectionScript | Out-File -FilePath $protectionPath -Encoding UTF8
Write-Host "✅ Временная защита создана: $protectionPath" -ForegroundColor Green

# Перезагружаем переменные окружения
Write-Host "`n🔄 Перезагрузка переменных окружения..." -ForegroundColor Cyan
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

Write-Host "`n✅ ИСПРАВЛЕНИЕ ЗАВЕРШЕНО!" -ForegroundColor Green
Write-Host "🔄 РЕКОМЕНДАЦИИ:" -ForegroundColor Yellow
Write-Host "1. Перезапустите терминал (закройте и откройте заново)" -ForegroundColor White
Write-Host "2. Проверьте команды: echo ok, python --version" -ForegroundColor White
Write-Host "3. Если проблема остается, запустите: . $env:TEMP\terminal_protection.ps1" -ForegroundColor White
Write-Host "`n📁 Резервные копии созданы в папке профиля PowerShell" -ForegroundColor Cyan

Read-Host "Нажмите Enter для выхода"

