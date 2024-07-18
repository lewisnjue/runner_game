# RUNNIG THE GAME 
if you are using linux ubuntu the game is compiled into these specific operating system since it 
is the one that i use but i will help with this 
## COMPILING THE GAME 
- first you will need to install all the dependances using pip you can do it as follows
```sh
pip install -r requirments.txt
```
this will install all the dependencies which i have included 
- second you will create a spec file as follows , make sure in your local computer you are in the project folder
  ```sh
  pyi-makespec main.py
  ```
- after this run the following command to have an executable file
  ```sh
  pyinstaller --onefile --windowed --add-data "graphics:graphics" --add-data "audio:audio" --add-data "font:font" main.py
  ```

-open the dist folder and run your game : **HAPPY GAMING **
