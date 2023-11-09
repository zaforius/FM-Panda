# FM-Panda
FM Panda is a python script for making scout files in Football Manager games using pandas. It uses a simple algorithm for rating FM players for every position according to their attributes.

# What does it do?

It takes html screenshots from inside the game (made with Ctrl + P) that include views of squads or player lists. 
It reads every attribute of every player and makes a final rating for every position using an ability algorith that the in game scouts use.

# What will i need?

- A working copy of FM 2023. More editions might be included in future versions.
- The required views that the script will read. Those are included in this repo and are two .fmf files that can be loaded with the "import view" button inside FM.

# The steps

1. Open FM and go to the squad or the player search view you want to rate.

   ![image](https://github.com/zaforius/FM-Panda/assets/120644523/03db90f1-2ef6-4298-b5ee-146f73d24568)

   (This is a player search screen)

2. Download the two .fmf files from this repo. Those are the custom views that show every attribute that the program will use to make an output. Import them to the game

   ![image](https://github.com/zaforius/FM-Panda/assets/120644523/e5e644d9-1c2c-4db8-9731-fe7dffc37f7f)

3. Choose the views

   ![image](https://github.com/zaforius/FM-Panda/assets/120644523/8b84e8d5-d763-4d66-8a97-dc41ab56b93e)

4. When you are sure that this is the squad or the list you want to see the players ratings, hit "Ctrl + P" and choose Web Page. Save the html file to a folder of your choice

   ![image](https://github.com/zaforius/FM-Panda/assets/120644523/357f69e2-7353-468d-8a55-fe9db250383e)

5. Open the programm. It will prompt you to choose a folder. Choose the folder you saved the html. Press the process html button.
   
6. Your result set will be a neat table with the last rows showing the accurate ratings of every player in the list for every position. It will be present in a file called FM Panda scout files in your desktop

    ![image](https://github.com/zaforius/FM-Panda/assets/120644523/a2c73aea-c85c-4788-966a-9ed1e5770bf8)


