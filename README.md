# Speedo Meter

### Core Features
1. **Network Monitoring**:
   - Tracks real-time download/upload speeds using `psutil`
   - Updates displayed speeds every second
   - Formats speeds as Kbps/Mbps

2. **Taskbar Integration**:
   - Automatically positions itself above the taskbar
   - Matches taskbar background color dynamically
   - Adjusts position when taskbar size changes

3. **Smart Visibility**:
   - Window becomes transparent when mouse hovers over it
   - Reappears when mouse moves away
   - Starts semi-transparent (85% opacity)

4. **Window Behavior**:
   - Borderless, always-on-top window
   - Click-through (doesn't block interactions)
   - No taskbar entry (tool window style)
   - Removed minimize capability

### Key Components
- **Background Thread**: Handles speed calculations
- **Color Sampling**: Uses `pyautogui` to detect taskbar color
- **Windows API**: Modifies window properties via `ctypes`
- **Dynamic Positioning**: Auto-adjusts based on text width and taskbar height

### User Experience
Displays a clean label showing:
`↓ [Download Speed] ↑ [Upload Speed]`
(e.g., `↓ 45 Mbps ↑ 3.2 Mbps`)

The window hides itself when you try to interact with the area it occupies, then reappears when you move the mouse away, making it non-intrusive while providing constant network monitoring.
