# Script PowerShell para rodar e reiniciar frontend e backend juntos

# Inicia os processos e guarda os objetos para controle em variáveis globais
$global:backendProc = Start-Process powershell -ArgumentList 'cd backend; npm run dev' -WindowStyle Minimized -PassThru
$global:llamaProc = Start-Process powershell -ArgumentList 'cd backend; node llama.js' -WindowStyle Minimized -PassThru
$global:frontendProc = Start-Process powershell -ArgumentList 'cd frontend; npm run dev' -WindowStyle Minimized -PassThru

Write-Host "`n========================================="
Write-Host "AgenteIAQA iniciado! Acesse em:"
Write-Host "- Frontend React:       http://localhost:5173"
Write-Host "- Backend Express API:  http://localhost:8000"
Write-Host "- Backend Llama (IA):   http://localhost:8001/llama"
Write-Host "========================================="
Write-Host "Pressione 'r' para reiniciar todos os servidores..."

while ($true) {
    $key = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    if ($key.Character -eq 'r') {
        Write-Host "`nReiniciando os servidores..."
        Stop-Process -Id $global:backendProc.Id -Force
        Stop-Process -Id $global:llamaProc.Id -Force
        Stop-Process -Id $global:frontendProc.Id -Force
        
        Start-Sleep -Seconds 2  # Aguarda 2 segundos para encerrar
        
        $global:backendProc = Start-Process powershell -ArgumentList 'cd backend; npm run dev' -WindowStyle Minimized -PassThru
        $global:llamaProc = Start-Process powershell -ArgumentList 'cd backend; node llama.js' -WindowStyle Minimized -PassThru
        $global:frontendProc = Start-Process powershell -ArgumentList 'cd frontend; npm run dev' -WindowStyle Minimized -PassThru
        
        Write-Host "Servidores reiniciados! Pressione 'r' para reiniciar novamente."
    }
}
