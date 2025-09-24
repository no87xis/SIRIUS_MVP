# ЭКСТРЕННОЕ ИСПРАВЛЕНИЕ ПРЕФИКСА "qс"
Write-Host "🚨 ЭКСТРЕННОЕ ИСПРАВЛЕНИЕ ПРЕФИКСА 'qс'" -ForegroundColor Red
Write-Host "========================================" -ForegroundColor Red
Write-Host ""

Write-Host "❌ ПРОБЛЕМА: Все команды получают префикс 'qс'" -ForegroundColor Yellow
Write-Host "✅ РЕШЕНИЕ: Удаляем пакет qrcode и очищаем систему" -ForegroundColor Green
Write-Host ""

# Шаг 1: Удаляем пакет qrcode
Write-Host "🔍 Шаг 1: Удаляем пакет qrcode..." -ForegroundColor Cyan
try {
    & pip uninstall qrcode -y
    & pip uninstall "qrcode[pil]" -y
    Write-Host "✅ Пакет qrcode удален" -ForegroundColor Green
} catch {
    Write-Host "⚠️ Ошибка удаления qrcode: $_" -ForegroundColor Yellow
}

Write-Host ""

# Шаг 2: Очищаем кэш pip
Write-Host "🔍 Шаг 2: Очищаем кэш pip..." -ForegroundColor Cyan
try {
    & pip cache purge
    Write-Host "✅ Кэш pip очищен" -ForegroundColor Green
} catch {
    Write-Host "⚠️ Ошибка очистки кэша: $_" -ForegroundColor Yellow
}

Write-Host ""

# Шаг 3: Очищаем переменные окружения
Write-Host "🔍 Шаг 3: Очищаем переменные окружения..." -ForegroundColor Cyan
try {
    $currentPath = [Environment]::GetEnvironmentVariable("PATH", "User")
    if ($currentPath -and $currentPath.Contains("qс")) {
        $newPath = $currentPath -replace "qс", ""
        [Environment]::SetEnvironmentVariable("PATH", $newPath, "User")
        Write-Host "✅ PATH (User) очищен от 'qс'" -ForegroundColor Green
    }
    
    $currentPath = [Environment]::GetEnvironmentVariable("PATH", "Machine")
    if ($currentPath -and $currentPath.Contains("qс")) {
        $newPath = $currentPath -replace "qс", ""
        [Environment]::SetEnvironmentVariable("PATH", $newPath, "Machine")
        Write-Host "✅ PATH (Machine) очищен от 'qс'" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠️ Ошибка очистки переменных: $_" -ForegroundColor Yellow
}

Write-Host ""

# Шаг 4: Очищаем профиль PowerShell
Write-Host "🔍 Шаг 4: Очищаем профиль PowerShell..." -ForegroundColor Cyan
$profilePaths = @(
    "$env:USERPROFILE\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1",
    "$env:USERPROFILE\Documents\PowerShell\Microsoft.PowerShell_profile.ps1",
    "$env:USERPROFILE\AppData\Roaming\Microsoft\Windows\PowerShell\Microsoft.PowerShell_profile.ps1"
)

foreach ($profilePath in $profilePaths) {
    if (Test-Path $profilePath) {
        try {
            $content = Get-Content $profilePath -Raw
            if ($content -and $content.Contains("qс")) {
                Remove-Item $profilePath -Force
                Write-Host "✅ Профиль удален: $profilePath" -ForegroundColor Green
            }
        } catch {
            Write-Host "⚠️ Ошибка обработки профиля $profilePath : $_" -ForegroundColor Yellow
        }
    }
}

Write-Host ""
Write-Host "✅ ИСПРАВЛЕНИЕ ЗАВЕРШЕНО!" -ForegroundColor Green
Write-Host ""
Write-Host "🔄 РЕКОМЕНДАЦИИ:" -ForegroundColor Cyan
Write-Host "1. Закройте ВСЕ терминалы" -ForegroundColor White
Write-Host "2. Перезапустите Cursor" -ForegroundColor White
Write-Host "3. Проверьте команды: echo ok, python --version" -ForegroundColor White
Write-Host "4. Если проблема остается - перезагрузите компьютер" -ForegroundColor White
Write-Host ""
Write-Host "Нажмите любую клавишу для продолжения..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")


