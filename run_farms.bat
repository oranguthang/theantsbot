FOR /F "tokens=*" %%A IN (devices.txt) DO (
  START "" "C:\Program Files\BlueStacks_nxt\HD-Player.exe" --instance %%A --cmd launchApp --package "com.star.union.planetant"
  TIMEOUT 15
)
