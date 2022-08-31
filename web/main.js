function registerKeyring() {
    // Register to keyring from login form
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    if (eel.register_keyring(username, password)() == false) {
        show_error();
    } else {
        eel.start_taskbar()();
        window.close();
    }
}

function show_error() {
    const notyf = new Notyf();
    notyf.error('Error: Invalid username or password');
}

function openHelp() {
    window.open('https://github.com/Mister-SOSA/UIC-AutoLAN-Tool');
}