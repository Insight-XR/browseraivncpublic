#!/usr/bin/env python3
"""
Simple Chrome test script for website compatibility testing
Just opens Chrome and keeps it open for manual testing via VNC
"""

import os
import time
from playwright.sync_api import sync_playwright

def main():
    """Open Chrome and keep it open for testing"""
    print("🚀 Starting simple Chrome test...")
    
    with sync_playwright() as p:
        # Launch Chrome with stealth settings
        browser = p.chromium.launch(
            headless=False,  # Show browser window
            channel="chrome",  # Use real Google Chrome
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-blink-features=AutomationControlled",
                "--disable-extensions",
                "--disable-plugins",
                "--disable-images",  # Faster loading
                "--disable-javascript",  # Remove if you need JS
                "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            ]
        )
        
        # Create a new page
        page = browser.new_page()
        
        # Add stealth features
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => false,
            });
            
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5],
            });
            
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en'],
            });
            
            window.chrome = {
                runtime: {},
            };
        """)
        
        # Navigate to a simple starting page
        print("🌐 Opening Chrome with Google homepage...")
        page.goto("https://www.google.com")
        
        print("✅ Chrome is now open!")
        print("🌐 Connect via VNC: http://localhost:6080/vnc.html")
        print("📝 Test your websites manually in the browser")
        print("⏳ Browser will stay open for 10 minutes...")
        print("💡 Press Ctrl+C to stop early")
        
        try:
            # Keep browser open for 10 minutes
            for i in range(600):  # 600 seconds = 10 minutes
                time.sleep(1)
                if i % 60 == 0:  # Print every minute
                    minutes_left = (600 - i) // 60
                    print(f"⏰ {minutes_left} minutes remaining...")
                    
        except KeyboardInterrupt:
            print("\n🛑 Stopping early...")
        
        print("🔄 Closing browser...")
        browser.close()
        print("✅ Test completed!")

if __name__ == "__main__":
    main() 