param(
    [string]$VoiceName = "Microsoft Zira Desktop",
    [int]$Rate = 0,
    [string]$PidFile = "$env:USERPROFILE\.claude\voice-out\current_speech.pid"
)

# Record our own PID immediately so the stop script can kill us mid-speech.
$PID | Out-File -FilePath $PidFile -Encoding ascii -Force

try {
    Add-Type -AssemblyName System.Speech
    $synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
    try { $synth.SelectVoice($VoiceName) } catch { }
    $synth.Rate = $Rate

    $text = [Console]::In.ReadToEnd()
    if ($text.Trim().Length -gt 0) {
        $synth.Speak($text)
    }
} finally {
    if (Test-Path $PidFile) {
        $current = Get-Content $PidFile -ErrorAction SilentlyContinue
        if ($current -eq "$PID") {
            Remove-Item $PidFile -Force -ErrorAction SilentlyContinue
        }
    }
}
