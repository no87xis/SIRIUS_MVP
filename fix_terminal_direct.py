#!/usr/bin/env python3
"""
Прямое исправление префикса "qс" в терминале через Python
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
import winreg

def backup_file(file_path, backup_suffix=".backup"):
    """Создание резервной копии файла"""
    if Path(file_path).exists():
        backup_path = f"{file_path}{backup_suffix}"
        shutil.copy2(file_path, backup_path)
        print(f"   ✅ Резервная копия создана: {backup_path}")
        return backup_path
    return None

def fix_powershell_profile():
    """Исправление профиля PowerShell"""
    print("🔍 Проверка профиля PowerShell...")
    
    # Возможные пути к профилю
    profile_paths = [
        os.path.expanduser("~\\Documents\\WindowsPowerShell\\Microsoft.PowerShell_profile.ps1"),
        os.path.expanduser("~\\Documents\\PowerShell\\Microsoft.PowerShell_profile.ps1"),
        os.path.expanduser("~\\AppData\\Roaming\\Microsoft\\Windows\\PowerShell\\Microsoft.PowerShell_profile.ps1")
    ]
    
    for profile_path in profile_paths:
        if Path(profile_path).exists():
            print(f"   📁 Найден профиль: {profile_path}")
            
            try:
                with open(profile_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if 'qс' in content:
                    print("   ⚠️ Найден префикс 'qс' в профиле")
                    backup_file(profile_path)
                    
                    # Удаляем префикс "qс"
                    new_content = content.replace('qс', '')
                    
                    with open(profile_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    
                    print("   ✅ Профиль PowerShell исправлен")
                    return True
                else:
                    print("   ✅ Префикс 'qс' не найден в профиле")
            except Exception as e:
                print(f"   ❌ Ошибка обработки профиля: {e}")
        else:
            print(f"   ❌ Профиль не найден: {profile_path}")
    
    return False

def fix_environment_variables():
    """Исправление переменных окружения"""
    print("🔍 Проверка переменных окружения...")
    
    env_vars = ['PATH', 'PSModulePath', 'PSExecutionPolicyPreference']
    fixed_vars = []
    
    for var in env_vars:
        try:
            # Проверяем пользовательские переменные
            user_value = os.environ.get(var, '')
            if 'qс' in user_value:
                print(f"   ⚠️ Найден префикс 'qс' в переменной {var} (User)")
                
                # Создаем резервную копию
                backup_file(f"env_{var}_user.txt", f".backup_{var}_user")
                with open(f"env_{var}_user.txt", 'w') as f:
                    f.write(user_value)
                
                # Очищаем переменную
                new_value = user_value.replace('qс', '')
                os.environ[var] = new_value
                
                # Устанавливаем через setx
                try:
                    subprocess.run(['setx', var, new_value], check=True, capture_output=True)
                    print(f"   ✅ Переменная {var} (User) исправлена")
                    fixed_vars.append(f"{var} (User)")
                except:
                    print(f"   ⚠️ Не удалось установить переменную {var} через setx")
            
            # Проверяем системные переменные
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, f"SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment") as key:
                    machine_value = winreg.QueryValueEx(key, var)[0]
                    if 'qс' in machine_value:
                        print(f"   ⚠️ Найден префикс 'qс' в переменной {var} (Machine)")
                        
                        # Создаем резервную копию
                        backup_file(f"env_{var}_machine.txt", f".backup_{var}_machine")
                        with open(f"env_{var}_machine.txt", 'w') as f:
                            f.write(machine_value)
                        
                        # Очищаем переменную
                        new_value = machine_value.replace('qс', '')
                        
                        # Устанавливаем через setx с /M
                        try:
                            subprocess.run(['setx', var, new_value, '/M'], check=True, capture_output=True)
                            print(f"   ✅ Переменная {var} (Machine) исправлена")
                            fixed_vars.append(f"{var} (Machine)")
                        except:
                            print(f"   ⚠️ Не удалось установить переменную {var} через setx /M")
            except:
                pass  # Переменная не найдена в реестре
                
        except Exception as e:
            print(f"   ❌ Ошибка обработки переменной {var}: {e}")
    
    return fixed_vars

def fix_registry():
    """Исправление реестра Windows"""
    print("🔍 Проверка реестра Windows...")
    
    registry_keys = [
        (winreg.HKEY_CURRENT_USER, "Software\\Microsoft\\PowerShell"),
        (winreg.HKEY_CURRENT_USER, "Console"),
        (winreg.HKEY_CURRENT_USER, "Software\\Microsoft\\Command Processor")
    ]
    
    fixed_keys = []
    
    for hkey, subkey in registry_keys:
        try:
            with winreg.OpenKey(hkey, subkey) as key:
                i = 0
                while True:
                    try:
                        name, value, _ = winreg.EnumValue(key, i)
                        if isinstance(value, str) and 'qс' in value:
                            print(f"   ⚠️ Найден префикс 'qс' в реестре: {subkey}\\{name}")
                            
                            # Создаем резервную копию
                            backup_file(f"reg_{subkey.replace('\\', '_')}_{name}.txt", f".backup_reg")
                            with open(f"reg_{subkey.replace('\\', '_')}_{name}.txt", 'w') as f:
                                f.write(value)
                            
                            # Очищаем значение
                            new_value = value.replace('qс', '')
                            winreg.SetValueEx(key, name, 0, winreg.REG_SZ, new_value)
                            
                            print(f"   ✅ Значение в реестре исправлено: {subkey}\\{name}")
                            fixed_keys.append(f"{subkey}\\{name}")
                        i += 1
                    except OSError:
                        break
        except FileNotFoundError:
            print(f"   ℹ️ Ключ реестра не найден: {subkey}")
        except Exception as e:
            print(f"   ❌ Ошибка обработки реестра {subkey}: {e}")
    
    return fixed_keys

def fix_vscode_config():
    """Исправление конфигурации VS Code"""
    print("🔍 Проверка конфигурации VS Code...")
    
    vscode_files = [
        ".vscode/settings.json",
        ".vscode/tasks.json",
        ".vscode/launch.json",
        ".vscode/extensions.json"
    ]
    
    fixed_files = []
    
    for file_path in vscode_files:
        if Path(file_path).exists():
            print(f"   📁 Найден файл: {file_path}")
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if 'qс' in content:
                    print(f"   ⚠️ Найден префикс 'qс' в {file_path}")
                    backup_file(file_path)
                    
                    # Удаляем префикс "qс"
                    new_content = content.replace('qс', '')
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    
                    print(f"   ✅ {file_path} исправлен")
                    fixed_files.append(file_path)
                else:
                    print(f"   ✅ Префикс 'qс' не найден в {file_path}")
            except Exception as e:
                print(f"   ❌ Ошибка обработки {file_path}: {e}")
        else:
            print(f"   ❌ Файл не найден: {file_path}")
    
    return fixed_files

def create_protection_script():
    """Создание скрипта защиты"""
    print("🛡️ Создание скрипта защиты...")
    
    protection_script = '''# Временная защита от префикса "qс"
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
'''
    
    protection_path = "terminal_protection.ps1"
    with open(protection_path, 'w', encoding='utf-8') as f:
        f.write(protection_script)
    
    print(f"   ✅ Скрипт защиты создан: {protection_path}")

def main():
    """Основная функция исправления"""
    print("🔧 ПРЯМОЕ ИСПРАВЛЕНИЕ ПРЕФИКСА 'qс' В ТЕРМИНАЛЕ")
    print("=" * 60)
    
    # Проверяем права администратора
    try:
        import ctypes
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
        if not is_admin:
            print("⚠️ Рекомендуется запустить от имени администратора для полного исправления")
    except:
        pass
    
    # Выполняем исправления
    fixes = [
        ("Профиль PowerShell", fix_powershell_profile),
        ("Переменные окружения", fix_environment_variables),
        ("Реестр Windows", fix_registry),
        ("Конфигурация VS Code", fix_vscode_config)
    ]
    
    results = {}
    
    for fix_name, fix_func in fixes:
        print(f"\n📋 {fix_name}...")
        try:
            result = fix_func()
            results[fix_name] = result
        except Exception as e:
            print(f"   ❌ Ошибка в {fix_name}: {e}")
            results[fix_name] = False
    
    # Создаем скрипт защиты
    create_protection_script()
    
    # Выводим результаты
    print("\n" + "=" * 60)
    print("📊 РЕЗУЛЬТАТЫ ИСПРАВЛЕНИЯ:")
    
    for fix_name, result in results.items():
        if result:
            if isinstance(result, list) and result:
                print(f"   ✅ {fix_name}: исправлено {len(result)} элементов")
            elif isinstance(result, bool) and result:
                print(f"   ✅ {fix_name}: исправлено")
            else:
                print(f"   ✅ {fix_name}: проверено, проблем не найдено")
        else:
            print(f"   ❌ {fix_name}: ошибка или проблемы не найдены")
    
    print("\n🛡️ СКРИПТ ЗАЩИТЫ:")
    print("   ✅ terminal_protection.ps1 создан")
    
    print("\n🔄 РЕКОМЕНДАЦИИ:")
    print("1. Перезапустите терминал (закройте и откройте заново)")
    print("2. Проверьте команды: echo ok, python --version")
    print("3. Если проблема остается, запустите: .\\terminal_protection.ps1")
    print("4. При необходимости перезагрузите компьютер")
    
    print("\n📁 Резервные копии созданы в текущей папке")
    
    return True

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
        sys.exit(1)



