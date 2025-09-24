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

Write-Host "🛡️ Защита от префикса 'qс' активирована" -ForegroundColor Green
