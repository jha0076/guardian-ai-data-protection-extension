// background.js
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === 'pasteEvent') {
    const pastedText = message.pastedText;
    chrome.storage.local.set({ pastedText: pastedText }, function() {
      
    });
    // chrome.windows.create({
    //   url: 'popup.html',
    //   type: 'popup',
    //   width: 400,
    //   height: 300
    // })
  }
  else if(message.action === 'pasteText'){
    const pasteText = message.text;
    chrome.storage.local.set({ protectedText: pasteText }, function() {
      let queryOptions = { active: true, lastFocusedWindow: true };
      chrome.tabs.query(queryOptions, ([tab]) => {
      console.log(tab)
      
      chrome.scripting.executeScript({target:{tabId:tab.id},files:['contentScript2.js']})
      })
    });
  }
});
