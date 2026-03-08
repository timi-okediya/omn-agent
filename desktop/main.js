console.log("main process working");

const electron = require("electron");
const path = require("path");
const url = require("url");

const app = electron.app;
const BrowserWindow = electron.BrowserWindow;

let win;
// let childwin
function createWindow() {
  // parentWind = new BrowserWindow()
  // childwind = new BrowserWindow({
  //   parent: parentWind,
  //   title: "child",
  //   modal: true
  // })
  // childwind.loadURL("https...")
  // childwind.once('ready-to-show', () => childwind.show())
  win = new BrowserWindow(
    {
      width: 600,
      height: 600,
      maxHeight: 600,
      maxWidth: 600,
      // backgroundColor: "#000",
      frame: false
    }
  );



  win.loadURL(
    url.format({
      pathname: path.join(__dirname, "index.html"),
      protocol: "file",
      slashes: true,
    }),
  );

  win.webContents.openDevTools();
  win.on("closed", () => {
    win = null;
  });
}

app.on("ready", createWindow);

app.on("window-all-closed", () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})


app.on("activate", () => {
  if (win === null) {
    createWindow()
  }
})
