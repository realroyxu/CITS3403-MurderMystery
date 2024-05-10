// global variable (boolean) that indicates if the instructions/about us message should be opened or closed
var showMessages = true;

// global variable (Element) that represents the highest HTML element in the document tree
var root = document.documentElement;

// set the time in cache back to 0
window.localStorage.setItem("time", 0);


document.onreadystatechange = function () {
    /**
    * Alter the class of the body once the window has finished loading
    */
    if (document.readyState === "complete") {
        document.getElementById("body").className = "all-loaded";
    }
}

/**
 * Changes the inner HTML of the "Play a Sudoku" div to display the two options the user can select from
 */
function playOption() {
    document.getElementById("playcontainer").innerHTML = `
    <button class="playbutton" onclick="chooseOption()">Choose a Sudoku</button>
    <button class="playbutton" onclick="location.href='/input_play'">Input a Sudoku</button>
    `;
}

/**
 * Changes the inner HTML of the "Choose a Sudoku" div to display the four options the user can select from
 */
function chooseOption() {
    document.getElementById("playcontainer").innerHTML = `
    <form action="/play" method="POST">
    <button id="easy" name="easy" value="easy" type="submit" class="difficultybutton">Easy</button>
    <button id="medium" name="medium" value="medium" type="submit" class="difficultybutton">Medium</button>
    <button id="hard" name="hard" value="hard" type="submit" class="difficultybutton">Hard</button>
    <button id="expert" name="expert" value="expert" type="submit" class="difficultybutton">Expert</button>
    </form>
    `;
}

/**
 * Changes the inner HTML of the "Change Theme" div to display the theme options the user can select from
 */
function themeOption() {
    document.getElementById("changetheme").innerHTML = `
    <div id="themescontainer">
    <div class="themes" id="dark" onclick="window.localStorage.setItem('storedTheme', this.id); changeTheme(); revertChangeTheme()"></div>
    <div class="themes" id="tan" onclick="window.localStorage.setItem('storedTheme', this.id); changeTheme(); revertChangeTheme()"></div>
    <div class="themes" id="light" onclick="window.localStorage.setItem('storedTheme', this.id); changeTheme(); revertChangeTheme()"></div>
    <div class="themes" id="retro" onclick="window.localStorage.setItem('storedTheme', this.id); changeTheme(); revertChangeTheme()"></div>
    </div>
    `;
}

/**
 * If a theme has been selected, reverts the "Change Theme" div back to its original HTML
 */
function revertChangeTheme() {
    document.getElementById("changetheme").innerHTML = `
    <div onclick="themeOption()">Change Theme</div>`;
}

/**
 * Changes theme based on user specified selection
 */
function changeTheme() {

    // create a local variable "themeid" that stores which theme to set
    var themeid;

    // if there is no theme stored in cache yet, set the default to the "tan" theme
    if (window.localStorage.getItem("storedTheme") == null) {
        themeid = "tan";
    }

    // else set the theme to the stored theme
    else {
        themeid = window.localStorage.getItem("storedTheme");
    }

    // if the desired theme change is "tan", change CSS variables to the corresponding color palette
    if (themeid == "tan") {

    // change document CSS colors
    root.style.setProperty('--primaryColor', "#401B00");
    root.style.setProperty('--itemBackground', "#333333");
    root.style.setProperty('--textColor', "#CCCCCC");
    root.style.setProperty('--readOnlyColor', "#666666");
    root.style.setProperty('--tableColor', "#444444");
    root.style.setProperty('--headerColor', "#555555");
    root.style.setProperty('--tableItemBackground', "#222222");
    root.style.setProperty('--buttonBackground', "#555555");
    root.style.setProperty('--buttonText', "#CCCCCC");
    root.style.setProperty('--shiftColor', "#888888");
    root.style.setProperty('--messageTextColor', "#999999");
    root.style.setProperty('--focusText', "#CCCCCC");
    root.style.setProperty('--highlightOpacity', "brightness(80%)");
    root.style.setProperty('--shiftIndication', "#CCCCCC");
    root.style.setProperty('--linkColor', "#AAAAAA");

    // change table colors
    root.style.setProperty('--color1', "#FFCCCC");
    root.style.setProperty('--color2', "#ffdab9");
    root.style.setProperty('--color3', "#99FF99");
    root.style.setProperty('--color4', "#99FFFF");
    root.style.setProperty('--color5', root.style.getPropertyValue('--itemBackground'));
    root.style.setProperty('--color6', "#99CCFF");
    root.style.setProperty('--color7', "#CC99FF");
    root.style.setProperty('--color8', "#b0c4de");
    root.style.setProperty('--color9', "#FF99CC");

    // change home icon color
    document.getElementById("homesquare").style.backgroundImage = "url(/css+js/css/images/homeTan.png)";

    // store the theme "tan" in local cache
    window.localStorage.setItem("storedTheme", "tan");

}

// else if the desired theme change is "dark", change CSS variables to the corresponding color palette
else if (themeid == "dark") {

    // change document CSS colors
    root.style.setProperty('--primaryColor', "#1F1F1F");
    root.style.setProperty('--itemBackground', "#333333");
    root.style.setProperty('--textColor', "#CCCCCC");
    root.style.setProperty('--readOnlyColor', "#666666");
    root.style.setProperty('--tableColor', "#444444");
    root.style.setProperty('--headerColor', "#555555");
    root.style.setProperty('--tableItemBackground', "#222222");
    root.style.setProperty('--buttonBackground', "#555555");
    root.style.setProperty('--buttonText', "#CCCCCC");
    root.style.setProperty('--shiftColor', "#888888");
    root.style.setProperty('--messageTextColor', "#999999");
    root.style.setProperty('--focusText', "#CCCCCC");
    root.style.setProperty('--highlightOpacity', "brightness(80%)");
    root.style.setProperty('--shiftIndication', "#CCCCCC");
    root.style.setProperty('--linkColor', "#AAAAAA");

    // change table colors
    root.style.setProperty('--color1', "#FFCCCC");
    root.style.setProperty('--color2', "#ffdab9");
    root.style.setProperty('--color3', "#99FF99");
    root.style.setProperty('--color4', "#99FFFF");
    root.style.setProperty('--color5', root.style.getPropertyValue('--itemBackground'));
    root.style.setProperty('--color6', "#99CCFF");
    root.style.setProperty('--color7', "#CC99FF");
    root.style.setProperty('--color8', "#b0c4de");
    root.style.setProperty('--color9', "#FF99CC");

    // change home icon color
    document.getElementById("homesquare").style.backgroundImage = "url(/css+js/css/images/homeDark.png)";

    // store the theme "dark" in local cache
    window.localStorage.setItem("storedTheme", "dark");
}

// else if the desired theme change is "retro", change CSS variables to the corresponding color palette
else if (themeid == "retro") {

    // change document CSS colors
    root.style.setProperty('--primaryColor', "#D9C3B6");
    root.style.setProperty('--itemBackground', "#333333");
    root.style.setProperty('--textColor', "#CCCCCC");
    root.style.setProperty('--readOnlyColor', "#666666");
    root.style.setProperty('--tableColor', "#444444");
    root.style.setProperty('--headerColor', "#555555");
    root.style.setProperty('--tableItemBackground', "#222222");
    root.style.setProperty('--buttonBackground', "#555555");
    root.style.setProperty('--buttonText', "#CCCCCC");
    root.style.setProperty('--shiftColor', "#888888");
    root.style.setProperty('--messageTextColor', "#999999");
    root.style.setProperty('--focusText', "#CCCCCC");
    root.style.setProperty('--highlightOpacity', "brightness(80%)");
    root.style.setProperty('--shiftIndication', "#CCCCCC");
    root.style.setProperty('--linkColor', "#AAAAAA");

    // change table colors
    root.style.setProperty('--color1', "#FFCCCC");
    root.style.setProperty('--color2', "#ffdab9");
    root.style.setProperty('--color3', "#99FF99");
    root.style.setProperty('--color4', "#99FFFF");
    root.style.setProperty('--color5', root.style.getPropertyValue('--itemBackground'));
    root.style.setProperty('--color6', "#99CCFF");
    root.style.setProperty('--color7', "#CC99FF");
    root.style.setProperty('--color8', "#b0c4de");
    root.style.setProperty('--color9', "#FF99CC");

    // change home icon color
    document.getElementById("homesquare").style.backgroundImage = "url(/css+js/css/images/homeRetro.png)";

    // store the theme "retro" in local cache
    window.localStorage.setItem("storedTheme", "retro");
}

// else the desired theme change is "light", change CSS variables to the corresponding color palette
else {

    // change document CSS colors
    root.style.setProperty('--primaryColor', "#E5E5E5");
    root.style.setProperty('--itemBackground', "#E5E5E5");
    root.style.setProperty('--textColor', "#CCCCCC");
    root.style.setProperty('--readOnlyColor', "#666666");
    root.style.setProperty('--tableColor', "#444444");
    root.style.setProperty('--headerColor', "#555555");
    root.style.setProperty('--tableItemBackground', "#222222");
    root.style.setProperty('--buttonBackground', "#555555");
    root.style.setProperty('--buttonText', "#CCCCCC");
    root.style.setProperty('--shiftColor', "#888888");
    root.style.setProperty('--messageTextColor', "#999999");
    root.style.setProperty('--focusText', "#CCCCCC");
    root.style.setProperty('--highlightOpacity', "brightness(80%)");
    root.style.setProperty('--shiftIndication', "#CCCCCC");
    root.style.setProperty('--linkColor', "#AAAAAA");

    // change table colors
    root.style.setProperty('--color1', "#FFCCCC");
    root.style.setProperty('--color2', "#ffdab9");
    root.style.setProperty('--color3', "#99FF99");
    root.style.setProperty('--color4', "#99FFFF");
    root.style.setProperty('--color5', root.style.getPropertyValue('--itemBackground'));
    root.style.setProperty('--color6', "#99CCFF");
    root.style.setProperty('--color7', "#CC99FF");
    root.style.setProperty('--color8', "#b0c4de");
    root.style.setProperty('--color9', "#FF99CC");

    // change home icon color
    document.getElementById("homesquare").style.backgroundImage = "url(/css+js/css/images/homeLight.png)";

    // store the theme "light" in local cache
    window.localStorage.setItem("storedTheme", "light");
}
}

/**
 * Displays "Instructions" and "About Us" messages
 */
function messagesDisplay() {

    // if "showMessages" is true
    if (showMessages) {

        // hide the play and solve images
        document.getElementById("playimage").style.display = "none";
        document.getElementById("solveimage").style.display = "none";

        // display the "instructions" and "about us" divs
        document.getElementById("menuinstructionsdisplay").style.display = "block";
        document.getElementById("menuaboutdisplay").style.display = "block";

        // change the inner HTML to show a close option
        document.getElementById("messages").innerHTML = "Close Instructions<br>and About Us";

        // set "showMessages" to false
        showMessages = false;
    }

    // else "showMessages" is false
    else {

        // hide the "instructions" and "about us" divs
        document.getElementById("menuinstructionsdisplay").style.display = "none";
        document.getElementById("menuaboutdisplay").style.display = "none";

        // display the play and solve images
        document.getElementById("playimage").style.display = "block";
        document.getElementById("solveimage").style.display = "block";

        // change the inner HTML to show an open option
        document.getElementById("messages").innerHTML = "Instructions<br>and About Us";

        // set "showMessages" to true
        showMessages = true;
    }
}