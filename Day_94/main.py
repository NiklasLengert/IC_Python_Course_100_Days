import pyautogui
import time
import keyboard
import webbrowser

class DinoBot:
    def __init__(self):
        self.is_running = False
        self.start_time = None
        pyautogui.PAUSE = 0.01
        pyautogui.FAILSAFE = True
    
    def should_jump_by_timing(self):
        if self.start_time is None:
            return False
            
        elapsed = time.time() - self.start_time
        game_speed = min(1.0 + elapsed / 30.0, 3.0)
        
        base_interval = 1.5 / game_speed
        jump_intervals = [base_interval * i for i in [1, 1.8, 2.3, 3.1, 4.2, 5.0]]
        
        current_cycle = elapsed % 8.0
        
        for interval in jump_intervals:
            if abs(current_cycle - interval) < 0.2:
                return True
        
        return False
    
    def focus_game(self):
        screen_width, screen_height = pyautogui.size()
        center_x = screen_width // 2
        center_y = int(screen_height * 0.4)
        
        pyautogui.click(center_x, center_y)
        time.sleep(0.1)
    
    def jump(self):
        pyautogui.press('up')
    
    def run_bot(self):
        self.focus_game()
        pyautogui.press('up')
        time.sleep(1)
        
        self.start_time = time.time()
        self.is_running = True
        last_jump_time = 0
        print("Bot running! Press 'q' to quit.")
        
        while self.is_running:
            try:
                current_time = time.time()
                
                if keyboard.is_pressed('q'):
                    break
                
                if current_time - last_jump_time > 0.5:
                    if self.should_jump_by_timing():
                        self.jump()
                        last_jump_time = current_time
                
                time.sleep(0.08)
                
            except KeyboardInterrupt:
                break
        
        self.is_running = False
        print("Bot stopped!")

def main():
    print("=== Chrome Dinosaur Game Bot ===")
    print("Opening the game in your browser...")
    
    webbrowser.open('https://chromedino.com/')
    print("Waiting for page to load...")
    time.sleep(8)
    
    bot = DinoBot()
    bot.run_bot()

if __name__ == "__main__":
    main()
